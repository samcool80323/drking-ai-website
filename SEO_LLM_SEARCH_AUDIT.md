# DrKing SEO and LLM Search Audit

## Information architecture update — 17 September 2026

- Added indexable `/industries` and `/solutions` collection pages with descriptive tiles and CollectionPage, ItemList and BreadcrumbList structured data.
- Added both hubs to desktop navigation, mobile navigation, the shared footer, XML sitemap and `llms.txt`.
- Nested industry and solution detail-page breadcrumbs beneath the relevant hub so crawlers can understand the content hierarchy.
- Linked the two hubs to each other and linked the solutions hub to high-intent challenge pages, strengthening crawl paths without changing existing page intent.

**Audit date:** 17 September 2026  
**Website:** https://drking.ai  
**Scope:** 44 indexable HTML pages (the original 42 pages plus the Industries and Solutions hubs), live response behaviour, crawl/index controls, on-page SEO, structured data, internal linking, content trust, and agent/LLM discovery.
**Status:** repair implemented and verified locally; production status is verified separately after each deployment.

## Repair run — 17 September 2026

The audit has been converted into a repeatable local repair loop at `scripts/seo-repair-loop.mjs`. It runs normalisation, SEO repair, structural validation, SEO validation, regression audit and production-build preparation until the source stabilises. The current run stabilises after two passes.

### Completed locally

- Removed the sitewide `200` catch-all and added explicit permanent redirects for `/features_page` and `/ai-voice` variants.
- Added a branded, responsive, `noindex` 404 document; the Cloudflare Pages emulator returns it with HTTP 404.
- Added `Content-Signal: ai-train=no, search=yes, ai-input=yes` to `robots.txt` and response-header rules.
- Added a maintained `/llms.txt` and a homepage `describedby` Link response header.
- Consolidated structured data into one valid graph on every indexable page, with one stable DrKing Organisation node and accurate provider/publisher references.
- Removed the incorrect `MedicalBusiness` identity for DrKing and changed generic clinic-category nodes to audiences.
- Rewrote every metadata outlier identified by the audit; all 44 titles and descriptions are unique and inside the current review bands.
- Expanded relevant shared navigation so all 44 indexable pages have at least one incoming internal link.
- Repaired all detected heading-level jumps with non-visual section headings.
- Added intrinsic dimensions to shared logo images on all pages.
- Added a sitewide qualification explaining that uncited performance percentages and financial scenarios are illustrative and results vary.
- Added persistent SEO validation and a local HTTP preview that mirrors clean URLs, redirects, discovery headers and custom 404 behaviour.

### Verified locally

- 44/44 indexable routes return HTTP 200 in the Cloudflare Pages emulator.
- Random nonexistent route returns HTTP 404 with the branded `noindex,follow` page.
- Confirmed legacy routes return 301 to their selected current equivalents.
- Cloudflare Pages emulator parsed four redirects and three header rules without error.
- XML sitemap contains exactly the 44 indexable canonical URLs.
- Zero orphan pages, broken internal links, duplicate titles, duplicate descriptions, heading skips, duplicate IDs or invalid inline scripts.
- Exactly one consolidated JSON-LD graph and one canonical DrKing Organisation node per indexable page.
- Enquiry Function unit tests pass without sending a real enquiry.
- Production build contains `404.html`, `_redirects`, `_headers`, `robots.txt` and `llms.txt`.

### Still blocked or approval-dependent

- Production deployment and Git remote status are verified separately from local validation for every release.
- The `www` to apex redirect is a zone-level redirect; Cloudflare Pages `_redirects` does not support domain-level matching.
- Cloudflare Markdown for Agents is a zone setting. It remains disabled until authorised zone access is restored.
- Search Console reindexing and stale-result cleanup require Search Console access after deployment.
- A live browser visual/Core Web Vitals run remains unavailable because the browser security-policy check could not be completed.
- Unsupported commercial statistics still require a business evidence register with approved primary sources. The new visible qualification reduces ambiguity but does not turn unsupported claims into verified facts.

## Executive summary

DrKing has a sound crawl foundation: HTTPS works, all 44 intended indexable pages have canonical tags, the XML sitemap contains all 44 URLs, `robots.txt` is valid, major AI-search crawlers are explicitly allowed, every page has a title, description and one H1, and no duplicate page titles, duplicate descriptions, thin pages, or missing image alt text were found.

