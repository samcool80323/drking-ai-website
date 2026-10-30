"""Build vendor integration pages for DrKing.

Generates one page per PMS vendor with practice-specific problems,
workflows, use cases and an honest integration status.
Reuses the blog-article design system. Only writes the named HTML routes.
"""
from pathlib import Path
from html import escape
import json

from cliniko_visuals import cliniko_hero, cliniko_usecase

root = Path(__file__).resolve().parents[1]
source = (root / 'ai-voice-receptionist.html').read_text()
body_open = source.index('<body>')
main_open = source.index('<main id="main">', body_open)
footer_open = source.index('<footer class="site-footer">', main_open)
footer_end = source.index('</footer>', footer_open) + len('</footer>')
shell = source[body_open + len('<body>'):main_open]
site_footer = source[footer_open:footer_end]


def integration_graphic(vendor_initial, vendor_name, accent, is_dental):
    tooth = '''
<path d="M20 8c-2-4-7-6-11-4s-6 7-4 12c1 4 3 7 4 12 0 2 1 4 3 4s3-2 3-4c0-3 1-6 3-6s3 3 3 6c0 2 1 4 3 4s3-2 3-4c1-5 3-8 4-12 2-5 0-10-4-12s-9 0-11 4z" fill="none" stroke="CURRENT" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''' if is_dental else '''
<circle cx="24" cy="24" r="14" fill="none" stroke="CURRENT" stroke-width="2"/>
<path d="M17 24h14M24 17v14" stroke="CURRENT" stroke-width="2" stroke-linecap="round"/>'''
    return f'''<figure class="article-figure hero-figure" role="img" aria-label="Illustration showing how DrKing connects a patient's phone call to {escape(vendor_name)}: the caller on the left, DrKing AI in the centre handling the conversation, and the {escape(vendor_name)} calendar on the right receiving the booking.">
<svg viewBox="0 0 560 440" xmlns="http://www.w3.org/2000/svg" role="img">
<defs><linearGradient id="bgv" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9eade"/><stop offset="1" stop-color="#f7f5f2"/></linearGradient></defs>
<rect width="560" height="440" rx="28" fill="url(#bgv)"/>
<path d="M30 400C110 430 220 380 300 410s180 15 230-15v30H30Z" fill="#dfe6df" opacity=".7"/>
<g transform="translate(36,120)">
<rect x="0" y="0" width="120" height="200" rx="24" fill="#fffdf9" stroke="#d8d5cd" stroke-width="2"/>
<rect x="0" y="0" width="120" height="48" rx="24" fill="#0d5c5c"/><rect x="0" y="24" width="120" height="24" fill="#0d5c5c"/>
<circle cx="60" cy="24" r="12" fill="none" stroke="#f7f5f2" stroke-width="1.5"/>
<path d="M56 20l8 8m0-8l-8 8" stroke="#c8553d" stroke-width="2" stroke-linecap="round"/>
<text x="60" y="44" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#f2ede4">Patient calls</text>
<g transform="translate(20,80)"><circle cx="20" cy="20" r="20" fill="{accent}" opacity=".12"/><circle cx="20" cy="20" r="14" fill="{accent}" opacity=".2"/><circle cx="20" cy="20" r="8" fill="{accent}"/></g>
<text x="60" y="140" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10" fill="#65655e">Your patient,</text>
<text x="60" y="154" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10" fill="#65655e">ready to book</text>
</g>
<g transform="translate(220,80)">
<rect x="0" y="0" width="140" height="280" rx="24" fill="#0d5c5c"/>
<text x="70" y="40" text-anchor="middle" font-family="Newsreader,serif" font-size="16" fill="#f2ede4">DrKing AI</text>
<g transform="translate(35,60)">
<rect x="0" y="0" width="70" height="30" rx="15" fill="#104c4c"/>
<text x="35" y="20" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#aed5c9">answers</text>
</g>
<g transform="translate(35,100)">
<rect x="0" y="0" width="70" height="30" rx="15" fill="#104c4c"/>
<text x="35" y="20" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#aed5c9">books</text>
</g>
<g transform="translate(35,140)">
<rect x="0" y="0" width="70" height="30" rx="15" fill="#104c4c"/>
<text x="35" y="20" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#aed5c9">confirms</text>
</g>
<g transform="translate(35,190)">
<rect x="0" y="0" width="70" height="56" rx="14" fill="#f3f5ef"/>
<text x="35" y="22" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" font-weight="600" fill="#0d4848">SMS sent</text>
<text x="35" y="38" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="8" fill="#344d45">Booking details</text>
</g>
</g>
<g transform="translate(404,120)">
<rect x="0" y="0" width="120" height="200" rx="24" fill="#fffdf9" stroke="{accent}" stroke-width="2.5"/>
<g transform="translate(36,36)">{tooth.replace('CURRENT',accent)}</g>
<text x="60" y="110" text-anchor="middle" font-family="Newsreader,serif" font-size="18" fill="#1c1814">{escape(vendor_initial)}</text>
<text x="60" y="128" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#65655e">{escape(vendor_name)}</text>
<g transform="translate(30,150)">
<rect x="0" y="0" width="60" height="28" rx="6" fill="#e3eae3"/>
<text x="30" y="18" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="8" font-weight="600" fill="#17483e">calendar</text>
</g>
</g>
<g stroke="#0d5c5c" stroke-width="2" fill="none" opacity=".4">
<path d="M160 200 C 185 180, 200 170, 218 165" stroke-dasharray="3 6"/>
</g>
<g stroke="{accent}" stroke-width="2" fill="none" opacity=".5">
<path d="M362 200 C 380 180, 392 170, 404 165" stroke-dasharray="3 6"/>
</g>
</svg>
<figcaption>How the pieces connect: your patient calls, DrKing handles the conversation, and the booking arrives in {escape(vendor_name)}. General illustration, not a screenshot of the actual integration.</figcaption>
</figure>'''


