const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
};

const respond = (body, status = 200) => Response.json(body, { status, headers: JSON_HEADERS });

const text = (value, maximum) => String(value ?? '').trim().slice(0, maximum);

// Notification recipients — info@drking.ai gets the primary, BCCs go to Samir
const NOTIFY_TO = 'info@drking.ai';
const NOTIFY_BCC = 'samcool80@gmail.com, sam@rankmybusiness.com.au';

async function sendEmailNotification(env, { name, practice, email, phone, type }) {
  const subject = `New ${type} submission — ${name} (${practice})`;
  const body = [
    `New form submission on drking.ai`,
    ``,
    `Type: ${type}`,
    `Name: ${name}`,
    `Practice: ${practice}`,
    `Email: ${email}`,
    `Phone: ${phone}`,
    ``,
    `Stored in D1 database (drking-enquiries).`,
  ].join('\n');

  try {
    await fetch('https://api.mailchannels.net/tx/v1/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        personalizations: [
          { to: [{ email: NOTIFY_TO }], bcc: [{ email: 'samcool80@gmail.com' }, { email: 'sam@rankmybusiness.com.au' }] },
        ],
        from: { email: 'noreply@mail.drking.ai', name: 'DrKing Website' },
        subject,
        content: [{ type: 'text/plain', value: body }],
      }),
    });
  } catch (err) {
    console.error('Email notification failed:', String(err));
  }
}

export async function onRequestPost({ request, env }) {
  try {
    const body = await request.json();

    // Validate required fields
    const required = ['name', 'practice', 'email', 'phone', 'consent'];
    for (const field of required) {
      if (!body[field] || body[field].toString().trim() === '') {
        return respond({ error: 'All fields are required.' }, 400);
      }
    }

    if (body.consent !== 'on' && body.consent !== true) {
      return respond({ error: 'You must provide consent to submit this form.' }, 400);
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(body.email)) {
      return respond({ error: 'Please enter a valid email address.' }, 400);
    }

    // Sanitize inputs
    const sanitize = (str) => str.toString().trim().substring(0, 250);
    const name = sanitize(body.name);
    const practice = sanitize(body.practice);
    const email = sanitize(body.email);
    const phone = sanitize(body.phone);

    // Store in D1 — binding is "DB" per wrangler.toml
    if (env.DB) {
      try {
        await env.DB.prepare(
          'INSERT INTO submissions (name, practice, email, phone, consent, created_at) VALUES (?, ?, ?, ?, 1, datetime(\'now\'))'
        ).bind(name, practice, email, phone).run();
      } catch (dbErr) {
        // D1 table might not exist yet — create it and retry
        try {
          await env.DB.prepare(
            'CREATE TABLE IF NOT EXISTS submissions (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, practice TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, consent INTEGER DEFAULT 1, created_at TEXT NOT NULL DEFAULT (datetime(\'now\')))'
          ).run();
          await env.DB.prepare(
            'INSERT INTO submissions (name, practice, email, phone, consent, created_at) VALUES (?, ?, ?, ?, 1, datetime(\'now\'))'
          ).bind(name, practice, email, phone).run();
        } catch (retryErr) {
          console.error('D1 storage failed:', String(retryErr));
        }
      }
    }

    // Send email notification (non-blocking)
    sendEmailNotification(env, { name, practice, email, phone, type: 'AIDA member offer' });

    return respond({
      success: true,
      message: 'Your AIDA member offer request has been received. We will contact you within one business day.'
    });

  } catch (err) {
    return respond({ error: 'An error occurred. Please try again or call +61 483 981 666.' }, 500);
  }
}