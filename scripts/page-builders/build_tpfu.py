import json, shutil, sys
REPO = '/app/data/workspaces/drking-two-guides-20261030'
SRC = REPO + '/patient-reactivation.html'
DST = REPO + '/treatment-plan-follow-up.html'
shutil.copyfile(SRC, DST)
s = open(DST, encoding='utf-8').read()

TITLE = 'Treatment Plan Follow-Up for Clinics | DrKing'
DESC = ('Treatment plan follow-up for accepted but unscheduled treatment: personalised SMS and email, '
        'AI replies, booking and team hand-off for Australian practices.')
assert len(TITLE) <= 60 and 70 <= len(DESC) <= 160, (len(TITLE), len(DESC))
URL = 'https://drking.ai/treatment-plan-follow-up'
PLUS = '<svg fill="none" stroke="currentColor" stroke-width="1.5"><use href="#plus"/></svg>'

FAQ = [
 ('What is treatment plan follow-up?',
  'It’s a planned, respectful check-in with patients who accepted a treatment plan but haven’t booked or returned. DrKing sends personalised SMS and email follow-ups, answers routine replies and helps patients book, while your team handles anything that needs a person.'),
 ('How is this different from patient reactivation?',
  'Patient reactivation contacts lapsed patients who haven’t visited for a while. Treatment plan follow-up focuses on patients who already agreed to specific treatment but haven’t scheduled it, so messages refer to that open plan and run on their own timing.'),
 ('What if a patient asks about cost or the treatment itself?',
  'DrKing passes cost, payment and clinical questions to your practice team in the same inbox, so a person can respond. It doesn’t give clinical advice or negotiate fees. Routine questions, such as available times, can be answered automatically.'),
 ('When does the follow-up stop?',
  'Your practice sets the stop rules. A sequence can end when the patient books, says they’re not going ahead, asks to wait or opts out. Messages include a clear way to stop future messages.'),
 ('Can we choose which patients are followed up?',
  'Yes. Your team defines who is included before anything is sent. Use patients with appropriate permission to contact, exclude anyone who has opted out, and confirm your practice’s patient data and messaging requirements during setup.'),
]

n = 0
def rep(old, new):
    global s, n
    c = s.count(old)
    assert c >= 1, 'MISSING: ' + old[:90]
    s = s.replace(old, new, 1); n += 1

# ---- FAQ blocks (visible + JSON-LD), replaced as exact original substrings
i = s.find('<div class="faq-list">'); j = s.find('</div></section>', i)
old_faq = s[i:j]
rep(old_faq, '<div class="faq-list">' + ''.join(
    f'<details><summary>{q}{PLUS}</summary><p>{a}</p></details>' for q, a in FAQ))
i = s.find('"mainEntity":['); j = s.find(']},{"@type":"BreadcrumbList"', i)
rep(s[i:j + 1], '"mainEntity":' + json.dumps([
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ],
    ensure_ascii=False, separators=(',', ':')))

# ---- head / SEO
rep('<title>Clinic Patient Reactivation Campaigns Australia | DrKing</title>', f'<title>{TITLE}</title>')
rep('<meta name="description" content="Bring lapsed patients back with DrKing. Personalised SMS patient reactivation campaigns, automated replies and AI booking for Australian clinics.">',
    f'<meta name="description" content="{DESC}">')
rep('<link rel="canonical" href="https://drking.ai/patient-reactivation">', f'<link rel="canonical" href="{URL}">')
rep('<meta property="og:title" content="Your next patient already knows you. | DrKing">', f'<meta property="og:title" content="{TITLE}">')
rep('<meta property="og:description" content="Turn forgotten patient relationships into new appointments with personalised reactivation campaigns.">',
    f'<meta property="og:description" content="{DESC}">')
rep('<meta property="og:url" content="https://drking.ai/patient-reactivation">', f'<meta property="og:url" content="{URL}">')
rep('"@id":"https://drking.ai/patient-reactivation#webpage","url":"https://drking.ai/patient-reactivation","name":"Clinic Patient Reactivation Campaigns Australia | DrKing","description":"Bring lapsed patients back with DrKing. Personalised SMS patient reactivation campaigns, automated replies and AI booking for Australian clinics."',
    f'"@id":"{URL}#webpage","url":"{URL}","name":"{TITLE}","description":"{DESC}"')
