import os as _os, sys as _sys
if _os.environ.get('DRKING_ALLOW_LEGACY') != '1':
    _sys.exit('LEGACY GENERATOR: the committed *.html files are now the source of truth (claims cleaned, sprites restored 2026-10-31). Re-running this would overwrite them with old copy. Set DRKING_ALLOW_LEGACY=1 only if you have ported those fixes into this script.')
"""Build two brand-awareness blog posts for DrKing.

Generates narrative, blog-style pages about the missed-call text-back flow and
the voice AI answering flow, with honest vendor integration statuses and
original inline SVG illustrations in the existing brand palette.
Only writes the two named HTML routes. Does not touch product pages, /aida,
claim revisions, Cloudflare, routing, or production.
"""
from pathlib import Path
from html import escape
import json

root = Path(__file__).resolve().parents[1]
source = (root / 'ai-voice-receptionist.html').read_text()
body_open = source.index('<body>')
main_open = source.index('<main id="main">', body_open)
footer_open = source.index('<footer class="site-footer">', main_open)
footer_end = source.index('</footer>', footer_open) + len('</footer>')
shell = source[body_open + len('<body>'):main_open]
site_footer = source[footer_open:footer_end]

VENDORS_NOW = [
    ('Cliniko', 'Allied health'),
    ('Nookal', 'Allied health'),
    ('Power Diary', 'Allied health · Psychology'),
    ('Dentally', 'Dental'),
    ('Dental4Web', 'Dental'),
]
VENDORS_ROADMAP = [
    ('Core Practice', 'Planned', 'Scope and timing being confirmed. The standalone toolkit works today.'),
    ('Best Practice', 'Waitlist open', 'Register interest and the team will keep you updated.'),
]


def vendor_grid(now, roadmap):
    cards = ''.join(
        f'<li class="vendor-card now"><span class="vendor-name">{escape(n)}</span>'
        f'<span class="vendor-type">{escape(t)}</span>'
        f'<span class="vendor-status">Available now</span></li>'
        for n, t in now
    )
    road = ''.join(
        f'<li class="vendor-card road"><span class="vendor-name">{escape(n)}</span>'
        f'<span class="vendor-status">{escape(s)}</span>'
        f'<p class="vendor-note">{escape(d)}</p></li>'
        for n, s, d in roadmap
    )
    return (
        f'<div class="vendor-intro"><p>DrKing works alongside your practice management system — not instead of it. '
        f'If your practice runs one of these systems, booking details flow straight into your existing calendar. '
        f'On another system? Every DrKing tool still runs standalone while the integration roadmap grows.</p></div>'
        f'<ul class="vendor-grid" role="list">{cards}</ul>'
        f'<h3 class="roadmap-heading">On the roadmap</h3>'
        f'<ul class="vendor-grid roadmap" role="list">{road}</ul>'
    )


