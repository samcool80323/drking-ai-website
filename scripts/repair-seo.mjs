import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const pages = fs.readdirSync(root).filter((file) => file.endsWith('.html') && file !== '404.html').sort();

const metadata = {
  'about.html': {
    description: 'Meet DrKing, the Australian AI communication and growth platform helping medical, dental and allied health practices connect patients with care.',
  },
  'admin-overhead.html': {
    description: 'Reduce routine clinic admin with DrKing. Automate calls, bookings and patient enquiries while giving Australian practice teams more time for care.',
  },
  'after-hours.html': {
    title: 'After-Hours Call Answering for Australian Clinics | DrKing',
    description: 'Keep helping patients after reception closes with Australian clinic call answering, appointment booking and SMS confirmations from DrKing.',
  },
  'aged-care.html': {
    description: 'DrKing supports Australian aged-care communication with family call handling, urgent concern routing and configurable interaction logging.',
  },
  'ai-chat.html': {
    description: 'DrKing AI chat helps Australian clinics answer patient questions, capture enquiries and guide people towards appointments around the clock.',
  },
  'allied-health.html': {
    title: 'AI Communication for Allied Health Practices | DrKing',
    description: 'DrKing helps Australian allied health practices answer enquiries, support appointment booking and follow up with patients between visits.',
  },
  'appointment-reminders.html': {
    description: 'Help reduce no-shows with configurable SMS and WhatsApp appointment reminders, rescheduling and follow-up for Australian practices.',
  },
  'case-studies.html': {
    description: 'DrKing Australian clinic case studies are coming soon. Learn what evidence will be shared and explore relevant dental, GP and allied health pages.',
  },
  'dentists.html': {
    description: 'DrKing helps Australian dental practices answer calls, capture enquiries, support online booking and follow up with prospective patients.',
  },
  'general-practice.html': {
    title: 'Patient Communication for Australian GP Clinics | DrKing',
    description: 'DrKing helps Australian GP clinics answer routine enquiries, support appointment booking and send configurable patient reminders.',
  },
  'integrations.html': {
    description: 'Review DrKing integrations for Australian healthcare practices, including current availability for Cliniko, Nookal, Power Diary and Dentally.',
  },
  'lead-management.html': {
    description: 'Bring Australian clinic enquiries into one pipeline with DrKing lead management, channel tracking and configurable follow-up workflows.',
  },
  'medical-centres.html': {
    description: 'DrKing helps Australian medical centres coordinate calls, enquiries, cross-location booking and reporting across multiple clinics.',
  },
  'missed-call-recovery.html': {
    description: 'Follow up unanswered clinic calls with configurable SMS workflows that capture details and guide Australian patients towards booking.',
  },
  'missed-calls.html': {
    title: 'Missed Call Recovery for Australian Clinics | DrKing',
    description: 'DrKing helps Australian clinics respond to missed calls, capture patient enquiries and guide people towards an appointment.',
  },
  'online-reviews.html': {
    description: 'Build a consistent review-request process with DrKing automation and reputation workflows designed for Australian healthcare practices.',
  },
  'patient-no-shows.html': {
    description: 'Support appointment attendance with configurable reminders, rescheduling, wait-list workflows and deposits for Australian clinics.',
  },
  'specialists.html': {
    title: 'Appointment Automation for Specialist Clinics | DrKing',
    description: 'DrKing helps Australian specialist clinics capture referrals, support appointment booking, manage wait lists and follow up with patients.',
  },
  'terms.html': {
    description: 'Read the DrKing terms covering accounts, subscriptions, acceptable use and responsibilities for the Australian clinic communication platform.',
  },
  'vs-call-answering.html': {
    title: 'DrKing vs Call Answering Services for Clinics',
  },
  'vs-chatbots.html': {
    title: 'DrKing vs Generic Chatbots for Australian Clinics',
    description: 'Compare DrKing with generic chatbots across clinic booking, communication channels, after-hours support and integration workflows.',
  },
  'vs-practice-management.html': {
    title: 'DrKing vs Practice Management Software',
  },
  'vs-receptionist.html': {
    title: 'DrKing vs Human Receptionists for Australian Clinics',
    description: 'Compare DrKing and human reception across availability, call handling, bookings and team support for Australian healthcare practices.',
  },
};

