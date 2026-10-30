// Public lead records must never be returned without verified authentication.
// The former handler read names, emails, phone numbers and form fields from D1
// without checking the caller. Keep this route closed until an owner-approved
// authenticated dashboard is implemented and independently security-reviewed.
export function onRequestGet() {
  return new Response('Forbidden', {
    status: 403,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Robots-Tag': 'noindex, nofollow',
    },
  });
}