The original highest-priority problem was the Cloudflare Pages catch-all rule in `_redirects`, which returned the homepage for unknown URLs. It has been removed, selected retired URLs have explicit redirects, and unknown paths now use the branded 404 response.

Entity schema and internal-link gaps have been repaired with one stable DrKing organisation identity, two collection hubs and zero orphan pages. Unsupported commercial statistics and financial examples still require a business-owned evidence register.

The supplied agent-readiness tests place the site at **Level 1 — Basic Web Presence**. Content Signals and Markdown for Agents are useful additions. Web Bot Auth, DNS-AID, API catalog, MCP/A2A, OAuth and commerce discovery are not appropriate unless DrKing actually launches the corresponding public bot, agent, API, authentication service, or commerce endpoint.

## Prioritised issue tracker

| Priority | Area | Confirmed finding | Required change | Status |
|---|---|---|---|---|
| P0 | Indexing | Any nonexistent path returns the homepage with `200`, including `/not-a-real-page-llm-seo-test` and missing `/.well-known/*` files. Root cause: `/* /:splat 200` in `_redirects`. | Remove the catch-all. Keep clean URL handling, add a branded 404 page, and verify unknown paths return HTTP 404. | Fixed and verified locally |
| P0 | Legacy URLs | `/features_page` and `/ai-voice` return the homepage with `200`. Search results still exposed old content/snippets, including stale address and compliance wording. | Add explicit permanent redirects to the closest current pages (`/features_page` to a selected current hub, `/ai-voice` to `/ai-voice-receptionist`) or return 410 where no equivalent exists. Use Search Console URL inspection/removals only after server behaviour is corrected. | Fixed and verified locally |
| P1 | Canonical host | `https://www.drking.ai/` and `/about` return `200` instead of redirecting to the apex host. HTML canonicals point to the apex, but the duplicate host remains crawlable. | Add a zone-level or Worker/Page Rule permanent redirect from `www` to `https://drking.ai/:path`. | Found; not fixed |
| P1 | Claims and trust | Numerous pages contain percentages, revenue figures and outcome claims with little or no visible sourcing. Only a small number link to sources such as ABS or Harvard Business School. | Build a claim register with owner, source, publication date, scope and approved wording. Cite credible primary/Australian sources near claims; clearly label calculator scenarios and illustrative examples; qualify or remove claims that cannot be evidenced. | Found; business evidence needed |
| P1 | Entity schema | Organisation identity is inconsistent. `general-practice` marks DrKing itself as `MedicalBusiness`; `dentists` gives the organisation URL as `/dentists`; some category pages model generic clinic categories as businesses. | Define one reusable `Organization` node with a stable `@id` (`https://drking.ai/#organization`), apex URL, logo, contact details and truthful identifiers. Reference it as publisher/provider from WebPage, Service and SoftwareApplication nodes. Model clinic types as audiences/categories, not DrKing's business type. | Fixed and verified locally |
| P1 | Internal links | Ten pages have zero incoming links from other HTML pages: `case-studies`, `client-intake`, `patient-reactivation`, `payment-collection`, `referral-partner`, `security`, and all four comparison pages. Four more have only one incoming link: `admin-overhead`, `online-booking`, `online-reviews`, `roi-calculator`. | Add contextually relevant links from solution/industry pages and appropriate footer or resource hubs. Do not add sitewide links merely to inflate counts. | Fixed and verified locally |
| P1 | Snippet quality | 21 descriptions fall outside the audit's 70–160 character review band and nine titles exceed 60 characters. | Rewrite for distinct search intent, Australian context and accurate value propositions. Treat length as a snippet-quality guideline, not a ranking rule. | Fixed and verified locally |
| P1 | LLM usage policy | `robots.txt` has no Content Signals directive. | For the stated goal of appearing in AI search while blocking training, use `Content-Signal: ai-train=no, search=yes, ai-input=yes`. | Implemented locally |
| P1 | Agent-readable responses | Requests with `Accept: text/markdown` return HTML; no Markdown for Agents response or token-count headers are present. | Enable Cloudflare Markdown for Agents if available for this zone; verify `Content-Type: text/markdown`, `Vary: Accept`, `x-markdown-tokens`, and preservation of the chosen Content Signal. | Found; Cloudflare setting required |
| P2 | LLM orientation | No real `/llms.txt` exists; the path currently soft-404s to homepage HTML. | Publish a concise, maintained `/llms.txt` listing canonical facts and core pages. | Implemented locally |
| P2 | Discovery headers | Homepage Link header contains only a Google Fonts preconnect; no agent-useful registered relation is present. | Add a conservative `describedby` Link header for the maintained `/llms.txt`. | Implemented locally |
| P2 | Heading structure | H1-to-H3 jumps occur on `ai-voice-receptionist`, `analytics`, `contact`, `online-booking`, and `vs-call-answering`. | Restore sequential section hierarchy without changing visual styling. | Fixed and verified locally |
| P2 | Image layout stability | The original 42 pages contained at least one shared image without explicit `width` and `height` attributes. | Add intrinsic dimensions to shared logos and other images to reserve layout space. Confirm actual CLS with a performance trace. | Fixed locally; CLS trace blocked |
| P2 | Asset delivery | Static CSS, JS and fonts use a short four-hour revalidation policy rather than long-lived versioned caching. The site also depends on a remote Newsreader stylesheet. | Fingerprint/version static assets and apply long-lived immutable caching. Consider self-hosting the permitted Newsreader files for predictability. Validate impact before and after. | Opportunity; not measured |
| P2 | Content depth and proof | The site has many commercial landing pages but no substantive resource/article library or published client case studies. The current case-study page correctly says its cards are placeholders. | Publish only real, consented evidence: Australian implementation guides, integration explainers, privacy/security notes, original data methodology, and named or responsibly anonymised case studies with dates and measurable baselines. | Editorial programme |