def sms_graphic():
    return '''<figure class="article-figure hero-figure" role="img" aria-label="Illustration of a missed call turning into a text conversation and a booked appointment. A soft phone outline shows a missed-call notification at the top, a friendly text exchange in the middle, and a confirmed calendar slot at the bottom.">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" role="img">
<defs>
<linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9eade"/><stop offset="1" stop-color="#f7f5f2"/></linearGradient>
</defs>
<rect width="560" height="520" rx="28" fill="url(#bg1)"/>
<path d="M40 470C120 500 220 440 300 470s180 20 220-10v40H40Z" fill="#dfe6df" opacity=".7"/>
<g transform="translate(180,40)">
<rect x="0" y="0" width="200" height="420" rx="30" fill="#fffdf9" stroke="#d8d5cd" stroke-width="2"/>
<rect x="0" y="0" width="200" height="56" rx="30" fill="#0d5c5c"/><rect x="0" y="30" width="200" height="26" fill="#0d5c5c"/>
<circle cx="100" cy="28" r="14" fill="none" stroke="#f7f5f2" stroke-width="2"/>
<path d="M94 22l12 12m0-12l-12 12" stroke="#c8553d" stroke-width="2.5" stroke-linecap="round"/>
<text x="100" y="52" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="11" fill="#f2ede4">Missed call · just now</text>
<g transform="translate(18,80)">
<rect x="0" y="0" width="164" height="34" rx="17" fill="#eef3ee"/>
<text x="12" y="22" font-family="Geomanist,sans-serif" font-size="11.5" fill="#1c1814">Hi! Sorry we missed you.</text>
</g>
<g transform="translate(18,124)">
<rect x="0" y="0" width="164" height="48" rx="17" fill="#eef3ee"/>
<text x="12" y="20" font-family="Geomanist,sans-serif" font-size="11.5" fill="#1c1814">Would you like to book</text>
<text x="12" y="36" font-family="Geomanist,sans-serif" font-size="11.5" fill="#1c1814">an appointment?</text>
</g>
<g transform="translate(30,184)">
<rect x="0" y="0" width="152" height="34" rx="17" fill="#0d5c5c"/>
<text x="12" y="22" font-family="Geomanist,sans-serif" font-size="11.5" fill="#f7f5f2">Yes — tomorrow?</text>
</g>
<g transform="translate(18,230)">
<rect x="0" y="0" width="164" height="48" rx="17" fill="#eef3ee"/>
<text x="12" y="20" font-family="Geomanist,sans-serif" font-size="11.5" fill="#1c1814">9:30 am is available</text>
<text x="12" y="36" font-family="Geomanist,sans-serif" font-size="11.5" fill="#1c1814">with Dr Patel. Book it?</text>
</g>
<g transform="translate(30,290)">
<rect x="0" y="0" width="152" height="34" rx="17" fill="#0d5c5c"/>
<text x="12" y="22" font-family="Geomanist,sans-serif" font-size="11.5" fill="#f7f5f2">Yes please!</text>
</g>
<g transform="translate(40,352)">
<rect x="0" y="0" width="120" height="48" rx="14" fill="#e3eae3" stroke="#a8c5b5" stroke-width="1.5"/>
<circle cx="20" cy="24" r="10" fill="#0d5c5c"/>
<path d="M15 24l3.5 3.5L26 20" stroke="#f7f5f2" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<text x="38" y="21" font-family="Geomanist,sans-serif" font-size="10" font-weight="600" fill="#17483e">Booked</text>
<text x="38" y="34" font-family="Geomanist,sans-serif" font-size="9" fill="#344d45">Tomorrow · 9:30 am</text>
</g>
</g>
<g transform="translate(44,120)">
<circle cx="22" cy="22" r="22" fill="#c8553d" opacity=".9"/>
<text x="22" y="27" text-anchor="middle" font-family="Newsreader,serif" font-size="20" fill="#fffdf9">1</text>
</g>
<g transform="translate(494,250)">
<circle cx="22" cy="22" r="22" fill="#0d5c5c" opacity=".9"/>
<text x="22" y="27" text-anchor="middle" font-family="Newsreader,serif" font-size="20" fill="#f7f5f2">2</text>
</g>
<g transform="translate(60,390)">
<circle cx="22" cy="22" r="22" fill="#a8c5b5"/>
<text x="22" y="27" text-anchor="middle" font-family="Newsreader,serif" font-size="20" fill="#17483e">3</text>
</g>
</svg>
<figcaption>The three beats of the text-back journey: the missed call, the conversation, the confirmed booking. Illustrative conversation, not a real patient.</figcaption>
</figure>'''


