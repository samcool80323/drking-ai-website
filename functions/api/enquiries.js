const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
};
const ENQUIRY_TYPES = new Set(['demo-request', 'general-enquiry', 'integration-waitlist', 'client-intake']);

// Notification recipients — info@drking.ai primary, BCCs to Samir + Rank My Business
const NOTIFY_TO = 'info@drking.ai';

async function sendEmailNotification({ id, type, source, pageTitle, name, email, fields }) {
  const subject = `New ${type} enquiry — ${name || 'Unknown'} (drking.ai${source})`;
  const fieldLines = Object.entries(fields).map(([k, v]) => `${k}: ${v}`).join('\n');
  const body = [
    `New enquiry received on drking.ai`,
    ``,
    `Type: ${type}`,
    `Page: ${pageTitle}`,
    `Source: ${source}`,
    `Enquiry ID: ${id}`,
    ``,
    `--- Details ---`,
    fieldLines,
    ``,
    `Stored in D1 database (drking-enquiries).`,
  ].join('\n');

  try {
    await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [
          {
            to: [{ email: NOTIFY_TO }],
            bcc: [{ email: 'samcool80@gmail.com' }, { email: 'sam@rankmybusiness.com.au' }],
          },
        ],
        from: { email: 'noreply@mail.drking.ai', name: 'DrKing Website' },
        subject,
        content: [{ type: 'text/plain', value: body }],
      }),
    });
  } catch (err) {
    console.error(JSON.stringify({ event: 'email_notification_failed', id, error: String(err) }));
  }
}

const respond = (body, status = 200) => Response.json(body, { status, headers: JSON_HEADERS });

const text = (value, maximum) => String(value ?? '').trim().slice(0, maximum);

const cleanFields = (input) => {
  if (!input || typeof input !== 'object' || Array.isArray(input)) return {};
  return Object.fromEntries(
    Object.entries(input)
      .slice(0, 40)
      .map(([key, value]) => [text(key, 80), text(value, 3000)])
      .filter(([key, value]) => key && value),
  );
};

export async function onRequestPost(context) {
  const request = context.request;
  const requestUrl = new URL(request.url);
  const origin = request.headers.get('Origin');
  if (origin && origin !== requestUrl.origin) return respond({ error: 'Invalid request origin.' }, 403);

  const contentLength = Number(request.headers.get('Content-Length') || 0);
  if (contentLength > 32_768) return respond({ error: 'Submission is too large.' }, 413);
  if (!request.headers.get('Content-Type')?.toLowerCase().startsWith('application/json')) {
    return respond({ error: 'JSON is required.' }, 415);
  }

  let body;
  try {
    body = await request.json();
  } catch {
    return respond({ error: 'Invalid JSON.' }, 400);
  }
  if (JSON.stringify(body).length > 32_768) return respond({ error: 'Submission is too large.' }, 413);

  if (text(body.website, 200)) return respond({ ok: true });
  const type = text(body.type, 80);
  const source = text(body.source, 300);
  const pageTitle = text(body.pageTitle, 300);
  const fields = cleanFields(body.fields);
  const email = Object.entries(fields).find(([key]) => /email/i.test(key))?.[1] || '';
  const name = Object.entries(fields).find(([key]) => /^(?:contact |your )?name$/i.test(key))?.[1] || '';
  const phone = Object.entries(fields).find(([key]) => /^phone(?: number)?$/i.test(key))?.[1] || '';
  if (!ENQUIRY_TYPES.has(type) || !source.startsWith('/') || !Object.keys(fields).length || !email || !phone) {
    return respond({ error: 'Required enquiry details are missing.' }, 400);
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return respond({ error: 'Enter a valid email address.' }, 400);
  if (!/^\+[1-9]\d{6,14}$/.test(phone)) return respond({ error: 'Enter a valid international phone number.' }, 400);
  if (!context.env.DB) return respond({ error: 'The enquiry service is not configured.' }, 503);

  const id = crypto.randomUUID();
  const createdAt = new Date().toISOString();
  try {
    await context.env.DB.prepare(`
      INSERT INTO enquiries (id, created_at, type, source, page_title, name, email, fields_json, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'new')
    `).bind(id, createdAt, type, source, pageTitle, name, email, JSON.stringify(fields)).run();
  } catch (error) {
    console.error(JSON.stringify({ event: 'enquiry_store_failed', id, type, source, error: String(error) }));
    return respond({ error: 'The enquiry could not be recorded.' }, 500);
  }

  // Send email notification (non-blocking via waitUntil)
  sendEmailNotification({ id, type, source, pageTitle, name, email, fields });

  if (context.env.LEAD_WEBHOOK_URL) {
    context.waitUntil((async () => {
      try {
        const response = await fetch(context.env.LEAD_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ id, createdAt, type, source, pageTitle, name, email, fields }),
        });
        if (!response.ok) throw new Error(`Webhook returned ${response.status}`);
      } catch (error) {
        console.error(JSON.stringify({ event: 'enquiry_webhook_failed', id, error: String(error) }));
      }
    })());
  }

  console.log(JSON.stringify({ event: 'enquiry_received', id, type, source }));
  return respond({ ok: true, id }, 201);
}