## Agent and LLM readiness scorecard

| Check | Live result | Recommendation |
|---|---|---|
| `robots.txt` | Pass | Retain explicit search-crawler rules and add the chosen Content Signal. |
| XML sitemap | Pass | Retain all 44 canonical URLs; update only when pages change. |
| AI crawler access | Pass | `OAI-SearchBot`, `PerplexityBot`, and `Claude-SearchBot` are allowed; `GPTBot` is blocked. Review this policy quarterly because crawler names and controls can change. |
| Content Signals | Pass | Retain the approved `ai-train=no, search=yes, ai-input=yes` directive and review it if business policy changes. |
| Markdown negotiation | Fail | Enable and retest through Cloudflare. |
| Useful Link relations | Pass | The homepage advertises the maintained `/llms.txt` resource with `rel="describedby"`. |
| Web Bot Auth directory | Informational/neutral | Not an SEO feature. Do not publish a JWKS unless DrKing sends signed outbound bot/agent requests and can securely operate key rotation. |
| DNS-AID | Fail | Not relevant to the current marketing site. It is experimental agent endpoint discovery, not a prerequisite for Google or LLM search visibility. Revisit only if DrKing launches a public agent endpoint; enable DNSSEC first. |
| API catalog / OAuth / MCP / A2A / Agent Skills / WebMCP / ARD | Scanner failures | Expected for a marketing website. Do not create empty or misleading manifests. |
| Commerce discovery | Neutral | Not applicable; the website is not an agentic commerce service. |

## Page-level on-page findings

The baseline had nine titles above the 60-character review threshold and 20 descriptions above the 160-character review threshold. These have been rewritten and the current validator reports no outliers, duplicates or missing values across the 44 indexable pages.

The first audit output reported the `after-hours` description as 32 characters because its apostrophe exposed a bug in the original audit expression. The description itself was not 32 characters. The persistent validator now parses quoted attributes correctly and includes a regression check for this case.

The thresholds remain snippet-quality review guides rather than direct ranking rules.

## Confirmed strengths

- 44 intended indexable HTML pages and 44 canonical sitemap entries.
- Every page has a unique title and unique meta description.
- Every page has exactly one H1.
- No duplicate main-content pages detected in the source scan.
- No pages under 300 visible words in the source scan.
- No missing `alt` attributes detected on images.
- Canonical tags use the HTTPS apex domain.
- HTTP apex redirects to HTTPS.
- Australian English, AUD labelling, Hawthorn address and Australian privacy framing are present in current source.
- The case-study page clearly labels its examples as forthcoming placeholders rather than claiming fabricated results.
- Current contact and integration content is represented in the sitemap.

## Content and entity recommendations for search and LLM citation

