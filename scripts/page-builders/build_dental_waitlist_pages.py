#!/usr/bin/env python3
"""Fork core-practice-integration.html into EXACT / Praktika / CareStack waitlist pages.
Text-only changes via asserted str.replace."""
import json, re, sys, pathlib

REPO = pathlib.Path('/app/data/workspaces/drking-two-guides-20261030')
SRC = (REPO / 'core-practice-integration.html').read_text()
T = ' style="color:var(--teal)"'  # same inline link style the fork uses in its CTA


def rep(s, old, new, count=1, log=None):
    n = s.count(old)
    if n != count:
        sys.exit(f'FAIL: expected {count} of {old[:90]!r}, found {n}')
    if log is not None:
        log.append(n)
    return s.replace(old, new)


def feat(i, h, p, link=''):
    return (f'<article class="feature reveal"><span class="feature-index">0{i}</span><div><h3>{h}</h3>'
            f'<p>{p}</p>{link}</div></article>')


def faq_html(faqs):
    out = []
    for k, (q, a) in enumerate(faqs):
        out.append(f'<details{" open" if k == 0 else ""}><summary>{q}</summary><p>{a}</p></details>')
    return ''.join(out)


def stats_html(stats):
    return ''.join(f'<div class="stat"><div class="stat-value">{v}</div><div class="stat-label">{l}</div></div>'
                   for v, l in stats)


# ---- fork-source fragments that get replaced (asserted) ----
OLD_FEATURES = SRC[SRC.index('<div class="feature-list">') + len('<div class="feature-list">'):SRC.index('</div></section>\n<section id="clinics"')]
OLD_FAQ = SRC[SRC.index('<div class="faqs reveal">') + len('<div class="faqs reveal">'):SRC.index('</div></section>\n<section id="book-demo"')]
OLD_STATS = SRC[SRC.index('<div class="wrap stats">') + len('<div class="wrap stats">'):SRC.index('</div></section>\n<section id="how-it-works"')]
OLD_LD = re.search(r'<script type="application/ld\+json" id="structured-data">(.*?)</script>', SRC, re.S).group(1)
OLD_TITLE = 'DrKing + Core Practice | AI Receptionist for Dental'
OLD_DESC = 'A DrKing + Core Practice integration is planned. Every DrKing tool works alongside it today. Register interest to move it up the roadmap.'

V = {}

