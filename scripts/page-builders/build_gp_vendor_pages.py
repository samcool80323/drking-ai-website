#!/usr/bin/env python3
"""Fork core-practice-integration.html into three GP waitlist vendor pages (text-only replacements)."""
import json, re, sys, os
REPO = "/app/data/workspaces/drking-two-guides-20261030"
SRC = os.path.join(REPO, "core-practice-integration.html")
src = open(SRC, encoding="utf-8").read()

# ---- old strings (exact, from fork) ----
O = {
 "doctype": "<!doctype html>",
 "title": "<title>DrKing + Core Practice | AI Receptionist for Dental</title>",
 "meta": '<meta name="description" content="A DrKing + Core Practice integration is planned. Every DrKing tool works alongside it today. Register interest to move it up the roadmap.">',
 "canon": '<link rel="canonical" href="https://drking.ai/core-practice-integration">',
 "og": '<meta property="og:title" content="Core Practice. On the roadmap. | DrKing"><meta property="og:description" content="A DrKing + Core Practice integration is planned. Every DrKing tool works alongside it today. Register interest to move it up the roadmap.">',
 "ogurl": '<meta property="og:url" content="https://drking.ai/core-practice-integration">',
 "crumb": '<span>Solutions</span><span aria-hidden="true">/</span><span aria-current="page">Missed call recovery</span>',
 "eyebrow": '<div class="eyebrow">DrKing + Core Practice integration</div>',
 "h1": '<h1 id="hero-title">Core Practice.<br>On the <em>roadmap.</em></h1>',
 "lede": "<p>If your dental practice runs Core Practice, the direct integration is on the roadmap — with scope and timing being confirmed. In the meantime, every DrKing tool works alongside it today, and registering your interest helps us set its priority.</p>",
 "micro": "Planned for Core Practice. Toolkit available today.</div>",
 "artlabel": 'aria-label="Example: a missed call at 10:42 receives an instant text-back. The patient replies and their appointment is booked."',
 "f1": "<strong>Missed call</strong><small>New patient · just now</small>",
 "time": "<span>10:42</span>",
 "head": "Riverbend Dental<small>Core Practice · powered by DrKing</small>",
 "chattime": '<div class="chat-time">Today 9:15 am</div>',
 "b1": '<div class="bubble">Hi Kate! Sorry we missed your call to Riverbend Dental. Would you like to book an appointment?</div>',
 "b2": '<div class="bubble reply">Yes please! Is there anything this week?</div>',
 "b3": '<div class="bubble">Of course. We have Thursday 2:00 pm with Dr Lee. Shall I book you in?</div>',
 "b4": '<div class="bubble reply">That would be great, thanks!</div>',
 "input": '<div class="chat-input">Text message <span>↑</span></div>',
 "speed": "Toolkit today.<br>Integration soon.",
 "f2": "<strong>Appointment booked</strong><small>Thursday, 2:00 pm · Dr Lee</small>",
 "caption": '<span class="art-caption">Illustrative conversation. Not a screenshot of Core Practice.</span>',
 "statsaria": 'aria-label="Missed call recovery at a glance"',
 "stats": '<div class="stat"><div class="stat-value">1<span> inbox</span></div><div class="stat-label">For calls, chat, SMS, email and social</div></div><div class="stat"><div class="stat-value">Auto<span> SMS</span></div><div class="stat-label">Text-back after a missed call</div></div><div class="stat"><div class="stat-value">2-way<span> SMS</span></div><div class="stat-label">Patients reply to book a time</div></div><div class="stat"><div class="stat-value">24<span>/7</span></div><div class="stat-label">AI web chat and online booking</div></div>',
 "howhead": "<div class=\"eyebrow\">A missed call isn't the end of the conversation</div><h2>Three steps. No extra work for your front desk.</h2><p>Three simple steps. No extra work for your front desk.</p>",
 "s1": "<h3>Call missed.</h3><p>Your team is chair-side with patients. DrKing detects the missed call instantly.</p><span class=\"small-label\">The moment the call ends</span>",
 "s2": "<h3>Instant text sent.</h3><p>A personalised text acknowledges the call and offers to help book an appointment.</p><span class=\"small-label\">Straight away</span>",
 "s3": "<h3>Booking request in.</h3><p>The patient replies with a time. Your team gets the details to confirm it in Core Practice.</p><span class=\"small-label\">Direct integration planned</span>",
 "feathead": "<div class=\"eyebrow\">Everything your front desk needs.</div><h2>The conversations that<br>fill your chairs.</h2><p>Give every patient a way forward, even when you can't get to the phone.</p><a class=\"text-link feature-link\" href=\"/missed-calls\">Explore missed call solutions <span aria-hidden=\"true\">↗</span></a>",
 "c1": "<h3>Instant Text-Back</h3><p>A warm, helpful SMS straight after a missed call. Reach patients while they're still looking for care.</p>",
 "c2": "<h3>Smart Personalisation</h3><p>A welcome for new patients. A familiar hello for returning ones. DrKing checks your CRM and tailors the message.</p>",
 "c3": "<h3>Booking by SMS</h3><p>Turn a quick reply into a booking request. Direct booking into Core Practice is planned.</p>",
 "c4": "<h3>Patient Details in Your CRM</h3><p>Patient details and booking information flow into your CRM, so your team has the context when they need it.</p>",
 "c5": "<h3>After-hours Coverage</h3><p>Evenings, weekends and public holidays. Missed callers get the same automatic text-back, 24/7.</p><a class=\"text-link\" href=\"/after-hours\">Explore after-hours care <span aria-hidden=\"true\">↗</span></a>",
 "c6": "<h3>Reminders That Reduce No-Shows</h3><p>SMS reminders before each appointment help patients keep the time they booked — fewer gaps, less chasing.</p>",
 "ctxstat": '<div class="context-number">24/7</div><p>coverage. Every DrKing tool works alongside Core Practice today.</p><span class="source">Direct Core Practice integration is planned</span>',
 "ctxcopy": "<div class=\"eyebrow\">Made for dental practices</div><h2>Core Practice.<br>Easier to reach.</h2><p>When someone calls your clinic, they're ready to take the next step. Missed call text-back helps Australian clinics keep that conversation going — and gives patients one less reason to call somewhere else.</p><div class=\"related\"><a href=\"/dentists\">For dental clinics <span aria-hidden=\"true\">↗</span></a><a href=\"/general-practice\">For general practice <span aria-hidden=\"true\">↗</span></a></div>",
 "faqeyebrow": '<div class="eyebrow">Good questions about Core Practice + DrKing</div>',
 "faqs": "<details open><summary>How fast is the text-back?</summary><p>Straight away. The patient gets a personalised SMS automatically after a missed call.</p></details><details><summary>Can the patient book via SMS?</summary><p>Yes. The patient replies with their preferred time, and DrKing AI books it, depending on your calendar or practice software setup.</p></details><details><summary>Does it work after hours?</summary><p>Yes. Missed call recovery operates 24/7. After-hours callers get the same automatic text-back.</p></details><details><summary>Can it tell new and existing patients apart?</summary><p>Yes. DrKing checks your CRM and personalises the message accordingly.</p></details><details><summary>What about spam calls?</summary><p>DrKing AI screens and filters spam numbers. No text-back sent to known spam.</p></details>",
 "ctaeyebrow": '<div class="eyebrow">Your next patient is calling</div>',
 "ctah2": "<h2>Don't let a missed call<br>be a <em>missed connection.</em></h2>",
 "ctap": "<p>See how DrKing helps fill your Core Practice calendar — even when your team is busy.</p>",
 "ctastory": '<a href="/missed-call-text-ai" style="color:var(--teal)">Read the story: the call you missed, the conversation you didn&#8217;t &#8594;</a>',
 "ctamicro": '<div class="micro">Works alongside Core Practice today.</div>',
}

