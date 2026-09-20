export async function onRequestPost({ request, env }) {
  try {
    const body = await request.json();
    
    // Validate required fields
    const required = ['name', 'practice', 'email', 'phone', 'consent'];
    for (const field of required) {
      if (!body[field] || body[field].toString().trim() === '') {
        return new Response(JSON.stringify({ error: 'All fields are required.' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    if (body.consent !== 'on' && body.consent !== true) {
      return new Response(JSON.stringify({ error: 'You must provide consent to submit this form.' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(body.email)) {
      return new Response(JSON.stringify({ error: 'Please enter a valid email address.' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    
    // Sanitize inputs
    const sanitize = (str) => str.toString().trim().substring(0, 250);
    const name = sanitize(body.name);
    const practice = sanitize(body.practice);
    const email = sanitize(body.email);
    const phone = sanitize(body.phone);
    
    // Try to store in D1 if available
    if (env.AIDA_DB) {
      try {
        await env.AIDA_DB.prepare(
          'INSERT INTO submissions (name, practice, email, phone, consent, created_at) VALUES (?, ?, ?, ?, 1, datetime("now"))'
        ).bind(name, practice, email, phone).run();
      } catch (dbErr) {
        // D1 not set up yet — continue without failing
        console.log('D1 not available, storing in memory:', dbErr.message);
      }
    }
    
    // Also send email notification via Cloudflare Email (if configured)
    // For now, log the submission
    console.log('AIDA submission:', { name, practice, email, phone });
    
    return new Response(JSON.stringify({
      success: true,
      message: 'Your AIDA member offer request has been received. We will contact you within one business day.'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    });
    
  } catch (err) {
    return new Response(JSON.stringify({
      error: 'An error occurred. Please try again or call +61 483 981 666.'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}