rep('"name":"Patient reactivation","item":"https://drking.ai/patient-reactivation"', f'"name":"Treatment plan follow-up","item":"{URL}"')

# ---- hero
rep('<div class="eyebrow">Patient reactivation · Made for Australian clinics</div>', '<div class="eyebrow">Treatment plan follow-up · For Australian practices</div>')
rep("<h1 id=\"hero-title\">Some patients haven't<br class=\"desktop-break\"> been back in a while.<br>They're not <em>lost</em> —<br>they're forgotten.</h1>",
    '<h1 id="hero-title">They said yes<br class="desktop-break"> to the treatment plan.<br>Then the <em>booking</em><br>didn’t happen.</h1>')
rep("<p>Some lapsed patients just need a friendly hello. DrKing finds patients who haven't visited in 6+ months and runs personalised SMS and email reactivation campaigns every month.</p>",
    '<p>Treatment plan follow-up for accepted but unscheduled treatment. DrKing sends personalised SMS and email check-ins, answers routine replies and helps patients book.</p>')
rep('href="#revenue">Bring your patients back', 'href="#revenue">See a follow-up sequence')
rep(' A little follow-up. A healthier practice.</div>', ' Respectful follow-up. Your team stays in charge.</div>')
rep('aria-label="Illustrative SMS conversation: a clinic welcomes Sarah back, she asks for Thursday, and an appointment is booked."',
    'aria-label="Illustrative SMS conversation: a practice follows up Daniel about his accepted crown treatment, he asks about cost, and the question goes to the team."')
rep('<strong>A familiar face, rediscovered.</strong><span>Last visit: 18 months ago</span>',
    '<strong>Treatment plan accepted.</strong><span>Crown · not yet booked</span>')
rep('Your clinic, with DrKing<small>A thoughtful check-in</small>', 'Your practice, with DrKing<small>A friendly follow-up</small>')
rep("Hi Sarah, it's been a little while! We'd love to see you at the clinic again. Would you like to book a check-up?",
    'Hi Daniel, just checking in about the crown we discussed. Would you like us to find a time for it?')
rep('<div class="message reply">Hi! Yes please. Do you have anything on Thursday?</div>',
    '<div class="message reply">Yes, but can I ask about paying it off first?</div>')
rep('<div class="message confirm">Absolutely. We have 10:30 am on Thursday. Shall I book you in?</div>',
    '<div class="message confirm">Of course. I’ll ask our team to call you.</div>')
rep('<strong>Patient reactivated</strong><small>One message. A new appointment.</small>',
    '<strong>Handed to your team</strong><small>Cost question. A person replies.</small>')
rep('Sometimes, all it takes is hello.<svg', 'Often, one question is in the way.<svg')

# ---- capability tiles (stats band)
rep('aria-label="Patient reactivation at a glance"', 'aria-label="Treatment plan follow-up at a glance"')
rep('<div class="stat-number">Monthly</div><div class="stat-label">reactivation campaigns</div>',
    '<div class="stat-number">SMS + email</div><div class="stat-label">personalised follow-up sequences</div>')
rep('<div class="stat-number">SMS + email</div><div class="stat-label">personal invitations to return</div>',
    '<div class="stat-number">Two-way</div><div class="stat-label">AI replies to routine questions</div>')
rep('<div class="stat-number">12-month</div><div class="stat-label">campaign calendar</div>',
    '<div class="stat-number">Hand-off</div><div class="stat-label">for cost and clinical questions</div>')
rep('<div class="stat-label">for every reply</div>', '<div class="stat-label">for replies and bookings</div>')
rep('What DrKing runs for your clinic, month after month.', 'What DrKing does after a patient accepts a plan.')

# ---- problem list
rep('<div class="eyebrow">The quiet gap in your practice</div>', '<div class="eyebrow">Why accepted treatment goes unbooked</div>')
rep("<h2 id=\"problem-heading\">They didn't leave.<br>Life just <em>got in the way.</em></h2>",
    '<h2 id="problem-heading">They said yes.<br>Then <em>life intervened.</em></h2>')
rep('<p>A busy week becomes a missed check-up. A missed check-up becomes a year. And a patient who trusts you slips through the cracks.</p>',
    '<p>Cost, nerves, timing or simply forgetting. Unscheduled treatment usually has a real, understandable reason, and it deserves a respectful follow-up.</p>')