def faq_html(faqs):
    out = []
    for i, (q, a) in enumerate(faqs):
        out.append(f"<details{' open' if i == 0 else ''}><summary>{q}</summary><p>{a}</p></details>")
    return "".join(out)

def stats_html(stats):
    return "".join(f'<div class="stat"><div class="stat-value">{v}<span>{u}</span></div><div class="stat-label">{l}</div></div>' for v, u, l in stats)

ARROW = ' <span aria-hidden="true">↗</span>'

PAGES = {
"best-practice-integration": dict(
 name="Best Practice", product="Bp Premier",
 title="Best Practice Software + AI Receptionist | DrKing",
 meta="Use DrKing alongside Best Practice software today: AI receptionist, web chat, booking requests and SMS reminders for GPs. No integration yet — waitlist open.",
 eyebrow="Best Practice software + DrKing",
 h1="Best Practice.<br>Use DrKing <em>today.</em>",
 lede="If your GP practice runs Best Practice software (Bp Premier), you can use DrKing’s AI receptionist, web chat, online booking requests and SMS reminders alongside it today. There’s no Best Practice integration yet — the waitlist is open.",
 micro="Best Practice integration: waitlist open. Toolkit available today.",
 artlabel="Example: a missed call during the morning rush gets a text-back. The patient asks for a repeat script and the request is passed to the practice team.",
 f1=("Missed call", "Morning rush · 8:47 am"), time="8:49",
 head=("Elmwood Family Medical", "SMS · powered by DrKing"), chattime="Today 8:49 am",
 bubbles=["Hi Priya, sorry we missed your call. How can we help today?",
          "Can I get my script repeated?",
          "I’ve sent that to our team to check with your GP.",
          "Great, thanks!"],
 inputtxt="Text message", speed="Toolkit today.<br>Waitlist open.",
 f2=("Sent to the team", "Repeat script · staff to follow up"),
 caption="Illustrative conversation. Not a screenshot of Bp Premier.",
 statsaria="DrKing alongside Best Practice at a glance",
 stats=[("1", " inbox", "Calls, chat and SMS for the front desk"), ("AI", " voice", "Routine calls answered, day or night"), ("Auto", " SMS", "Text-back when the lines are busy"), ("24", "/7", "Web chat and booking requests")],
 howhead=("The 8:30 am phone rush", "Three steps. Less pressure on reception.", "How DrKing supports a Best Practice front desk while your phones are flat out."),
 steps=[("Enquiry lands.", "A call, text or web chat comes in while every line is busy. DrKing answers or texts back.", "Phone, SMS or web chat"),
        ("Routine handled.", "Opening hours, new-patient questions and booking requests are answered by the AI receptionist.", "Routine enquiries"),
        ("Staff take the rest.", "Repeat-script, referral and results questions go to your team, who book in Bp Premier as usual.", "No integration yet")],
 feathead=("Everything your front desk needs.", "Routine enquiries,<br>off the phones.", "Standalone DrKing tools that run next to Best Practice — no connection required.", "/ai-voice-receptionist", "Explore the AI voice receptionist"),
 cards=[("AI Receptionist", "Answers routine GP calls — hours, location, new-patient questions — and passes everything else to staff.", None),
        ("AI Web Chat", "Patients on your website get quick answers and can leave a booking request any time.", None),
        ("Online Booking Requests", "Patients choose a preferred time. Your team confirms it in Bp Premier, since there’s no sync yet.", ("/online-booking", "Explore online booking")),
        ("One Inbox", "Calls, chat, SMS and email conversations sit in one DrKing inbox, so nothing is scattered.", None),
        ("Missed-call Text-back", "When reception can’t pick up, the caller gets a text so they can reply instead of redialling.", None),
        ("SMS Reminders", "Appointment reminders sent from DrKing help patients remember the time they booked.", ("/appointment-reminders", "Explore reminders"))],
 ctxstat=("Today", "DrKing tools work alongside Best Practice. No integration yet.", "Status: waitlist open"),
 ctxcopy=("Made for general practice", "Bp Premier.<br>Clear boundaries.", "DrKing handles routine GP enquiries. Repeat-script, referral and results questions are routed to your staff with the details collected. Urgent or clinical concerns go to the practice team, and patients are told to call 000 in an emergency. DrKing gives no clinical advice."),
 faqeyebrow="Good questions about Best Practice + DrKing",
 faqs=[("Does DrKing integrate with Best Practice?", "Not yet. There’s no Best Practice integration today, and DrKing doesn’t read or write your Bp Premier appointment book or patient records. The waitlist is open on our integrations page."),
       ("Can I use DrKing alongside Bp Premier today?", "Yes. The AI receptionist, web chat, online booking requests, SMS reminders, missed-call text-back and one inbox all run as standalone tools. Your team confirms bookings in Bp Premier as usual."),
       ("What happens with repeat-script requests?", "DrKing collects the patient’s details and routes the request to your staff. It doesn’t give clinical advice or approve scripts — your practice decides how each request is handled."),
       ("What about urgent or emergency calls?", "Urgent or clinical concerns are passed to your practice team. In an emergency, patients are told to call 000."),
       ("How do I join the waitlist?", "Register on the integrations page. Waitlist interest helps us decide which practice software to prioritise; it isn’t a promised date.")],
 cta=("Busy phones, calmer reception", "Keep Best Practice.<br>Add a <em>helping hand.</em>", "See how DrKing works alongside Best Practice today — and join the waitlist for a future integration.", "Join the Best Practice waitlist on our integrations page", "No Best Practice integration yet. Waitlist open."),
 swname="DrKing AI Receptionist for Best Practice users",
 swdesc="Standalone DrKing tools for GP practices that use Best Practice software: AI receptionist, web chat, online booking requests, SMS reminders, missed-call text-back and one inbox. No Best Practice integration yet; waitlist open.",
),
"medicaldirector-integration": dict(
 name="MedicalDirector", product="MedicalDirector",
 title="MedicalDirector + AI Receptionist for GPs | DrKing",
 meta="Run DrKing’s AI receptionist, web chat and SMS reminders alongside MedicalDirector today. No MedicalDirector integration yet — join the waitlist.",
 eyebrow="MedicalDirector + DrKing",
 h1="Keep your PMS.<br>Add <em>DrKing.</em>",
 lede="If your GP practice uses MedicalDirector, DrKing’s AI receptionist, web chat, online booking requests and SMS reminders can run alongside it today. There’s no MedicalDirector integration yet — the waitlist is open.",
 micro="MedicalDirector integration: waitlist open. Toolkit available today.",
 artlabel="Example: an evening web chat where a patient asks about blood test results. The question goes to the practice team and a follow-up booking request is logged.",
 f1=("After-hours chat", "Web chat · 7:15 pm"), time="7:15",
 head=("Harbourside Medical", "Web chat · powered by DrKing"), chattime="Tonight 7:15 pm",
 bubbles=["Hi Tom, thanks for messaging Harbourside Medical. How can we help?",
          "Are my blood results back?",
          "Your GP covers results, so I’ve told our team. Book a follow-up?",
          "Yes, Monday morning"],
 inputtxt="Type a message", speed="Toolkit today.<br>Waitlist open.",
 f2=("Booking request in", "Mon am · Dr Nguyen · to confirm"),
 caption="Illustrative conversation. Not a screenshot of MedicalDirector.",
 statsaria="DrKing alongside MedicalDirector at a glance",
 stats=[("24", "/7", "Web chat when the practice is closed"), ("1", " inbox", "Every enquiry ready for the morning"), ("AI", " voice", "Routine calls answered for the desk"), ("2-way", " SMS", "Reminders patients can reply to")],
 howhead=("When the practice is closed", "Three steps. A clear inbox by morning.", "How DrKing handles after-hours GP enquiries next to MedicalDirector."),
 steps=[("Question after hours.", "A patient messages via web chat or SMS in the evening, when reception has gone home.", "Evenings and weekends"),
        ("AI answers or routes.", "Routine questions get an answer. Results, referral and script questions are flagged for staff.", "Clear triage boundaries"),
        ("Team follows up.", "Next morning, staff see each request in one inbox and book in MedicalDirector themselves.", "No integration yet")],
 feathead=("Everything your front desk needs.", "After-hours questions,<br>sorted by morning.", "Standalone DrKing tools for GP practices on MedicalDirector — nothing to connect.", "/ai-voice-receptionist", "Explore the AI voice receptionist"),
 cards=[("AI Web Chat", "Answers common questions on your website after hours and collects booking requests for staff.", None),
        ("AI Receptionist", "Picks up routine calls about hours, location and new patients, and hands off anything clinical.", None),
        ("One Inbox", "Overnight chats, texts and calls are waiting in one place when reception opens.", None),
        ("Online Booking Requests", "Patients request a time online. Staff confirm it in MedicalDirector — there’s no sync.", ("/online-booking", "Explore online booking")),
        ("SMS Reminders", "Reminder texts from DrKing help patients keep their appointment, and they can reply.", ("/appointment-reminders", "Explore reminders")),
        ("Missed-call Text-back", "Calls missed during a busy session get a text so the patient can reply in their own time.", None)],
 ctxstat=("Today", "DrKing tools work alongside MedicalDirector. No integration yet.", "Status: waitlist open"),
 ctxcopy=("Made for general practice", "Results questions.<br>Routed to staff.", "DrKing never interprets results or gives clinical advice. Results, referral and repeat-script questions are passed to your team with the patient’s message. Urgent or clinical concerns go to the practice team, and patients are told to call 000 in an emergency."),
 faqeyebrow="Good questions about MedicalDirector + DrKing",
 faqs=[("Does DrKing integrate with MedicalDirector?", "Not yet. There’s no MedicalDirector integration today, and DrKing doesn’t read or write your appointment book or patient records. The waitlist is open on our integrations page."),
       ("Which MedicalDirector product does it work with?", "DrKing runs as standalone tools, so it can sit alongside whichever MedicalDirector product your practice uses. There’s no connection to either your clinical or practice management software."),
       ("Can patients ask about results after hours?", "They can ask, but DrKing won’t discuss results. It routes the question to your staff and can log a follow-up booking request for the team to confirm."),
       ("What about urgent or emergency messages?", "Urgent or clinical concerns are passed to your practice team. In an emergency, patients are told to call 000."),
       ("How do I join the waitlist?", "Register on the integrations page. Waitlist interest helps us decide which practice software to prioritise; it isn’t a promised date.")],
 cta=("Closed for the night, still reachable", "Keep MedicalDirector.<br>Add <em>after-hours help.</em>", "See how DrKing works alongside MedicalDirector today — and join the waitlist for a future integration.", "Join the MedicalDirector waitlist on our integrations page", "No MedicalDirector integration yet. Waitlist open."),
 swname="DrKing AI Receptionist for MedicalDirector users",
 swdesc="Standalone DrKing tools for GP practices that use MedicalDirector: AI web chat, AI receptionist, online booking requests, SMS reminders, missed-call text-back and one inbox. No MedicalDirector integration yet; waitlist open.",
),
"zedmed-integration": dict(
 name="Zedmed", product="Zedmed",
 title="Zedmed + AI Receptionist for GP Practices | DrKing",
 meta="GP practices on Zedmed can use DrKing’s AI receptionist, missed-call text-back and online booking requests today. No Zedmed integration yet — waitlist open.",
 eyebrow="Zedmed + DrKing for GP practices",
 h1="Zedmed.<br>Plus <em>DrKing, today.</em>",
 lede="If your GP practice runs on Zedmed, you can add DrKing’s AI receptionist, missed-call text-back, online booking requests and SMS reminders alongside it today. There’s no Zedmed integration yet — the waitlist is open.",
 micro="Zedmed integration: waitlist open. Toolkit available today.",
 artlabel="Example: the AI receptionist answers a lunchtime call, then texts a new patient a booking link and flags their referral question for staff.",
 f1=("Call answered", "AI receptionist · 12:10 pm"), time="12:14",
 head=("Kestrel Street Clinic", "SMS · powered by DrKing"), chattime="Today 12:14 pm",
 bubbles=["Hi Grace, thanks for calling. Here’s our new-patient booking link.",
          "Can I get a physio referral too?",
          "Referrals need your GP, so I’ve flagged it for our team.",
          "Great, thank you"],
 inputtxt="Text message", speed="Toolkit today.<br>Waitlist open.",
 f2=("New patient request", "Referral query · flagged for staff"),
 caption="Illustrative conversation. Not a screenshot of Zedmed.",
 statsaria="DrKing alongside Zedmed at a glance",
 stats=[("AI", " voice", "Lunchtime and overflow calls answered"), ("Auto", " SMS", "Text-back after a missed call"), ("1", " inbox", "Calls, SMS, chat and email together"), ("24", "/7", "Online booking requests")],
 howhead=("Lunch breaks and new patients", "Three steps. Fewer callbacks for staff.", "How DrKing covers calls for a Zedmed practice when the desk is short-staffed."),
 steps=[("Call answered.", "Reception is on a break or another line. The AI receptionist picks up routine calls.", "AI voice receptionist"),
        ("Link sent.", "New patients get a text with your online booking request link, so they can choose a time.", "Online booking requests"),
        ("Flagged for staff.", "Referral, script and results questions are flagged. Staff enter bookings in Zedmed.", "No integration yet")],
 feathead=("Everything your front desk needs.", "Cover for the desk,<br>without the hold music.", "Standalone DrKing tools that work next to Zedmed — no connection required.", "/ai-voice-receptionist", "Explore the AI voice receptionist"),
 cards=[("AI Receptionist", "Answers routine calls when staff are busy and sends a summary of each call to the inbox.", None),
        ("Missed-call Text-back", "If a call still slips through, DrKing texts the caller so they can reply instead of waiting on hold.", None),
        ("Online Booking Requests", "New and returning patients request a time. Your team confirms it in Zedmed — no sync yet.", ("/online-booking", "Explore online booking")),
        ("AI Web Chat", "Website visitors can ask about services and opening hours and leave their details.", None),
        ("One Inbox", "Call summaries, SMS, web chat and email in one DrKing inbox for the whole front desk.", None),
        ("SMS Reminders", "Reminders from DrKing help patients turn up for the time they requested.", ("/appointment-reminders", "Explore reminders"))],
 ctxstat=("Today", "DrKing tools work alongside Zedmed. No integration yet.", "Status: waitlist open"),
 ctxcopy=("Made for general practice", "Routine calls.<br>Safe handovers.", "The AI receptionist handles routine questions and booking requests. Referral, repeat-script and results questions are flagged for staff with the caller’s details. Urgent or clinical concerns go to the practice team, and callers are told to call 000 in an emergency. No clinical advice is given."),
 faqeyebrow="Good questions about Zedmed + DrKing",
 faqs=[("Does DrKing integrate with Zedmed?", "Not yet. There’s no Zedmed integration today, and DrKing doesn’t read or write your Zedmed appointment book or patient records. The waitlist is open on our integrations page."),
       ("Can DrKing book straight into Zedmed?", "No. Patients send booking requests through DrKing, and your team enters the appointment in Zedmed. DrKing’s tools work as standalone tools until an integration exists."),
       ("What happens with referral requests?", "DrKing takes the caller’s details and flags the request for your staff. It doesn’t decide on referrals or give clinical advice — your GPs and team do."),
       ("What about urgent or emergency calls?", "Urgent or clinical concerns are passed to your practice team. In an emergency, callers are told to call 000."),
       ("How do I join the waitlist?", "Register on the integrations page. Waitlist interest helps us decide which practice software to prioritise; it isn’t a promised date.")],
 cta=("Short-staffed at lunch?", "Keep Zedmed.<br>Add a <em>calm front desk.</em>", "See how DrKing works alongside Zedmed today — and join the waitlist for a future integration.", "Join the Zedmed waitlist on our integrations page", "No Zedmed integration yet. Waitlist open."),
 swname="DrKing AI Receptionist for Zedmed users",
 swdesc="Standalone DrKing tools for GP practices that use Zedmed: AI receptionist, missed-call text-back, online booking requests, web chat, SMS reminders and one inbox. No Zedmed integration yet; waitlist open.",
),
}