V['exact'] = dict(
    name='EXACT', slug='exact-integration',
    title='EXACT Dental Software + AI Receptionist | DrKing',
    desc='Use DrKing alongside EXACT dental software today: AI receptionist, web chat, booking requests, SMS reminders and recall. No integration yet; waitlist open.',
    eyebrow='EXACT dental software + AI receptionist',
    h1='EXACT +<br><em>AI receptionist.</em>',
    hero_p=f'Run EXACT dental software? Add DrKing’s <a href="/ai-voice-receptionist"{T}>AI receptionist</a>, web chat, online booking requests and SMS reminders alongside it today. There’s no EXACT integration yet, so your team keeps booking in EXACT — and the waitlist is open.',
    aria='Example: a new patient asks about a check-up after hours. DrKing collects the details and sends a booking request for the team to confirm in EXACT.',
    f1=('New patient enquiry', 'Web chat · after hours'), f2=('Booking request in', 'Team confirms in EXACT'),
    clock='7:42', chat_time='Today 7:40 pm', practice='Harbourside Dental',
    chat=['Hi Priya! Thanks for contacting Harbourside Dental. Are you a new patient looking for a check-up?',
          'Yes, I’ve just moved here. Anything next week?',
          'Welcome! I can request Tuesday 9:30 am with Dr Okafor. Shall I send that to our team?',
          'Yes please, thank you!'],
    stats=[('1<span> inbox</span>', 'Calls, chat, SMS, email and social together'),
           ('AI<span> voice</span>', 'Answers new-patient calls when you’re busy'),
           ('24<span>/7</span>', 'Web chat and online booking requests'),
           ('SMS<span> recall</span>', 'Reminders and hygiene recall messages')],
    how=('New-patient enquiries, handled', 'Three steps. Your team stays in EXACT.',
         'DrKing handles the first conversation. Your team books the patient in EXACT.'),
    steps=[('Enquiry comes in.', 'A new patient calls, chats on your website or sends a message. DrKing’s AI receptionist answers.', 'Phone, chat, SMS or social'),
           ('Details collected.', 'DrKing asks what they need — a check-up, a clean or a specific concern — and when suits them.', 'Saved to one inbox'),
           ('Team confirms.', 'Your team sees the request in DrKing and books the patient in EXACT.', 'No EXACT integration yet')],
    feat_head=('DrKing alongside EXACT', 'New patients in.<br>Lapsed patients back.',
               'Standalone DrKing tools your EXACT practice can switch on today.',
               '/ai-voice-receptionist', 'Explore the AI voice receptionist'),
    features=[('AI Voice Receptionist', 'Answers calls when the front desk is busy, takes new-patient details and passes them to your team.', ''),
              ('AI Web Chat', 'Replies to website visitors day and night and turns their questions into booking requests.', ''),
              ('Online Booking Requests', 'Patients choose a preferred time online. Your team confirms it in EXACT.', ''),
              ('SMS Reminders', 'Appointment reminders by SMS help patients keep the time they booked.', ''),
              ('Reactivation Campaigns', 'Monthly reactivation messages invite lapsed patients back for their next check-up.', '<a class="text-link" href="/patient-reactivation">Explore patient reactivation <span aria-hidden="true">↗</span></a>'),
              ('Treatment-Plan Follow-up', 'Reminds patients who accepted a treatment plan but haven’t booked it yet.', '')],
    ctx=('No EXACT integration yet · Waitlist open', 'For EXACT dental practices', 'EXACT practices.<br>Easier to reach.',
         f'EXACT is the dental practice management software from Software of Excellence. DrKing doesn’t connect to it yet, so it doesn’t read or change your EXACT appointment book or patient records. DrKing handles calls, chats and follow-up, then hands each request to your team. <a href="/integrations"{T}>Join the EXACT waitlist</a> for a direct integration.'),
    ctx_p='Today, DrKing’s standalone tools work alongside EXACT.',
    faq_eyebrow='Good questions about EXACT + DrKing',
    faqs=[('Does DrKing integrate with EXACT?', 'Not yet. There is no DrKing integration with EXACT today, and DrKing doesn’t read or write your EXACT appointment book or patient records. The EXACT waitlist is open on our integrations page.'),
          ('Can we use DrKing alongside EXACT now?', 'Yes. The AI receptionist, web chat, online booking requests, SMS reminders, reactivation campaigns and treatment-plan follow-up run as standalone DrKing tools. Your team keeps confirming appointments in EXACT.'),
          ('How are new-patient enquiries handled?', 'DrKing answers the call or chat, collects the enquiry details and adds them to one inbox, so your team can follow up and book the new patient in EXACT.'),
          ('What happens with a toothache or emergency call?', 'DrKing flags urgent requests for your team with the details collected so far. It doesn’t give clinical advice, and anyone with a medical emergency is told to call 000.'),
          ('How do we join the EXACT waitlist?', 'Choose EXACT on the waitlist form on our integrations page. Registered interest helps us decide which integrations to build next.')],
    cta=('Ready when you are', 'Keep EXACT.<br>Add an <em>AI receptionist.</em>',
         'See how DrKing works alongside EXACT for new-patient enquiries, recalls and follow-up.',
         '/unscheduled-treatment-follow-up', 'Read: following up treatment that never got booked →',
         'No EXACT integration yet. Waitlist open.'),
    app=('DrKing for EXACT dental practices', 'AI receptionist, web chat, online booking requests, SMS reminders, reactivation campaigns and treatment-plan follow-up that work alongside EXACT. No EXACT integration yet; waitlist open.',
         ['AI Voice Receptionist', 'AI Web Chat', 'Online Booking Requests', 'SMS Reminders', 'Reactivation Campaigns', 'Treatment-Plan Follow-up']),
)

