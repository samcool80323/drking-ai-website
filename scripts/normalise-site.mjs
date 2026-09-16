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

const siteHeader = `<header class="site-header">
<a class="brand" href="/" aria-label="DrKing home"><img class="brand-logo" src="/drking-logo.svg" alt="DrKing"></a>
<nav class="nav-links navlinks" id="site-desktop-nav" aria-label="Main navigation">
<div class="mega-menu"><button type="button" class="mega-toggle" aria-haspopup="true">Industries</button><div class="mega-panel">
<a class="mega-item" href="/dentists"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Dental Clinics</span><span class="mega-desc">Capture every call, book more chairs</span></span></a>
<a class="mega-item" href="/general-practice"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">General Practice</span><span class="mega-desc">Reduce wait times, lighten reception</span></span></a>
<a class="mega-item" href="/specialists"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Specialists</span><span class="mega-desc">Convert more referrals into patients</span></span></a>
<a class="mega-item" href="/allied-health"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Allied Health</span><span class="mega-desc">Keep patients on their treatment plan</span></span></a>
<a class="mega-item" href="/medical-centres"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Medical Centres</span><span class="mega-desc">Multi-location support</span></span></a>
<a class="mega-item" href="/cosmetic-clinics"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Cosmetic Clinics</span><span class="mega-desc">Respond while interest is high</span></span></a>
<a class="mega-item" href="/veterinary"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Veterinary</span><span class="mega-desc">After-hours enquiry support</span></span></a>
<a class="mega-item" href="/aged-care"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Aged Care</span><span class="mega-desc">Clear family communication</span></span></a>
</div></div>
<div class="mega-menu"><button type="button" class="mega-toggle" aria-haspopup="true">Solutions</button><div class="mega-panel">
<a class="mega-item" href="/ai-voice-receptionist"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">AI Voice Receptionist</span><span class="mega-desc">Answer calls around the clock</span></span></a>
<a class="mega-item" href="/ai-chat"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">AI Web Chat</span><span class="mega-desc">Help website visitors take action</span></span></a>
<a class="mega-item" href="/missed-call-recovery"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Missed Call Recovery</span><span class="mega-desc">Follow up unanswered calls</span></span></a>
<a class="mega-item" href="/text-to-pay"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Text-to-Pay</span><span class="mega-desc">Simple SMS payment links</span></span></a>
<a class="mega-item" href="/review-generator"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Review Generator</span><span class="mega-desc">Consistent review invitations</span></span></a>
<a class="mega-item" href="/appointment-reminders"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Reminders</span><span class="mega-desc">Support appointment attendance</span></span></a>
<a class="mega-item" href="/lead-management"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Lead CRM</span><span class="mega-desc">Bring enquiries into one pipeline</span></span></a>
<a class="mega-item" href="/analytics"><span class="mega-icon" aria-hidden="true">+</span><span class="mega-text"><span class="mega-title">Analytics</span><span class="mega-desc">See which channels create demand</span></span></a>
</div></div>
<a href="/integrations">Integrations</a><a href="/about">About</a>
</nav>
<div class="header-right"><a class="button teal" href="/demo">Let’s talk <span aria-hidden="true">↗</span></a><button type="button" class="menu-toggle menu-button mobile-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-nav"><svg aria-hidden="true" viewBox="0 0 24 24"><path d="M4 8h16M4 16h16" fill="none" stroke="currentColor" stroke-width="1.5"></path></svg></button></div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="Mobile navigation" inert>
<div class="mobile-group"><div class="mobile-group-label">Industries</div><a href="/dentists">Dental Clinics</a><a href="/general-practice">General Practice</a><a href="/specialists">Specialists</a><a href="/allied-health">Allied Health</a><a href="/medical-centres">Medical Centres</a><a href="/cosmetic-clinics">Cosmetic Clinics</a><a href="/veterinary">Veterinary</a><a href="/aged-care">Aged Care</a></div>
<div class="mobile-group"><div class="mobile-group-label">Solutions</div><a href="/ai-voice-receptionist">AI Voice Receptionist</a><a href="/ai-chat">AI Web Chat</a><a href="/missed-call-recovery">Missed Call Recovery</a><a href="/text-to-pay">Text-to-Pay</a><a href="/review-generator">Reviews</a><a href="/appointment-reminders">Reminders</a><a href="/lead-management">Lead CRM</a><a href="/analytics">Analytics</a></div>
<div class="mobile-group"><div class="mobile-group-label">Company</div><a href="/integrations">Integrations</a><a href="/about">About</a><a href="/contact">Contact</a></div>
<a href="/demo" class="mobile-cta">Book a Free Demo</a>
</nav>`;