def voice_graphic():
    return '''<figure class="article-figure hero-figure" role="img" aria-label="Illustration of a call being answered by an AI voice assistant that books, flags for staff, or escalates to a person. Soft concentric voice waves lead from a phone icon to three labelled destinations: a calendar for bookings, a flag for staff review, and a person for urgent concerns.">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" role="img">
<defs>
<linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9eade"/><stop offset="1" stop-color="#f7f5f2"/></linearGradient>
</defs>
<rect width="560" height="520" rx="28" fill="url(#bg2)"/>
<path d="M40 470C120 500 220 440 300 470s180 20 220-10v40H40Z" fill="#dfe6df" opacity=".7"/>
<g transform="translate(70,190)">
<circle cx="56" cy="70" r="56" fill="#0d5c5c" opacity=".08"/>
<circle cx="56" cy="70" r="42" fill="#0d5c5c" opacity=".12"/>
<circle cx="56" cy="70" r="28" fill="#0d5c5c"/>
<text x="56" y="76" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="14" fill="#f7f5f2">ring</text>
</g>
<g stroke="#0d5c5c" stroke-width="2" fill="none" opacity=".5">
<path d="M150 215 C 210 170, 260 150, 300 120" stroke-dasharray="2 7"/>
<path d="M150 245 C 220 245, 270 245, 310 245" stroke-dasharray="2 7"/>
<path d="M150 275 C 210 320, 260 340, 300 370" stroke-dasharray="2 7"/>
</g>
<g transform="translate(310,70)">
<rect x="0" y="0" width="210" height="100" rx="18" fill="#fffdf9" stroke="#a8c5b5" stroke-width="2"/>
<g transform="translate(20,24)"><rect x="0" y="0" width="22" height="22" rx="6" fill="#e3eae3"/><path d="M5 11h4v6H5zM11 7h4v10h-4zM17 9h4v8h-4z" fill="#0d5c5c"/></g>
<text x="54" y="34" font-family="Geomanist,sans-serif" font-size="13" font-weight="600" fill="#1c1814">Books it</text>
<text x="54" y="52" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">Checks your calendar and</text>
<text x="54" y="66" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">confirms the slot by SMS</text>
</g>
<g transform="translate(310,196)">
<rect x="0" y="0" width="210" height="100" rx="18" fill="#fffdf9" stroke="#a8c5b5" stroke-width="2"/>
<g transform="translate(20,24)"><path d="M11 2l9 4v6c0 6-9 11-9 11S2 18 2 12V6Z" fill="none" stroke="#c8553d" stroke-width="2"/><path d="M8 12l2.5 2.5L15 9" stroke="#c8553d" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="54" y="34" font-family="Geomanist,sans-serif" font-size="13" font-weight="600" fill="#1c1814">Flags it</text>
<text x="54" y="52" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">Complex or uncertain requests</text>
<text x="54" y="66" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">reach a person, with context</text>
</g>
<g transform="translate(310,322)">
<rect x="0" y="0" width="210" height="100" rx="18" fill="#fffdf9" stroke="#a8c5b5" stroke-width="2"/>
<g transform="translate(20,24)"><circle cx="11" cy="8" r="4.5" fill="none" stroke="#0d5c5c" stroke-width="2"/><path d="M3 26c1-7 4-10 8-10s7 3 8 10" fill="none" stroke="#0d5c5c" stroke-width="2" stroke-linecap="round"/></g>
<text x="54" y="34" font-family="Geomanist,sans-serif" font-size="13" font-weight="600" fill="#1c1814">Escalates it</text>
<text x="54" y="52" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">Urgent concerns follow your</text>
<text x="54" y="66" font-family="Geomanist,sans-serif" font-size="10.5" fill="#65655e">clinic&#8217;s agreed protocol</text>
</g>
<g transform="translate(180,430)">
<rect x="0" y="0" width="220" height="44" rx="22" fill="#0d5c5c"/>
<text x="110" y="27" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="11" fill="#f2ede4">Every call. Every hour. Answered.</text>
</g>
</svg>
<figcaption>Three destinations a call can take: booked, flagged for a person, or escalated by your protocol. General flow, not a guaranteed configuration for every practice.</figcaption>
</figure>'''