def use_case_cards(cases):
    return ''.join(
        f'<article class="use-case"><span class="uc-number">{i+1:02d}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></article>'
        for i,(t,d) in enumerate(cases)
    )


def workflow_steps(steps):
    return ''.join(
        f'<div class="wf-step"><span class="wf-num">{i+1:02d}</span><h3>{escape(t)}</h3><p>{escape(d)}</p></div>'
        for i,(t,d) in enumerate(steps)
    )


PAGES = [
    {
        'slug': 'dentally-integration',
        'vendor': 'Dentally', 'initial': 'D', 'accent': '#0d5c5c', 'dental': True,
        'title': 'DrKing + Dentally Integration | DrKing',
        'description': 'Connect DrKing to Dentally. Missed-call text-back, voice AI and 24/7 booking flow straight into your Dentally calendar.',
        'h1': 'DrKing meets <em>Dentally.</em>',
        'lede': 'Your Dentally calendar is already the heartbeat of the practice. DrKing keeps that heartbeat steady — answering the calls you miss, texting the patients who slip through, and booking straight into Dentally.',
        'status_label': 'Available now',
        'status_note': 'DrKing connects with Dentally today. Talk to our team about the setup that suits your workflow.',
        'problems': [
            ('Chair-side hours are your busiest phone hours',
             'Your team is turning over rooms, managing treatment plans and checking in patients. The phone rings in the middle of all that, and nobody can reach it. Most callers won\u2019t leave a voicemail — they call the next practice on the list.'),
            ('Recall gaps quietly empty the calendar',
             'Patients who finished a treatment plan six months ago aren\u2019t thinking about their next check-up. Without a consistent recall touch, those chairs stay empty and the gap only grows.'),
            ('After-hours enquiries go nowhere',
             'A toothache doesn\u2019t wait for opening hours. A patient who calls at 7 pm and reaches voicemail has often booked somewhere else by morning.'),
        ],
        'workflows': [
            ('Call missed, text sent', 'DrKing detects the missed call and sends a warm SMS within 60 seconds — while the patient is still holding their phone. The text offers to book an appointment.'),
            ('AI books into Dentally', 'When the patient replies, DrKing checks your real Dentally availability and offers actual open slots. The booking lands in your Dentally calendar automatically.'),
            ('Confirmations and reminders', 'The patient receives an SMS confirmation instantly. A reminder is scheduled before the appointment, reducing no-shows without extra work for your team.'),
            ('Reviews after treatment', 'After a completed visit, DrKing can invite the patient to leave a Google review — building your practice\u2019s reputation while the experience is fresh.'),
        ],
        'use_cases': [
            ('The 2 pm new-patient enquiry',
             'A new patient calls while your entire team is chair-side. The call goes unanswered. DrKing texts back instantly, offers times from your Dentally calendar, and the new patient is booked before they think about calling anyone else.'),
            ('The recall that books itself',
             'A patient due for a six-month check-up receives a friendly text with available Dentally slots. They reply with a time. The booking is confirmed. Your front desk sees a filled chair, not a growing recall list.'),
            ('The Sunday-night emergency',
             'A patient calls at 8 pm on a Sunday with a broken tooth. DrKing\u2019s voice AI answers, gathers the details and flags it for your team to follow up first thing Monday morning — with the full context.'),
        ],
    },
    {
        'slug': 'dental4web-integration',
        'vendor': 'Dental4Web & Dental4Windows', 'short': 'Dental4Web', 'initial': 'D4W', 'accent': '#0d5c5c', 'dental': True,
        'title': 'DrKing + Dental4Web Integration | DrKing',
        'description': 'Connect DrKing to Dental4Web. Missed-call text-back, voice AI and 24/7 booking flow straight into your Dental4Web calendar.',
        'h1': 'DrKing meets <em>Dental4Web.</em>',
        'lede': 'Your Dental4Web calendar is the centre of your practice. DrKing keeps it full \u2014 answering the calls you miss, texting patients back instantly, and booking straight into Dental4Web.',
        'status_label': 'Available now',
        'status_note': 'DrKing connects with Dental4Windows and Dental4Web today. Talk to our team about the setup that suits your workflow.',
        'problems': [
            ('Your front desk can\u2019t be in two places at once',
             'The phone rings while a patient is standing at the counter and a dentist is asking for a chart update. Something gives — and it\u2019s usually the caller on the line.'),
            ('Treatment follow-up is nobody\u2019s job',
             'After a major treatment plan, patients often have questions, concerns or scheduling needs. Without a structured follow-up, those conversations happen ad hoc — or not at all.'),
            ('Online reputation is an afterthought',
             'Happy patients rarely think to leave a review unless asked. The ask has to be timely, personal and effortless — which is hard when your team is already stretched.'),
        ],
        'workflows': [
            ('Call missed, text sent', 'DrKing detects the missed call and sends a warm SMS within 60 seconds \u2014 while the patient is still holding their phone. The text offers to book an appointment.'),
            ('AI books into Dental4Web', 'When the patient replies, DrKing checks your real Dental4Web availability and offers actual open slots. The booking lands in your D4Web calendar automatically.'),
            ('Confirmations and reminders', 'The patient receives an SMS confirmation instantly. A reminder is scheduled before the appointment, reducing no-shows without extra work for your team.'),
            ('Reviews after treatment', 'After a completed visit, DrKing can invite the patient to leave a Google review \u2014 building your practice\u2019s reputation while the experience is fresh.'),
        ],
        'use_cases': [
            ('The 2 pm new-patient enquiry',
             'A new patient calls while your entire team is chair-side. The call goes unanswered. DrKing texts back instantly, offers times from your Dental4Web calendar, and the new patient is booked before they think about calling anyone else.'),
            ('The recall that books itself',
             'A patient due for a six-month check-up receives a friendly text with available D4Web slots. They reply with a time. The booking is confirmed. Your front desk sees a filled chair, not a growing recall list.'),
            ('The review that writes itself',
             'A patient finishes a crown prep and leaves happy. DrKing\u2019s review invitation arrives while the good feeling is fresh. The Google review posts before the anaesthetic wears off.'),
        ],
    },
    {
        'slug': 'core-practice-integration',
        'vendor': 'Core Practice', 'initial': 'CP', 'accent': '#a8c5b5', 'dental': True,
        'title': 'DrKing + Core Practice Integration | DrKing',
        'description': 'A DrKing + Core Practice integration is planned. Every DrKing tool works alongside it today. Register interest to move it up the roadmap.',
        'h1': 'DrKing meets <em>Core Practice.</em>',
        'lede': 'If your dental practice runs Core Practice, the DrKing integration is on the roadmap — with scope and timing being confirmed with practices like yours. The standalone toolkit works today, and registering your interest moves the integration up the queue.',
        'status_label': 'Planned',
        'status_note': 'Core Practice practices can use the full DrKing toolkit today — AI voice, chat, booking, reminders, reviews and text-to-pay. Register interest and be first in line when the direct integration is ready.',
        'problems': [
            ('Phone interruptions break your clinical rhythm',
             'A dentist\u2019s day is built around chair time. Every phone interruption breaks that rhythm — for the receptionist answering it and the clinician hearing it.'),
            ('New patient enquiries arrive at the worst moment',
             'The phone rings during a procedure, a consult, or the two minutes your team actually gets to breathe. New patients don\u2019t call back — they book with whoever answers first.'),
            ('The admin list never gets shorter',
             'Recalls, confirmations, follow-ups, review requests — each one is a task your front desk has to remember, find time for, and execute. The list grows faster than the day.'),
        ],
        'workflows': [
            ('Standalone toolkit, available today', 'DrKing\u2019s AI voice receptionist, missed-call text-back, 24/7 online booking, SMS reminders, review invitations, text-to-pay and patient reactivation all run alongside Core Practice today.'),
            ('Your voice, answered around the clock', 'DrKing AI answers every call — during chair-side hours, at lunch, after close, on weekends. Callers hear your practice name, get real times, and the booking is confirmed by SMS.'),
            ('Direct Core Practice integration (planned)', 'Scope and timing are being confirmed with practices. Register your interest and you\u2019ll be first in line — and your registration helps move the integration up the roadmap.'),
        ],
        'use_cases': [
            ('The lunchtime rush',
             'Your front desk steps away for twelve minutes. Three calls come in. DrKing answers all three, books two appointments and flags one for a callback. Your team returns to a calmer desk and a fuller calendar.'),
            ('The patient who almost went elsewhere',
             'A new patient calls at 6:15 pm on a Friday. Your practice closed at 5. DrKing\u2019s voice AI answers, offers Monday morning slots, and the booking is confirmed before the patient Googles another dentist.'),
            ('The follow-up that builds trust',
             'After a complex treatment plan, the patient receives a friendly check-in text with a simple way to reach your team if they have questions. It\u2019s the kind of touch that builds a practice\u2019s reputation quietly.'),
        ],
    },
    {
        'slug': 'cliniko-integration',
        'vendor': 'Cliniko', 'initial': 'C', 'accent': '#0d5c5c', 'dental': False,
        'title': 'DrKing + Cliniko Integration | DrKing',
        'description': 'Connect DrKing to Cliniko. Missed-call text-back, voice AI and 24/7 booking flow straight into your Cliniko calendar.',
        'h1': 'DrKing meets <em>Cliniko.</em>',
        'lede': 'Your Cliniko calendar keeps the practice running. DrKing keeps it full — answering calls your team can\u2019t get to, texting patients who\u2019ve slipped through, and booking straight into Cliniko.',
        'status_label': 'Available now',
        'status_note': 'DrKing connects with Cliniko today. Talk to our team about the setup that suits your workflow.',
        'problems': [
            ('Treatment rooms and reception can\u2019t overlap',
             'Your physios, osteos or chiros are with patients. The phone is ringing in an empty or understaffed reception. Someone has to choose: the person in front of you, or the person on the line.'),
            ('Appointment gaps are invisible until they cost you',
             'A cancelled 2 pm slot means lost revenue and an unbalanced day. Without a system to fill those gaps quickly, they stay empty.'),
            ('New patients don\u2019t wait',
             'A new patient looking for a physio calls three practices. The first one to answer gets the booking. The second and third get voicemail — and the patient moves on.'),
        ],
        'workflows': [
            ('Call missed, text sent', 'DrKing detects the missed call and sends a warm SMS within 60 seconds. The text offers to book an appointment — meeting the patient while they\u2019re still holding their phone.'),
            ('AI books into Cliniko', 'When the patient replies, DrKing checks your real Cliniko availability and offers actual open slots. The booking lands in your Cliniko calendar automatically.'),
            ('Reminders that reduce no-shows', 'SMS reminders go out before each appointment. Patients confirm or reschedule with a quick reply — fewer no-shows, fewer empty slots, less chasing for your team.'),
            ('After-hours, covered', 'Evenings, weekends, early mornings — DrKing answers. Your patients get a real conversation and a confirmed booking, not a voicemail box.'),
        ],
        'use_cases': [
            ('The patient between sessions',
             'Your whole team is in treatment rooms. A patient calls to reschedule. DrKing answers, moves the appointment to Thursday, and sends a confirmation — your Cliniko calendar updates without anyone leaving a session.'),
            ('The new enquiry at 7 am',
             'A runner tweaks a hamstring on a Saturday morning. They call your practice. DrKing\u2019s voice AI answers, offers Monday\u2019s first available, and the new patient is booked before they\u2019ve finished their coffee.'),
            ('The cancelled slot that refills',
             'A 3 pm cancellation comes in at 11 am. DrKing texts your waitlist, offers the slot, and fills it by 11:20. Your team doesn\u2019t have to think about it.'),
        ],
        'custom_hero': cliniko_hero(),
        'custom_secondary': cliniko_usecase(),
    },
    {
        'slug': 'nookal-integration',
        'vendor': 'Nookal', 'initial': 'N', 'accent': '#0d5c5c', 'dental': False,
        'title': 'DrKing + Nookal Integration | DrKing',
        'description': 'Connect DrKing to Nookal. Missed-call text-back, voice AI and 24/7 booking flow straight into your Nookal calendar.',
        'h1': 'DrKing meets <em>Nookal.</em>',
        'lede': 'If your practice runs on Nookal, DrKing fits right alongside it — answering missed calls, sending instant text-backs, and booking patients straight into your Nookal calendar, around the clock.',
        'status_label': 'Available now',
        'status_note': 'DrKing connects with Nookal today. Talk to our team about the setup that suits your workflow.',
        'problems': [
            ('Hands are on patients, not phones',
             'Your remedial massage therapists, myotherapists or physios are mid-session. The phone rings in the next room. By the time someone can reach it, the caller has hung up.'),
            ('After-hours callers have already moved on by morning',
             'A sore back doesn\u2019t respect opening hours. Someone who calls at 8 pm and reaches voicemail has usually booked with a competitor before your team arrives the next day.'),
            ('The admin pile grows between sessions',
             'Confirmations, recalls, rebooking messages — every one is a task that stacks up between treatment sessions and eats the gaps in your team\u2019s day.'),
        ],
        'workflows': [
            ('Call missed, text sent', 'DrKing detects the missed call and texts the patient within 60 seconds — a warm SMS that offers to help them book. No voicemail, no dead end.'),
            ('AI books into Nookal', 'The patient replies. DrKing checks your real Nookal availability, offers actual open slots, and the booking lands in your Nookal calendar automatically.'),
            ('Reminders that work', 'Each appointment gets an SMS reminder. Patients confirm or reschedule with a reply. Fewer no-shows, fewer gaps, less chasing.'),
            ('Always on', 'DrKing doesn\u2019t clock off. Evenings, weekends, public holidays — every caller gets a conversation and a next step.'),
        ],
        'use_cases': [
            ('The mid-session call',
             'A patient calls to book a follow-up while your whole team is in treatment rooms. DrKing texts back, offers Thursday morning from your Nookal calendar, and confirms the booking — nobody had to interrupt a session.'),
            ('The Sunday sports injury',
             'A footballer hurts a shoulder at 4 pm on a Sunday. They call. DrKing\u2019s voice AI answers, gathers the details, and books them into Monday\u2019s first available Nookal slot.'),
            ('The rebooking that actually happens',
             'After a good session, a patient means to rebook but forgets. DrKing\u2019s reactivation text arrives at the right moment with available times. They reply. The Nookal calendar fills.'),
        ],
    },
    {
        'slug': 'power-diary-integration',
        'vendor': 'Power Diary', 'initial': 'PD', 'accent': '#c8553d', 'dental': False,
        'title': 'DrKing + Power Diary Integration | DrKing',
        'description': 'Connect DrKing to Power Diary. Missed-call text-back, voice AI and 24/7 booking flow straight into your Power Diary calendar.',
        'h1': 'DrKing meets <em>Power Diary.</em>',
        'lede': 'Power Diary keeps your psychology or allied health practice organised. DrKing keeps it reachable — answering calls your team can\u2019t take, sending texts that get replies, and booking straight into Power Diary.',
        'status_label': 'Available now',
        'status_note': 'DrKing connects with Power Diary today. Talk to our team about the setup that suits your workflow.',
        'problems': [
            ('Confidential sessions mean silent phones',
             'A psychologist in session can\u2019t answer the phone. Not shouldn\u2019t — can\u2019t. Every call that goes to voicemail during a session is a potential new client who won\u2019t call back.'),
            ('New client enquiries are time-sensitive',
             'When someone finally works up the courage to call a therapist, that window is narrow. A voicemail means they may lose the momentum — and call someone else, or no one.'),
            ('The admin between clients never ends',
             'Confirmations, reminders, follow-ups, new client forms — the admin stacks up between sessions and competes with the few moments your team has to breathe.'),
        ],
        'workflows': [
            ('Call missed, text sent', 'DrKing detects the missed call and sends a calm, professional SMS within 60 seconds — acknowledging the call and offering to help book a time.'),
            ('AI books into Power Diary', 'When the client replies, DrKing checks your real Power Diary availability and offers open slots. The booking lands in your Power Diary calendar automatically.'),
            ('Reminders that reduce no-shows', 'SMS reminders before each appointment help clients keep the time they booked — reducing the gap between intention and attendance.'),
            ('Privacy-respecting by design', 'DrKing handles administrative communication — bookings, times, confirmations. It never asks about clinical concerns, and anything sensitive is routed to your team.'),
        ],
        'use_cases': [
            ('The call during a session',
             'A new client calls while you\u2019re in a confidential session. DrKing texts back with a warm, professional message offering available times. The client replies. The Power Diary slot fills — and you find out after your session ends.'),
            ('The 9 pm enquiry',
             'Someone decides at 9 pm that they want to book a first appointment. DrKing\u2019s voice AI answers, offers times from your Power Diary calendar, and the booking is confirmed — before they have time to reconsider.'),
            ('The client who needs a reminder',
             'A regular client has a Tuesday session but forgot to add it to their calendar. DrKing\u2019s SMS reminder arrives Monday afternoon. They show up. The slot doesn\u2019t go to waste.'),
        ],
    },
]

