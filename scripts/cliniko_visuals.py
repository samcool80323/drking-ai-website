"""Cliniko hero visual: organic blob + HTML conversation, matching homepage design."""


def cliniko_hero():
    """HTML composition using the homepage's organic SVG + styled chat elements."""
    return '''<div class="cliniko-visual" aria-label="Example: DrKing turns a Saturday morning missed call into a confirmed Monday appointment in the Cliniko calendar." role="img">
<svg class="cv-organism" viewBox="0 0 600 590" aria-hidden="true"><g class="outer"><path fill="#E4EADF" d="M306 40C378 20 455 77 476 140C500 211 580 218 567 308C554 398 487 401 451 466C415 531 330 563 261 525C191 487 124 529 76 461C27 392 63 330 59 261C54 190 86 117 158 108C229 99 235 59 306 40Z"/><path fill="#A8C5B5" d="M313 101C365 61 435 122 445 185C455 248 525 278 478 345C431 412 413 471 339 468C265 465 243 415 177 409C111 403 101 326 135 272C169 218 153 169 215 154C265 142 277 128 313 101Z" opacity=".35"/><path fill="#0D5C5C" d="M284 165C317 122 380 152 390 204C400 256 448 272 421 321C395 370 358 372 333 410C308 448 240 452 212 415C184 378 148 355 152 310C156 265 132 224 158 190C184 156 251 208 284 165Z" opacity=".08"/></g></svg>

<div class="cv-hand-note">Saturday morning.<br>Nobody at the desk.<svg viewBox="0 0 70 55" aria-hidden="true"><path d="M9 3C39-3 61 18 42 45m-5-13 5 15 14-5" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg></div>

<div class="cv-conversation">
  <div class="cv-msg">
    <div class="cv-msg-head"><span class="cv-mini-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M21 11a9 9 0 0 1-9 9H4l-3 2 2-6a9 9 0 1 1 18-5Z"/><path d="M7 10h10M7 14h6"/></svg></span>New patient enquiry <span class="cv-time">8:42 am</span></div>
    <p>Hi, I hurt my hamstring running.
Can I book for Monday morning?</p>
  </div>
  <div class="cv-reply">
    <span class="cv-reply-label"><svg width="12" height="12" viewBox="0 0 40 40" aria-hidden="true"><path d="M20 1C23 13 27 17 39 20C27 23 23 27 20 39C17 27 13 23 1 20C13 17 17 13 20 1Z" fill="currentColor"/></svg>DrKing · always here</span>
    Of course. Monday 9:00 am is available
with Sarah. Shall I save you a spot?
    <span class="cv-reply-time">Delivered in seconds &#10003;&#10003;</span>
  </div>
</div>

<div class="cv-booking">
  <span class="cv-booking-check"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg></span>
  <div><strong>Booked in Cliniko.</strong><small>Mon 9:00 am · Sarah · Initial consult</small></div>
</div>

<div class="cv-caption"><span class="cv-live-dot"></span>YOUR PATIENTS. ALWAYS HEARD.</div>
</div>'''


def cliniko_usecase():
    """Same composition reused as the secondary visual."""
    return cliniko_hero()