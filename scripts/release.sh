#!/usr/bin/env bash
# DrKing.ai release: full quality gate -> curated bundle -> push -> Cloudflare Pages -> live verify.
# Usage: scripts/release.sh "commit message" [--no-deploy]
# Requires a committed working tree for HTML/assets (it refuses to deploy uncommitted pages).
set -euo pipefail
cd "$(dirname "$0")/.."
MSG="${1:?commit message required}"; NO_DEPLOY="${2:-}"
FN=/app/data/.hermes/profiles/seoad-factory/cache/scratch/drking-functions-build

echo "== 1. Quality gate"
node scripts/validate-site.mjs >/dev/null || { node scripts/validate-site.mjs; exit 1; }
node scripts/validate-seo.mjs  >/dev/null || { node scripts/validate-seo.mjs;  exit 1; }
python3 scripts/restore-svg-sprites.py --check >/dev/null || { echo "Undefined SVG symbols: run scripts/restore-svg-sprites.py"; exit 1; }
python3 - <<'PY'
import json, subprocess, sys
r = json.loads(subprocess.check_output(['python3', 'scripts/audit-static.py', '--json']))
tech = {p: [i for i in v if not i[0].startswith('claim:')] for p, v in r.items()}
tech = {p: v for p, v in tech.items() if v}
if tech:
    print('Static audit technical issues:', json.dumps(tech, indent=1)[:3000]); sys.exit(1)
claims = sum(1 for v in r.values() for i in v if i[0].startswith('claim:'))
print(f'static audit ok; {claims} numeric/absolute claim mentions to keep reviewing (see audit-static.py)')
PY

echo "== 2. Commit + push to DrKing GitHub master"
git add -A -- '*.html' assets fonts favicon.* apple-touch-icon.png sitemap.xml robots.txt llms.txt _headers _redirects scripts .github 2>/dev/null || true
git diff --cached --quiet || git commit -q -m "$MSG"
SHA=$(git rev-parse HEAD)
git push -q origin HEAD:master
[ "$(git ls-remote origin refs/heads/master | cut -f1)" = "$SHA" ] || { echo "push read-back mismatch"; exit 1; }
echo "pushed $SHA"
[ "$NO_DEPLOY" = "--no-deploy" ] && exit 0

echo "== 3. Curated bundle (static + Pages Functions)"
node scripts/build-pages.mjs >/dev/null
mkdir -p "$FN"
npx --yes wrangler pages functions build functions --outdir "$FN" --output-routes-path "$FN/_routes.json" >/dev/null 2>&1
head -c 200 "$FN/index.js" | grep -q 'form-data' && { echo "functions bundle is multipart, abort"; exit 1; }
cp "$FN/index.js" dist/_worker.js; cp "$FN/_routes.json" dist/_routes.json
grep -q '/api/leads' dist/_routes.json || { echo "/api/leads route missing from bundle, abort"; exit 1; }

echo "== 4. Deploy"
PREV=$(npx wrangler pages deployment list --project-name drking-ai 2>/dev/null | awk -F'│' '/Production/{gsub(/ /,"",$2);print $2;exit}')
echo "previous production deployment: $PREV"
npx wrangler pages deploy dist --project-name drking-ai --branch main --commit-hash "$SHA" --commit-message "$MSG" --commit-dirty=true 2>&1 | tail -2

echo "== 5. Live verification"
sleep 6
fail=0
for path in / /dentists /demo /integrations /sitemap.xml /favicon.ico; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -A Mozilla/5.0 "https://drking.ai$path"); echo "$code $path"; [ "$code" = 200 ] || fail=1
done
for path in /api/leads '/api/leads?limit=1'; do
  code=$(curl -s -o /dev/null -w '%{http_code}' -A Mozilla/5.0 "https://drking.ai$path"); echo "$code $path (must be 403)"; [ "$code" = 403 ] || fail=1
done
[ $fail = 0 ] && echo "RELEASE OK $SHA (rollback target: $PREV)" || { echo "LIVE CHECK FAILED — investigate; rollback target $PREV (never roll back to a build that re-exposes /api/leads)"; exit 1; }
