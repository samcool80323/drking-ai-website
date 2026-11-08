#!/usr/bin/env python3
"""Sitewide topical interlinking: a 'Related' card strip on every main page.

Cluster model (SEOAD topical relevance):
  Solutions (what DrKing does) <-> Problems (why clinics need it) <-> Industries (who) <->
  Integrations (which PMS) <-> Journal guides (how-to) <-> Comparisons.
Each page links to 3-4 hand-picked neighbours. Targets that don't exist yet are skipped,
so re-run after adding pages. Idempotent: replaces content between <!-- drking-related -->
markers and removes the older <!-- drking-guides --> strip. Card text comes from the
target's own meta description, so it stays accurate when pages change.
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LABEL = {  # route: (eyebrow, card title)
    'ai-voice-receptionist': ('Solution', 'AI voice receptionist'), 'ai-chat': ('Solution', 'AI web chat'),
    'missed-call-recovery': ('Solution', 'Missed-call text-back'), 'online-booking': ('Solution', 'Online booking'),
    'appointment-reminders': ('Solution', 'Appointment reminders'), 'patient-reactivation': ('Solution', 'Patient reactivation'),
    'treatment-plan-follow-up': ('Solution', 'Treatment plan follow-up'), 'text-to-pay': ('Solution', 'Text-to-pay'),
    'payment-collection': ('Solution', 'Payment collection'), 'review-generator': ('Solution', 'Google review requests'),
    'lead-management': ('Solution', 'One inbox for every lead'), 'analytics': ('Solution', 'Source and conversion analytics'),
    'missed-calls': ('Problem', 'Missed calls'), 'patient-no-shows': ('Problem', 'Patient no-shows'),
    'slow-follow-up': ('Problem', 'Slow follow-up'), 'after-hours': ('Problem', 'After-hours enquiries'),
    'admin-overhead': ('Problem', 'Admin overhead'), 'multi-location-chaos': ('Problem', 'Multi-location coordination'),
    'online-reviews': ('Problem', 'Online reviews'),
    'dentists': ('Industry', 'Dental clinics'), 'general-practice': ('Industry', 'General practice'),
    'specialists': ('Industry', 'Specialist clinics'), 'allied-health': ('Industry', 'Allied health'),
    'medical-centres': ('Industry', 'Medical centres'), 'cosmetic-clinics': ('Industry', 'Cosmetic clinics'),
    'veterinary': ('Industry', 'Veterinary clinics'), 'aged-care': ('Industry', 'Aged care'),
    'physiotherapy': ('Industry', 'Physiotherapy clinics'), 'psychology': ('Industry', 'Psychology practices'),
    'chiropractic': ('Industry', 'Chiropractic clinics'), 'podiatry': ('Industry', 'Podiatry clinics'),
    'cliniko-integration': ('Integration', 'Cliniko + DrKing'), 'nookal-integration': ('Integration', 'Nookal + DrKing'),
    'power-diary-integration': ('Integration', 'Power Diary + DrKing'), 'dentally-integration': ('Integration', 'Dentally + DrKing'),
    'dental4web-integration': ('Integration', 'Dental4Web + DrKing'), 'core-practice-integration': ('Integration', 'Core Practice (planned)'),
    'best-practice-integration': ('Integration', 'Best Practice + DrKing'), 'medicaldirector-integration': ('Integration', 'MedicalDirector + DrKing'),
    'zedmed-integration': ('Integration', 'Zedmed + DrKing'), 'exact-integration': ('Integration', 'EXACT + DrKing'),
    'praktika-integration': ('Integration', 'Praktika + DrKing'), 'carestack-integration': ('Integration', 'CareStack + DrKing'),
    'integrations': ('Integrations', 'All practice software integrations'),
    'vs-receptionist': ('Compare', 'DrKing vs a human receptionist'), 'vs-call-answering': ('Compare', 'DrKing vs call answering services'),
    'vs-chatbots': ('Compare', 'DrKing vs generic chatbots'), 'vs-practice-management': ('Compare', 'DrKing vs practice software'),
    'unscheduled-treatment-follow-up': ('Guide', 'Following up unscheduled treatment'),
    'patient-reactivation-calendar': ('Guide', 'A 12-month reactivation calendar'),
    'no-show-to-lost-patient': ('Guide', 'From no-show to lost patient'),
    'ai-receptionist-for-dental-practices-questions-to-ask': ('Guide', 'Dental AI receptionist buying questions'),
    'ai-receptionist-pilot-plan': ('Guide', 'AI receptionist pilot plan'), 'missed-call-audit': ('Guide', 'Missed-call audit worksheet'),
    'missed-call-voice-ai': ('Guide', 'Missed calls and voice AI'), 'missed-call-text-ai': ('Guide', 'Missed calls and text AI'),
    'roi-calculator': ('Tool', 'Missed-opportunity calculator'), 'security': ('Trust', 'Security and data handling'),
}
GP = ['general-practice', 'best-practice-integration', 'medicaldirector-integration', 'zedmed-integration']
ALLIED = ['physiotherapy', 'psychology', 'chiropractic', 'podiatry']
RELATED = {
    'index': ['ai-voice-receptionist', 'dentists', 'patient-reactivation', 'integrations'],
    'about': ['ai-voice-receptionist', 'integrations', 'security', 'blog'],
    'ai-voice-receptionist': ['after-hours', 'missed-call-recovery', 'dentists', 'ai-receptionist-for-dental-practices-questions-to-ask'],
    'ai-chat': ['ai-voice-receptionist', 'online-booking', 'vs-chatbots', 'lead-management'],
    'missed-call-recovery': ['missed-calls', 'ai-voice-receptionist', 'lead-management', 'missed-call-audit'],
    'online-booking': ['appointment-reminders', 'ai-chat', 'integrations', 'after-hours'],
    'appointment-reminders': ['patient-no-shows', 'no-show-to-lost-patient', 'online-booking', 'text-to-pay'],
    'patient-reactivation': ['treatment-plan-follow-up', 'patient-reactivation-calendar', 'analytics', 'dentists'],
    'treatment-plan-follow-up': ['unscheduled-treatment-follow-up', 'patient-reactivation', 'text-to-pay', 'dentists'],
    'text-to-pay': ['payment-collection', 'appointment-reminders', 'treatment-plan-follow-up', 'lead-management'],
    'payment-collection': ['text-to-pay', 'admin-overhead', 'analytics'],
    'review-generator': ['online-reviews', 'appointment-reminders', 'analytics'],
    'online-reviews': ['review-generator', 'analytics', 'cosmetic-clinics'],
    'lead-management': ['analytics', 'slow-follow-up', 'ai-chat', 'missed-call-recovery'],
    'analytics': ['lead-management', 'patient-reactivation', 'multi-location-chaos'],
    'missed-calls': ['missed-call-recovery', 'ai-voice-receptionist', 'after-hours', 'missed-call-audit'],
    'patient-no-shows': ['appointment-reminders', 'no-show-to-lost-patient', 'patient-reactivation', 'online-booking'],
    'slow-follow-up': ['lead-management', 'treatment-plan-follow-up', 'unscheduled-treatment-follow-up', 'ai-chat'],
    'after-hours': ['ai-voice-receptionist', 'ai-chat', 'online-booking', 'vs-call-answering'],
    'admin-overhead': ['ai-voice-receptionist', 'online-booking', 'text-to-pay', 'lead-management'],
    'multi-location-chaos': ['medical-centres', 'analytics', 'lead-management'],
    'dentists': ['dentally-integration', 'dental4web-integration', 'treatment-plan-follow-up', 'ai-receptionist-for-dental-practices-questions-to-ask'],
    'general-practice': ['best-practice-integration', 'medicaldirector-integration', 'medical-centres', 'ai-voice-receptionist'],
    'specialists': ['ai-voice-receptionist', 'appointment-reminders', 'treatment-plan-follow-up', 'medical-centres'],
    'allied-health': ALLIED + [],
    'medical-centres': ['general-practice', 'multi-location-chaos', 'analytics', 'best-practice-integration'],
    'cosmetic-clinics': ['lead-management', 'ai-chat', 'online-reviews', 'treatment-plan-follow-up'],
    'veterinary': ['ai-voice-receptionist', 'after-hours', 'appointment-reminders', 'online-booking'],
    'aged-care': ['ai-voice-receptionist', 'after-hours', 'lead-management'],
    'physiotherapy': ['cliniko-integration', 'nookal-integration', 'appointment-reminders', 'chiropractic'],
    'psychology': ['power-diary-integration', 'cliniko-integration', 'ai-voice-receptionist', 'allied-health'],
    'chiropractic': ['cliniko-integration', 'patient-reactivation', 'physiotherapy', 'podiatry'],
    'podiatry': ['cliniko-integration', 'nookal-integration', 'treatment-plan-follow-up', 'physiotherapy'],
    'cliniko-integration': ['physiotherapy', 'psychology', 'nookal-integration', 'integrations'],
    'nookal-integration': ['physiotherapy', 'podiatry', 'cliniko-integration', 'integrations'],
    'power-diary-integration': ['psychology', 'allied-health', 'cliniko-integration', 'integrations'],
    'dentally-integration': ['dentists', 'treatment-plan-follow-up', 'dental4web-integration', 'integrations'],
    'dental4web-integration': ['dentists', 'treatment-plan-follow-up', 'dentally-integration', 'integrations'],
    'core-practice-integration': ['dentists', 'exact-integration', 'praktika-integration', 'integrations'],
    'best-practice-integration': ['general-practice', 'medicaldirector-integration', 'zedmed-integration', 'integrations'],
    'medicaldirector-integration': ['general-practice', 'best-practice-integration', 'zedmed-integration', 'integrations'],
    'zedmed-integration': ['general-practice', 'best-practice-integration', 'medicaldirector-integration', 'integrations'],
    'exact-integration': ['dentists', 'praktika-integration', 'carestack-integration', 'integrations'],
    'praktika-integration': ['dentists', 'exact-integration', 'carestack-integration', 'integrations'],
    'carestack-integration': ['dentists', 'exact-integration', 'praktika-integration', 'integrations'],
    'integrations': ['cliniko-integration', 'dentally-integration', 'best-practice-integration', 'exact-integration'],
    'vs-receptionist': ['ai-voice-receptionist', 'vs-call-answering', 'admin-overhead'],
    'vs-call-answering': ['ai-voice-receptionist', 'after-hours', 'vs-receptionist'],
    'vs-chatbots': ['ai-chat', 'ai-voice-receptionist', 'vs-call-answering'],
    'vs-practice-management': ['integrations', 'lead-management', 'online-booking'],
    'ai-receptionist-for-dental-practices-questions-to-ask': ['dentists', 'ai-voice-receptionist', 'missed-call-audit', 'integrations'],
    'ai-receptionist-pilot-plan': ['ai-voice-receptionist', 'missed-call-audit', 'vs-receptionist'],
    'missed-call-audit': ['missed-calls', 'missed-call-recovery', 'ai-receptionist-pilot-plan'],
    'missed-call-voice-ai': ['ai-voice-receptionist', 'missed-calls', 'missed-call-text-ai'],
    'missed-call-text-ai': ['missed-call-recovery', 'missed-calls', 'missed-call-voice-ai'],
    'roi-calculator': ['missed-calls', 'patient-reactivation', 'analytics'],
    'security': ['about', 'integrations', 'ai-voice-receptionist'],
    'case-studies': ['dentists', 'general-practice', 'allied-health'],
    'solutions': ['treatment-plan-follow-up', 'unscheduled-treatment-follow-up', 'patient-reactivation-calendar'],
    'industries': ALLIED,
}
LABEL['blog'] = ('Journal', 'DrKing Journal')
LABEL['about'] = ('Company', 'About DrKing')
END = re.compile(r'<section class="[^"]*\b(cta|closing|demo-section|final-cta|article-cta|guide-cta|cta-shell|cta-section|cta-wrap)\b')
CSS = ('<style id="drking-related-css">.dk-guides{width:min(1200px,calc(100% - 40px));margin:0 auto;padding:24px 0 72px}'
       '.dk-guides h2{font:300 clamp(30px,3.2vw,42px)/1.12 Newsreader,serif;letter-spacing:-.6px;margin:12px 0 24px;color:#1C1814}'
       '.dk-guides h2 em{color:#0D5C5C}.dk-guides-k{font-size:12px;letter-spacing:2px;text-transform:uppercase;color:#0D5C5C;font-weight:500}'
       '.dk-guides-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px}'
       '.dk-guide{display:block;background:#fff;border-radius:22px;padding:24px;box-shadow:0 2px 4px #1c18140a,0 12px 24px #1c18140f;color:#1C1814;text-decoration:none;transition:transform .2s}'
       '.dk-guide:hover{transform:translateY(-3px)}.dk-guide span{font-size:12px;letter-spacing:1.4px;text-transform:uppercase;color:#b94a32}'
       '.dk-guide strong{display:block;font:300 23px/1.25 Newsreader,serif;margin:10px 0 8px}.dk-guide p{margin:0;font-size:15px;line-height:1.6;color:#5f5c55}</style>')


def meta_desc(route):
    f = ROOT / ('index.html' if route == 'index' else f'{route}.html')
    m = re.search(r'<meta name="description" content="([^"]*)"', f.read_text(encoding='utf-8'))
    d = html.unescape(m.group(1)) if m else ''
    if len(d) > 125:
        d = d[:125].rsplit(' ', 1)[0].rstrip(',.;:—-') + '…'
    return d


def exists(route):
    return (ROOT / f'{route}.html').exists()


def main():
    done = 0
    for page, targets in RELATED.items():
        f = ROOT / f'{page}.html'
        if not f.exists():
            continue
        s = f.read_text(encoding='utf-8')
        s = re.sub(r'<!-- drking-(?:guides|related) -->.*?<!-- /drking-(?:guides|related) -->', '', s, flags=re.S)
        s = re.sub(r'<style id="drking-guides-css">.*?</style>\n?', '', s, flags=re.S)
        t = [x for x in targets if exists(x) and x != page][:4]
        if not t:
            continue
        cards = ''.join(f'<a class="dk-guide" href="/{x}"><span>{LABEL[x][0]}</span><strong>{html.escape(LABEL[x][1])}</strong><p>{html.escape(meta_desc(x))}</p></a>' for x in t)
        block = (f'<!-- drking-related --><section class="dk-guides" aria-labelledby="dk-related-h"><div class="dk-guides-k">Keep exploring</div>'
                 f'<h2 id="dk-related-h">Related <em>for your practice</em></h2><div class="dk-guides-grid">{cards}</div></section><!-- /drking-related -->')
        main_s, main_e = s.index('<main'), s.index('</main>')
        ends = [m for m in END.finditer(s, main_s, main_e)]
        at = ends[-1].start() if ends else main_e
        s = s[:at] + block + s[at:]
        if 'drking-related-css' not in s:
            s = s.replace('</head>', CSS + '\n</head>', 1)
        f.write_text(s, encoding='utf-8'); done += 1
    print('pages with related strip:', done)


main()