PAGES = [
    {
        'slug': 'missed-call-text-ai',
        'title': 'A Missed Call. A Text. An Appointment. | DrKing',
        'description': 'What happens after a patient calls your clinic and nobody picks up — and how a simple text conversation turns that moment into a booked appointment.',
        'eyebrow': 'Clinic stories / 01',
        'h1': 'The call you missed. The conversation you <em>didn&#8217;t.</em>',
        'lede': 'Your front desk is already doing three things at once. The phone rings out. Here&#8217;s what can happen next — and why a short text, sent while the caller is still holding their phone, changes everything.',
        'graphic': sms_graphic(),
        'sections': '''
<section class="article-section" aria-labelledby="s1"><span class="step-tag">01 · The moment</span><h2 id="s1">It starts with a ring that goes unanswered.</h2>
<p>Nobody plans to miss a call. Your receptionist is checking in a patient, or walking someone through a form, or simply taking a breath between tasks. The phone rings twice, three times, and then it stops.</p>
<p>For the caller, that silence is a small, quiet decision point. Do they call back later? Do they try the next practice on the list? Or do they just&#8230; move on? Most won&#8217;t leave a voicemail. The moment passes and your clinic never knows it happened.</p>
<p>That&#8217;s the problem worth solving — not answering every call with more staff, or working your team harder, but catching the moment before it disappears.</p></section>

<section class="article-section soft" aria-labelledby="s2"><span class="step-tag">02 · The text</span><h2 id="s2">A short text, sent while they&#8217;re still holding the phone.</h2>
<p>DrKing detects the missed call and sends a warm SMS to the caller within sixty seconds — before they&#8217;ve had time to ring anyone else. It&#8217;s a simple message that acknowledges the call and offers the next step: <em>&#8220;Sorry we missed your call. Would you like to book an appointment?&#8221;</em></p>
<p>It feels like a person, not a system. Because it should. The caller is still thinking about your clinic — the text meets them exactly there.</p>
<blockquote class="pull-quote"><p>The best time to answer a missed call is while the caller is still looking at their phone.</p></blockquote></section>

<section class="article-section" aria-labelledby="s3"><span class="step-tag">03 · The conversation</span><h2 id="s3">From a quick reply to a confirmed booking.</h2>
<p>When the patient replies, the conversation continues naturally. They ask about times. DrKing checks your practice&#8217;s availability and offers real slots. They pick one. The appointment is confirmed and the details flow into your calendar and CRM — the same records your team already uses.</p>
<p>No phone tag. No &#8220;we&#8217;ll call you back.&#8221; Just a short exchange that ends with a patient who knows when they&#8217;re coming in and a front desk that didn&#8217;t have to chase anything.</p>
<p>And when the enquiry is something the text conversation can&#8217;t resolve — a clinical question, a concern that needs a person — it&#8217;s flagged for your team with the context, so the follow-up starts informed rather than from zero.</p></section>

<section class="article-section soft vendor-section" aria-labelledby="s4"><span class="step-tag">04 · Your systems</span><h2 id="s4">It fits the practice management system you already run.</h2>
VENDORS_HERE
<p class="vendor-footnote">Integration status is labelled honestly. Nothing is called &#8220;live&#8221; until it is. Check the <a href="/integrations">full integrations page</a> for the current roadmap.</p></section>

<section class="article-section" aria-labelledby="s5"><span class="step-tag">05 · The point</span><h2 id="s5">A missed call isn&#8217;t the end of the conversation.</h2>
<p>It used to be. The phone would ring, nobody would answer, and both sides would move on — one to the next practice, the other to the next task, neither aware of what almost happened.</p>
<p>A short text changes the shape of that moment. The caller feels acknowledged. The practice stays in the conversation. And the appointment that might have quietly disappeared gets booked while it still matters.</p>
<p>That&#8217;s the whole idea: not more software in your day, but a small bridge over the gap that already exists between &#8220;we missed you&#8221; and &#8220;see you tomorrow.&#8221;</p></section>''',
        'cta_heading': 'See the text-back flow for your clinic.',
        'cta_text': 'Ask the DrKing team to walk you through a missed-call text conversation using your practice&#8217;s real availability and setup.',
        'product_link': '/missed-call-recovery',
        'product_label': 'Explore Missed Call Recovery',
    },
    {
        'slug': 'missed-call-voice-ai',
        'title': 'Every Call Answered, Even the Ones You Miss | DrKing',
        'description': 'When your front desk can\u2019t pick up, an AI voice receptionist can \u2014 greeting callers, booking appointments and routing what needs a person.',
        'eyebrow': 'Clinic stories / 02',
        'h1': 'The voice that picks up <em>when you can&#8217;t.</em>',
        'lede': 'The phone doesn&#8217;t wait for a quiet moment. It rings during check-in, during a difficult conversation, at 8:42 pm on a Friday. Here&#8217;s what it sounds like when every one of those calls still gets answered.',
        'graphic': voice_graphic(),
        'sections': '''
<section class="article-section" aria-labelledby="v1"><span class="step-tag">01 · The caller</span><h2 id="v1">What your caller hears.</h2>
<p>It sounds like your practice. The AI voice receptionist greets the caller by your clinic&#8217;s name, listens to what they need, and responds in natural, conversational speech — not a menu of buttons, not a robotic loop of &#8220;press one for&#8230;&#8221;</p>
<p>For the caller, the experience is simple: they called a clinic, and a clinic answered. They ask about an appointment. They get offered real times from your calendar. They confirm. An SMS arrives with the details.</p>
<p>It&#8217;s a conversation that ends with &#8220;see you then&#8221; — not a voicemail they hope someone checks.</p></section>

<section class="article-section soft" aria-labelledby="v2"><span class="step-tag">02 · The routes</span><h2 id="v2">Not every call needs the same ending.</h2>
<p>Routine enquiries — booking, availability, practice information — are handled end-to-end. The caller gets what they need and your calendar fills itself.</p>
<p>But a useful assistant knows what it doesn&#8217;t know. When a caller asks something the AI can&#8217;t resolve, the request is flagged for your staff with the full context, so nobody has to repeat themselves when a person follows up.</p>
<p>And urgent concerns follow your clinic&#8217;s own escalation protocol — connecting the caller to an on-call clinician or directing them to emergency services, exactly as your practice has agreed. The AI never diagnoses. It routes.</p>
<blockquote class="pull-quote"><p>A good assistant doesn&#8217;t pretend to know everything. It knows where each conversation should go next.</p></blockquote></section>

<section class="article-section" aria-labelledby="v3"><span class="step-tag">03 · Your team</span><h2 id="v3">What this actually means for your front desk.</h2>
<p>It&#8217;s not about replacing your team. It&#8217;s about what happens to the person standing in front of them. When the phone is answered before the third ring, your receptionist can finish the conversation they&#8217;re having — the one with a human being who took time out of their day to come in.</p>
<p>After hours, weekends, lunch breaks, the busiest hour of the busiest day: the line is open. Not with a recording, but with a conversation that can actually complete the task.</p>
<p>Your team gets the space to do the work only they can do. The phone gets answered anyway.</p></section>

<section class="article-section soft vendor-section" aria-labelledby="v4"><span class="step-tag">04 · Your systems</span><h2 id="v4">It fits the practice management system you already run.</h2>
VENDORS_HERE
<p class="vendor-footnote">Integration status is labelled honestly. Nothing is called &#8220;live&#8221; until it is. Check the <a href="/integrations">full integrations page</a> for the current roadmap.</p></section>

<section class="article-section" aria-labelledby="v5"><span class="step-tag">05 · The hours</span><h2 id="v5">The calls that used to disappear into the evening.</h2>
<p>Monday, 9:15 am — answered. Friday, 8:42 pm — answered. Sunday, 6:30 am — answered. Different hours, same greeting, same ability to finish what the caller started.</p>
<p>For a practice, that&#8217;s not just fewer missed calls. It&#8217;s the difference between a patient who books with you at 9 pm on a Sunday and one who finds someone else by Monday morning.</p>
<p>Every call gets a voice. Every caller gets a next step. That&#8217;s the whole point.</p></section>''',
        'cta_heading': 'Hear it for yourself.',
        'cta_text': 'Ask the DrKing team to demonstrate the AI voice receptionist with your clinic&#8217;s name, availability and escalation preferences.',
        'product_link': '/ai-voice-receptionist',
        'product_label': 'Explore the AI Voice Receptionist',
    },
]