for page in PAGES:
    url = 'https://drking.ai/' + page['slug']
    title, description = page['title'], page['description']
    vendor = page['vendor']
    graph = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': 'https://drking.ai/#organization', 'name': 'DrKing', 'url': 'https://drking.ai/'},
        {'@type': 'WebPage', '@id': url + '#webpage', 'name': title, 'description': description,
         'url': url, 'inLanguage': 'en-AU', 'publisher': {'@id': 'https://drking.ai/#organization'}},
    ]}
    problems_html = ''.join(
        f'<article class="problem-card"><h3>{escape(t)}</h3><p>{escape(d)}</p></article>'
        for t, d in page['problems']
    )
    secondary = page.get('custom_secondary','')
    secondary_html = f'\n<div class="secondary-art">{secondary}</div>\n' if secondary else ''
    sections = f'''
<section class="article-section" aria-labelledby="p1"><span class="step-tag">The problems</span>
<h2 id="p1">What your front desk is actually up against.</h2>
<div class="problem-grid">{problems_html}</div></section>

<section class="article-section soft" aria-labelledby="p2"><span class="step-tag">The workflows</span>
<h2 id="p2">How DrKing works with {escape(vendor)}.</h2>
<div class="workflow-grid">{workflow_steps(page['workflows'])}</div>
<div class="status-banner"><span class="status-dot"></span><div><strong>{escape(page['status_label'])}</strong><p>{escape(page['status_note'])}</p></div></div></section>
{secondary_html}
<section class="article-section" aria-labelledby="p3"><span class="step-tag">Use cases</span>
<h2 id="p3">Moments where it makes the difference.</h2>
<div class="use-case-grid">{use_case_cards(page['use_cases'])}</div></section>

<section class="article-section" aria-labelledby="p4"><span class="step-tag">Good to know</span>
<h2 id="p4">Honest answers about this integration.</h2>
<details open><summary>Can I use DrKing with {escape(vendor)} today?</summary><p>{escape(page['status_note'])}</p></details>
<details><summary>Does DrKing replace my reception team?</summary><p>No. DrKing handles routine administrative communication — booking, availability, practice information. Complex, sensitive or clinical conversations are flagged for your staff with the full context. Your team stays responsible for what matters most.</p></details>
<details><summary>What if my practice uses a different PMS?</summary><p>Every DrKing tool — AI voice receptionist, text-back, online booking, reminders, reviews, text-to-pay — runs alongside any practice management system. Check the <a href="/integrations">full integrations page</a> for the current roadmap.</p></details></section>'''

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
        '<link rel="stylesheet" href="/assets/vendor-pages.css">\n'
        '<script src="/assets/site-shell.js" defer></script>\n'
        f'<script type="application/ld+json" id="structured-data">{json.dumps(graph, ensure_ascii=False, separators=(",", ":"))}</script>\n'
        '</head><body>\n'
    )
    hero_art = page.get('custom_hero') or integration_graphic(page['initial'], vendor, page['accent'], page['dental'])
    hero = (
        '<main id="main" class="blog-article"><div class="article-wrap">'
        '<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span>'
        f'<a href="/integrations">Integrations</a><span aria-hidden="true">/</span><span>{escape(page["vendor"])}</span></nav></div>'
        f'<section class="article-hero" aria-labelledby="article-title"><div class="article-wrap hero-grid">'
        f'<div><p class="article-eyebrow">Integration · {escape(page["status_label"])}</p>'
        f'<h1 id="article-title">{page["h1"]}</h1>'
        f'<p class="article-lede">{page["lede"]}</p></div>'
        f'<div class="hero-art">{hero_art}</div>'
        '</div></section><div class="article-wrap article-main">'
    )
    cta = (
        '<section class="article-cta" aria-labelledby="article-cta-title">'
        f'<div><span class="step-tag">Next step</span><h2 id="article-cta-title">See it with your practice.</h2>'
        f'<p>Ask the DrKing team to demonstrate the missed-call text-back and voice AI using a workflow like yours.</p></div>'
        f'<div class="cta-links"><a class="article-button" href="/demo">Book a free demo <span aria-hidden="true">&#8599;</span></a>'
        f'<a class="article-secondary" href="/integrations">All integrations <span aria-hidden="true">&#8594;</span></a></div>'
        '</section></div></main>'
    )
    (root / (page['slug'] + '.html')).write_text(head + shell + hero + sections + cta + site_footer + '\n</body></html>\n')
    print('built', page['slug'] + '.html')