rep("<h3>Your patient list holds people you've lost touch with</h3><p>They already know your team. They already trust your care. But without a way to spot who hasn't returned, those relationships sit quietly in your database.</p>",
    '<h3>Cost or timing needs a conversation</h3><p>Some patients need to plan for the expense or wait for a better month. They need an easy way to ask questions, not pressure to decide.</p>')
rep('<h3>Nobody has time to call lapsed patients</h3><p>Your reception team is looking after the people in front of them. Working through an 18-month-old patient list never quite makes it to the top of the day.</p>',
    '<h3>Nerves and busy lives get in the way</h3><p>Some patients feel anxious about the treatment. Others simply forget once they leave the room. A gentle, well-timed reminder respects both.</p>')
rep("<h3>Returning patients don't need to be found all over again</h3><p>No new audience to find. No introduction to make. Reconnecting with an existing patient can mean less acquisition spend and more of your time devoted to care.</p>",
    '<h3>Reception rarely has time to chase open plans</h3><p>Your front desk is looking after the patients in front of them. Working through accepted-but-unbooked plans rarely makes it to the top of the day.</p>')

# ---- former calculator -> example sequence (no dollar figures)
rep('<div class="eyebrow">The opportunity hiding in plain sight</div>', '<div class="eyebrow">An example follow-up sequence</div>')
rep('<h2 id="revenue-heading">A small nudge.<br>A rather big <em>difference.</em></h2>',
    '<h2 id="revenue-heading">A gentle nudge.<br>At the <em>right moment.</em></h2>')
rep("<p>Start with your own list size. Use the slider below.<br>The result is <strong>an example estimate, not a forecast.</strong></p><p>The rate and visit value are examples. Your clinic's will differ.</p>",
    '<p>Here’s how follow-up could run once a patient accepts a plan but doesn’t book.<br>The timing shown is <strong>an example, not a rule.</strong></p><p>Your practice sets the steps, channels and stop rules.</p>')
i = s.find('<div class="calculator reveal">'); j = s.find('</p></div></div></section>', i) + len('</p></div>')
rep(s[i:j], '<div class="calculator reveal"><div class="calc-label"><span>Example sequence</span><output>3 steps</output></div>'
    '<div class="calc-math"><div><strong>Day 3</strong><span>example SMS</span></div><span class="multiply">→</span>'
    '<div><strong>Week 2</strong><span>example email</span></div><span class="multiply">→</span>'
    '<div><strong>Reply</strong><span>AI or your team</span></div></div>'
    '<div class="calc-result"><output>Booked</output><span>or stopped when the patient opts out or asks to wait</span></div>'
    '<p class="fine-print">Example timing only, not a recommendation. You choose the steps, channels, wording and stop rules during setup. Cost and clinical questions always go to your practice team.</p></div>')

# ---- how it works
rep('<div class="eyebrow">From “it\'s been a while” to “see you Thursday”</div>', '<div class="eyebrow">From “I’ll call to book” to “see you Tuesday”</div>')
rep('<h2 id="how-heading">The follow-up you meant to do.<br><em>Already taken care of.</em></h2>',
    '<h2 id="how-heading">Open treatment plans,<br><em>followed up with care.</em></h2>')
rep('<p>DrKing turns your patient list into thoughtful conversations, then helps those conversations become appointments.</p>',
    '<p>DrKing turns accepted-but-unbooked treatment into respectful conversations, then helps those conversations become appointments.</p>')
rep("<h3>Find the familiar faces</h3><p>Identify patients who haven't visited in 6+ months. Build a focused reactivation audience from your patient records, with campaigns run each month.</p>",
    '<h3>Build the follow-up list</h3><p>Start with patients who accepted a treatment plan but haven’t booked or returned. Your team decides who is included and when outreach begins.</p>')
rep("<h3>Send a personal hello</h3><p>Reach out by SMS or email with a personalised invitation to return. DrKing handles routine replies automatically, so interest doesn't disappear in an unattended inbox.</p>",
    '<h3>Send a personal follow-up</h3><p>Personalised SMS and email sequences check in about the treatment discussed. DrKing replies to routine questions in two-way conversations, so interest isn’t left waiting.</p>')