for page in PAGES:
    url = 'https://drking.ai/' + page['slug']
    title, description = page['title'], page['description']
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': 'https://drking.ai/#organization', 'name': 'DrKing', 'url': 'https://drking.ai/'},
        {'@type': 'WebPage', '@id': url + '#webpage', 'name': title, 'description': description,
         'url': url, 'inLanguage': 'en-AU', 'publisher': {'@id': 'https://drking.ai/#organization'}},
        {'@type': 'Article', '@id': url + '#article', 'headline': title.replace(' | DrKing', ''), 'description': description,
         'inLanguage': 'en-AU', 'publisher': {'@id': 'https://drking.ai/#organization'}, 'mainEntityOfPage': {'@id': url + '#webpage'}},
    ]}
    sections = page['sections'].replace('VENDORS_HERE', vendor_grid(VENDORS_NOW, VENDORS_ROADMAP))
    head = (
        '<!doctype html>\n<html lang="en-AU"><head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="index,follow">\n'
        f'<title>{escape(title)}</title>\n'
        f'<meta name="description" content="{escape(description, quote=True)}">\n'
        f'<link rel="canonical" href="{url}">\n'
        f'<meta property="og:type" content="article"><meta property="og:title" content="{escape(title, quote=True)}">'
        f'<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:url" content="{url}">\n'
        '<link rel="stylesheet" href="/assets/site-shell.css?v=4">\n'
        '<link rel="stylesheet" href="/assets/blog-articles.css">\n'
        '<script src="/assets/site-shell.js" defer></script>\n'
        f'<script type="application/ld+json" id="structured-data">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        '</head><body>\n'
    )
    hero = (
        '<main id="main" class="blog-article"><div class="article-wrap">'
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span>'
        f'<a href="/solutions">Solutions</a><span aria-hidden="true">/</span><span>{escape(page["eyebrow"].split("/")[0].strip())}</span></nav></div>'
        f'<section class="article-hero" aria-labelledby="article-title"><div class="article-wrap hero-grid">'
        f'<div><p class="article-eyebrow">{escape(page["eyebrow"])}</p><h1 id="article-title">{page["h1"]}</h1>'
        f'<p class="article-lede">{page["lede"]}</p></div>'
        f'<div class="hero-art">{page["graphic"]}</div>'
        '</div></section><div class="article-wrap article-main">'
    )
    cta = (
        '<section class="article-cta" aria-labelledby="article-cta-title">'
        f'<div><span class="step-tag">Next step</span><h2 id="article-cta-title">{page["cta_heading"]}</h2>'
        f'<p>{page["cta_text"]}</p></div>'
        f'<div class="cta-links"><a class="article-button" href="/demo">Book a free demo <span aria-hidden="true">&#8599;</span></a>'
        f'<a class="article-secondary" href="{page["product_link"]}">{page["product_label"]} <span aria-hidden="true">&#8594;</span></a></div>'
        '</section></div></main>'
    )
    (root / (page['slug'] + '.html')).write_text(head + shell + hero + sections + cta + site_footer + '\n</body></html>\n')
    print('built', page['slug'] + '.html')