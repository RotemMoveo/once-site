#!/usr/bin/env bash
# מפרסם את התוכן של "גלי/ONCE site" לענף gh-pages.
# ה-URL שנוצר: https://rotemmoveo.github.io/once-site/
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/גלי/ONCE site"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

[ -d "$SRC" ] || { echo "לא נמצאה התיקייה: $SRC" >&2; exit 1; }

echo "מעתיק את האתר..."
tar cf - -C "$SRC" . | tar xf - -C "$WORK"
find "$WORK" -name '.DS_Store' -delete
touch "$WORK/.nojekyll"   # בלי זה GitHub Pages מדלג על תיקיות שמתחילות ב-_

cd "$WORK"
git init -q -b gh-pages
git add -A
git commit -q -m "Deploy ONCE site — $(date '+%Y-%m-%d %H:%M')"
git remote add origin "$(git -C "$ROOT" remote get-url origin)"

echo "מעלה ל-gh-pages..."
git push -q --force origin gh-pages

echo "פורסם. הבנייה לוקחת דקה בערך:"
echo "https://rotemmoveo.github.io/once-site/"
