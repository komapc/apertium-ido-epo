# Comprehensive Fix Plan for Ido-Esperanto Translation Errors

**Date:** December 20, 2025  
**Test Sentence:** "Ido esas konstruktita linguo derivante de Reformita Esperanto..."

## Executive Summary

After translating a comprehensive test sentence and analyzing the errors, we identified **8 major categories of issues**. This document provides a detailed fix plan with priorities, time estimates, and specific actions.

**Current Translation Output (after recompilation):**
```
Ido estas #Konstruita lingvo *derivante de Reformita Esperanton (reformita lingvon 
konstruas de Esperanto, faras @d @l #originalo @kreint de Esperanto) adoptas kiel 
Esperanto reformas en #Parizo @d @l #Delegitaro, delegacio  je @l #24-a de oktobro 
*1907. Ido *kreesis por havi malmultan #Polisemio, estas #sate konciza, @facil 
#Lerno #E uzebla. @Ol *kreesis por esti #Internacia planlingvo por personoj de 
diversaj originoj #E estas @l *maxim @sucecoz de @l multa Esperanto-derivaĵoj, 
*quin @on *nomizas *Esperantidoj@.
```

**Error Legend:**
- `@` = Word not in bilingual dictionary (bidix)
- `*` = Word not recognized by morphological analyzer (monodix)
- `#` = Word recognized but translation has issues

---

## Priority 1: CRITICAL (Block Translation Quality)

### 1.1 Add Disambiguation Rules (CG3) for Ido
**Problem:** The `ido-epo` pipeline has NO disambiguation step. When words have multiple morphological readings, the first reading is used, which is often wrong.

**Example:**
```bash
$ echo "la" | lt-proc ido-epo.automorf.bin
^la/l<adj>/la<det>$   # Two readings: adjective OR determiner

$ echo "la" | lt-proc ido-epo.automorf.bin | apertium-pretransfer -n | lt-proc -b ido-epo.autobil.bin
^l<adj>/@l<adj>$      # First reading picked → WRONG → bidix lookup fails
```

**Solution:**
1. Create `apertium-ido-epo.ido.rlx` with CG3 disambiguation rules
2. Add `cg-proc` step to `modes.xml` for `ido-epo` mode

**File Changes:**
- Create: `apertium-ido-epo.ido.rlx`
- Modify: `modes.xml`

**Time Estimate:** 2-4 hours

**Key Rules Needed:**
```cg3
# Select determiner "la" before nouns/adjectives
SELECT la IF (1 N OR ADJ);

# Remove adjective reading "l" when it's the article
REMOVE l-adj IF (0 la-det);
```

---

### 1.2 Fix "l'" Entry in Monodix (Elided Article)
**Problem:** In Ido, "l'" is the elided form of "la" (used before vowels). Currently defined as **preposition** instead of **determiner**.

**Current (WRONG):**
```xml
<e lm="l'">
  <i>l'</i>
  <par n="__pr" />   <!-- WRONG: preposition -->
</e>
```

**Required (CORRECT):**
```xml
<e lm="l'">
  <i>l'</i>
  <par n="__det" />  <!-- CORRECT: determiner -->
</e>
```

**Solution:**
1. Add entry to source JSON: `projects/data/sources/source_function_words.json`
2. Regenerate dictionaries

**Source Entry to Add:**
```json
{
  "lemma": "l'",
  "pos": "det",
  "morphology": { "paradigm": "__det" },
  "translations": [{ "target": "la", "target_pos": "det", "confidence": 1.0 }],
  "source": "manual"
}
```

**Time Estimate:** 15 minutes

---

### 1.3 Extend Noun Paradigm with Accusative Case
**Problem:** The `o__n` paradigm only handles nominative case. Accusative (-n suffix) is missing.

**Current Paradigm:**
```xml
<pardef n="o__n">
  <e><p><l>o</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
  <e><p><l>i</l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>
</pardef>
```

**Extended Paradigm:**
```xml
<pardef n="o__n">
  <!-- Nominative -->
  <e><p><l>o</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
  <e><p><l>i</l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>
  <!-- Accusative -->
  <e><p><l>on</l><r><s n="n"/><s n="sg"/><s n="acc"/></r></p></e>
  <e><p><l>in</l><r><s n="n"/><s n="pl"/><s n="acc"/></r></p></e>
</pardef>
```

**File:** `projects/data/pardefs.xml`

**Time Estimate:** 30 minutes (including testing)

---

### 1.4 Extend Verb Paradigm with Passive Voice
**Problem:** Ido uses `-es-` infix for passive voice. This is not captured in the paradigm.

**Ido Passive Voice Formation:**
- Active: `krear` (to create)
- Passive infinitive: `kreesar` (to be created)
- Passive present: `kreesas` (is being created)
- Passive past: `kreesis` (was created) ← **This appears in our test**
- Passive future: `kreesos` (will be created)
- Passive conditional: `kreesus` (would be created)

