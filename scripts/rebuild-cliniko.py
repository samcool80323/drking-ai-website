import os as _os, sys as _sys
if _os.environ.get('DRKING_ALLOW_LEGACY') != '1':
    _sys.exit('LEGACY GENERATOR: the committed *.html files are now the source of truth (claims cleaned, sprites restored 2026-10-31). Re-running this would overwrite them with old copy. Set DRKING_ALLOW_LEGACY=1 only if you have ported those fixes into this script.')
"""Build the Cliniko integration page using the missed-call-recovery page's
exact design system — same CSS, same structure, Cliniko-specific content."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
src = (root / 'missed-call-recovery.html').read_text()

# ── content replacements ──────────────────────────────────────────────
R = [
    # meta
    ('<title>DrKing — Missed Call Text-Back for Australian Clinics</title>',
     '<title>DrKing + Cliniko — AI Receptionist for Your Practice</title>'),
    ('<meta name="description" content="',
     '<meta name="description" content="Connect DrKing AI to your Cliniko practice. Missed-call text-back, voice AI and 24/7 booking flow straight into your Cliniko calendar.'),
    ('<link rel="canonical" href="https://drking.ai/missed-call-recovery">',
     '<link rel="canonical" href="https://drking.ai/cliniko-integration">'),
    # hero
    ('<div class="eyebrow">Missed call recovery</div>',
     '<div class="eyebrow">DrKing + Cliniko integration</div>'),
    ('Missed call.<br>Instant text.<br>Lead <em>captured.</em>',
     'Your Cliniko calendar.<br>Always <em>full.</em>'),
    ('62% of callers hang up instead of leaving voicemail — and you never even knew they called. DrKing sends an instant SMS to every missed caller within 60 seconds, captures their details, and books the appointment.',
     'When your physio, osteo or chiro team is in treatment rooms, DrKing answers the calls you can\u2019t get to. Missed-call text-back, voice AI and 24/7 booking \u2014 flowing straight into your Cliniko calendar.'),
    ('>Recover your missed calls <',
     '>See it with your practice <'),
    ('Built for Australian clinics. Ready around the clock.',
     'Available now for Cliniko practices.'),
    # float card (missed)
    ('<strong>Missed call</strong><small>New patient · just now</small>',
     '<strong>Missed call</strong><small>Sat 8:42 am · new patient</small>'),
    # chat head
    ('>d.</div>Greenwood Family Clinic<small>SMS · powered by DrKing</small>',
     '>d.</div>Riverside Physiotherapy<small>Cliniko · powered by DrKing</small>'),
    # conversation
    ('Today 10:42 am', 'Saturday 8:42 am'),
    ('Hi Sophie! Sorry we missed your call to Greenwood Family Clinic. Would you like to book an appointment?',
     'Hi Jess! Sorry we missed your call to Riverside Physiotherapy. Would you like to book an appointment?'),
    ('Yes please! Is there anything tomorrow morning?',
     'Yes! I hurt my hamstring running. Anything Monday morning?'),
    ('Of course. We have 9:30 am with Dr Patel. Shall I book you in?',
     'Of course. Monday 9:00 am is available with Sarah. Shall I book you in?'),
    ('That would be great, thanks!',
     'That would be great, thanks!'),
    # speed note
    ('A little text.<br>A big difference.',
     'Saturday call.<br>Monday booking.'),
    # float card (booked)
    ('<strong>Appointment booked</strong><small>Tomorrow, 9:30 am · Dr Patel</small>',
     '<strong>Booked in Cliniko</strong><small>Mon 9:00 am · Sarah · Initial consult</small>'),
    ('Illustrative patient conversation',
     'Illustrative conversation. Not a screenshot of Cliniko.'),
    # how-it-works heading
    ('A missed call isn\u2019t the end of the conversation',
     'How DrKing works with your Cliniko calendar'),
    ('From ringing out to booked in.',
     'Three steps. No extra work for your front desk.'),
    ('Three simple steps. No extra work for your front desk.',
     'Every missed call becomes a conversation that books.'),
    # step 1
    ('01',
     '01'),
    ('<h3>Call missed.</h3>',
     '<h3>Call missed.</h3>'),
    ('Your team is busy, or the clinic is closed. DrKing detects the missed call instantly.',
     'Your team is in treatment rooms. DrKing detects the missed call instantly.'),
    ('The moment the call ends',
     'The moment the call ends'),
    # step 2
    ('<h3>Instant SMS sent.</h3>',
     '<h3>Instant text sent.</h3>'),
    ('A personalised text acknowledges the call and offers to help book an appointment.',
     'A personalised text reaches the patient within 60 seconds, offering to book.'),
    ('Within 60 seconds',
     'Within 60 seconds'),
    # step 3
    ('<h3>Lead captured.</h3>',
     '<h3>Booked in Cliniko.</h3>'),
    ('The patient replies. DrKing AI books the appointment and updates your CRM, automatically.',
     'The patient replies. DrKing checks your Cliniko availability and the booking lands in your calendar.'),
    ('One less thing on your list',
     'Straight into Cliniko'),
    # features section
    ('Thoughtful follow-up. On autopilot.',
     'Everything your front desk needs.'),
    ('Every missed call.<br>A new possibility.',
     'The conversations that<br>fill your calendar.'),
    ('Give every patient a way forward, even when you can\u2019t get to the phone.',
     'Every tool works alongside Cliniko from day one \u2014 no waiting for an integration to switch on.'),
    ('>Explore missed call solutions <',
     '>Explore all DrKing solutions <'),
    ('/missed-calls\'>
     '/solutions\'>
    # feature 1
    ('<h3>Instant Text-Back</h3>',
     '<h3>Instant Text-Back</h3>'),
    ('A warm, helpful SMS within 60 seconds. Reach patients while they\u2019re still looking for care.',
     'A warm, helpful SMS within 60 seconds. Reach patients while they\u2019re still thinking about your practice.'),
    # feature 2
    ('<h3>Smart Personalisation</h3>',
     '<h3>Smart Personalisation</h3>'),
    ('A welcome for new patients. A familiar hello for returning ones. DrKing checks your CRM and tailors the message.',
     'A welcome for new patients. A familiar hello for returning ones. DrKing personalises every conversation.'),
    # feature 3
    ('<h3>Auto-Booking via SMS</h3>',
     '<h3>Auto-Booking into Cliniko</h3>'),
    ('Turn a quick reply into a confirmed appointment. Patients share their preferred time, and DrKing AI handles the booking.',
     'Turn a quick reply into a confirmed appointment. The booking lands in your Cliniko calendar automatically.'),
    # feature 4
    ('<h3>CRM Integration</h3>',
     '<h3>After-Hours Cover</h3>'),
    ('Patient details and booking information flow into your CRM, so your team has the context when they need it.',
     'Evenings, weekends, public holidays. Every caller gets the same instant response, 24/7.'),
    # feature 5
    ('<h3>After-Hours Coverage</h3>',
     '<h3>Voice AI Receptionist</h3>'),
    ('Evenings, weekends and public holidays. Every missed caller gets the same instant response, 24/7.',
     'DrKing AI answers every call in natural, conversational speech \u2014 greeting callers by your practice name.'),
    # feature 6
    ('<h3>Spam Filtering</h3>',
     '<h3>Reminders That Reduce No-Shows</h3>'),
    ('Keep the focus on real patients. DrKing AI screens calls and filters known spam numbers before sending a text.',
     'SMS reminders before each appointment help patients keep the time they booked \u2014 fewer gaps, less chasing.'),
    # context stat
    ('26%',
     '24/7'),
    ('of Australians waited longer than acceptable for a GP.',
     'coverage. Your patients can reach you whenever they need to.'),
    ('<span class="source">Source: ABS, Patient Experiences 2024\u201325</span>',
     '<span class="source">Every DrKing tool works alongside Cliniko today</span>'),
    ('Make the first step easier',
     'Made for allied health'),
    ('Getting care starts<br>with getting a response.',
     'Physio, osteo, chiro.<br>Always reachable.'),
    ('When someone calls your clinic, they\u2019re ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going — and gives patients one less reason to call somewhere else.',
     'When someone calls your practice, they\u2019re ready to book. DrKing keeps that conversation going \u2014 and the booking flows straight into Cliniko, so your team sees a filled calendar, not a growing callback list.'),
    # related links
    ('/dentists\'>For dental clinics <span aria-hidden="true">\u2197</span></a><a href="/general-practice\'>For general practice <span aria-hidden="true">\u2197</span></a>',
     '/dentists\'>For dental clinics <span aria-hidden="true">\u2197</span></a><a href="/allied-health\'>For allied health <span aria-hidden="true">\u2197</span></a>'),
    # FAQ
    ('A few things you might be wondering',
     'Good questions about Cliniko + DrKing'),
    ('Good questions.<br>Simple answers.',
     'Clear answers.<br>No surprises.'),
    ('How fast is the text-back?',
     'Can I use DrKing with Cliniko today?'),
    ('Within 60 seconds of the missed call. The patient gets a personalised SMS acknowledging their call.',
     'Yes. DrKing connects with Cliniko today. Talk to our team about the setup that suits your practice.'),
    ('Can the patient book via SMS?',
     'How does the booking reach Cliniko?'),
    ('Yes. The patient replies with their preferred time, and DrKing AI books the appointment automatically.',
     'When the patient confirms a time, DrKing checks your Cliniko availability and the booking lands in your calendar automatically.'),
    ('Does it work after hours?',
     'Does it work after hours?'),
    ('Yes. Missed call recovery operates 24/7. After-hours callers get the same instant response.',
     'Yes. Every DrKing tool runs 24/7 \u2014 evenings, weekends, public holidays.'),
    ('Can it tell new and existing patients apart?',
     'Can it tell new and existing patients apart?'),
    ('Yes. DrKing checks your CRM and personalises the message accordingly.',
     'Yes. DrKing personalises the conversation for new and returning patients.'),
    ('What about spam calls?',
     'What about complex or clinical questions?'),
    ('DrKing AI screens and filters spam numbers. No text-back sent to known spam.',
     'Complex or sensitive requests are flagged for your team with the full context. The AI handles routine bookings \u2014 your staff handle what needs a person.'),
    # CTA
    ('Your next patient is calling',
     'Your next patient is calling'),
    ('Don\u2019t let a missed call<br>be a <em>missed connection.</em>',
     'Your Cliniko calendar,<br>always <em>within reach.</em>'),
    ('See how DrKing turns unanswered calls into booked appointments.',
     'See how DrKing fills your Cliniko calendar \u2014 even when your team is in treatment rooms.'),
    ('A little less chasing. A lot more caring.',
     'Booked in Cliniko. No extra work.'),
]

for old, new in R:
    if old in src:
        src = src.replace(old, new, 1)
    else:
        print(f'SKIP (not found): {old[:60]}...')

(root / 'cliniko-integration.html').write_text(src)
print('Built cliniko-integration.html using missed-call-recovery design system')