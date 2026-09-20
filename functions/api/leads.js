const JSON_HEADERS = {
  'Content-Type': 'application/json; charset=utf-8',
  'Cache-Control': 'no-store',
  'Access-Control-Allow-Origin': '*',
};

const respond = (body, status = 200) => Response.json(body, { status, headers: JSON_HEADERS });

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const page = Math.max(1, parseInt(url.searchParams.get('page') || '1', 10));
  const perPage = Math.min(100, parseInt(url.searchParams.get('per_page') || '50', 10));
  const type = url.searchParams.get('type') || 'all';
  
  const offset = (page - 1) * perPage;
  let leads = [];
  let total = 0;
  
  try {
    if (!env.DB) {
      return respond({ error: 'Database not configured' }, 503);
    }
    
    // Fetch from enquiries table
    if (type === 'all' || type === 'enquiries') {
      const countResult = await env.DB.prepare('SELECT COUNT(*) as c FROM enquiries').bind().first();
      total += countResult?.c || 0;
      
      const rows = await env.DB.prepare(
        `SELECT id, created_at, type, source, page_title, name, email, fields_json, status 
         FROM enquiries 
         ORDER BY created_at DESC 
         LIMIT ? OFFSET ?`
      ).bind(perPage, offset).all();
      
      if (rows.results) {
        leads = leads.concat(rows.results.map(r => ({
          ...r,
          source_table: 'enquiries',
          source: r.source,
          practice: '',
        })));
      }
    }
    
    // Fetch from submissions table (AIDA)
    if (type === 'all' || type === 'submissions') {
      const subCount = await env.DB.prepare('SELECT COUNT(*) as c FROM submissions').bind().first();
      total += subCount?.c || 0;
      
      const subs = await env.DB.prepare(
        `SELECT id, created_at, name, practice, email, phone 
         FROM submissions 
         ORDER BY created_at DESC 
         LIMIT ? OFFSET ?`
      ).bind(perPage, offset).all();
      
      if (subs.results) {
        leads = leads.concat(subs.results.map(r => ({
          id: 'aida-' + r.id,
          created_at: r.created_at,
          type: 'aida-offer',
          source: '/aida',
          page_title: 'AIDA Member Offer',
          name: r.name,
          email: r.email,
          fields_json: JSON.stringify({ name: r.name, practice: r.practice, email: r.email, phone: r.phone }),
          status: 'new',
          source_table: 'submissions',
          practice: r.practice,
        })));
      }
    }
    
    // Sort all leads by created_at desc
    leads.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    
    // Limit to perPage after merge
    leads = leads.slice(0, perPage);
    
    return respond({ leads, total, page, per_page: perPage });
  } catch (err) {
    console.error('Leads API error:', String(err));
    return respond({ error: 'Failed to fetch leads', leads: [], total: 0 }, 500);
  }
}