V['praktika'] = dict(
    name='Praktika', slug='praktika-integration',
    title='Praktika Dental Software + AI Receptionist | DrKing',
    desc='Use DrKing alongside Praktika today: AI receptionist, missed-call text-back and urgent toothache calls routed to your team. No integration yet; waitlist open.',
    eyebrow='Praktika dental software + AI receptionist',
    h1='Praktika +<br><em>AI receptionist.</em>',
    hero_p=f'Use Praktika dental software? DrKing’s <a href="/ai-voice-receptionist"{T}>AI receptionist</a> answers calls, texts back missed callers and flags toothache calls for your team — alongside Praktika today. There’s no Praktika integration yet, and the waitlist is open.',
    aria='Example: a patient with a toothache misses the practice by phone. DrKing texts back and flags the request as urgent for the team to call back.',
    f1=('Missed call', 'Toothache · 7:48 am'), f2=('Flagged for the team', 'Urgent call-back'),
    clock='7:52', chat_time='Today 7:49 am', practice='Northgate Dental',
    chat=['Hi Tom, sorry we missed your call to Northgate Dental. How can we help?',
          'I’ve got a bad toothache. Can someone see me today?',
          'Sorry you’re in pain. I’ve flagged this as urgent and our team will call you back. For a medical emergency, call 000.',
          'Thanks, I’ll keep my phone handy.'],
    stats=[('1<span> inbox</span>', 'Urgent requests with the details attached'),
           ('Text<span>-back</span>', 'SMS straight after a missed call'),
           ('AI<span> voice</span>', 'Answers when the front desk is chair-side'),
           ('12<span> months</span>', 'SMS and email campaign calendar')],
    how=('Toothache calls, routed to people', 'Three steps. Urgent calls reach your team.',
         'DrKing collects the details. Your clinicians decide what happens next.'),
    steps=[('Call comes in.', 'A patient calls about a toothache while your team is chair-side. DrKing answers or texts back.', 'Phone or missed call'),
           ('Details captured.', 'DrKing records the concern, contact details and preferred times. It gives no clinical advice.', 'Flagged as urgent'),
           ('Team calls back.', 'Your team sees the request in one inbox, triages it and books the visit in Praktika.', 'No Praktika integration yet')],
    feat_head=('DrKing alongside Praktika', 'Urgent calls flagged.<br>Routine ones booked.',
               'Standalone DrKing tools your Praktika practice can use today.',
               '/ai-voice-receptionist', 'Explore the AI voice receptionist'),
    features=[('Missed-Call Text-Back', 'A friendly SMS goes out after a missed call, so the patient can explain what they need.', ''),
              ('AI Voice Receptionist', 'Answers calls, collects details and flags urgent dental problems for your team to call back.', ''),
              ('One Inbox', 'Calls, web chat, SMS, email, WhatsApp, Facebook and Instagram messages in one place.', ''),
              ('Online Booking Requests', 'Routine check-ups and cleans can be requested online, then confirmed in Praktika.', ''),
              ('Treatment-Plan Follow-up', 'Follows up patients who accepted a treatment plan but haven’t booked or returned.', '<a class="text-link" href="/unscheduled-treatment-follow-up">Explore treatment follow-up <span aria-hidden="true">↗</span></a>'),
              ('SMS Reminders', 'Appointment reminders help patients keep the time they booked — less chasing for your team.', '')],
    ctx=('No Praktika integration yet · Waitlist open', 'For Praktika dental practices', 'Praktika practices.<br>Easier to reach.',
         f'Praktika is Australian cloud-based dental software. DrKing doesn’t connect to it yet, so it doesn’t read or change your Praktika appointment book or patient records. Its standalone tools handle calls, texts and follow-up alongside it. <a href="/integrations"{T}>Join the Praktika waitlist</a> for a direct integration.'),
    ctx_p='Today, DrKing’s standalone tools work alongside Praktika.',
    faq_eyebrow='Good questions about Praktika + DrKing',
    faqs=[('Does DrKing integrate with Praktika?', 'Not yet. There is no DrKing integration with Praktika today, and DrKing doesn’t read or write your Praktika appointment book or patient records. The Praktika waitlist is open on our integrations page.'),
          ('How are toothache and emergency calls handled?', 'DrKing collects the caller’s details and concern, then flags the request as urgent for your team to call back. It doesn’t give clinical advice, and anyone with a medical emergency is told to call 000.'),
          ('What happens when we miss a call?', 'DrKing sends a text-back after a missed call so the patient can reply with what they need. The conversation lands in one inbox for your team.'),
          ('Can patients book online?', 'Yes. Patients can request a time through DrKing online booking. Your team then confirms the appointment in Praktika.'),
          ('How do we join the Praktika waitlist?', 'Choose Praktika on the waitlist form on our integrations page. Registered interest helps us decide which integrations to build next.')],
    cta=('Ready when you are', 'Keep Praktika.<br>Add an <em>AI receptionist.</em>',
         'See how DrKing works alongside Praktika for missed calls, urgent requests and follow-up.',
         '/patient-reactivation', 'Read: bringing lapsed patients back with monthly reactivation →',
         'No Praktika integration yet. Waitlist open.'),
    app=('DrKing for Praktika dental practices', 'AI receptionist, missed-call text-back, one inbox, online booking requests, SMS reminders and treatment-plan follow-up that work alongside Praktika. No Praktika integration yet; waitlist open.',
         ['AI Voice Receptionist', 'Missed-Call Text-Back', 'One Inbox', 'Online Booking Requests', 'SMS Reminders', 'Treatment-Plan Follow-up']),
)

