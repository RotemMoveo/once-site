#!/usr/bin/env bash
# Keeps en/ in step with the Hebrew site.
#
# Rebuilds only when a Hebrew source is newer than the last build, so it costs
# almost nothing (~50ms) to call constantly. Called by deploy.sh — so a publish
# can never ship a stale English site — and by the PostToolUse hook in
# .claude/settings.json.
#
#   _en-build/sync.sh            rebuild if anything changed
#   _en-build/sync.sh --force    rebuild unconditionally
#   _en-build/sync.sh --hook     as above, but report an untranslated-strings
#                                warning as Claude Code hook JSON on stdout
#
# Exit 0 = en/ is current (a warning may still have been printed).
# Exit 2 = the build failed and en/ is now stale; the reason is on stderr.
set -uo pipefail

SITE="$(cd "$(dirname "$0")/.." && pwd)"
STAMP="$SITE/_en-build/.build-stamp"
cd "$SITE" || exit 1

force=0; hook=0
for a in "$@"; do
  case "$a" in --force) force=1 ;; --hook) hook=1 ;; esac
done

if [ -f "$STAMP" ] && [ "$force" = 0 ]; then
  changed="$(
    find . -maxdepth 1 -name '*.html' -newer "$STAMP" -print -quit
    find css js _en-build -type f -newer "$STAMP" -print -quit 2>/dev/null
  )"
  [ -n "$changed" ] || exit 0
fi

if ! out="$(python3 "$SITE/_en-build/build.py" 2>&1)"; then
  printf '%s\n' "$out" >&2
  cat >&2 <<'MSG'
The English build failed, so en/ is now out of date with the Hebrew site.
Usually a fixup in _en-build/fixups.py no longer matches the Hebrew source that
was just edited: paste the new source text into that entry (do not delete it,
it is still doing real work) and re-run
  python3 "_en-build/build.py"
MSG
  exit 2
fi

touch "$STAMP"

# The build succeeded, so en/ is current — but a string with no dictionary entry
# ships Hebrew copy on an English page. Warn loudly; never block the deploy.
case "$out" in
  *UNTRANSLATED*)
    missing="$(printf '%s' "$out" | sed -n '/^--- UNTRANSLATED/,$p')"
    if [ "$hook" = 1 ]; then
      printf '%s' "$missing" | python3 -c 'import json,sys
t=sys.stdin.read()
print(json.dumps({"systemMessage":"en/ rebuilt — but some strings have no English translation.","hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":"The English site was rebuilt, but these Hebrew strings have no entry in _en-build/dict_en.py, so they ship as Hebrew on the English pages. Add them:\n"+t}}))'
    else
      printf '%s\n' "$missing" >&2
      echo "^ these strings have no entry in _en-build/dict_en.py and ship as Hebrew on the English pages." >&2
    fi
    ;;
esac
exit 0
