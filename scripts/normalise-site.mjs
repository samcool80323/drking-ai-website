import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const pages = fs.readdirSync(root).filter((file) => file.endsWith('.html')).sort();
const removableStyleMarkers = [
  'Logo — ensure visible on all devices',
  'footer[style*="grid-template-columns:2fr 1fr 1fr 1fr 1fr"]',
  '/* Logo */',
  'id="DEFINITIVE-NAV"',
  'id="mobile-nav-force-hide"',
  'id="header-spacing"',
];

const navIcons = {
  industries: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="6" height="6" rx="1"></rect><rect x="14" y="4" width="6" height="6" rx="1"></rect><rect x="4" y="14" width="6" height="6" rx="1"></rect><rect x="14" y="14" width="6" height="6" rx="1"></rect></svg>',
  dental: '<svg viewBox="0 0 24 24"><path d="M12 5.1c-1.5 0-2.8-1.1-4.4-1.1C5.2 4 4 5.7 4 8c0 3.1 1.8 4.8 2.5 8.1.5 2.3 1.2 3.9 2.4 3.9 1.4 0 1.4-4.7 3.1-4.7s1.7 4.7 3.1 4.7c1.2 0 1.9-1.6 2.4-3.9C18.2 12.8 20 11.1 20 8c0-2.3-1.2-4-3.6-4-1.6 0-2.9 1.1-4.4 1.1Z"></path></svg>',
  generalPractice: '<svg viewBox="0 0 24 24"><path d="M9 4h6v5h5v6h-5v5H9v-5H4V9h5V4Z"></path></svg>',
  specialists: '<svg viewBox="0 0 24 24"><path d="M6 3v5a4 4 0 0 0 8 0V3"></path><path d="M4 3h4M12 3h4M10 16v1a4 4 0 0 0 8 0v-2"></path><circle cx="18" cy="12" r="3"></circle></svg>',
  alliedHealth: '<svg viewBox="0 0 24 24"><path d="M20.8 5.8a5 5 0 0 0-7.1 0L12 7.5l-1.7-1.7a5 5 0 0 0-7.1 7.1L12 21l8.8-8.1a5 5 0 0 0 0-7.1Z"></path><path d="m7.5 12 2.2-2 2.3 4 2-3 2.5 1"></path></svg>',
  medicalCentres: '<svg viewBox="0 0 24 24"><path d="M4 21V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v16"></path><path d="M9 8h6M12 5v6M8 14h2M14 14h2M8 18h2M14 18h2M2 21h20"></path></svg>',
  cosmeticClinics: '<svg viewBox="0 0 24 24"><path d="m12 3 1.4 4.1L17.5 8.5l-4.1 1.4L12 14l-1.4-4.1-4.1-1.4 4.1-1.4L12 3Z"></path><path d="m18.5 14 .8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8.8-2.2ZM5 14l.6 1.7 1.7.6-1.7.6L5 18.5l-.6-1.6-1.7-.6 1.7-.6L5 14Z"></path></svg>',
  veterinary: '<svg viewBox="0 0 24 24"><ellipse cx="7" cy="7" rx="2" ry="3"></ellipse><ellipse cx="17" cy="7" rx="2" ry="3"></ellipse><ellipse cx="4.5" cy="12" rx="1.8" ry="2.5"></ellipse><ellipse cx="19.5" cy="12" rx="1.8" ry="2.5"></ellipse><path d="M12 11c-3.2 0-6 3.4-6 6.1 0 2 1.5 3 3.2 3 1.1 0 1.8-.6 2.8-.6s1.7.6 2.8.6c1.7 0 3.2-1 3.2-3 0-2.7-2.8-6.1-6-6.1Z"></path></svg>',
  agedCare: '<svg viewBox="0 0 24 24"><circle cx="12" cy="7" r="3"></circle><path d="M6 21v-3a6 6 0 0 1 12 0v3M3 13c1.5 0 2.5.7 3.3 1.7M21 13c-1.5 0-2.5.7-3.3 1.7"></path></svg>',
  solutions: '<svg viewBox="0 0 24 24"><path d="M5 4v6M5 14v6M12 4v2M12 10v10M19 4v10M19 18v2"></path><path d="M2 10h6M9 6h6M16 14h6"></path></svg>',
  voice: '<svg viewBox="0 0 24 24"><path d="M7.2 4.7 9.5 8 7.8 9.7a14.8 14.8 0 0 0 6.5 6.5l1.7-1.7 3.3 2.3c.5.4.7 1 .5 1.6-.4 1.2-1.5 2-2.8 2C9.6 20.4 3.6 14.4 3.6 7c0-1.3.8-2.4 2-2.8.6-.2 1.2 0 1.6.5Z"></path><path d="M15 5a5 5 0 0 1 4 4M15 9a1 1 0 0 1 1 1"></path></svg>',
  chat: '<svg viewBox="0 0 24 24"><path d="M4 5h16v12H9l-5 4V5Z"></path><path d="M8 9h8M8 13h5"></path></svg>',
  missedCall: '<svg viewBox="0 0 24 24"><path d="M7.2 4.7 9.5 8 7.8 9.7a14.8 14.8 0 0 0 6.5 6.5l1.7-1.7 3.3 2.3c.5.4.7 1 .5 1.6-.4 1.2-1.5 2-2.8 2C9.6 20.4 3.6 14.4 3.6 7c0-1.3.8-2.4 2-2.8.6-.2 1.2 0 1.6.5Z"></path><path d="m14 4 6 6M20 4l-6 6"></path></svg>',
  payments: '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="2"></rect><path d="M3 10h18M7 15h4"></path></svg>',
  reviews: '<svg viewBox="0 0 24 24"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-2.9-5.6 2.9 1.1-6.2L3 9.6l6.2-.9L12 3Z"></path></svg>',
  reminders: '<svg viewBox="0 0 24 24"><path d="M6 9a6 6 0 0 1 12 0c0 7 3 7 3 7H3s3 0 3-7ZM10 20h4"></path></svg>',
  crm: '<svg viewBox="0 0 24 24"><circle cx="9" cy="8" r="3"></circle><path d="M3 20v-2a6 6 0 0 1 12 0v2M16 4a3 3 0 0 1 0 6M17 14a5 5 0 0 1 4 4v2"></path></svg>',
  analytics: '<svg viewBox="0 0 24 24"><path d="M4 20V10h4v10M10 20V4h4v16M16 20v-7h4v7M2 20h20"></path></svg>',
};

