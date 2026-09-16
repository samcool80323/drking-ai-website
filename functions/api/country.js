const HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'private, no-store',
  'X-Content-Type-Options': 'nosniff',
};

export function onRequestGet({ request }) {
  const country = String(request.cf?.country || '').toUpperCase();
  return Response.json({ country: /^[A-Z]{2}$/.test(country) ? country : 'AU' }, { headers: HEADERS });
}