V['carestack'] = dict(
    name='CareStack', slug='carestack-integration',
    title='CareStack Dental Software + AI Receptionist | DrKing',
    desc='Use DrKing alongside CareStack today: hygiene recall, reactivation campaigns, treatment follow-up and an AI receptionist. No integration yet; waitlist open.',
    eyebrow='CareStack dental software + AI receptionist',
    h1='CareStack +<br><em>AI receptionist.</em>',
    hero_p=f'On CareStack dental software? Add DrKing’s <a href="/ai-voice-receptionist"{T}>AI receptionist</a>, hygiene recall messages, reactivation campaigns and treatment-plan follow-up alongside it today. There’s no CareStack integration yet; your team books in CareStack and the waitlist is open.',
    aria='Example: a hygiene recall message invites a patient back. She replies by SMS and DrKing sends a booking request for the team to confirm in CareStack.',
    f1=('Hygiene recall', 'Reactivation campaign'), f2=('Request received', 'Team confirms in CareStack'),
    clock='11:06', chat_time='Today 11:00 am', practice='Bayview Dental',
    chat=['Hi Mia, it’s Bayview Dental. You’re due for your hygiene visit. Would you like to book a time?',
          'Yes please. Do you have a Saturday morning?',
          'Great! I’ve sent a Saturday morning request to our team, who will confirm your time by SMS.',
          'Perfect, thanks!'],
    stats=[('1<span> inbox</span>', 'Replies from recalls and campaigns together'),
           ('Monthly', 'Reactivation for lapsed patients'),
           ('SMS<span> recall</span>', 'Hygiene recall and reminder messages'),
           ('Follow<span>-up</span>', 'For accepted but unbooked treatment')],
    how=('Recall and treatment follow-up', 'Three steps. Lapsed patients come back.',
         'DrKing sends the messages and handles replies. Your team books in CareStack.'),
    steps=[('Message sent.', 'A monthly reactivation or hygiene recall campaign invites patients who are due back.', 'SMS or email'),
           ('Patient replies.', 'DrKing answers questions and collects a preferred time by two-way SMS.', 'Saved to one inbox'),
           ('Team books.', 'Your team sees the reply in DrKing and books the visit in CareStack.', 'No CareStack integration yet')],
    feat_head=('DrKing alongside CareStack', 'Recalls sent.<br>Treatment followed up.',
               'Standalone DrKing tools your CareStack practice can use today.',
               '/patient-reactivation', 'Explore patient reactivation'),
    features=[('Reactivation Campaigns', 'Monthly messages invite patients who haven’t been in for a while back for a visit.', ''),
              ('Hygiene Recall Messages', 'SMS and email campaigns, planned on a 12-month calendar, remind patients when they’re due.', ''),
              ('SMS Reminders', 'Appointment reminders help patients keep the time they booked.', ''),
              ('AI Voice Receptionist', 'Answers calls when your team is busy and passes booking requests to them.', ''),
              ('Treatment-Plan Follow-up', 'Follows up patients who accepted a treatment plan but didn’t book or return.', '<a class="text-link" href="/unscheduled-treatment-follow-up">Explore treatment follow-up <span aria-hidden="true">↗</span></a>'),
              ('One Inbox', 'Replies from SMS, email, web chat, calls and social media land in one place for your team.', '')],
    ctx=('No CareStack integration yet · Waitlist open', 'For CareStack dental practices', 'CareStack practices.<br>Easier to reach.',
         f'CareStack is cloud-based dental practice management software. DrKing doesn’t connect to it yet, so it doesn’t read or change your CareStack schedule or patient records. Its standalone campaigns and follow-up run alongside it, and your team books in CareStack. <a href="/integrations"{T}>Join the CareStack waitlist</a> for a direct integration.'),
    ctx_p='Today, DrKing’s standalone tools work alongside CareStack.',
    faq_eyebrow='Good questions about CareStack + DrKing',
    faqs=[('Does DrKing integrate with CareStack?', 'Not yet. There is no DrKing integration with CareStack today, and DrKing doesn’t read or write your CareStack schedule or patient records. The CareStack waitlist is open on our integrations page.'),
          ('How does hygiene recall work without an integration?', 'Your team chooses who to contact, and DrKing sends the recall or reactivation messages by SMS or email. Replies land in one inbox and your team books the visit in CareStack.'),
          ('Can DrKing follow up unbooked treatment?', 'Yes. DrKing can follow up patients who accepted a treatment plan but didn’t book or return, and pass their replies to your team.'),
          ('What about urgent or clinical questions?', 'Urgent and clinical questions are flagged for your team with the conversation attached. DrKing doesn’t give clinical advice, and anyone with a medical emergency is told to call 000.'),
          ('How do we join the CareStack waitlist?', 'Choose CareStack on the waitlist form on our integrations page. Registered interest helps us decide which integrations to build next.')],
    cta=('Ready when you are', 'Keep CareStack.<br>Add an <em>AI receptionist.</em>',
         'See how DrKing works alongside CareStack for recalls, reactivation and treatment follow-up.',
         '/online-booking', 'See how DrKing online booking requests work →',
         'No CareStack integration yet. Waitlist open.'),
    app=('DrKing for CareStack dental practices', 'Reactivation campaigns, hygiene recall messages, SMS reminders, an AI receptionist, treatment-plan follow-up and one inbox that work alongside CareStack. No CareStack integration yet; waitlist open.',
         ['Reactivation Campaigns', 'Hygiene Recall Messages', 'SMS Reminders', 'AI Voice Receptionist', 'Treatment-Plan Follow-up', 'One Inbox']),
)