const siteHeader = `<header class="site-header">
<a class="brand" href="/" aria-label="DrKing home"><img class="brand-logo" src="/drking-logo.svg" alt="DrKing" width="2020" height="616"></a>
<nav class="nav-links navlinks" id="site-desktop-nav" aria-label="Main navigation">
<div class="mega-menu"><button type="button" class="mega-toggle" aria-haspopup="true">Industries</button><div class="mega-panel">
<a class="mega-item mega-index" href="/industries"><span class="mega-icon" aria-hidden="true">${navIcons.industries}</span><span class="mega-text"><span class="mega-title">View all industries</span><span class="mega-desc">Find workflows for your type of practice</span></span></a>
<a class="mega-item" href="/dentists"><span class="mega-icon" aria-hidden="true">${navIcons.dental}</span><span class="mega-text"><span class="mega-title">Dental Clinics</span><span class="mega-desc">Capture every call, book more chairs</span></span></a>
<a class="mega-item" href="/general-practice"><span class="mega-icon" aria-hidden="true">${navIcons.generalPractice}</span><span class="mega-text"><span class="mega-title">General Practice</span><span class="mega-desc">Reduce wait times, lighten reception</span></span></a>
<a class="mega-item" href="/specialists"><span class="mega-icon" aria-hidden="true">${navIcons.specialists}</span><span class="mega-text"><span class="mega-title">Specialists</span><span class="mega-desc">Convert more referrals into patients</span></span></a>
<a class="mega-item" href="/allied-health"><span class="mega-icon" aria-hidden="true">${navIcons.alliedHealth}</span><span class="mega-text"><span class="mega-title">Allied Health</span><span class="mega-desc">Keep patients on their treatment plan</span></span></a>
<a class="mega-item" href="/medical-centres"><span class="mega-icon" aria-hidden="true">${navIcons.medicalCentres}</span><span class="mega-text"><span class="mega-title">Medical Centres</span><span class="mega-desc">Multi-location support</span></span></a>
<a class="mega-item" href="/cosmetic-clinics"><span class="mega-icon" aria-hidden="true">${navIcons.cosmeticClinics}</span><span class="mega-text"><span class="mega-title">Cosmetic Clinics</span><span class="mega-desc">Respond while interest is high</span></span></a>
<a class="mega-item" href="/veterinary"><span class="mega-icon" aria-hidden="true">${navIcons.veterinary}</span><span class="mega-text"><span class="mega-title">Veterinary</span><span class="mega-desc">After-hours enquiry support</span></span></a>
<a class="mega-item" href="/aged-care"><span class="mega-icon" aria-hidden="true">${navIcons.agedCare}</span><span class="mega-text"><span class="mega-title">Aged Care</span><span class="mega-desc">Clear family communication</span></span></a>
</div></div>
<div class="mega-menu"><button type="button" class="mega-toggle" aria-haspopup="true">Solutions</button><div class="mega-panel">
<a class="mega-item mega-index" href="/solutions"><span class="mega-icon" aria-hidden="true">${navIcons.solutions}</span><span class="mega-text"><span class="mega-title">View all solutions</span><span class="mega-desc">Explore communication and growth tools</span></span></a>
<a class="mega-item" href="/ai-voice-receptionist"><span class="mega-icon" aria-hidden="true">${navIcons.voice}</span><span class="mega-text"><span class="mega-title">AI Voice Receptionist</span><span class="mega-desc">Answer calls around the clock</span></span></a>
<a class="mega-item" href="/ai-chat"><span class="mega-icon" aria-hidden="true">${navIcons.chat}</span><span class="mega-text"><span class="mega-title">AI Web Chat</span><span class="mega-desc">Help website visitors take action</span></span></a>
<a class="mega-item" href="/missed-call-recovery"><span class="mega-icon" aria-hidden="true">${navIcons.missedCall}</span><span class="mega-text"><span class="mega-title">Missed Call Recovery</span><span class="mega-desc">Follow up unanswered calls</span></span></a>
<a class="mega-item" href="/text-to-pay"><span class="mega-icon" aria-hidden="true">${navIcons.payments}</span><span class="mega-text"><span class="mega-title">Text-to-Pay</span><span class="mega-desc">Simple SMS payment links</span></span></a>
<a class="mega-item" href="/review-generator"><span class="mega-icon" aria-hidden="true">${navIcons.reviews}</span><span class="mega-text"><span class="mega-title">Review Generator</span><span class="mega-desc">Consistent review invitations</span></span></a>
<a class="mega-item" href="/appointment-reminders"><span class="mega-icon" aria-hidden="true">${navIcons.reminders}</span><span class="mega-text"><span class="mega-title">Reminders</span><span class="mega-desc">Support appointment attendance</span></span></a>
<a class="mega-item" href="/lead-management"><span class="mega-icon" aria-hidden="true">${navIcons.crm}</span><span class="mega-text"><span class="mega-title">Lead CRM</span><span class="mega-desc">Bring enquiries into one pipeline</span></span></a>
<a class="mega-item" href="/analytics"><span class="mega-icon" aria-hidden="true">${navIcons.analytics}</span><span class="mega-text"><span class="mega-title">Analytics</span><span class="mega-desc">See which channels create demand</span></span></a>
</div></div>
<a href="/integrations">Integrations</a><a href="/about">About</a>
</nav>
<div class="header-right"><a class="button teal" href="/demo">Let’s talk <span aria-hidden="true">↗</span></a><button type="button" class="menu-toggle menu-button mobile-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M4 8h16M4 16h16" fill="none" stroke="currentColor" stroke-width="1.5"></path></svg></button></div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" inert>
<div class="mobile-group"><div class="mobile-group-label">Industries</div><a class="mobile-index-link" href="/industries">View all industries <span aria-hidden="true">→</span></a><a href="/dentists">Dental Clinics</a><a href="/general-practice">General Practice</a><a href="/specialists">Specialists</a><a href="/allied-health">Allied Health</a><a href="/medical-centres">Medical Centres</a><a href="/cosmetic-clinics">Cosmetic Clinics</a><a href="/veterinary">Veterinary</a><a href="/aged-care">Aged Care</a></div>
<div class="mobile-group"><div class="mobile-group-label">Solutions</div><a class="mobile-index-link" href="/solutions">View all solutions <span aria-hidden="true">→</span></a><a href="/ai-voice-receptionist">AI Voice Receptionist</a><a href="/ai-chat">AI Web Chat</a><a href="/missed-call-recovery">Missed Call Recovery</a><a href="/text-to-pay">Text-to-Pay</a><a href="/review-generator">Reviews</a><a href="/appointment-reminders">Reminders</a><a href="/lead-management">Lead CRM</a><a href="/analytics">Analytics</a></div>
<div class="mobile-group"><div class="mobile-group-label">Company</div><a href="/integrations">Integrations</a><a href="/about">About</a><a href="/contact">Contact</a></div>
<a href="/demo" class="mobile-cta">Book a Free Demo</a>
</nav>`;

