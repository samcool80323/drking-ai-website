import os as _os, sys as _sys
if _os.environ.get('DRKING_ALLOW_LEGACY') != '1':
    _sys.exit('LEGACY GENERATOR: the committed *.html files are now the source of truth (claims cleaned, sprites restored 2026-10-31). Re-running this would overwrite them with old copy. Set DRKING_ALLOW_LEGACY=1 only if you have ported those fixes into this script.')
"""Rebuild all vendor integration pages using the fork-and-replace approach.

Each page forks missed-call-recovery.html (the owner-approved design system)
and replaces only the content with vendor-specific copy.
"""
from pathlib import Path
import json, re

root = Path(__file__).resolve().parents[1]
SRC = (root / 'missed-call-recovery.html').read_text()

# Common replacements shared by all vendor pages (structural, not vendor-specific)
def base_replacements(vendor, h1_lead, h1_em, lede, eyebrow_text, micro_text, practice_name, patient_name):
    return [
        # meta
        ('<title>DrKing \u2014 Missed Call Text-Back for Australian Clinics</title>',
         f'<title>DrKing + {vendor} \u2014 AI Receptionist for Your Practice</title>'),
        ('<link rel="canonical" href="https://drking.ai/missed-call-recovery">',
         '',  # handled separately by caller
        ),
        # hero
        ('<div class="eyebrow">Missed call recovery</div>',
         f'<div class="eyebrow">DrKing + {vendor} integration</div>'),
        ('Missed call.<br>Instant text.<br>Lead <em>captured.</em>',
         f'{h1_lead}<br>{h1_em}'),
        ('62% of callers hang up instead of leaving voicemail \u2014 and you never even knew they called. DrKing sends an instant SMS to every missed caller within 60 seconds, captures their details, and books the appointment.',
         lede),
        ('>Recover your missed calls <', '>See it with your practice <'),
        ('Built for Australian clinics. Ready around the clock.', micro_text),
        # float card
        ('<strong>Missed call</strong><small>New patient \u00b7 just now</small>',
         '<strong>Missed call</strong><small>New patient \u00b7 just now</small>'),
        # chat
        ('Greenwood Family Clinic<small>SMS \u00b7 powered by DrKing</small>',
         f'{practice_name}<small>{vendor} \u00b7 powered by DrKing</small>'),
        ('Hi Sophie! Sorry we missed your call to Greenwood Family Clinic. Would you like to book an appointment?',
         f'Hi {patient_name}! Sorry we missed your call to {practice_name}. Would you like to book an appointment?'),
        ('Illustrative patient conversation',
         f'Illustrative conversation. Not a screenshot of {vendor}.'),
        # how-it-works heading
        ('A missed call isn\u2019t the end of the conversation',
         f'How DrKing works with your {vendor} calendar'),
        ('From ringing out to booked in.',
         'Three steps. No extra work for your front desk.'),
        # step 3
        ('<h3>Lead captured.</h3>', f'<h3>Booked in {vendor}.</h3>'),
        ('The patient replies. DrKing AI books the appointment and updates your CRM, automatically.',
         f'The patient replies. DrKing checks your {vendor} availability and the booking lands in your calendar.'),
        ('One less thing on your list', f'Straight into {vendor}'),
        # feature 3
        ('<h3>Auto-Booking via SMS</h3>', f'<h3>Auto-Booking into {vendor}</h3>'),
        ('Turn a quick reply into a confirmed appointment. Patients share their preferred time, and DrKing AI handles the booking.',
         f'Turn a quick reply into a confirmed appointment. The booking lands in your {vendor} calendar automatically.'),
        # CTA
        ('Don\u2019t let a missed call<br>be a <em>missed connection.</em>',
         f'Your {vendor} calendar,<br>always <em>within reach.</em>'),
        ('See how DrKing turns unanswered calls into booked appointments.',
         f'See how DrKing fills your {vendor} calendar \u2014 even when your team is busy.'),
        ('A little less chasing. A lot more caring.', f'Booked in {vendor}. No extra work.'),
    ]


