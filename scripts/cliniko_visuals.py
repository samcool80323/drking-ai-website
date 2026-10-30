"""Premium SVG illustrations for the Cliniko integration page.

Two original pieces: a hero showing the integration flow as an organic
scene, and a use-case moment showing the Saturday-morning sports injury.
Both drawn in DrKing's observed brand palette with layered depth.
"""
from html import escape


def cliniko_hero():
    """The connected practice: missed call flows through DrKing AI into Cliniko."""
    return '''<figure class="article-figure hero-figure cliniko-hero" role="img" aria-label="Illustration of a physiotherapy practice integration: a missed call from a Saturday morning patient flows through DrKing AI as a conversation stream and arrives as a confirmed Monday appointment in the Cliniko calendar. A treatment-room scene with a therapist and patient sits in the background.">
<svg viewBox="0 0 560 520" xmlns="http://www.w3.org/2000/svg" role="img">
<defs>
<linearGradient id="ck-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ecebe3"/><stop offset="1" stop-color="#f7f5f2"/></linearGradient>
<linearGradient id="ck-flow" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c8553d" stop-opacity=".7"/><stop offset=".5" stop-color="#0d5c5c" stop-opacity=".6"/><stop offset="1" stop-color="#0d5c5c" stop-opacity=".9"/></linearGradient>
<filter id="ck-soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#1c1814" flood-opacity=".06"/></filter>
</defs>

<rect width="560" height="520" rx="28" fill="url(#ck-bg)"/>

<!-- organic background: sage blob top-right -->
<path d="M320 -10 C 380 30, 460 20, 540 60 C 560 80, 550 140, 560 160 L 560 0 Z" fill="#a8c5b5" opacity=".1"/>
<!-- terracotta wash bottom-left -->
<path d="M-10 380 C 80 420, 160 390, 240 410 C 320 430, 400 400, 560 420 L 560 520 L 0 520 Z" fill="#c8553d" opacity=".04"/>
<!-- ground wave -->
<path d="M0 470 C 120 490, 220 460, 320 480 C 420 500, 500 470, 560 480 L 560 520 L 0 520 Z" fill="#a8c5b5" opacity=".08"/>

<!-- treatment room silhouette (background, very subtle) -->
<g opacity=".07" fill="#1c1814">
  <rect x="330" y="130" width="90" height="6" rx="3"/>
  <rect x="330" y="130" width="6" height="60" rx="3"/>
  <rect x="414" y="130" width="6" height="60" rx="3"/>
  <rect x="330" y="190" width="90" height="5" rx="2.5"/>
  <ellipse cx="375" cy="215" rx="50" ry="14"/>
</g>

<!-- ===== LEFT: the missed call ===== -->
<g transform="translate(28,110)" filter="url(#ck-soft)">
  <rect x="0" y="0" width="128" height="210" rx="24" fill="#fffdf9" stroke="#dcd9d0" stroke-width="1.5"/>
  <rect x="0" y="0" width="128" height="42" rx="24" fill="#0d5c5c"/>
  <rect x="0" y="21" width="128" height="21" fill="#0d5c5c"/>
  <text x="64" y="27" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10" letter-spacing="1" fill="#f2ede4">YOUR PATIENT</text>
  <circle cx="64" cy="74" r="22" fill="#c8553d" opacity=".1"/>
  <circle cx="64" cy="74" r="16" fill="#c8553d" opacity=".15"/>
  <circle cx="64" cy="74" r="11" fill="#c8553d"/>
  <path d="M59 74l3.5 3.5L69 70" stroke="#fffdf9" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="64" y="106" text-anchor="middle" font-family="Newsreader,serif" font-size="15" fill="#1c1814">Missed call</text>
  <text x="64" y="124" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10.5" fill="#716f66">Sat &#183; 8:42 am</text>
  <text x="64" y="140" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10.5" fill="#716f66">New patient</text>
  <line x1="30" y1="158" x2="98" y2="158" stroke="#e5e2d9" stroke-width="1"/>
  <text x="64" y="178" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#8a887f">Ready to book,</text>
  <text x="64" y="192" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9" fill="#8a887f">nobody to answer</text>
</g>

<!-- ===== flow: phone to AI ===== -->
<g stroke="url(#ck-flow)" stroke-width="2" fill="none">
  <path d="M162 195 C 180 185, 195 178, 210 172" stroke-dasharray="1 9" stroke-linecap="round"/>
  <path d="M162 210 C 180 205, 195 200, 210 195" stroke-dasharray="1 9" stroke-linecap="round" opacity=".6"/>
  <path d="M162 225 C 182 222, 198 220, 210 218" stroke-dasharray="1 9" stroke-linecap="round" opacity=".3"/>
</g>
<!-- terracotta pulse dot -->
<circle cx="165" cy="195" r="3.5" fill="#c8553d"/>
<circle cx="165" cy="195" r="7" fill="none" stroke="#c8553d" stroke-width="1" opacity=".4"/>

<!-- ===== CENTER: DrKing AI as conversation stream ===== -->
<g transform="translate(210,82)">
  <rect x="0" y="0" width="140" height="290" rx="26" fill="#0d5c5c" filter="url(#ck-soft)"/>
  <rect x="0" y="0" width="140" height="290" rx="26" fill="none" stroke="#093f3f" stroke-width="1"/>
  <!-- wordmark -->
  <text x="70" y="36" text-anchor="middle" font-family="Newsreader,serif" font-size="17" fill="#f2ede4">drking<span fill="#c8553d">.</span></text>

  <!-- conversation wave inside -->
  <g stroke="#aed5c9" stroke-width="1.5" fill="none" opacity=".5">
    <path d="M18 62 C 35 55, 55 58, 72 65 C 89 72, 105 70, 122 62"/>
    <path d="M18 76 C 38 70, 58 73, 75 79 C 92 85, 108 82, 122 76" opacity=".7"/>
    <path d="M18 90 C 40 85, 60 88, 77 93 C 94 98, 110 95, 122 90" opacity=".5"/>
  </g>

  <!-- three beats: answers / books / confirms -->
  <g font-family="Geomanist,sans-serif" font-size="9.5">
    <rect x="22" y="110" width="96" height="26" rx="13" fill="#104c4c"/>
    <text x="70" y="127" text-anchor="middle" fill="#aed5c9">answers warmly</text>
    <rect x="22" y="148" width="96" height="26" rx="13" fill="#104c4c"/>
    <text x="70" y="165" text-anchor="middle" fill="#aed5c9">books the slot</text>
    <rect x="22" y="186" width="96" height="26" rx="13" fill="#104c4c"/>
    <text x="70" y="203" text-anchor="middle" fill="#aed5c9">confirms by SMS</text>
  </g>

  <!-- result card inside AI block -->
  <g transform="translate(22,232)">
    <rect x="0" y="0" width="96" height="42" rx="12" fill="#f3f5ef"/>
    <circle cx="18" cy="21" r="8" fill="#0d5c5c"/>
    <path d="M14 21l2.5 2.5L22 17" stroke="#f3f5ef" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="34" y="18" font-family="Geomanist,sans-serif" font-size="8.5" font-weight="600" fill="#17483e">Mon 9:00 am</text>
    <text x="34" y="30" font-family="Geomanist,sans-serif" font-size="7.5" fill="#344d45">Initial consult &#183; 45 min</text>
  </g>
</g>

<!-- ===== flow: AI to Cliniko ===== -->
<g stroke="#0d5c5c" stroke-width="2" fill="none" opacity=".55">
  <path d="M358 195 C 374 185, 388 178, 402 172" stroke-dasharray="1 9" stroke-linecap="round"/>
  <path d="M358 210 C 374 205, 388 200, 402 195" stroke-dasharray="1 9" stroke-linecap="round" opacity=".6"/>
  <path d="M358 225 C 376 222, 390 220, 402 218" stroke-dasharray="1 9" stroke-linecap="round" opacity=".3"/>
</g>
<circle cx="360" cy="195" r="3.5" fill="#0d5c5c"/>
<circle cx="360" cy="195" r="7" fill="none" stroke="#0d5c5c" stroke-width="1" opacity=".4"/>

<!-- ===== RIGHT: Cliniko calendar ===== -->
<g transform="translate(402,110)" filter="url(#ck-soft)">
  <rect x="0" y="0" width="130" height="210" rx="22" fill="#fffdf9" stroke="#a8c5b5" stroke-width="2"/>
  <!-- header -->
  <rect x="0" y="0" width="130" height="46" rx="22" fill="#e3eae3"/>
  <rect x="0" y="23" width="130" height="23" fill="#e3eae3"/>
  <text x="65" y="18" text-anchor="middle" font-family="Newsreader,serif" font-size="13" fill="#17483e">Cliniko</text>
  <text x="65" y="36" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="8.5" fill="#344d45">Monday &#183; next week</text>
  <!-- calendar slots -->
  <g font-family="Geomanist,sans-serif" font-size="9">
    <rect x="16" y="58" width="98" height="26" rx="8" fill="#f0ede5" stroke="#e0ddd4" stroke-width="1"/>
    <text x="28" y="75" fill="#8a887f">8:00 am</text>
    <text x="90" y="75" fill="#b5b3aa" text-anchor="middle" font-size="8">booked</text>
    <rect x="16" y="92" width="98" height="26" rx="8" fill="#e3eae3" stroke="#a8c5b5" stroke-width="1.5"/>
    <text x="28" y="109" fill="#17483e" font-weight="600">9:00 am</text>
    <circle cx="90" cy="105" r="7" fill="#0d5c5c"/>
    <path d="M87 105l2 2 4-4" stroke="#f3f5ef" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="16" y="126" width="98" height="26" rx="8" fill="#f0ede5" stroke="#e0ddd4" stroke-width="1"/>
    <text x="28" y="143" fill="#8a887f">10:00 am</text>
    <text x="90" y="143" fill="#b5b3aa" text-anchor="middle" font-size="8">open</text>
  </g>
  <!-- new booking badge -->
  <g transform="translate(16,164)">
    <rect x="0" y="0" width="98" height="34" rx="10" fill="#0d5c5c"/>
    <text x="49" y="15" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="8" font-weight="600" fill="#f3f5ef">NEW BOOKING</text>
    <text x="49" y="27" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="7.5" fill="#aed5c9">via DrKing text-back</text>
  </g>
</g>

<!-- caption strip -->
<g transform="translate(140,478)">
  <rect x="0" y="0" width="280" height="32" rx="16" fill="#0d5c5c" opacity=".9"/>
  <text x="140" y="20" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10.5" fill="#f2ede4">Missed Saturday &#8594; booked Monday. No gap in between.</text>
</g>
</svg>
<figcaption>The full journey: your patient calls on a Saturday morning, DrKing AI handles the conversation, and a confirmed appointment arrives in your Cliniko calendar. Illustrative, not a screenshot of Cliniko.</figcaption>
</figure>'''