const siteFooter = `<footer class="site-footer">
<div class="site-footer-inner">
<div class="site-footer-brand"><a href="/" aria-label="DrKing home"><img src="/drking-logo.svg" alt="DrKing" width="2020" height="616"></a><p>Practical AI communication tools for Australian healthcare practices.</p></div>
<nav class="site-footer-nav" aria-label="Footer navigation">
<div><h2><a href="/industries">Industries</a></h2><a href="/dentists">Dental Clinics</a><a href="/general-practice">General Practice</a><a href="/specialists">Specialists</a><a href="/allied-health">Allied Health</a></div>
<div><h2><a href="/solutions">Solutions</a></h2><a href="/ai-voice-receptionist">AI Voice Receptionist</a><a href="/missed-call-recovery">Missed Call Recovery</a><a href="/online-booking">Online Booking</a><a href="/payment-collection">Payment Collection</a><a href="/patient-reactivation">Patient Reactivation</a><a href="/appointment-reminders">Reminders</a><a href="/analytics">Analytics</a></div>
<div><h2>Resources</h2><a href="/case-studies">Case Studies</a><a href="/roi-calculator">ROI Calculator</a><a href="/vs-receptionist">Compare Reception</a><a href="/vs-practice-management">Compare Practice Software</a><a href="/vs-call-answering">Compare Call Answering</a><a href="/vs-chatbots">Compare Chatbots</a></div>
<div><h2>Company</h2><a href="/about">About</a><a href="/integrations">Integrations</a><a href="/security">Security</a><a href="/referral-partner">Referral Partners</a><a href="/contact">Contact</a><a href="/demo">Book a Demo</a></div>
</nav>
</div>
<p class="site-footer-disclaimer">Performance percentages and financial examples are illustrative unless a cited source or verified case study is identified. Results vary by practice.</p>
<div class="site-footer-bottom"><p>© <span id="year">2026</span> DrKing. All rights reserved. All dollar amounts are AUD unless stated otherwise.</p><div><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div></div>
</footer>`;

