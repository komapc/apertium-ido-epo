#!/usr/bin/env bash
# Regression guard for the transfer-rule gaps fixed in apertium-ido-epo#203,
# #204, #205, #206 and #209 (apertium-ido-epo.ido-epo.t1x).
#
# #203/#206: kelka/multa/diversa/cetera/tanta/quanta are lexicalised <num> but
#   agree like adjectives; the "quant"/"corr_da" def-cats and their
#   verb/correlative rules fix subject/object case agreement on them.
# #204: "me donis a la puero la libro" (dative-marked indirect object before
#   the direct object) left the trailing determiner bare, producing a
#   "#la"-prefixed generation failure rather than a cosmetic artifact.
# #205: "qua"/"qui"/"qua libro" (interrogative pronoun/determiner) needed a
#   dedicated <itg> generation path distinct from the relative "kiu".
# #209: the vbintr def-cat listed only infinitive forms (venar, irar, ...),
#   but the Ido analyser emits the bare stem (venis -> ven<vblex>), so the
#   whole "intransitive verb + subject" rule family was dead until bare
#   stems were added — and fixing that exposed two more pre-existing bugs
#   that had never been reachable before: the vbintr rules didn't call
#   pii_to_past (past tense fell back to the infinitive, "Veni" instead of
#   "Venis"), and two coordinated-subject vbintr rules were shadowed by
#   their vblex sibling of equal pattern length (document-order tie).
#
# Run from the repo root after `make`: test/test_syntax_gaps.sh

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
    echo "  actual:   $actual"
    echo "  expected: $expected"
  fi
}

# --- #203/#206: quant/corr_da case agreement ---
check "quant: transitive object accusative" "Me havas multa amiki." "Mi havas multajn amikojn."
check "corr_da: standalone partitive"       "Tanta kati venis."     "Tiom da katoj venis."
check "corr_da: adjective + noun (new)"     "Tanta bela domi."      "Tiom da belaj domoj."
check "corr_da: after intransitive verb"    "Quanta bela domi venis." "Kiom da belaj domoj venis."

# --- #204: ditransitive dative word order + det tag injection ---
check "ditransitive: dative before direct object" "Me donis a la puero la libro." "Mi donis al la infano la libron."
check "det tag injection: copula subject"         "La urbo esas granda."          "La urbo estas granda."
check "det tag injection: transitive object"      "Me vidas la amiko."            "Mi vidas la amikon."
check "det tag injection: transitive object (2)"  "Me lektis la artiklo."         "Mi legis la artikolon."

# --- #205: interrogative pronoun/determiner ---
check "prn_itg: attributive qua + noun" "Qua libro tu lektas?" "Kiu libro vi legas?"

# --- #209: vbintr bare-stem matching + pii_to_past + rule ordering ---
check "vbintr: bare stem now matches (past tense)"    "Il venis."                    "Li venis."
check "vbintr: post-verbal subject stays nominative"  "Venis la kato."               "Venis la kato."
check "vbintr: quantified post-verbal subject"        "Venis multa homi."            "Venis multaj homoj."
check "vbintr: interrogative determiner subject"      "Qua venis?"                   "Kiu venis?"
check "vbintr: coordinated bare subjects"             "Venis kelka homi e kelka kati." "Venis kelkaj homoj kaj kelkaj katoj."
check "vbintr: coordinated determined subjects"       "Venis la kato e la hundo."    "Venis la kato kaj la hundo."
check "vbintr: another bare-stem verb"                "Il jacas."                    "Li kuŝas."
check "vbintr: past tense on another bare-stem verb"  "Il mortis."                   "Li mortis."

echo
echo "$pass passed, $fail failed"
[ "$fail" -eq 0 ]