**Extended Paradigm:**
```xml
<pardef n="ar__vblex">
  <!-- Active voice (existing) -->
  <e><p><l>ar</l><r><s n="vblex"/><s n="inf"/></r></p></e>
  <e><p><l>as</l><r><s n="vblex"/><s n="pri"/></r></p></e>
  <e><p><l>is</l><r><s n="vblex"/><s n="pii"/></r></p></e>
  <e><p><l>os</l><r><s n="vblex"/><s n="fti"/></r></p></e>
  <e><p><l>us</l><r><s n="vblex"/><s n="cni"/></r></p></e>
  <e><p><l>ez</l><r><s n="vblex"/><s n="imp"/></r></p></e>
  <e><p><l>ita</l><r><s n="vblex"/><s n="pp"/></r></p></e>
  
  <!-- Passive voice (NEW) -->
  <e><p><l>esar</l><r><s n="vblex"/><s n="pasv"/><s n="inf"/></r></p></e>
  <e><p><l>esas</l><r><s n="vblex"/><s n="pasv"/><s n="pri"/></r></p></e>
  <e><p><l>esis</l><r><s n="vblex"/><s n="pasv"/><s n="pii"/></r></p></e>
  <e><p><l>esos</l><r><s n="vblex"/><s n="pasv"/><s n="fti"/></r></p></e>
  <e><p><l>esus</l><r><s n="vblex"/><s n="pasv"/><s n="cni"/></r></p></e>
  <e><p><l>esez</l><r><s n="vblex"/><s n="pasv"/><s n="imp"/></r></p></e>
</pardef>
```

**Additional Required:**
1. Add `<sdef n="pasv"/>` to symbol definitions
2. Add transfer rules to convert passive to Esperanto (likely using "esti + participle" construction)

**File:** `projects/data/pardefs.xml`

**Time Estimate:** 1-2 hours (including transfer rules)

---

### 1.5 Extend Verb Paradigm with Participles
**Problem:** Present active participle (`-ante`) is not recognized.

**Example:**
```bash
$ echo "derivante" | lt-proc ido-epo.automorf.bin
^derivante/*derivante$   # Unknown!
```

**Ido Participles:**
- Present active: `-ante` (derivante = deriving)
- Past active: `-inte` (derivinte = having derived)
- Future active: `-onte` (derivonte = about to derive)
- Present passive: `-ate` (derivate = being derived)
- Past passive: `-ite` (derivite = having been derived)
- Future passive: `-ote` (derivote = about to be derived)

**Extended Paradigm (add to ar__vblex):**
```xml
<!-- Active participles -->
<e><p><l>ante</l><r><s n="vblex"/><s n="pprs"/></r></p></e>
<e><p><l>inte</l><r><s n="vblex"/><s n="ppst"/></r></p></e>
<e><p><l>onte</l><r><s n="vblex"/><s n="pfut"/></r></p></e>
<!-- Passive participles -->
<e><p><l>ata</l><r><s n="vblex"/><s n="pprs"/><s n="pasv"/></r></p></e>
<e><p><l>ita</l><r><s n="vblex"/><s n="ppst"/><s n="pasv"/></r></p></e>
<e><p><l>ota</l><r><s n="vblex"/><s n="pfut"/><s n="pasv"/></r></p></e>
```

**File:** `projects/data/pardefs.xml`

**Time Estimate:** 30 minutes

---

## Priority 2: HIGH (Significant Coverage Gaps)

### 2.1 Add Cardinal Number Handling
**Problem:** Plain numbers like `1907`, `24` are not recognized.

**Current:**
```bash
$ echo "1907" | lt-proc ido-epo.automorf.bin
^1907/*1907$   # Unknown!
```

**Solution:**
Use the existing `num_regex` paradigm in `pardefs.xml`:
```xml
<pardef n="num_regex">
  <e>
    <re>[0-9]+([.,][0-9]+)*</re>
    <p>
      <l/>
      <r><s n="num"/><s n="ciph"/><s n="sp"/><s n="nom"/></r>
    </p>
  </e>
</pardef>
```

This paradigm exists but may not be active. Need to verify the monodix generation includes it.

**Time Estimate:** 30 minutes

---

### 2.2 Add Missing Function Words
**Problem:** Several common Ido function words are not in the bidix.

**Missing words identified:**
| Ido | Esperanto | POS | Note |
|-----|-----------|-----|------|
| `maxim` | `plej` | adv | Superlative marker |
| `quin` | `kiun` | prn | "which" accusative |
| `on` | `oni` | prn | "one" (impersonal pronoun) |
| `Ol` | `ĝi` | prn | "it" pronoun |

**Solution:** Add to source JSON and regenerate.

**File:** `projects/data/sources/source_function_words.json`

**Time Estimate:** 30 minutes

---

### 2.3 Add Missing Verbs
**Problem:** Verb "nomizar" (to name) is not in the dictionary.