def build(slug, P):
    url = f"https://drking.ai/{slug}"
    N = {}
    N["doctype"] = "<!DOCTYPE html>"
    N["title"] = f"<title>{P['title']}</title>"
    N["meta"] = f'<meta name="description" content="{P["meta"]}">'
    N["canon"] = f'<link rel="canonical" href="{url}">'
    N["og"] = f'<meta property="og:title" content="{P["title"]}"><meta property="og:description" content="{P["meta"]}">'
    N["ogurl"] = f'<meta property="og:url" content="{url}">'
    N["crumb"] = f'<a href="/integrations">Integrations</a><span aria-hidden="true">/</span><span aria-current="page">{P["name"]}</span>'
    N["eyebrow"] = f'<div class="eyebrow">{P["eyebrow"]}</div>'
    N["h1"] = f'<h1 id="hero-title">{P["h1"]}</h1>'
    N["lede"] = f"<p>{P['lede']}</p>"
    N["micro"] = P["micro"] + "</div>"
    N["artlabel"] = f'aria-label="{P["artlabel"]}"'
    N["f1"] = f"<strong>{P['f1'][0]}</strong><small>{P['f1'][1]}</small>"
    N["time"] = f"<span>{P['time']}</span>"
    N["head"] = f"{P['head'][0]}<small>{P['head'][1]}</small>"
    N["chattime"] = f'<div class="chat-time">{P["chattime"]}</div>'
    for i, cls in enumerate(["bubble", "bubble reply", "bubble", "bubble reply"]):
        N[f"b{i+1}"] = f'<div class="{cls}">{P["bubbles"][i]}</div>'
    N["input"] = f'<div class="chat-input">{P["inputtxt"]} <span>↑</span></div>'
    N["speed"] = P["speed"]
    N["f2"] = f"<strong>{P['f2'][0]}</strong><small>{P['f2'][1]}</small>"
    N["caption"] = f'<span class="art-caption">{P["caption"]}</span>'
    N["statsaria"] = f'aria-label="{P["statsaria"]}"'
    N["stats"] = stats_html(P["stats"])
    e, h, p = P["howhead"]
    N["howhead"] = f'<div class="eyebrow">{e}</div><h2>{h}</h2><p>{p}</p>'
    for i, (h3, p, lab) in enumerate(P["steps"]):
        N[f"s{i+1}"] = f'<h3>{h3}</h3><p>{p}</p><span class="small-label">{lab}</span>'
    e, h, p, href, lt = P["feathead"]
    N["feathead"] = f'<div class="eyebrow">{e}</div><h2>{h}</h2><p>{p}</p><a class="text-link feature-link" href="{href}">{lt}{ARROW}</a>'
    for i, (h3, p, link) in enumerate(P["cards"]):
        extra = f'<a class="text-link" href="{link[0]}">{link[1]}{ARROW}</a>' if link else ""
        N[f"c{i+1}"] = f"<h3>{h3}</h3><p>{p}</p>{extra}"
    n, p, s = P["ctxstat"]
    N["ctxstat"] = f'<div class="context-number">{n}</div><p>{p}</p><span class="source">{s}</span>'
    e, h, p = P["ctxcopy"]
    N["ctxcopy"] = (f'<div class="eyebrow">{e}</div><h2>{h}</h2><p>{p}</p><div class="related">'
                    f'<a href="/general-practice">For general practice{ARROW}</a><a href="/medical-centres">For medical centres{ARROW}</a></div>')
    N["faqeyebrow"] = f'<div class="eyebrow">{P["faqeyebrow"]}</div>'
    N["faqs"] = faq_html(P["faqs"])
    e, h, p, story, micro = P["cta"]
    N["ctaeyebrow"] = f'<div class="eyebrow">{e}</div>'
    N["ctah2"] = f"<h2>{h}</h2>"
    N["ctap"] = f"<p>{p}</p>"
    N["ctastory"] = f'<a href="/integrations#waitlist" style="color:var(--teal)">{story} →</a>'
    N["ctamicro"] = f'<div class="micro">{micro}</div>'

    out = src
    n = 0
    for k, old in O.items():
        c = out.count(old)
        assert c >= 1, f"{slug}: MISSING old string for {k!r}"
        out = out.replace(old, N[k], 1)
        n += 1
    # JSON-LD
    m = re.search(r'<script type="application/ld\+json" id="structured-data">(.*?)</script>', out, re.S)
    old_ld = m.group(1)
    g = json.loads(old_ld)
    for node in g["@graph"]:
        t = node.get("@type")
        if t == "WebPage":
            node.update({"@id": url + "#webpage", "url": url, "name": P["title"], "description": P["meta"]})
        elif t == "SoftwareApplication":
            node.update({"name": P["swname"], "url": url, "description": P["swdesc"],
                         "featureList": [c[0] for c in P["cards"]]})
        elif t == "BreadcrumbList":
            node["itemListElement"] = [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://drking.ai/"},
                {"@type": "ListItem", "position": 2, "name": "Integrations", "item": "https://drking.ai/integrations"},
                {"@type": "ListItem", "position": 3, "name": P["name"], "item": url}]
        elif t == "FAQPage":
            node["mainEntity"] = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faqs"]]
    new_ld = json.dumps(g, ensure_ascii=False, separators=(",", ":"))
    assert out.count(old_ld) == 1
    out = out.replace(old_ld, new_ld, 1); n += 1
    # checks
    assert len(P["title"]) <= 60, (slug, len(P["title"]))
    assert 70 <= len(P["meta"]) <= 160, (slug, len(P["meta"]))
    for bad in ["Riverbend", "Kate", "Dr Lee", "Sam", "core-practice-integration\"", "roadmap"]:
        assert bad not in out.split('<footer')[0], (slug, bad)
    cp = out.count("Core Practice")
    assert cp == 1, (slug, "Core Practice left", cp)  # shared footer link only
    path = os.path.join(REPO, slug + ".html")
    assert not os.path.exists(path) or "--force" in sys.argv, f"{path} exists"
    open(path, "w", encoding="utf-8").write(out)
    print(f"{slug}.html: {n} replacements; title {len(P['title'])}c; meta {len(P['meta'])}c")

for slug, P in PAGES.items():
    build(slug, P)