VENDORS = {
    'dentally-integration': {
        'vendor': 'Dentally', 'slug': 'dentally-integration',
        'description': 'Connect DrKing AI to your Dentally practice. Missed-call text-back, voice AI and 24/7 booking flow straight into your Dentally calendar.',
        'h1_lead': 'Your Dentally calendar.', 'h1_em': 'Always <em>full.</em>',
        'lede': 'When your dental team is chair-side, DrKing answers the calls you can\u2019t get to. Missed-call text-back, voice AI and 24/7 booking \u2014 flowing straight into your Dentally calendar.',
        'micro': 'Available now for Dentally practices.',
        'practice': 'Bright Smile Dental', 'patient': 'Emma',
        'chat_time': 'Today 10:42 am',
        'chat_q': 'Yes please! Is there anything tomorrow morning?',
        'chat_a': 'Of course. We have 9:30 am with Dr Patel. Shall I book you in?',
        'chat_r': 'That would be great, thanks!',
        'booked_str': 'Appointment booked', 'booked_small': 'Tomorrow, 9:30 am \u00b7 Dr Patel',
        'speed': 'Chair-side call.<br>Booked anyway.',
        'team_busy': 'Your team is chair-side with patients. DrKing detects the missed call instantly.',
        'features_heading': 'Everything your front desk needs.',
        'features_sub': 'The conversations that<br>fill your chairs.',
        'features_intro': 'Every tool works alongside Dentally from day one \u2014 no waiting for an integration to switch on.',
        'feat2': ('<h3>Smart Personalisation</h3>', 'A welcome for new patients. A familiar hello for returning ones. DrKing personalises every conversation.'),
        'feat4': ('<h3>CRM Integration</h3>', 'Evenings, weekends and public holidays. Every caller gets the same instant response, 24/7.'),
        'feat5': ('<h3>After-Hours Coverage</h3>', 'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
        'feat6': ('<h3>Spam Filtering</h3>', 'SMS reminders before each appointment help patients keep the time they booked \u2014 fewer gaps, less chasing.'),
        'stat': ('26%', '24/7'), 'stat_text': 'of Australians waited longer than acceptable for a GP.', 'stat_new': 'coverage. Your patients can reach you whenever they need to.',
        'source': ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>', '<span class="source">Every DrKing tool works alongside Dentally today</span>'),
        'context_heading': 'Made for the first step easier', 'context_new': 'Made for dental practices',
        'context_h2': 'Getting care starts<br>with getting a response.', 'context_h2_new': 'Dental, ortho, cosmetic.<br>Always reachable.',
        'context_p': 'When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going \u2014 and gives patients one less reason to call somewhere else.',
        'context_p_new': 'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going \u2014 and the booking flows straight into Dentally, so your team sees filled chairs, not a growing callback list.',
        'faq_heading': 'Good questions about Dentally + DrKing',
        'faq1': ('How fast is the text-back?', 'Can I use DrKing with Dentally today?'),
        'faq1a': ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.', 'Yes. DrKing connects with Dentally today. Talk to our team about the setup that suits your practice.'),
        'faq2': ('Can the patient book via SMS?', 'How does the booking reach Dentally?'),
        'faq2a': ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.', 'When the patient confirms a time, DrKing checks your Dentally availability and the booking lands in your calendar automatically.'),
        'faq5': ('What about spam calls?', 'What about complex or clinical questions?'),
        'faq5a': ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.', 'Complex or sensitive requests are flagged for your team with the full context. The AI handles routine bookings \u2014 your staff handle what needs a person.'),
    },
    'dental4web-integration': {
        'vendor': 'Dental4Web', 'slug': 'dental4web-integration',
        'description': 'Connect DrKing AI to your Dental4Web practice. Missed-call text-back, voice AI and 24/7 booking flow straight into your D4Web calendar.',
        'h1_lead': 'Your Dental4Web calendar.', 'h1_em': 'Always <em>full.</em>',
        'lede': 'When your dental team is chair-side, DrKing answers the calls you can\u2019t get to. Missed-call text-back, voice AI and 24/7 booking \u2014 flowing straight into your Dental4Web calendar.',
        'micro': 'Available now for Dental4Windows and Dental4Web practices.',
        'practice': 'Harbour Dental Group', 'patient': 'Tom',
        'chat_time': 'Today 2:15 pm',
        'chat_q': 'Yes! I chipped a tooth. Anything tomorrow?',
        'chat_a': 'Of course. We have 8:30 am with Dr Chen. Shall I book you in?',
        'chat_r': 'Yes please, that works!',
        'booked_str': 'Booked in Dental4Web', 'booked_small': 'Tomorrow, 8:30 am \u00b7 Dr Chen',
        'speed': 'Chipped tooth.<br>Booked in minutes.',
        'team_busy': 'Your team is chair-side with patients. DrKing detects the missed call instantly.',
        'features_heading': 'Everything your front desk needs.',
        'features_sub': 'The conversations that<br>fill your chairs.',
        'features_intro': 'Every tool works alongside Dental4Web from day one \u2014 no waiting for an integration to switch on.',
        'feat2': ('<h3>Smart Personalisation</h3>', 'A welcome for new patients. A familiar hello for returning ones. DrKing personalises every conversation.'),
        'feat4': ('<h3>CRM Integration</h3>', 'Evenings, weekends and public holidays. Every caller gets the same instant response, 24/7.'),
        'feat5': ('<h3>After-Hours Coverage</h3>', 'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
        'feat6': ('<h3>Spam Filtering</h3>', 'SMS reminders before each appointment help patients keep the time they booked \u2014 fewer gaps, less chasing.'),
        'stat': ('26%', '24/7'), 'stat_text': 'of Australians waited longer than acceptable for a GP.', 'stat_new': 'coverage. Your patients can reach you whenever they need to.',
        'source': ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>', '<span class="source">Every DrKing tool works alongside Dental4Web today</span>'),
        'context_heading': 'Make the first step easier', 'context_new': 'Made for dental practices',
        'context_h2': 'Getting care starts<br>with getting a response.', 'context_h2_new': 'Dental4Windows & D4Web.<br>Always reachable.',
        'context_p': 'When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going \u2014 and gives patients one less reason to call somewhere else.',
        'context_p_new': 'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going \u2014 and the booking flows straight into Dental4Web, so your team sees filled chairs, not a growing callback list.',
        'faq_heading': 'Good questions about Dental4Web + DrKing',
        'faq1': ('How fast is the text-back?', 'Can I use DrKing with Dental4Web today?'),
        'faq1a': ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.', 'Yes. DrKing connects with Dental4Windows and Dental4Web today. Talk to our team about the setup that suits your practice.'),
        'faq2': ('Can the patient book via SMS?', 'How does the booking reach Dental4Web?'),
        'faq2a': ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.', 'When the patient confirms a time, DrKing checks your D4Web availability and the booking lands in your calendar automatically.'),
        'faq5': ('What about spam calls?', 'What about complex or clinical questions?'),
        'faq5a': ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.', 'Complex or sensitive requests are flagged for your team with the full context. The AI handles routine bookings \u2014 your staff handle what needs a person.'),
    },
    'core-practice-integration': {
        'vendor': 'Core Practice', 'slug': 'core-practice-integration',
        'description': 'A DrKing + Core Practice integration is planned. Every DrKing tool works alongside it today. Register interest to move it up the roadmap.',
        'h1_lead': 'Core Practice.', 'h1_em': 'Coming <em>soon.</em>',
        'lede': 'If your dental practice runs Core Practice, the direct integration is on the roadmap \u2014 with scope and timing being confirmed. In the meantime, every DrKing tool works alongside it today, and registering your interest moves the integration up the queue.',
        'micro': 'Planned for Core Practice. Toolkit available today.',
        'practice': 'Riverbend Dental', 'patient': 'Kate',
        'chat_time': 'Today 9:15 am',
        'chat_q': 'Yes please! Is there anything this week?',
        'chat_a': 'Of course. We have Thursday 2:00 pm with Dr Lee. Shall I book you in?',
        'chat_r': 'That would be great, thanks!',
        'booked_str': 'Appointment booked', 'booked_small': 'Thursday, 2:00 pm \u00b7 Dr Lee',
        'speed': 'Toolkit today.<br>Integration soon.',
        'team_busy': 'Your team is chair-side with patients. DrKing detects the missed call instantly.',
        'features_heading': 'Everything your front desk needs.',
        'features_sub': 'The conversations that<br>fill your chairs.',
        'features_intro': 'Every DrKing tool runs alongside Core Practice today \u2014 voice AI, text-back, booking, reminders, reviews. The direct integration is on the way.',
        'feat2': ('<h3>Smart Personalisation</h3>', 'A welcome for new patients. A familiar hello for returning ones. DrKing personalises every conversation.'),
        'feat4': ('<h3>CRM Integration</h3>', 'Evenings, weekends and public holidays. Every caller gets the same instant response, 24/7.'),
        'feat5': ('<h3>After-Hours Coverage</h3>', 'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
        'feat6': ('<h3>Spam Filtering</h3>', 'SMS reminders before each appointment help patients keep the time they booked \u2014 fewer gaps, less chasing.'),
        'stat': ('26%', '24/7'), 'stat_text': 'of Australians waited longer than acceptable for a GP.', 'stat_new': 'coverage. Every DrKing tool works alongside Core Practice today.',
        'source': ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>', '<span class="source">Direct Core Practice integration is planned</span>'),
        'context_heading': 'Make the first step easier', 'context_new': 'Made for dental practices',
        'context_h2': 'Getting care starts<br>with getting a response.', 'context_h2_new': 'Core Practice.<br>Always reachable.',
        'context_p': 'When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going \u2014 and gives patients one less reason to call somewhere else.',
        'context_p_new': 'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going today \u2014 and when the Core Practice integration ships, the booking will flow straight into your calendar.',
        'faq_heading': 'Good questions about Core Practice + DrKing',
        'faq1': ('How fast is the text-back?', 'Can I use DrKing with Core Practice today?'),
        'faq1a': ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.', 'Yes. Every DrKing tool \u2014 voice AI, text-back, booking, reminders, reviews \u2014 runs alongside Core Practice today. The direct integration is planned; register interest to move it up the roadmap.'),
        'faq2': ('Can the patient book via SMS?', 'When will the direct integration be ready?'),
        'faq2a': ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.', 'Scope and timing are being confirmed with practices. The more practices register interest, the sooner it moves up the roadmap. Your registration directly shapes the priority.'),
        'faq5': ('What about spam calls?', 'What about complex or clinical questions?'),
        'faq5a': ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.', 'Complex or sensitive requests are flagged for your team with the full context. The AI handles routine bookings \u2014 your staff handle what needs a person.'),
    },
    'nookal-integration': {
        'vendor': 'Nookal', 'slug': 'nookal-integration',
        'description': 'Connect DrKing AI to your Nookal practice. Missed-call text-back, voice AI and 24/7 booking flow straight into your Nookal calendar.',
        'h1_lead': 'Your Nookal calendar.', 'h1_em': 'Always <em>full.</em>',
        'lede': 'When your remedial massage, myotherapy or physio team is in treatment rooms, DrKing answers the calls you can\u2019t get to. Missed-call text-back, voice AI and 24/7 booking \u2014 flowing straight into your Nookal calendar.',
        'micro': 'Available now for Nookal practices.',
        'practice': 'Movement Therapy Clinic', 'patient': 'Alex',
        'chat_time': 'Saturday 8:42 am',
        'chat_q': 'Yes! I tweaked my shoulder at the gym. Anything Monday?',
        'chat_a': 'Of course. Monday 10:00 am is available with James. Shall I book you in?',
        'chat_r': 'That would be great, thanks!',
        'booked_str': 'Booked in Nookal', 'booked_small': 'Mon 10:00 am \u00b7 James \u00b7 Initial consult',
        'speed': 'Saturday call.<br>Monday booking.',
        'team_busy': 'Your team is in treatment rooms. DrKing detects the missed call instantly.',
        'features_heading': 'Everything your front desk needs.',
        'features_sub': 'The conversations that<br>fill your calendar.',
        'features_intro': 'Every tool works alongside Nookal from day one \u2014 no waiting for an integration to switch on.',
        'feat2': ('<h3>Smart Personalisation</h3>', 'A welcome for new patients. A familiar hello for returning ones. DrKing personalises every conversation.'),
        'feat4': ('<h3>CRM Integration</h3>', 'Evenings, weekends and public holidays. Every caller gets the same instant response, 24/7.'),
        'feat5': ('<h3>After-Hours Coverage</h3>', 'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
        'feat6': ('<h3>Spam Filtering</h3>', 'SMS reminders before each appointment help patients keep the time they booked \u2014 fewer gaps, less chasing.'),
        'stat': ('26%', '24/7'), 'stat_text': 'of Australians waited longer than acceptable for a GP.', 'stat_new': 'coverage. Your patients can reach you whenever they need to.',
        'source': ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>', '<span class="source">Every DrKing tool works alongside Nookal today</span>'),
        'context_heading': 'Make the first step easier', 'context_new': 'Made for allied health',
        'context_h2': 'Getting care starts<br>with getting a response.', 'context_h2_new': 'Massage, physio, chiro.<br>Always reachable.',
        'context_p': 'When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going \u2014 and gives patients one less reason to call somewhere else.',
        'context_p_new': 'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going \u2014 and the booking flows straight into Nookal, so your team sees a filled calendar, not a growing callback list.',
        'faq_heading': 'Good questions about Nookal + DrKing',
        'faq1': ('How fast is the text-back?', 'Can I use DrKing with Nookal today?'),
        'faq1a': ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.', 'Yes. DrKing connects with Nookal today. Talk to our team about the setup that suits your practice.'),
        'faq2': ('Can the patient book via SMS?', 'How does the booking reach Nookal?'),
        'faq2a': ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.', 'When the patient confirms a time, DrKing checks your Nookal availability and the booking lands in your calendar automatically.'),
        'faq5': ('What about spam calls?', 'What about complex or clinical questions?'),
        'faq5a': ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.', 'Complex or sensitive requests are flagged for your team with the full context. The AI handles routine bookings \u2014 your staff handle what needs a person.'),
    },
    'power-diary-integration': {
        'vendor': 'Power Diary', 'slug': 'power-diary-integration',
        'description': 'Connect DrKing AI to your Power Diary practice. Missed-call text-back, voice AI and 24/7 booking flow straight into your Power Diary calendar.',
        'h1_lead': 'Your Power Diary calendar.', 'h1_em': 'Always <em>full.</em>',
        'lede': 'A psychologist in session can\u2019t answer the phone. DrKing can \u2014 with a calm, professional response that respects confidentiality and books straight into your Power Diary calendar.',
        'micro': 'Available now for Power Diary practices.',
        'practice': 'Clear Mind Psychology', 'patient': 'Sam',
        'chat_time': 'Today 3:30 pm',
        'chat_q': 'Yes, I\u2019d like to book a first appointment. Anything next week?',
        'chat_a': 'Of course. We have Tuesday 10:00 am available. Shall I book you in?',
        'chat_r': 'Yes, that would be great.',
        'booked_str': 'Booked in Power Diary', 'booked_small': 'Tuesday, 10:00 am \u00b7 Initial consult',
        'speed': 'New client.<br>Booked calmly.',
        'team_busy': 'Your team is in confidential sessions. DrKing detects the missed call instantly.',
        'features_heading': 'Everything your practice needs.',
        'features_sub': 'The conversations that<br>fill your calendar.',
        'features_intro': 'Every tool works alongside Power Diary from day one \u2014 no waiting for an integration to switch on.',
        'feat2': ('<h3>Smart Personalisation</h3>', 'A calm, professional welcome for new clients. A familiar hello for returning ones. DrKing personalises every conversation.'),
        'feat4': ('<h3>CRM Integration</h3>', 'Evenings, weekends and public holidays. Every caller gets the same calm, instant response, 24/7.'),
        'feat5': ('<h3>After-Hours Coverage</h3>', 'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
        'feat6': ('<h3>Spam Filtering</h3>', 'SMS reminders before each appointment help clients keep the time they booked \u2014 fewer gaps, less chasing.'),
        'stat': ('26%', '24/7'), 'stat_text': 'of Australians waited longer than acceptable for a GP.', 'stat_new': 'coverage. Your clients can reach you whenever they\u2019re ready.',
        'source': ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>', '<span class="source">Every DrKing tool works alongside Power Diary today</span>'),
        'context_heading': 'Make the first step easier', 'context_new': 'Made for psychology practices',
        'context_h2': 'Getting care starts<br>with getting a response.', 'context_h2_new': 'Psychology, counselling.<br>Always reachable.',
        'context_p': 'When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going \u2014 and gives patients one less reason to call somewhere else.',
        'context_p_new': 'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going \u2014 and the booking flows straight into Power Diary, so your team sees a filled calendar, not a growing callback list.',
        'faq_heading': 'Good questions about Power Diary + DrKing',
        'faq1': ('How fast is the text-back?', 'Can I use DrKing with Power Diary today?'),
        'faq1a': ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.', 'Yes. DrKing connects with Power Diary today. Talk to our team about the setup that suits your practice.'),
        'faq2': ('Can the patient book via SMS?', 'How does the booking reach Power Diary?'),
        'faq2a': ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.', 'When the client confirms a time, DrKing checks your Power Diary availability and the booking lands in your calendar automatically.'),
        'faq5': ('What about spam calls?', 'What about sensitive or clinical questions?'),
        'faq5a': ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.', 'Sensitive or clinical concerns are flagged for your team with the full context. DrKing handles administrative bookings only \u2014 your staff handle what needs a person. The AI never asks about clinical matters.'),
    },
}


for slug, v in VENDORS.items():
    src = SRC
    # canonical
    src = src.replace(
        '<link rel="canonical" href="https://drking.ai/missed-call-recovery">',
        f'<link rel="canonical" href="https://drking.ai/{slug}">', 1)

    # meta description
    src = re.sub(r'<meta name="description" content="[^"]*"',
                 f'<meta name="description" content="{v["description"]}"', src, count=1)

    R = [
        ('<title>DrKing \u2014 Missed Call Text-Back for Australian Clinics</title>',
         f'<title>DrKing + {v["vendor"]} \u2014 AI Receptionist for Your Practice</title>'),
        ('<div class="eyebrow">Missed call recovery</div>',
         f'<div class="eyebrow">DrKing + {v["vendor"]} integration</div>'),
        ('Missed call.<br>Instant text.<br>Lead <em>captured.</em>',
         f'{v["h1_lead"]}<br>{v["h1_em"]}'),
        ('62% of callers hang up instead of leaving voicemail \u2014 and you never even knew they called. DrKing sends an instant SMS to every missed caller within 60 seconds, captures their details, and books the appointment.',
         v['lede']),
        ('>Recover your missed calls <', '>See it with your practice <'),
        ('Built for Australian clinics. Ready around the clock.', v['micro']),
        ('Greenwood Family Clinic<small>SMS \u00b7 powered by DrKing</small>',
         f'{v["practice"]}<small>{v["vendor"]} \u00b7 powered by DrKing</small>'),
        ('Today 10:42 am', v['chat_time']),
        ('Hi Sophie! Sorry we missed your call to Greenwood Family Clinic. Would you like to book an appointment?',
         f'Hi {v["patient"]}! Sorry we missed your call to {v["practice"]}. Would you like to book an appointment?'),
        ('Yes please! Is there anything tomorrow morning?', v['chat_q']),
        ('Of course. We have 9:30 am with Dr Patel. Shall I book you in?', v['chat_a']),
        ('That would be great, thanks!', v['chat_r']),
        ('A little text.<br>A big difference.', v['speed']),
        ('<strong>Appointment booked</strong><small>Tomorrow, 9:30 am \u00b7 Dr Patel</small>',
         f'<strong>{v["booked_str"]}</strong><small>{v["booked_small"]}</small>'),
        ('Illustrative patient conversation',
         f'Illustrative conversation. Not a screenshot of {v["vendor"]}.'),
        ('A missed call isn\u2019t the end of the conversation',
         f'How DrKing works with your {v["vendor"]} calendar'),
        ('From ringing out to booked in.', 'Three steps. No extra work for your front desk.'),
        ('Your team is busy, or the clinic is closed. DrKing detects the missed call instantly.',
         v['team_busy']),
        ('<h3>Instant SMS sent.</h3>', '<h3>Instant text sent.</h3>'),
        ('<h3>Lead captured.</h3>', f'<h3>Booked in {v["vendor"]}.</h3>'),
        ('The patient replies. DrKing AI books the appointment and updates your CRM, automatically.',
         f'The patient replies. DrKing checks your {v["vendor"]} availability and the booking lands in your calendar.'),
        ('One less thing on your list', f'Straight into {v["vendor"]}'),
        ('Thoughtful follow-up. On autopilot.', v['features_heading']),
        ('Every missed call.<br>A new possibility.', v['features_sub']),
        ('Give every patient a way forward, even when you can\u2019t get to the phone.',
         v['features_intro']),
        ('<h3>Auto-Booking via SMS</h3>', f'<h3>Auto-Booking into {v["vendor"]}</h3>'),
        ('Turn a quick reply into a confirmed appointment. Patients share their preferred time, and DrKing AI handles the booking.',
         f'Turn a quick reply into a confirmed appointment. The booking lands in your {v["vendor"]} calendar automatically.'),
        # features 2,4,5,6
        (v['feat2'][0], v['feat2'][1]),
        # feat3 handled above
        (v['feat4'][0], v['feat4'][1]),
        (v['feat5'][0], v['feat5'][1]),
        (v['feat6'][0], v['feat6'][1]),
        # context
        (v['stat'][0], v['stat'][1]),
        (v['stat_text'], v['stat_new']),
        (v['source'][0], v['source'][1]),
        (v['context_heading'], v['context_new']),
        (v['context_h2'], v['context_h2_new']),
        (v['context_p'], v['context_p_new']),
        # FAQ
        ('A few things you might be wondering', v['faq_heading']),
        ('Good questions.<br>Simple answers.', 'Clear answers.<br>No surprises.'),
        (v['faq1'][0], v['faq1'][1]),
        (v['faq1a'][0], v['faq1a'][1]),
        (v['faq2'][0], v['faq2'][1]),
        (v['faq2a'][0], v['faq2a'][1]),
        (v['faq5'][0], v['faq5'][1]),
        (v['faq5a'][0], v['faq5a'][1]),
        # CTA
        ('Don\u2019t let a missed call<br>be a <em>missed connection.</em>',
         f'Your {v["vendor"]} calendar,<br>always <em>within reach.</em>'),
        ('See how DrKing turns unanswered calls into booked appointments.',
         f'See how DrKing fills your {v["vendor"]} calendar \u2014 even when your team is busy.'),
        ('A little less chasing. A lot more caring.', f'Booked in {v["vendor"]}. No extra work.'),
    ]

    skipped = 0
    for pair in R:
        old, new = pair[0], pair[1]
        if old in src:
            src = src.replace(old, new, 1)
        else:
            skipped += 1

    # JSON-LD
    m = re.search(r'<script type="application/ld\+json"[^>]*>([\s\S]*?)</script>', src)
    if m:
        data = json.loads(m.group(1))
        for node in data.get('@graph', []):
            if node.get('@type') == 'WebPage':
                node['name'] = f'DrKing + {v["vendor"]} \u2014 AI Receptionist for Your Practice'
                node['description'] = v['description']
                node['url'] = f'https://drking.ai/{slug}'
        new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        src = src[:m.start(1)] + new_json + src[m.end(1):]

    (root / (slug + '.html')).write_text(src)
    applied = len(R) - skipped
    print(f'Built {slug}.html: {applied} applied, {skipped} skipped')