**Example:**
```bash
$ echo "nomizas" | lt-proc ido-epo.automorf.bin
^nomizas/*nomizas$   # Unknown!
```

**Solution:** Add to source JSON:
```json
{
  "lemma": "nomizar",
  "pos": "v",
  "morphology": { "paradigm": "ar__vblex" },
  "translations": [{ "target": "nomi", "target_pos": "v", "confidence": 1.0 }],
  "source": "manual"
}
```

**Time Estimate:** 15 minutes per verb

---

### 2.4 Add Correlative Case Paradigms
**Problem:** Correlatives (qua, quo, qui, etc.) don't have accusative forms.

**Ido Correlatives with case:**
- `qua` → `quan` (which, accusative)
- `ula` → `ulan` (some, accusative)
- etc.

**Solution:** Create a correlative paradigm with accusative.

**File:** `projects/data/pardefs.xml`

**Time Estimate:** 1 hour

---

## Priority 3: MEDIUM (Quality Improvements)

### 3.1 Fix Multi-word Expression Parsing
**Problem:** "konstruktita linguo" is parsed as a single proper noun, losing grammatical information.

```bash
$ echo "konstruktita linguo" | lt-proc ido-epo.automorf.bin
^konstruktita linguo/konstruktita linguo<np>$   # Parsed as proper noun
```

**Impact:** Cannot properly inflect or translate grammatically.

**Solution:** Review multi-word expression entries and consider removing overly general patterns.

**Time Estimate:** 1-2 hours

---

### 3.2 Add Adjective Accusative Forms
**Problem:** Adjectives also take `-n` suffix in accusative context in Ido.

**Extended Paradigm:**
```xml
<pardef n="a__adj">
  <e><p><l>a</l><r><s n="adj"/><s n="nom"/></r></p></e>
  <e><p><l>an</l><r><s n="adj"/><s n="acc"/></r></p></e>
</pardef>
```

**Time Estimate:** 30 minutes

---

## Implementation Order

### Phase 1: Quick Wins (1-2 hours total)
1. ✅ Recompile dictionaries (DONE)
2. Fix l' entry (15 min)
3. Add missing function words (30 min)
4. Add missing verbs (30 min)

### Phase 2: Paradigm Extensions (2-4 hours total)
1. Add accusative to noun paradigm (30 min)
2. Add passive voice to verb paradigm (1 hour)
3. Add participles to verb paradigm (30 min)
4. Add number handling (30 min)

### Phase 3: Disambiguation (2-4 hours total)
1. Create CG3 disambiguation rules (2-3 hours)
2. Update modes.xml to include disambiguation step (30 min)
3. Test and refine rules (1 hour)

### Phase 4: Testing & Validation
1. Rerun test sentence
2. Run full test suite
3. Test bidirectional translation

---

## Regeneration Workflow

After making changes, regenerate dictionaries using:

```bash
# 1. Update source JSON files in projects/data/sources/
# 2. Update pardefs.xml if paradigms changed
# 3. Run regeneration pipeline
cd /home/mark/apertium-dev/projects/data
python3 scripts/regenerate_all.py --validate-xml

# 4. Copy generated files
cp generated/ido.ido.dix ../../apertium/apertium-ido-epo/apertium-ido.ido.dix
cp generated/ido-epo.ido-epo.dix ../../apertium/apertium-ido-epo/apertium-ido-epo.ido-epo.dix

# 5. Recompile
cd ../../apertium/apertium-ido-epo
make clean && make

# 6. Test
echo "Ido esas konstruktita linguo" | apertium -d . ido-epo
```

---

## Files Requiring Changes

| File | Changes | Priority |
|------|---------|----------|
| `projects/data/pardefs.xml` | Add accusative, passive, participles | P1 |
| `projects/data/sources/source_function_words.json` | Add l', maxim, on, Ol, quin | P1-P2 |
| `apertium-ido-epo.ido.rlx` | Create disambiguation rules | P1 |
| `modes.xml` | Add cg-proc to ido-epo mode | P1 |
| `Makefile.am` | Add rlx compilation | P1 |

---

## Success Metrics

After implementing all fixes, the test sentence should translate to:
```
Ido estas konstruita lingvo derivanta de Reformita Esperanto (reformita lingvo 
konstruita de Esperanto, farita de la originala kreinto de Esperanto) adoptita 
kiel Esperanto reformita en Parizo de la Delegitaro je la 24-a de oktobro 1907. 
Ido kreiĝis por havi malmultan polisemion, estas sufiĉe konciza, facile lernebla 
kaj uzebla. Ĝi kreiĝis por esti Internacia helpa lingvo por personoj de diversaj 
originoj kaj estas la plej sukcesa de la multaj Esperanto-derivaĵoj, kiun oni 
nomas Esperantidoj.
```

**Current error count:** ~25+ errors
**Target error count:** <5 errors

