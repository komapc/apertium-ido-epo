#!/usr/bin/env bash
# Regression guard for the ido-epo conjunction fix (ke/se/kad/quankam/nam/
# quoniam/tamen/do/or). These words are tagged cnjcoo like the true
# coordinators (e/ed/o/od/ma/nek) by io_wiktionary, but their Esperanto
# targets cannot generate under <cnjcoo> — the transfer grammar
# (apertium-ido-epo.ido-epo.t1x) has to redirect each one to whichever tag
# its own dictionary entry supports. That redirect has to fire both for the
# standalone <cnjcoo> rule AND for every "noun cnjcoo noun"-family rule that
# also matches a cnjcoo token as part of a longer pattern — a sentence like
# "Voluntez selektar libro or filmo." exercises a different rule than a bare
# "E o ma nek do or." and can regress independently of it.
#
# A translation that falls back to the untagged/pass-through path shows up
# as a "#"-prefixed word in apertium's output (generator could not produce a
# surface form for the given lemma+tags) — that is exactly the failure mode
# this fix addresses, so this script fails loudly on any "#" reaching the
# output for these specific words.
#
# Run from the repo root after `make`: test/test_conjunctions.sh

set -u
cd "$(dirname "$0")/.."

pass=0
fail=0

check() {
  local desc="$1" input="$2" expected="$3"
  local actual
  actual=$(echo "$input" | apertium -d . ido-epo)
  if [ "$actual" = "$expected" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
    echo "FAIL: $desc"
    echo "  input:    $input"
    echo "  expected: $expected"
    echo "  actual:   $actual"
  fi
}

# --- standalone conjunction rule ---
check "ke (standalone)"      "Me pensas ke vu esas bona."          "Mi pensas ke vi estas bona."
check "se (standalone)"      "Se pluvos, me restos."                "Se pluvos, mi restos."
check "kad (standalone)"     "Kad tu venos?"                        "Ĉu vi venos?"
check "quankam (standalone)" "Quankam esas tarda, me venos."        "Kvankam estas forpasinta, mi venos."
check "nam (standalone)"     "Me restas hike nam pluvas."           "Mi restas tie ĉi ĉar pluvas."
check "quoniam (standalone)" "Me restas hike quoniam pluvas."       "Mi restas tie ĉi ĉar pluvas."
check "do (standalone)"      "Me laboros; do me repozos."           "Mi laboros; do mi ripozos."
check "or (standalone)"      "E o ma nek do or."                    "Kaj aŭ sed nek do nu."

# --- true coordinators unaffected by the redirect ---
check "ma (standalone)"      "Il esas richa ma yuna."               "Li estas riĉa sed juna."

# --- embedded in "noun cnjcoo noun" family rules (the part 6ea56bf missed) ---
check "or (verb nom-nom)"    "Voluntez selektar libro or filmo."    "Volontu selekti libron nu filmon."
check "ke (verb nom-nom)"    "Il vidas kato ke hundo."              "Li vidas katon ke hundon."
check "ke (verb adj-nom pair)" "Me havas richa amiko ke povra parento." "Mi havas riĉan amikon ke malriĉan parencon."

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
