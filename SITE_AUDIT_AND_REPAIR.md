# DrKing site-wide audit and repair

## Scope and boundaries

- Audited and repaired all 42 standalone HTML pages on `codex/sitewide-ui-ux-repair`.
- Preserved page-specific content and visual direction; this is not a redesign.
- Typography is restricted to Geomanist for UI/body copy and Newsreader for headings/editorial copy.
- No push, merge, deployment, form submission, message, purchase or external-service change was performed.
- Forms remain email-draft or `mailto:` experiences. No backend was invented.

## Confirmed baseline defects

| Severity | Finding | Evidence before repair | Status |
| --- | --- | --- | --- |
| Critical | Conflicting navigation controllers | All 42 pages had two or more scripts capable of controlling navigation | Fixed |
| Critical | Invalid page structure | Duplicate `main` landmarks on two pages; malformed body structures on Client Intake, Medical Centres, Multi-location, Privacy and Referral Partner | Fixed |
| Major | Navigation varied by page and breakpoint | Competing header markup and breakpoints from 600px to 800px | Fixed |
| Major | Repeated override payload | About 10.4 MB across the HTML set, including copied nav/footer CSS and roughly 200 `!important` uses per page | Fixed; HTML set is about 1.85 MB |
| Major | Missing typography assets | 11 pages requested Newsreader files that were not present | Fixed |
| Major | Broken internal destinations | 23 unresolved references, including `/book-demo`, `/book-a-demo`, `/multi-location-management` and missing font preloads | Fixed |
| Major | Invalid nested/stray markup | Unclosed CTA link, stray containers and an unclosed legal dialog | Fixed |
| Major | Accessibility defects | Implicit input/button types, invalid ARIA labels, duplicate label/control associations and unlabeled interactive groups | Fixed |
| Major | Australian calculator mismatch | ROI output and schema/disclaimer used USD | Fixed to AUD |
| Moderate | Repeated footer implementations | Inline footer copied to every page with inconsistent structure | Fixed with shared responsive footer |
| Moderate | Content fragment defect | Legal copy ended with “or write to .” | Fixed |
| Moderate | Obsolete live-page fragment CTA | CTA targeted `#button-LZar9xGjf-` on the live homepage | Fixed to `/demo` |
| Critical regression | Reveal content hidden after shared-footer insertion | Synchronous page scripts enabled `.js` reveal styles, then threw because `#year` had not been parsed yet | Fixed by placing the shared footer before page-end scripts and validating DOM order |

## Implemented repairs

- One canonical header, desktop mega menu, full-screen mobile menu and footer on every page.
- One shared interaction controller with legacy-handler isolation, outside-click close, Escape close, focus return, mobile focus trap, breakpoint reset and `aria-current` handling.
- One 1080px navigation breakpoint, consistent logo/header sizing, touch targets, layering and sticky-header offset.
- Shared responsive typography, form controls, focus treatment, media constraints, reduced-motion behaviour and footer grid.
- Canonical internal routes and complete 42-page sitemap alignment.
- Explicit form control types and corrected calculator label/output semantics.
- Repaired page-body structure on the five malformed page types and malformed JSON-LD on Case Studies and Referral Partner.
- Added reproducible audit, validation, normalisation and clean-URL preview scripts.

## Verification actually performed

- [x] `node scripts/validate-site.mjs`: 42 pages, zero structural/script/JSON-LD problems.
- [x] `html-validate '*.html'`: all 42 pages passed the configured recommended rules.
- [x] `node scripts/audit-site.mjs`: zero duplicate IDs, missing font assets, broken internal references or duplicate menu controllers.
- [x] Parsed every inline JavaScript block with Node's JavaScript parser.
- [x] Parsed every JSON-LD block as JSON.
- [x] Compared the canonical header/mobile-nav fragment across all pages: one identical variant across 42 pages.
- [x] Checked all script references made through `getElementById` and `querySelector('#…')`: no missing target IDs.
- [x] Inspected all nine forms and their submit paths without submitting them.
- [x] Verified all 42 clean local routes and core shared assets over HTTP: 42/42 returned 200.
- [x] Verified sitemap/page parity: 42 sitemap routes and 42 HTML pages, no omissions or extras.
- [x] Verified the normalisation process is idempotent by comparing full-file hashes across consecutive runs.
- [x] Verified synchronous page scripts do not reference `#year` before the shared footer exists in the DOM.
- [x] Confirmed only Geomanist and Newsreader are named font families (plus generic fallbacks).
- [x] Confirmed the linked ABS 2024–25 source supports the page's 26% GP waiting-time statement.
- [x] Confirmed the ICO, ABS and Harvard Business School third-party reference pages resolve.
- [ ] Browser visual, keyboard and console pass at mobile/tablet/desktop widths.
- [ ] Core Web Vitals trace and before/after browser screenshots.

## Remaining limitations and blockers

- The Codex in-app browser refused localhost before navigation because its admin-enforced security policy could not be verified. It was retried after the final repair and remained blocked. No browser-security bypass or alternate automation workaround was used.
- The dedicated Chrome DevTools performance trace integration is unavailable in this task, so no Lighthouse/Core Web Vitals numbers are claimed.
- The Google Maps and LeadConnector form destinations could not be opened by the safe web checker. Their URLs were preserved and no form was submitted.
- Because browser execution is blocked, responsive layout, visible focus, keyboard interaction and runtime console behaviour are strongly covered by code/static checks but not claimed as visually verified.

## Preview and repeatable commands

```sh
node scripts/preview.mjs
node scripts/normalise-site.mjs
node scripts/validate-site.mjs
node scripts/audit-site.mjs
html-validate '*.html'
```

Local preview: `http://127.0.0.1:4174/`