rep('<h3>Make coming back easy</h3><p>AI booking helps returning patients find a suitable appointment. Capture interested replies for follow-up and pass questions that need a human to your team.</p>',
    '<h3>Book it, or hand it over</h3><p>AI booking helps ready patients find a time. Cost and clinical questions go to your practice team, and opt-outs or stop rules end the sequence.</p>')
rep('href="/lead-management">Explore lead management', 'href="/unscheduled-treatment-follow-up">Read the follow-up guide')

# ---- features
rep('<div class="eyebrow">More care. Less chasing.</div>', '<div class="eyebrow">Respectful, not pushy.</div>')
rep('<h2 id="features-heading">A welcome back.<br>Without the<br><em>extra workload.</em></h2>',
    '<h2 id="features-heading">Open plans, handled.<br>Without the<br><em>phone tag.</em></h2>')
rep("<p>Everything a clinic patient reactivation campaign needs, from the first message to the next visit.</p>",
    '<p>What treatment plan follow-up needs, from the first message to the booked appointment.</p>')
rep("<h3>The right patients, at the right time</h3><p>Focus on patients overdue for a visit. Set your reactivation window around your clinic's recall needs.</p>",
    '<h3>Sequences that suit your practice</h3><p>Set the timing, channels and wording of personalised SMS and email follow-ups for unscheduled treatment.</p>')
rep('<h3>Personal messages. Automatic replies.</h3><p>Start with a familiar, friendly SMS. Keep the conversation moving when patients reply, even when reception is busy.</p>',
    '<h3>Two-way replies, handled by AI</h3><p>When patients reply, DrKing answers routine questions and keeps the conversation moving, even when reception is busy.</p>')
rep('<h3>A shorter path back to the chair</h3><p>AI-assisted booking helps patients choose a time without the back-and-forth of phone tag.</p>',
    '<h3>A person for cost and clinical questions</h3><p>Fee, payment and treatment questions go to your team, who can send a <a href="/text-to-pay" style="color:var(--teal);text-decoration:underline;text-underline-offset:4px">text-to-pay</a> link where suitable. No clinical advice from AI.</p>')
rep("<h3>Fewer interested patients slip away</h3><p>Capture returning-patient enquiries and keep follow-up organised, including people who are interested but aren't ready to book.</p>",
    '<h3>Stop rules and opt-outs built in</h3><p>Sequences end when a patient books, opts out or asks to wait. Messages include a clear way to stop.</p>')
rep("<h3>Keep the next appointment on track</h3><p>Pair reactivation with <a href=\"/appointment-reminders\" style=\"color:var(--teal);text-decoration:underline;text-underline-offset:4px\">appointment reminders</a> to help patients remember the visit they've just booked.</p>",
    '<h3>One inbox, tracked to the booking</h3><p>Replies land in one inbox, with replies and bookings tracked. Pair with <a href="/appointment-reminders" style="color:var(--teal);text-decoration:underline;text-underline-offset:4px">appointment reminders</a> for the visit itself.</p>')

# ---- audience
rep('<p>For Australian clinics that put patient relationships first.</p>', '<p>For practices that want accepted treatment to go ahead.</p>')
rep('<a class="btn" href="/allied-health">Allied health', '<a class="btn" href="/patient-reactivation">Lapsed patients')

# ---- FAQ intro
rep('<p>A closer look at bringing your patients back with DrKing.</p>', '<p>A closer look at treatment plan follow-up with DrKing.</p>')

# ---- closing
rep('<h2 id="closing-heading">Your next patient<br>already <em>knows you.</em></h2>', '<h2 id="closing-heading">They already<br>said <em>yes.</em></h2>')
rep('<p>Give them a reason to come back. DrKing takes care of the follow-up.</p>', '<p>Help them take the next step. DrKing takes care of the follow-up.</p>')
rep("href=\"#revenue\">Find your clinic's opportunity", 'href="/demo">Book a demo')

# ---- script: calculator input removed -> null-safe
rep("patients.addEventListener('input'", "patients&&patients.addEventListener('input'")

open(DST, 'w', encoding='utf-8').write(s)
print('replacements:', n)
for bad in ['Sarah', 'reactivated', 'lapsed patients', '$200', '15%', '$36,000', 'id="patients"', 'Thursday']:
    print(bad, s.count(bad))