const organisation = {
  '@type': 'Organization',
  '@id': 'https://drking.ai/#organization',
  name: 'DrKing',
  url: 'https://drking.ai/',
  logo: {
    '@type': 'ImageObject',
    url: 'https://drking.ai/drking-logo.svg',
    width: 2020,
    height: 616,
  },
  email: 'info@drking.ai',
  telephone: '+61 483 981 666',
  description: 'Australian AI communication and practice-growth platform for healthcare organisations.',
  address: {
    '@type': 'PostalAddress',
    streetAddress: '1 Elgin Pl',
    addressLocality: 'Hawthorn',
    addressRegion: 'VIC',
    postalCode: '3122',
    addressCountry: 'AU',
  },
  areaServed: { '@type': 'Country', name: 'Australia' },
};

const orgReference = () => ({ '@id': organisation['@id'] });
const pageTypes = new Set(['WebPage', 'AboutPage', 'ContactPage', 'CollectionPage']);

function hasType(node, type) {
  const values = Array.isArray(node?.['@type']) ? node['@type'] : [node?.['@type']];
  return values.includes(type);
}

function normaliseNested(value, topLevel = false) {
  if (Array.isArray(value)) return value.map((item) => normaliseNested(item, false));
  if (!value || typeof value !== 'object') return value;

  if (!topLevel && hasType(value, 'Organization') && value.name === 'DrKing') return orgReference();

  const result = {};
  for (const [key, nested] of Object.entries(value)) result[key] = normaliseNested(nested, false);
  return result;
}

function normaliseNode(node, file) {
  const result = normaliseNested(node, true);

  if (hasType(result, 'MedicalBusiness') && result.name === 'DrKing') {
    return {
      '@type': 'Service',
      '@id': `https://drking.ai/${file.replace(/\.html$/, '')}#service`,
      name: 'Patient communication software for Australian general practice clinics',
      url: `https://drking.ai/${file.replace(/\.html$/, '')}`,
      description: result.description,
      serviceType: 'Patient communication and appointment workflow software',
      provider: orgReference(),
      areaServed: { '@type': 'Country', name: 'Australia' },
      audience: { '@type': 'Audience', audienceType: 'Australian general practice clinics' },
    };
  }

  if (hasType(result, 'MedicalBusiness')) {
    const { additionalType, medicalSpecialty, ...rest } = result;
    return {
      ...rest,
      '@type': 'Audience',
      audienceType: result.name,
    };
  }

  if (hasType(result, 'SoftwareApplication')) {
    result.provider = orgReference();
    result.publisher = orgReference();
  }
  if (hasType(result, 'Service')) result.provider = orgReference();
  if ([...pageTypes].some((type) => hasType(result, type))) {
    result.inLanguage = 'en-AU';
    result.publisher = orgReference();
  }
  return result;
}