for (const file of pages) {
  const full = path.join(root, file);
  let html = fs.readFileSync(full, 'utf8');

  html = html.replace(/<html\s+lang=["'][^"']+["']/i, '<html lang="en-AU"');

  html = html.replace(/<link[^>]+(?:fonts\.googleapis\.com|fonts\.gstatic\.com|\/assets\/site-shell\.css)[^>]*>\s*/gi, '');
  html = html.replace(/<style>html\{overflow-x:hidden!important\}body\{overflow-x:hidden!important\}<\/style>\s*/gi, '');
  html = html.replace(/<script[^>]+src=["']\/assets\/site-shell\.js["'][^>]*><\/script>\s*/gi, '');
  html = html.replace(/<script[^>]+src=["']\/assets\/international-phone\.js["'][^>]*><\/script>\s*/gi, '');
  html = html.replace(/<link[^>]+fonts\.googleapis\.com[^>]*>\s*/gi, '');
  html = html.replace(/<link[^>]+fonts\.gstatic\.com[^>]*>\s*/gi, '');
  html = html.replace(/<link[^>]+href=["']\/fonts\/newsreader-[^"']+["'][^>]*>\s*/gi, '');
  html = html.replace(/<style([^>]*)>([\s\S]*?)<\/style>/gi, (block, attrs, css) => {
    if (removableStyleMarkers.some((marker) => block.includes(marker))) return '';
    const cleaned = css.replace(/@font-face\s*\{[^{}]*font-family\s*:\s*['"]?(?:Geomanist|Newsreader)['"]?[^{}]*\}/gi, '');
    return cleaned.trim() ? `<style${attrs}>${cleaned}</style>` : '';
  });

  html = html.replace(/<script\s+id=["'](?:universal-menu|mega-hover-js)["'][^>]*>[\s\S]*?<\/script>\s*/gi, '');
  html = html.replace(/<script>\s*document\.addEventListener\(["']DOMContentLoaded["'],function\(\)\{document\.querySelectorAll\(["']\.mega-menu["']\)[\s\S]*?<\/script>\s*/gi, '');
  html = html.replace(/(<(?:div|button)\s+class=["'][^"']*\b(?:mega-menu|mega-toggle|mega-panel)\b[^"']*["'])\s+style=["'][^"']*["']/gi, '$1');
  html = html.replace(/(<a\s+class=["'][^"']*\bbrand\b[^"']*["']\s+href=)["']#["']/gi, '$1"/"');
  html = html.replace(/class=["']menu-toggle(?:\s+menu-button\s+mobile-toggle)?["']/gi, 'class="menu-toggle menu-button mobile-toggle"');
  html = html.replace(/<nav\s+class=["']nav-links(?:\s+navlinks)?["'](?:\s+id=["']nav-links["'])?/gi, '<nav class="nav-links navlinks" id="nav-links"');
  html = html.replace(/<!-- legacy-nav-proxies:start -->[\s\S]*?<!-- legacy-nav-proxies:end -->\s*/gi, '');
  html = html.replace(/<body([^>]*)>/i, '<body$1>\n<!-- legacy-nav-proxies:start --><div hidden class="legacy-nav-proxies"><button type="button" class="menu-toggle menu-button mobile-toggle" aria-expanded="false"></button><div class="nav-links navlinks" id="nav-links"></div><div id="navigation"></div><div id="main-nav"></div><div id="mobile-menu"></div><div class="dropdown"></div><div class="industry"></div></div><!-- legacy-nav-proxies:end -->');
  html = html.replace(/<header\s+class=["']site-header["'][\s\S]*?<main\s+id=["']main["'][^>]*>/i, `${siteHeader}\n<main id="main">`);
  html = html.replace(/<body\s+style=["']overflow-x\s*:\s*hidden["']>/i, '<body>');

  const mainMatches = [...html.matchAll(/<main\s+id=["']main["'][^>]*>/gi)];
  if (mainMatches.length > 1) {
    html = html.slice(0, mainMatches[0].index) + html.slice(mainMatches[1].index);
  }

  html = html.replaceAll('/book-demo', '/demo');
  html = html.replaceAll('/book-a-demo', '/demo');
  html = html.replaceAll('href="https://drking.ai/demo"', 'href="/demo"');
  html = html.replaceAll("href='https://drking.ai/demo'", "href='/demo'");
  html = html.replaceAll('https://drking.ai/#button-LZar9xGjf-', '/demo');
  html = html.replaceAll('/multi-location-management', '/multi-location-chaos');
  html = html.replaceAll('/#book-demo', '/demo');
  html = html.replaceAll(' or write to .', '.');
  html = html.replaceAll('hello@drking.ai', 'info@drking.ai');

  // Keep security and privacy language aligned with the Australian market.
  // Avoid advertising overseas frameworks or unverified certifications.
  const securityAnswer = 'Clinical records remain in your practice management system. DrKing’s data handling is reviewed against the Australian Privacy Principles and the requirements agreed for your deployment. Ask us about the applicable controls and responsibilities.';
  const securityClaims = [
    'No clinical data is stored. DrKing is designed to support GDPR and Australian Privacy Principles requirements, with HIPAA-ready workflows and PCI-compliant payments. Ask us about the controls and configuration for your practice.',
    'DrKing does not store clinical or patient health records. It operates on secure, encrypted infrastructure compliant with GDPR, Australian Privacy Principles, and HIPAA for communication workflows.',
    'No clinical data is stored. DrKing is built around GDPR and Australian Privacy Principles (APP), is HIPAA ready, and supports PCI-compliant payments.',
    'No clinical data is stored in DrKing. The platform uses GDPR, Australian Privacy Principles and HIPAA-ready infrastructure. Ask our team about the security requirements for your particular setup.',
    'No clinical data is stored. DrKing is designed to support GDPR and Australian Privacy Principles requirements, with HIPAA-ready workflows and PCI-compliant payments. Ask us about the controls and configuration for your practice.',
  ];
  for (const claim of securityClaims) html = html.replaceAll(claim, securityAnswer);
  html = html.replaceAll('GDPR<small>Privacy</small>', 'Data<small>Minimisation</small>');
  html = html.replaceAll('HIPAA<small>Ready</small>', 'Australian<small>Focused</small>');
  html = html.replaceAll('GDPR', 'Data minimisation');
  html = html.replaceAll('HIPAA Ready', 'Australian-focused');
  html = html.replaceAll('HIPAA readiness', 'Australian deployment review');
  html = html.replaceAll('HIPAA-ready', 'Australian-focused');
  html = html.replaceAll('HIPAA', 'Australian Privacy Principles');
  html = html.replaceAll('PCI Compliant', 'Secure payment handling');
  html = html.replaceAll('PCI<small>Compliant</small>', 'Payments<small>Secure handling</small>');
  html = html.replaceAll('PCI-compliant payments', 'secure payment handling');
  html = html.replaceAll('PCI compliance', 'secure payment handling');
  html = html.replaceAll('ISO-Certified Servers', 'Deployment-specific review');
  html = html.replaceAll('ISO-Certified<br>Servers', 'Deployment-specific<br>review');
  html = html.replaceAll('ISO-certified servers', 'deployment-specific review');

  // Forms now submit to the same-site enquiry service. Email remains a
  // clearly labelled fallback only when the endpoint is unavailable.
  html = html.replaceAll('This opens your email app with your details ready to send. Add your DrKing contact, review, and send to get started.', 'Submitted securely to DrKing. Business details only, please; do not include patient information or passwords.');
  html = html.replaceAll('Opens an email draft.<br>Review it, then hit send.', 'Submitted securely to DrKing.<br>Business details only, please.');
  html = html.replaceAll('This opens a draft in your email app to info@drking.ai. Review and send it to request your demo. Please don’t include patient or clinical information.', 'Submitted securely to DrKing. Please don’t include patient or clinical information.');
  html = html.replaceAll('This will open your email app with a pre-filled draft. Review it and press send to complete your request.', 'Your request is submitted securely to DrKing. Please don’t include patient or clinical information.');
  html = html.replaceAll('Your email draft is ready. Review it in your email app, add your DrKing contact, and press send. Your details have not been submitted yet.', 'Your details are ready to submit securely to DrKing.');
  html = html.replaceAll('Opens a prefilled email. Just review and send.<br>Your details are only used to arrange your demo.', 'Submitted securely to DrKing.<br>Your details are only used to arrange your demo.');
  html = html.replaceAll('Tell us a little about your team. We’ll prepare an email request for you to send to DrKing.', 'Tell us a little about your team and submit your demo request securely to DrKing.');
  html = html.replaceAll('Prepare my demo email', 'Submit my demo request');
  html = html.replaceAll('Opens your email app. Send the draft to request your demo. Please don’t include resident or health information. You can also email', 'Submitted securely to DrKing. Please don’t include resident or health information. If the service is unavailable, email');
  html = html.replaceAll('Tell us a little about your practice. Send your request by email and our team will help find a time that suits you.', 'Tell us a little about your practice and submit your request securely. Our team will help find a time that suits you.');
  html = html.replaceAll('Email my demo request', 'Submit my demo request');
  html = html.replaceAll('Opens your email app with your request ready to send. Or call', 'Submitted securely to DrKing. Or call');
  html = html.replaceAll('This form opens your email app with your enquiry ready to send.', 'This form submits your enquiry securely to DrKing.');
  html = html.replaceAll('Email My Demo Request', 'Submit My Demo Request');
  html = html.replaceAll('Opens a prefilled email to <a href="mailto:info@drking.ai">info@drking.ai</a>. Send it from your email app to register your interest.', 'Submitted securely to DrKing. If the service is unavailable, use the email fallback shown after you submit.');

  const formTypes = {
    'demo-form': 'demo-request',
    'enquiry-form': 'general-enquiry',
    'waitlist-form': 'integration-waitlist',
    'intake-form': 'client-intake',
  };
  html = html.replace(/<form\b([^>]*\bid=["']([^"']+)["'][^>]*)>/gi, (tag, attributes, id) => {
    const type = formTypes[id];
    if (!type || /\bdata-drking-form=/i.test(attributes)) return tag;
    return `<form${attributes} data-drking-form="${type}">`;
  });

  // Every website enquiry needs a callable phone number. Existing phone fields
  // are made required; forms without one receive markup matching their layout.
  html = html.replace(/<form\b[^>]*data-drking-form=["'][^"']+["'][^>]*>[\s\S]*?<\/form>/gi, (form) => {
    let updated = form
      .replace(/(<label\b[^>]*for=["'][^"']*phone[^"']*["'][^>]*>[^<]*?)\s*<span>\(optional\)<\/span>/i, '$1 <span>(required)</span>')
      .replace(/<input\b([^>]*\btype=["']tel["'][^>]*)>/gi, (tag, attributes) => /\brequired\b/i.test(attributes) ? tag : `<input${attributes} required>`);
    if (/<input\b[^>]*\btype=["']tel["']/i.test(updated)) return updated;

    const idPrefix = /\bid=["']demo-form["']/i.test(updated) ? 'demo-' : '';
    const input = `<label for="${idPrefix}phone">Phone number</label><input id="${idPrefix}phone" name="phone" type="tel" autocomplete="tel" required maxlength="40">`;
    const field = updated.includes('class="form-field"')
      ? `<div class="form-field">${input}</div>`
      : updated.includes('class="field"')
        ? `<div class="field">${input}</div>`
        : input;
    return updated.replace(/<button\b([^>]*\btype=["']submit["'][^>]*)>/i, `${field}<button$1>`);
  });

  if (file === 'integrations.html') {
    html = html.replace(/<script>document\.addEventListener\("DOMContentLoaded",function\(\)\{var mt=document\.querySelector\("\.menu-toggle"\)[\s\S]*?<\/script>\s*/i, '');
    html = html.replace("document.documentElement.classList.add('js');\nconst menu=document.querySelector('.menu-toggle'), navigation=document.querySelector('.nav-links');\nfunction closeMenu(){navigation.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu')}\nmenu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';navigation.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu')});\nnavigation.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu()});\ndocument.addEventListener('keydown',e=>{if(e.key==='Escape'&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus()}});\ndocument.addEventListener('click',e=>{if(!e.target.closest('.nav'))closeMenu()});\nwindow.matchMedia('(min-width:601px)').addEventListener('change',closeMenu);\n", "document.documentElement.classList.add('js');\n");
  }
  if (file === 'contact.html') {
    html = html.replaceAll('or start an email draft.', 'or send an online enquiry.');
    html = html.replaceAll('Absolutely. Use the , or call us on', 'Absolutely. Use the enquiry form, or call us on');
    html = html.replaceAll('The form opens your email app with a draft addressed to our team. Your message is only sent when you send that email. If no email app opens, copy your message into an email to <a href="mailto:info@drking.ai">info@drking.ai</a>.', 'The form securely records your enquiry for the DrKing team. If the service is unavailable, you can choose the clearly labelled email fallback.');
    html = html.replaceAll('You’ll find us at , Australia.', 'You’ll find us at 1 Elgin Pl, Hawthorn VIC 3122, Australia.');
  }
  if (file === 'privacy.html') {
    html = html.replace(/<div class="template-note">[\s\S]*?<\/div>\s*/i, '');
    const formPrivacyParagraph = '<p>Website enquiry forms send business contact details to DrKing’s Cloudflare-hosted enquiry service. Enquiries are stored in an access-controlled database and may be forwarded to the configured customer relationship management system.</p>';
    if (!html.includes(formPrivacyParagraph)) {
      html = html.replaceAll(
        '<p>Please only share information needed for your enquiry. This website is not a channel for providing patient health records or requesting medical care.</p>',
        `<p>Please only share information needed for your enquiry. This website is not a channel for providing patient health records or requesting medical care.</p>${formPrivacyParagraph}`,
      );
    }
    while (html.includes(formPrivacyParagraph + formPrivacyParagraph)) html = html.replaceAll(formPrivacyParagraph + formPrivacyParagraph, formPrivacyParagraph);
    html = html.replaceAll(
      '<p>Where applicable law requires a legal basis, we rely on the performance of a contract, compliance with a legal obligation, our legitimate interests in running and securing the service, or your consent. The basis depends on the information and the purpose for which it is used.</p>',
      '<p>We handle personal information for the purposes for which it was collected, related purposes you would reasonably expect, purposes you consent to, and purposes otherwise permitted or required by Australian law.</p>',
    );
    html = html.replaceAll(
      '<p>If information is processed outside your country, applicable data protection requirements and appropriate transfer safeguards should be followed. The protections available in another country may differ from those where you live.</p>',
      '<p>If personal information is disclosed to a recipient outside Australia, we assess the arrangement against the Australian Privacy Principles and take reasonable steps appropriate to the circumstances. Privacy protections in another country may differ from those in Australia.</p>',
    );
    html = html.replaceAll(
      '<p>Depending on your location and applicable law, you may have the right to:</p><ul><li>Request access to the personal information held about you.</li><li>Ask for inaccurate or incomplete information to be corrected.</li><li>Request deletion, restriction, or a portable copy of your information.</li><li>Object to certain processing, including direct marketing.</li><li>Withdraw consent where processing is based on your consent.</li></ul><p>To make a request, use the contact guidance below. We may need to verify your identity before responding. Some rights are subject to legal exceptions; requests should be handled within the time limits required by applicable law.</p><p>You may also raise a concern with your local data protection authority. For information about UK privacy rights, visit the <a href="https://ico.org.uk/for-the-public/">Information Commissioner’s Office</a>.</p>',
      '<p>Under Australian privacy law, you may ask to:</p><ul><li>Access personal information we hold about you.</li><li>Correct personal information that is inaccurate, out of date, incomplete, irrelevant, or misleading.</li><li>Opt out of direct marketing communications.</li><li>Make a privacy complaint and receive a response.</li></ul><p>To make a request, use the contact guidance below. We may need to verify your identity before responding, and legal exceptions may apply.</p><p>If you are not satisfied with our response, you can contact the <a href="https://www.oaic.gov.au/privacy/privacy-complaints">Office of the Australian Information Commissioner</a>.</p>',
    );
    html = html.replaceAll('<a class="button" href="https://drking.ai/">Visit DrKing', '<a class="button" href="/contact">Contact DrKing');
  }
  if (file === 'security.html') {
    html = html.replaceAll('Explore DrKing security compliance: no clinical data stored, enterprise-grade protection, complete communication records, and privacy-conscious automation for your clinic.', 'Explore DrKing’s Australian-focused security approach, data boundaries and deployment-specific controls for clinic communication workflows.');
    html = html.replaceAll('No clinical data stored. Built secure from the ground up. Explore security and privacy at DrKing.', 'Clinical records remain in your practice system. Explore DrKing’s security and privacy approach.');
    html = html.replaceAll('No clinical data stored.<br>Built <em>secure</em> from<br>the ground up.', 'Clinical records stay<br>in your <em>practice system.</em>');
    html = html.replaceAll('DrKing intentionally avoids handling patient health records. We focus solely on lead generation, communication, and automation — keeping your clinic secure and compliant with Australian healthcare standards.', 'DrKing is designed for enquiries, communication and business automation, while clinical records remain in your practice systems. The controls and responsibilities for your deployment are confirmed during setup.');
    html = html.replaceAll('Enterprise-grade<br>protection.', 'Access controls,<br>confirmed for you.');
    html = html.replaceAll('Two-factor authentication, role-based access, and audit logs help keep your account protected and the right information in the right hands.', 'Available identity, access and activity-recording controls are confirmed for your selected services and deployment before rollout.');
    html = html.replaceAll('Complete communication<br>records.', 'Communication history,<br>where configured.');
    html = html.replaceAll('A full audit trail gives your team a clear record of communications. Stay accountable, keep context, and follow every conversation with confidence.', 'Configured communication history can help authorised team members preserve context and follow conversations. Retention and access settings are confirmed during setup.');
    html = html.replaceAll('DrKing provides two-factor authentication, role-based access, and audit logs. Together, these features help your team manage who has access and maintain visibility into account activity.', 'Available identity, access and activity-recording controls depend on the selected services and deployment. We confirm the applicable controls and responsibilities before rollout.');
    html = html.replaceAll('DrKing’s security approach includes Data minimisation, Australian deployment review, the Australian Privacy Principles, secure payment handling, and deployment-specific review. Australian deployment review describes preparedness; it is not a certification. Your clinic’s compliance also depends on how you configure and use the platform.', 'DrKing’s approach focuses on data minimisation, the Australian Privacy Principles, access controls and secure payment handling where applicable. The exact controls and responsibilities are confirmed for your deployment; these statements are not certifications.');
    html = html.replaceAll('Yes. Complete communication records provide a full audit trail, helping your team follow conversations, preserve context, and maintain accountability.', 'Communication history is available where it is part of the configured service. Access, retention and export options are confirmed for your deployment.');
  }
  if (file === 'terms.html') {
    html = html.replace(/<div class="template">[\s\S]*?<\/div>\s*/i, '');
    const australianTermsParagraph = '<p>These Terms are governed by the laws of Victoria, Australia. Nothing in these Terms excludes, restricts, or modifies any guarantee, right, or remedy that cannot lawfully be excluded under the Australian Consumer Law or other applicable Australian law.</p>';
    if (!html.includes(australianTermsParagraph)) {
      html = html.replaceAll(
        '<p>If a provision is found unenforceable, the remaining provisions continue in effect. A delay in enforcing a right does not waive that right. These Terms and any applicable purchase or feature-specific terms form the agreement regarding your use of the Service.</p>',
        `<p>If a provision is found unenforceable, the remaining provisions continue in effect. A delay in enforcing a right does not waive that right. These Terms and any applicable purchase or feature-specific terms form the agreement regarding your use of the Service.</p>${australianTermsParagraph}`,
      );
    }
    while (html.includes(australianTermsParagraph + australianTermsParagraph)) html = html.replaceAll(australianTermsParagraph + australianTermsParagraph, australianTermsParagraph);
  }
  if (file === 'roi-calculator.html') {
    html = html.replace(/<script>\s*\/\/ Wire up mobile-nav toggle for roi-calculator[\s\S]*?<\/script>\s*/i, '');
    html = html.replace("new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'", "new Intl.NumberFormat('en-AU',{style:'currency',currency:'AUD'");
    html = html.replaceAll('"priceCurrency":"USD"', '"priceCurrency":"AUD"');
    html = html.replaceAll('Patient value means revenue per completed appointment, in USD.', 'Patient value means revenue per completed appointment, in AUD.');
    html = html.replaceAll('Average patient value in US dollars', 'Average patient value in Australian dollars');
  }
  if (file === 'online-reviews.html') {
    html = html.replace('`$${Math.round(value*.05/1000)}K–$${Math.round(value*.09/1000)}K`', '`A$${Math.round(value*.05/1000)}K–A$${Math.round(value*.09/1000)}K`');
  }
  if (file === 'multi-location-chaos.html') {
    html = html.replace(/A*\$1\.54M/g, () => 'A$1.54M');
    html = html.replace(
      /total>=1e6\?'(?:A)?\$'\+\(total\/1e6\)\.toFixed\(2\)\+'M':'(?:A)?\$'\+Math\.round\(total\/1000\)\+'K'/,
      () => "total>=1e6?'A$'+(total/1e6).toFixed(2)+'M':'A$'+Math.round(total/1000)+'K'",
    );
  }
  if (file === 'patient-reactivation.html') {
    html = html.replace("const patients=document.getElementById('patients'),format=new Intl.NumberFormat('en-AU');", "const patients=document.getElementById('patients'),format=new Intl.NumberFormat('en-AU'),money=new Intl.NumberFormat('en-AU',{style:'currency',currency:'AUD',maximumFractionDigits:0});");
    html = html.replace("document.getElementById('revenue-total').textContent='$'+format.format(value*.15*200)", "document.getElementById('revenue-total').textContent=money.format(value*.15*200)");
  }
  if (file === 'medical-centres.html') {
    html = html.replace(/<form class="calculator" onsubmit="return false">([\s\S]*?)<\/form>/i, '<div class="calculator">$1</div>');
    html = html.replace(/<label class="input-row" for="([^"]+)">([\s\S]*?<input[^>]*id="\1"[^>]*>)<\/label>/gi, '<label class="input-row">$2</label>');
  }

  if (file === 'case-studies.html' || file === 'referral-partner.html') {
    html = html.replace(/(<script\s+type=["']application\/ld\+json["']>)([\s\S]*?)(<\/script>)/i, (block, open, json, close) => {
      try {
        JSON.parse(json);
        return block;
      } catch {
        return `${open}${json.trimEnd()}]}${close}`;
      }
    });
  }

  // Replace repeated inline footers with one shared component. A legacy About
  // footer closed its legal dialog by mistake, so repair any dialog imbalance
  // immediately before the first following script.
  html = html.replace(/<footer\b[\s\S]*?<\/footer>\s*/gi, '');
  html = html.replace(/<\/footer>\s*/gi, '');
  const dialogOpenCount = (html.match(/<dialog\b/gi) || []).length;
  const dialogCloseCount = (html.match(/<\/dialog>/gi) || []).length;
  if (dialogOpenCount > dialogCloseCount) {
    const lastDialog = html.toLowerCase().lastIndexOf('<dialog');
    const nextScript = html.toLowerCase().indexOf('<script', lastDialog);
    const insertionPoint = nextScript >= 0 ? nextScript : html.toLowerCase().indexOf('</body>');
    const closingTags = '</dialog>'.repeat(dialogOpenCount - dialogCloseCount);
    html = html.slice(0, insertionPoint) + closingTags + '\n' + html.slice(insertionPoint);
  }

  html = html.replace(/<button\b(?![^>]*\btype=)/gi, '<button type="button"');
  html = html.replace(/<input\b(?![^>]*\btype=)/gi, '<input type="text"');
  html = html.replace(/<noscript>\s*<style>[\s\S]*?<\/style>\s*<\/noscript>\s*/gi, '');
  html = html.replace(/<label for="enquiries">Your daily after-hours enquiries <output id="enquiry-count" for="enquiries">8<\/output><\/label>/g, '<label for="enquiries">Your daily after-hours enquiries <span id="enquiry-count">8</span></label>');
  html = html.replace(/<label for="missed-calls">Unanswered calls per day <output id="call-count" for="missed-calls">3<\/output><\/label>/g, '<label for="missed-calls">Unanswered calls per day <span id="call-count">3</span></label>');
  html = html.replace(/<label for="locations">Number of clinic locations <output id="location-value" for="locations">5<\/output><\/label>/g, '<label for="locations">Number of clinic locations <span id="location-value">5</span></label>');
  html = html.replace(/<label for="appointments">Appointments per week <output id="appointments-value" for="appointments">40<\/output><\/label>/g, '<label for="appointments">Appointments per week <span id="appointments-value">40</span></label>');
  html = html.replace(/<label for="price">Average appointment value <output id="price-value" for="price">\$250<\/output><\/label>/g, '<label for="price">Average appointment value <span id="price-value">$250</span></label>');
  html = html.replace(/<label for="rate">No-show rate <output id="rate-value" for="rate">15%<\/output><\/label>/g, '<label for="rate">No-show rate <span id="rate-value">15%</span></label>');
  html = html.replace(/<div\b([^>]*)>/gi, (tag, attributes) => {
    if (!/\baria-label=/i.test(attributes) || /\brole=/i.test(attributes)) return tag;
    const className = attributes.match(/\bclass=["']([^"']*)["']/i)?.[1] || '';
    const role = /\bbreadcrumb\b/i.test(className)
      ? 'navigation'
      : /\b(?:hero-art|calendar-demo|feature-art|little-story|dashboard|platform-logo|bar-chart|flow)\b/i.test(className)
        ? 'img'
        : 'group';
    return `<div role="${role}"${attributes}>`;
  });
  html = html.replace(/<span\b([^>]*\bclass=["'][^"']*\bstatus\b[^"']*["'][^>]*\baria-label=["'][^"']+["'][^>]*)>/gi, (tag, attributes) => /\brole=/i.test(attributes) ? tag : `<span role="status"${attributes}>`);
  html = html.replace(/<svg\b([^>]*\baria-label=["'][^"']+["'][^>]*)>/gi, (tag, attributes) => /\brole=/i.test(attributes) ? tag : `<svg role="img"${attributes}>`);
  html = html.replace(/<label class="calc-label" for="residents">([\s\S]*?<input[^>]*id="residents"[^>]*>)<\/label>/gi, '<label class="calc-label">$1</label>');
  // Keep the footer before page-end inline scripts. Several original page
  // controllers update #year synchronously and also enable reveal animations;
  // placing the footer after those scripts makes the year lookup throw and can
  // leave the page content permanently transparent.
  html = html.replace(/<\/main>/i, `</main>\n${siteFooter}`);

  html = html.replace(/<script[^>]+src=["']\/assets\/form-submissions\.js["'][^>]*><\/script>\s*/gi, '');
  html = html.replace(/<meta\s+(?:property|name)=["'](?:og:(?:site_name|locale|image(?::(?:secure_url|type|width|height|alt))?)|twitter:(?:card|image|image:alt))["'][^>]*>\s*/gi, '');
  const socialImage = '<meta property="og:site_name" content="DrKing">\n<meta property="og:locale" content="en_AU">\n<meta property="og:image" content="https://drking.ai/assets/drking-social-share.jpg?v=ae223eb8">\n<meta property="og:image:secure_url" content="https://drking.ai/assets/drking-social-share.jpg?v=ae223eb8">\n<meta property="og:image:type" content="image/jpeg">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n<meta property="og:image:alt" content="DrKing AI communication for Australian healthcare practices — a clinician welcoming a patient with calls, messages and appointment booking.">\n<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:image" content="https://drking.ai/assets/drking-social-share.jpg?v=ae223eb8">\n<meta name="twitter:image:alt" content="DrKing AI communication for Australian healthcare practices — a clinician welcoming a patient with calls, messages and appointment booking.">\n';
  const assets = `${socialImage}<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300..600;1,300..600&amp;display=swap" rel="stylesheet">\n<link rel="stylesheet" href="/assets/site-shell.css">\n<script src="/assets/site-shell.js" defer></script>\n<script src="/assets/international-phone.js" defer></script>\n<script src="/assets/form-submissions.js" defer></script>\n`;
  html = html.replace(/<\/head>/i, `${assets}</head>`);
  fs.writeFileSync(full, html);
}