def cliniko_usecase():
    """Saturday morning: a runner tweaks a hamstring, DrKing catches the call."""
    return '''<figure class="article-figure secondary-figure" role="img" aria-label="Illustration of the Saturday-morning use case: a runner with a hamstring injury calls the practice at 8:42 am while the team is unavailable. DrKing AI answers, offers Monday morning availability, and the new patient is booked before they finish their coffee.">
<svg viewBox="0 0 560 260" xmlns="http://www.w3.org/2000/svg" role="img">
<defs>
<linearGradient id="ck-uc-bg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ecebe3"/><stop offset="1" stop-color="#e9eade"/></linearGradient>
</defs>
<rect width="560" height="260" rx="24" fill="url(#ck-uc-bg)"/>
<path d="M0 220 C 100 240, 200 210, 300 230 C 400 250, 480 220, 560 230 L 560 260 L 0 260 Z" fill="#a8c5b5" opacity=".07"/>

<!-- runner silhouette (abstract, terracotta) -->
<g transform="translate(40,50)" opacity=".8">
  <circle cx="32" cy="18" r="10" fill="none" stroke="#c8553d" stroke-width="2"/>
  <path d="M32 28 C 30 40, 28 52, 32 62 C 34 70, 38 76, 44 80" stroke="#c8553d" stroke-width="2" fill="none" stroke-linecap="round"/>
  <path d="M32 34 L 18 50 M32 38 L 48 48 M32 62 L 20 78 M32 62 L 46 70" stroke="#c8553d" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- motion lines -->
  <path d="M12 30 L 4 30 M12 40 L 2 40 M12 50 L 6 50" stroke="#c8553d" stroke-width="1.5" stroke-linecap="round" opacity=".3"/>
  <!-- ground -->
  <path d="M4 82 L 60 82" stroke="#c8553d" stroke-width="2" stroke-linecap="round" opacity=".15"/>
</g>
<text x="75" y="145" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10" fill="#716f66">Saturday morning</text>
<text x="75" y="160" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="10" fill="#716f66">8:42 am</text>

<!-- arrow to phone -->
<path d="M120 95 C 140 85, 155 80, 170 78" stroke="#c8553d" stroke-width="1.5" stroke-dasharray="2 6" fill="none" stroke-linecap="round" opacity=".5"/>

<!-- phone with DrKing conversation -->
<g transform="translate(170,30)">
  <rect x="0" y="0" width="220" height="200" rx="20" fill="#fffdf9" stroke="#d8d5cd" stroke-width="1.5" filter="url(#ck-soft)"/>
  <rect x="0" y="0" width="220" height="34" rx="20" fill="#0d5c5c"/>
  <rect x="0" y="17" width="220" height="17" fill="#0d5c5c"/>
  <text x="110" y="22" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="9.5" fill="#f2ede4">DrKing voice AI &#183; answered</text>
  <!-- conversation bubbles -->
  <g font-family="Geomanist,sans-serif" font-size="9">
    <rect x="14" y="44" width="130" height="24" rx="12" fill="#eef3ee"/>
    <text x="26" y="60" fill="#3d4340">&#8220;Hi, I hurt my hamstring.&#8221;</text>
    <rect x="76" y="78" width="130" height="24" rx="12" fill="#0d5c5c"/>
    <text x="88" y="94" fill="#f3f5ef">&#8220;I can help with that.&#8221;</text>
    <rect x="76" y="112" width="130" height="24" rx="12" fill="#0d5c5c"/>
    <text x="88" y="128" fill="#f3f5ef">&#8220;Monday 9:00 am works?&#8221;</text>
    <rect x="14" y="146" width="130" height="24" rx="12" fill="#eef3ee"/>
    <text x="26" y="162" fill="#3d4340">&#8220;Yes, that&#8217;s perfect.&#8221;</text>
  </g>
  <!-- confirmed badge -->
  <g transform="translate(14,178)">
    <rect x="0" y="0" width="192" height="14" rx="7" fill="#e3eae3"/>
    <text x="96" y="11" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="7.5" font-weight="600" fill="#17483e">Booked &#183; Mon 9:00 am &#183; SMS sent</text>
  </g>
</g>

<!-- arrow to calendar -->
<path d="M398 95 C 415 85, 430 80, 445 78" stroke="#0d5c5c" stroke-width="1.5" stroke-dasharray="2 6" fill="none" stroke-linecap="round" opacity=".5"/>

<!-- Cliniko mini card -->
<g transform="translate(445,50)">
  <rect x="0" y="0" width="100" height="140" rx="16" fill="#fffdf9" stroke="#a8c5b5" stroke-width="1.5"/>
  <text x="50" y="20" text-anchor="middle" font-family="Newsreader,serif" font-size="11" fill="#17483e">Cliniko</text>
  <line x1="12" y1="30" x2="88" y2="30" stroke="#e5e2d9" stroke-width="1"/>
  <rect x="12" y="42" width="76" height="30" rx="8" fill="#e3eae3" stroke="#a8c5b5" stroke-width="1"/>
  <text x="20" y="55" font-family="Geomanist,sans-serif" font-size="8" fill="#17483e" font-weight="600">Mon 9:00</text>
  <text x="20" y="66" font-family="Geomanist,sans-serif" font-size="7.5" fill="#344d45">New patient</text>
  <circle cx="70" cy="52" r="6" fill="#0d5c5c"/>
  <path d="M67 52l2 2 4-4" stroke="#f3f5ef" stroke-width="1.2" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="12" y="80" width="76" height="18" rx="6" fill="#f0ede5"/>
  <text x="20" y="93" font-family="Geomanist,sans-serif" font-size="7.5" fill="#8a887f">10:00 open</text>
  <text x="50" y="122" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="7" fill="#716f66">Calendar updated</text>
  <text x="50" y="132" text-anchor="middle" font-family="Geomanist,sans-serif" font-size="7" fill="#716f66">automatically</text>
</g>
</svg>
<figcaption>The Saturday-morning moment: a runner calls with a hamstring injury, DrKing AI answers and books Monday 9:00 am, and the Cliniko calendar updates before anyone reaches the office. Illustrative conversation.</figcaption>
</figure>'''