1. **Create a canonical entity statement.** Use the same concise facts in the homepage, About page, Organisation schema and optional `llms.txt`: what DrKing is, who it serves, where it operates, and what it does not do.
2. **Show accountable expertise.** Add real leadership/team information, relevant experience, editorial ownership and last-reviewed dates where accurate and approved. Do not invent credentials.
3. **Make important claims citable.** Place source links next to factual statistics. Prefer Australian primary sources, original methodology or product data with a defined period and sample. Separate product capability, illustrative scenarios and verified client outcomes.
4. **Use answer-first sections.** Begin core pages with a short direct definition, intended user, supported workflow and limitations, followed by detail. This improves human comprehension and machine extraction without keyword stuffing.
5. **Build topic clusters, not word-count targets.** Link each industry page to relevant solution, integration, privacy/security and evidence pages. Publish content only where it answers a real clinic question. Google does not prescribe a preferred word count.
6. **Clarify integration states.** Keep active, waitlist, planned and subject-to-vendor-access states explicit and consistent in page copy and structured data.
7. **Keep medical boundaries explicit.** Continue distinguishing administrative automation from clinical advice, triage and emergency care.

## Recommended implementation phases

### Phase 1 — Crawl and index repair

1. Remove the catch-all `200` rewrite.
2. Add a real 404 page and verify its HTTP status.
3. Inventory historical indexed URLs and add only relevant permanent redirects.
4. Redirect `www` to the apex host.
5. Validate status codes, canonicals, sitemap and robots again.
6. Submit the sitemap and request reindexing in Google Search Console and Bing Webmaster Tools after deployment.

### Phase 2 — Entity, schema and internal architecture

1. Centralise the Organisation JSON-LD definition and repair incorrect page-level types.
2. Add truthful logo/contact/identity fields and stable cross-references.
3. Link the ten orphaned pages from relevant hubs and content.
4. Repair heading jumps and priority titles/descriptions.
5. Validate structured data and crawl the full site for new broken links.

### Phase 3 — Evidence and answer quality

1. Build and review the commercial-claim register.
2. Add primary citations, methodology notes and clear illustrative-result labels.
3. Improve About/expertise signals with approved real-world information.
4. Publish a small number of high-value Australian clinic resources and verified case studies.

### Phase 4 — LLM access controls

1. Confirm the desired Content Signals policy.
2. Enable Markdown for Agents and test representative pages.
3. Optionally publish a maintained `/llms.txt` and a conservative `describedby` Link header.
4. Re-run the agent-readiness scanner after soft 404s are fixed so missing optional resources are reported accurately.

### Phase 5 — Measurement and iteration

1. Run mobile and desktop Lighthouse/Core Web Vitals traces on representative templates.
2. Review Search Console indexing, query/page performance, enhancements and Core Web Vitals.
3. Review Bing Webmaster Tools, analytics landing-page conversions and crawl logs.
4. Track index coverage, non-brand impressions, qualified demo conversions and citations/referrals from AI search separately.

## Tests performed

- Inspected all 44 indexable HTML files for titles, descriptions, canonical tags, H1 count, headings, structured data, image alt text, image dimensions, word count, duplicates, internal incoming links and external source links.
- Parsed the XML sitemap and matched its 44 URLs to the repository pages.
- Fetched live homepage, robots, sitemap, known pages, legacy URLs, a random nonexistent URL, `www` variants and agent well-known paths.
- Tested live `Accept: text/markdown` content negotiation.
- Queried DNS-AID candidates and DNSSEC validation indicators.
- Ran the supplied agent-readiness scanner and reviewed each result.
- Checked public search results for stale indexed routes/snippets.
- Inspected Cloudflare Pages build, redirect and Worker configuration in the repository.
- Attempted a live rendered browser pass; the browser security policy check was unavailable, so no visual or Core Web Vitals result is claimed here.

## Not tested / access required

- Google Search Console coverage, manual actions, crawl stats, URL Inspection and removals.
- Bing Webmaster Tools and IndexNow submission history.
- Google Business Profile, local citations and NAP consistency outside this website.
- Analytics, conversions, backlink quality and keyword/rank history.
- Field Core Web Vitals/CrUX and a successful browser performance trace.
- Exact Cloudflare zone plan/availability for Markdown for Agents and DNSSEC state in the dashboard.

## Decision log

- No production or source changes were made because this request was an audit.
- No fake JWKS, API catalog, OAuth metadata, MCP/A2A card, agent skill, ARD or commerce manifest is recommended.
- Proposed Content Signals favour discoverability and LLM answers while declining training: `ai-train=no, search=yes, ai-input=yes`. This remains a business-policy decision.
- `/llms.txt` and agent-useful Link headers are optional enhancements, not substitutes for crawlability, evidence, structured content and correct HTTP status codes.