const siteFooter = `<footer class="site-footer">
<div class="site-footer-inner">
<div class="site-footer-brand"><a href="/" aria-label="DrKing home"><img src="/drking-logo.svg" alt="DrKing"></a><p>Practical AI communication tools for Australian healthcare practices.</p></div>
<nav class="site-footer-nav" aria-label="Footer navigation">
<div><h2>Industries</h2><a href="/dentists">Dental Clinics</a><a href="/general-practice">General Practice</a><a href="/specialists">Specialists</a><a href="/allied-health">Allied Health</a></div>
<div><h2>Solutions</h2><a href="/ai-voice-receptionist">AI Voice Receptionist</a><a href="/missed-call-recovery">Missed Call Recovery</a><a href="/appointment-reminders">Reminders</a><a href="/analytics">Analytics</a></div>
<div><h2>Company</h2><a href="/about">About</a><a href="/integrations">Integrations</a><a href="/contact">Contact</a><a href="/demo">Book a Demo</a></div>
</nav>
</div>
<div class="site-footer-bottom"><p>© <span id="year">2026</span> DrKing. All rights reserved.</p><div><a href="/privacy">Privacy</a><a href="/terms">Terms</a></div></div>
</footer>`;

for (const file of pages) {
  const full = path.join(root, file);
  let html = fs.readFileSync(full, 'utf8');

  html = html.replace(/<link[^>]+(?:fonts\.googleapis\.com|fonts\.gstatic\.com|\/assets\/site-shell\.css)[^>]*>\s*/gi, '');
  html = html.replace(/<style>html\{overflow-x:hidden!important\}body\{overflow-x:hidden!important\}<\/style>\s*/gi, '');
  html = html.replace(/<script[^>]+src=["']\/assets\/site-shell\.js["'][^>]*><\/script>\s*/gi, '');
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
  html = html.replaceAll('https://drking.ai/demo', '/demo');
  html = html.replaceAll('https://drking.ai/#button-LZar9xGjf-', '/demo');
  html = html.replaceAll('/multi-location-management', '/multi-location-chaos');
  html = html.replaceAll('/#book-demo', '/demo');
  html = html.replaceAll(' or write to .', '.');

  if (file === 'integrations.html') {
    html = html.replace(/<script>document\.addEventListener\("DOMContentLoaded",function\(\)\{var mt=document\.querySelector\("\.menu-toggle"\)[\s\S]*?<\/script>\s*/i, '');
    html = html.replace("document.documentElement.classList.add('js');\nconst menu=document.querySelector('.menu-toggle'), navigation=document.querySelector('.nav-links');\nfunction closeMenu(){navigation.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open menu')}\nmenu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';navigation.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close menu':'Open menu')});\nnavigation.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu()});\ndocument.addEventListener('keydown',e=>{if(e.key==='Escape'&menu.getAttribute('aria-expanded')==='true'){closeMenu();menu.focus()}});\ndocument.addEventListener('click',e=>{if(!e.target.closest('.nav'))closeMenu()});\nwindow.matchMedia('(min-width:601px)').addEventListener('change',closeMenu);\n", "document.documentElement.classList.add('js');\n");
  }
  if (file === 'roi-calculator.html') {
    html = html.replace(/<script>\s*\/\/ Wire up mobile-nav toggle for roi-calculator[\s\S]*?<\/script>\s*/i, '');
    html = html.replace("new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'", "new Intl.NumberFormat('en-AU',{style:'currency',currency:'AUD'");
    html = html.replaceAll('"priceCurrency":"USD"', '"priceCurrency":"AUD"');
    html = html.replaceAll('Patient value means revenue per completed appointment, in USD.', 'Patient value means revenue per completed appointment, in AUD.');
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

  const assets = '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,300..600;1,300..600&amp;display=swap" rel="stylesheet">\n<link rel="stylesheet" href="/assets/site-shell.css">\n<script src="/assets/site-shell.js" defer></script>\n';
  html = html.replace(/<\/head>/i, `${assets}</head>`);
  fs.writeFileSync(full, html);
}