def build(v):
    s, log = SRC, []
    n = v['name']
    url = f'https://drking.ai/{v["slug"]}'
    assert len(v['title']) <= 60, (v['title'], len(v['title']))
    assert 70 <= len(v['desc']) <= 160, (len(v['desc']))
    # JSON-LD (rebuilt from the fork's graph, same compact serialisation)
    g = json.loads(OLD_LD)
    for node in g['@graph']:
        t = node['@type']
        if t == 'WebPage':
            node.update({'@id': url + '#webpage', 'url': url, 'name': v['title'], 'description': v['desc']})
        elif t == 'SoftwareApplication':
            node.update({'name': v['app'][0], 'url': url, 'description': v['app'][1], 'featureList': v['app'][2]})
        elif t == 'BreadcrumbList':
            node['itemListElement'][1].update({'name': 'Integrations', 'item': 'https://drking.ai/integrations'})
            node['itemListElement'][2].update({'name': n, 'item': url})
        elif t == 'FAQPage':
            node['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in v['faqs']]
    s = rep(s, OLD_LD, json.dumps(g, ensure_ascii=False, separators=(',', ':')), 1, log)
    # head
    s = rep(s, f'<title>{OLD_TITLE}</title>', f'<title>{v["title"]}</title>', 1, log)
    s = rep(s, OLD_DESC, v['desc'], 2, log)
    s = rep(s, 'https://drking.ai/core-practice-integration"', url + '"', 2, log)
    s = rep(s, 'content="Core Practice. On the roadmap. | DrKing"', f'content="{v["title"]}"', 1, log)
    # breadcrumb
    s = rep(s, '<span>Solutions</span><span aria-hidden="true">/</span><span aria-current="page">Missed call recovery</span>',
            f'<span>Integrations</span><span aria-hidden="true">/</span><span aria-current="page">{n}</span>', 1, log)
    # hero
    s = rep(s, '<div class="eyebrow">DrKing + Core Practice integration</div>', f'<div class="eyebrow">{v["eyebrow"]}</div>', 1, log)
    s = rep(s, 'Core Practice.<br>On the <em>roadmap.</em>', v['h1'], 1, log)
    s = rep(s, 'If your dental practice runs Core Practice, the direct integration is on the roadmap — with scope and timing being confirmed. In the meantime, every DrKing tool works alongside it today, and registering your interest helps us set its priority.', v['hero_p'], 1, log)
    s = rep(s, 'Planned for Core Practice. Toolkit available today.', f'No {n} integration yet. Waitlist open.', 1, log)
    s = rep(s, 'Example: a missed call at 10:42 receives an instant text-back. The patient replies and their appointment is booked.', v['aria'], 1, log)
    s = rep(s, '<strong>Missed call</strong><small>New patient · just now</small>', f'<strong>{v["f1"][0]}</strong><small>{v["f1"][1]}</small>', 1, log)
    s = rep(s, '<span>10:42</span>', f'<span>{v["clock"]}</span>', 1, log)
    s = rep(s, 'Riverbend Dental<small>Core Practice · powered by DrKing</small>', f'{v["practice"]}<small>AI receptionist · powered by DrKing</small>', 1, log)
    s = rep(s, '<div class="chat-time">Today 9:15 am</div>', f'<div class="chat-time">{v["chat_time"]}</div>', 1, log)
    c = v['chat']
    s = rep(s, '<div class="bubble">Hi Kate! Sorry we missed your call to Riverbend Dental. Would you like to book an appointment?</div>', f'<div class="bubble">{c[0]}</div>', 1, log)
    s = rep(s, '<div class="bubble reply">Yes please! Is there anything this week?</div>', f'<div class="bubble reply">{c[1]}</div>', 1, log)
    s = rep(s, '<div class="bubble">Of course. We have Thursday 2:00 pm with Dr Lee. Shall I book you in?</div>', f'<div class="bubble">{c[2]}</div>', 1, log)
    s = rep(s, '<div class="bubble reply">That would be great, thanks!</div>', f'<div class="bubble reply">{c[3]}</div>', 1, log)
    s = rep(s, 'Toolkit today.<br>Integration soon.', 'Toolkit today.<br>Waitlist open.', 1, log)
    s = rep(s, '<strong>Appointment booked</strong><small>Thursday, 2:00 pm · Dr Lee</small>', f'<strong>{v["f2"][0]}</strong><small>{v["f2"][1]}</small>', 1, log)
    s = rep(s, 'Illustrative conversation. Not a screenshot of Core Practice.', f'Illustrative conversation. Not a screenshot of {n}.', 1, log)
    # stats
    s = rep(s, 'aria-label="Missed call recovery at a glance"', f'aria-label="DrKing alongside {n} at a glance"', 1, log)
    s = rep(s, OLD_STATS, stats_html(v['stats']), 1, log)
    # how it works
    h = v['how']
    s = rep(s, "<div class=\"eyebrow\">A missed call isn't the end of the conversation</div><h2>Three steps. No extra work for your front desk.</h2><p>Three simple steps. No extra work for your front desk.</p>",
            f'<div class="eyebrow">{h[0]}</div><h2>{h[1]}</h2><p>{h[2]}</p>', 1, log)
    old_steps = [('Call missed.', 'Your team is chair-side with patients. DrKing detects the missed call instantly.', 'The moment the call ends'),
                 ('Instant text sent.', 'A personalised text acknowledges the call and offers to help book an appointment.', 'Straight away'),
                 ('Booking request in.', 'The patient replies with a time. Your team gets the details to confirm it in Core Practice.', 'Direct integration planned')]
    for (oh, op, ol), (nh, np, nl) in zip(old_steps, v['steps']):
        s = rep(s, f'<h3>{oh}</h3><p>{op}</p><span class="small-label">{ol}</span>', f'<h3>{nh}</h3><p>{np}</p><span class="small-label">{nl}</span>', 1, log)
    # features
    fh = v['feat_head']
    s = rep(s, "<div class=\"eyebrow\">Everything your front desk needs.</div><h2>The conversations that<br>fill your chairs.</h2><p>Give every patient a way forward, even when you can't get to the phone.</p><a class=\"text-link feature-link\" href=\"/missed-calls\">Explore missed call solutions <span aria-hidden=\"true\">↗</span></a>",
            f'<div class="eyebrow">{fh[0]}</div><h2>{fh[1]}</h2><p>{fh[2]}</p><a class="text-link feature-link" href="{fh[3]}">{fh[4]} <span aria-hidden="true">↗</span></a>', 1, log)
    s = rep(s, OLD_FEATURES, ''.join(feat(i + 1, *f) for i, f in enumerate(v['features'])), 1, log)
    # context / honest status card
    cx = v['ctx']
    s = rep(s, '<div class="context-number">24/7</div><p>coverage. Every DrKing tool works alongside Core Practice today.</p><span class="source">Direct Core Practice integration is planned</span>',
            f'<div class="context-number">Today</div><p>{v["ctx_p"]}</p><span class="source">{cx[0]}</span>', 1, log)
    s = rep(s, '<div class="eyebrow">Made for dental practices</div><h2>Core Practice.<br>Easier to reach.</h2>', f'<div class="eyebrow">{cx[1]}</div><h2>{cx[2]}</h2>', 1, log)
    s = rep(s, "<p>When someone calls your clinic, they're ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going — and gives patients one less reason to call somewhere else.</p>", f'<p>{cx[3]}</p>', 1, log)
    s = rep(s, '<a href="/general-practice">For general practice <span aria-hidden="true">↗</span></a></div></div></section>',
            '<a href="/integrations">Integration status <span aria-hidden="true">↗</span></a></div></div></section>', 1, log)
    # FAQ
    s = rep(s, '<div class="eyebrow">Good questions about Core Practice + DrKing</div>', f'<div class="eyebrow">{v["faq_eyebrow"]}</div>', 1, log)
    s = rep(s, OLD_FAQ, faq_html(v['faqs']), 1, log)
    # CTA
    ct = v['cta']
    s = rep(s, "<div class=\"eyebrow\">Your next patient is calling</div><h2>Don't let a missed call<br>be a <em>missed connection.</em></h2><p>See how DrKing helps fill your Core Practice calendar — even when your team is busy.</p>",
            f'<div class="eyebrow">{ct[0]}</div><h2>{ct[1]}</h2><p>{ct[2]}</p>', 1, log)
    s = rep(s, '<a href="/missed-call-text-ai" style="color:var(--teal)">Read the story: the call you missed, the conversation you didn&#8217;t &#8594;</a>',
            f'<a href="{ct[3]}" style="color:var(--teal)">{ct[4]}</a>', 1, log)
    s = rep(s, '<div class="micro">Works alongside Core Practice today.</div>', f'<div class="micro">{ct[5]}</div>', 1, log)
    # leftovers: only the shared footer link may mention Core Practice
    body = s.replace('<a href="/core-practice-integration">Core Practice (planned)</a>', '')
    for bad in ('Core Practice', 'Riverbend', 'Kate', 'Dr Lee', 'Sam', 'Planned', 'roadmap', 'Spam', 'spam'):
        if bad in body:
            sys.exit(f'FAIL {v["slug"]}: leftover {bad!r} at {body[body.index(bad)-80:body.index(bad)+40]!r}')
    assert s.lower().startswith('<!doctype html>')
    (REPO / f'{v["slug"]}.html').write_text(s)
    print(f'{v["slug"]}.html: {len(log)} replacements OK; title {len(v["title"])}c, desc {len(v["desc"])}c')


for key in ('exact', 'praktika', 'carestack'):
    build(V[key])