function normaliseStructuredData(html, file, title, description, canonical) {
  const scripts = [...html.matchAll(/<script\b([^>]*)type=["']application\/ld\+json["']([^>]*)>([\s\S]*?)<\/script>/gi)];
  const nodes = [];

  for (const match of scripts) {
    const data = JSON.parse(match[3]);
    if (Array.isArray(data['@graph'])) nodes.push(...data['@graph']);
    else {
      const { '@context': ignored, ...node } = data;
      nodes.push(node);
    }
  }

  const filtered = nodes
    .filter((node) => !(hasType(node, 'Organization') && node.name === 'DrKing'))
    .map((node) => normaliseNode(node, file))
    .filter((node) => file !== 'index.html' || !hasType(node, 'WebSite'));

  const existingPage = filtered.find((node) => [...pageTypes].some((type) => hasType(node, type)));
  if (existingPage) {
    existingPage['@id'] ||= `${canonical}#webpage`;
    existingPage.url = canonical;
    existingPage.name = title;
    existingPage.description = description;
    existingPage.inLanguage = 'en-AU';
    existingPage.publisher = orgReference();
  } else {
    filtered.unshift({
      '@type': file === 'about.html' ? 'AboutPage' : 'WebPage',
      '@id': `${canonical}#webpage`,
      url: canonical,
      name: title,
      description,
      inLanguage: 'en-AU',
      publisher: orgReference(),
    });
  }

  if (file === 'index.html') {
    filtered.unshift({
      '@type': 'WebSite',
      '@id': 'https://drking.ai/#website',
      url: 'https://drking.ai/',
      name: 'DrKing',
      inLanguage: 'en-AU',
      publisher: orgReference(),
    });
  }

  const graph = {
    '@context': 'https://schema.org',
    '@graph': [organisation, ...filtered],
  };
  const replacement = `<script type="application/ld+json" id="structured-data">${JSON.stringify(graph)}</script>`;
  if (!scripts.length) return html.replace('</head>', `${replacement}\n</head>`);

  let updated = html;
  for (let index = scripts.length - 1; index >= 0; index -= 1) {
    const match = scripts[index];
    updated = updated.slice(0, match.index) + (index === 0 ? replacement : '') + updated.slice(match.index + match[0].length);
  }
  return updated;
}

for (const file of pages) {
  const fullPath = path.join(root, file);
  let html = fs.readFileSync(fullPath, 'utf8');
  const changes = metadata[file] || {};

  if (changes.title) html = html.replace(/<title>[\s\S]*?<\/title>/i, `<title>${changes.title}</title>`);
  if (changes.description) {
    html = html.replace(/<meta\b[^>]*\bname=["']description["'][^>]*>/i, (tag) => {
      if (/\bcontent=["']/i.test(tag)) return tag.replace(/\bcontent=(["'])[\s\S]*?\1/i, `content="${changes.description}"`);
      return tag.replace(/\s*\/?\s*>$/, ` content="${changes.description}">`);
    });
  }

  const expectedCanonical = file === 'index.html' ? 'https://drking.ai/' : `https://drking.ai/${file.slice(0, -5)}`;
  html = html.replace(/<link\s+rel=["']canonical["']\s+href=["'][^"']+["']\s*\/?\s*>/i, `<link rel="canonical" href="${expectedCanonical}">`);

  const title = html.match(/<title>([\s\S]*?)<\/title>/i)?.[1].replace(/<[^>]+>/g, '').trim();
  const descriptionTag = html.match(/<meta\b[^>]*\bname=["']description["'][^>]*>/i)?.[0];
  const description = descriptionTag?.match(/\bcontent=(["'])([\s\S]*?)\1/i)?.[2];
  const canonical = html.match(/<link\s+rel=["']canonical["']\s+href=["']([^"']+)/i)?.[1];
  if (!title || !description || !canonical) throw new Error(`Missing SEO metadata in ${file}`);

  html = normaliseStructuredData(html, file, title, description, canonical);

  const hiddenSectionHeadings = {
    'ai-voice-receptionist.html': ['<div role="img" class="hero-art"', '<h2 class="sr-only">AI receptionist call preview</h2><div role="img" class="hero-art"'],
    'analytics.html': ['<div class="hero-art" id="dashboard">', '<h2 class="sr-only">Illustrative clinic analytics dashboard</h2><div class="hero-art" id="dashboard">'],
    'contact.html': ['<section class="contact-band" aria-label="Contact DrKing">', '<section class="contact-band" aria-label="Contact DrKing"><h2 class="sr-only">Contact DrKing</h2>'],
    'online-booking.html': ['<div class="hero-art"><svg class="blob"', '<h2 class="sr-only">Interactive online booking preview</h2><div class="hero-art"><svg class="blob"'],
    'vs-call-answering.html': ['<div class="hero-art" role="img"', '<h2 class="sr-only">Call answering comparison example</h2><div class="hero-art" role="img"'],
  };
  if (hiddenSectionHeadings[file] && !html.includes(hiddenSectionHeadings[file][1].split('</h2>')[0])) {
    html = html.replace(...hiddenSectionHeadings[file]);
  }

  if (file === 'demo.html' && !html.includes('href="/client-intake"')) {
    html = html.replace(
      '<p>Here’s what to know before we say hello.</p>',
      '<p>Here’s what to know before we say hello. Already working with DrKing? Continue to the <a href="/client-intake">client intake form</a>.</p>',
    );
  }

  html = html.replace(/<img\b([^>]*src=["']\/drking-logo\.svg["'][^>]*)>/gi, (tag, attributes) => {
    let updated = attributes.replace(/\swidth=["'][^"']*["']/gi, '').replace(/\sheight=["'][^"']*["']/gi, '');
    return `<img${updated} width="2020" height="616">`;
  });

  fs.writeFileSync(fullPath, html);
}

console.log(`Repaired metadata and structured data on ${pages.length} pages.`);
