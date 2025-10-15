# Proposed Test Sentences for PR Fixes

**Based on:** Review of latest 20 PRs to apertium-ido-epo  
**Date:** October 15, 2025

---

## Test Sentences by Category

### 1. CRITICAL BUG FIXES (PR #24)

#### Ido Language Name (was: tradukar bug)
```
INPUT:  Me lernas Ido
EXPECT: Mi lernas Ido (not "mi lernas tradukar")

INPUT:  La gramatiko di Ido
EXPECT: La gramatiko de Ido (not "de tradukar")

INPUT:  Lua himno esas bela
EXPECT: Ĝia himno estas bela (not "sia himno")
```

**Grammar tested:** Proper language name translation, possessive pronoun (lua → ĝia vs incorrect sia)

---

### 2. INTRANSITIVE VERBS (PR #23)

#### Post-verbal subjects stay nominative
```
INPUT:  Norde jacas Oceano Atlantiko
EXPECT: Norde kuŝas Oceano Atlantiko (not "Oceanon")

INPUT:  En la chambro dormis la infanti
EXPECT: En la ĉambro dormis la infanoj (not "infanojn")

INPUT:  Ye la pordo staris granda kato
EXPECT: Ĉe la pordo staris granda kato (not "grandan katon")
```

**Grammar tested:** Intransitive verbs don't mark post-verbal subjects with accusative

**Verbs covered:** jacar (kuŝi), dormar (dormi), star (stari)

---

### 3. INFINITIVE PRESERVATION (PR #23)

#### Infinitives remain infinitives
```
INPUT:  La populi komencis okupar la lando
EXPECT: La popoloj komencis okupi la lando (not "okupas")

INPUT:  Il volas manjar la pomo
EXPECT: Li volas manĝi la pomon (not "manĝas")

INPUT:  Ni devas laborar
EXPECT: Ni devas labori (not "laboras")
```

**Grammar tested:** Infinitive forms preserved in auxiliary + verb constructions

**Impact:** Affects ALL auxiliary verbs (volar, devar, komencar, etc.)

---

### 4. PRODUCTIVE SUFFIX: -eso → -eco (PR #22)

#### Abstract quality nouns
```
INPUT:  La richeso di la lando
EXPECT: La riĉeco de la lando

INPUT:  La beleso di la naturo
EXPECT: La beleco de la naturo

INPUT:  Sekureso esas importanta
EXPECT: Sekureco estas grava
```

**Transformation tested:** Automatic -eso → -eco for ANY word (post-generator rule)

**Productivity:** Works for unknown words too

---

### 5. PRODUCTIVE SUFFIX: -ala → -a (PR #22)

#### Relational adjectives
```
INPUT:  La mondala ekonomio
EXPECT: La monda ekonomio

INPUT:  La republikala sistemo
EXPECT: La republika sistemo

INPUT:  La kulturala richeso
EXPECT: La kultura riĉeco

INPUT:  La demografiala krizo
EXPECT: La demografia krizo

INPUT:  La parlamentala demokratio
EXPECT: La parlamenta demokratio
```

**Transformation tested:** Automatic -ala → -a for ANY adjective (post-generator rule)

**Examples from PRs:** parlamentala, mondala, republikala, kulturala, demografiala

---

### 6. PARTICIPLES (PR #18)

#### Active participles
```
INPUT:  La laboranta homo
EXPECT: La laboranta homo

INPUT:  La fininta laboro
EXPECT: La fininta laboro

INPUT:  La venonta yari
EXPECT: La venontaj jaroj
```

#### Passive participles
```
INPUT:  La amata kanto
EXPECT: La amata kanto

INPUT:  La skribita libro
EXPECT: La skribita libro

INPUT:  La farota tasko
EXPECT: La farota tasko
```

**Morphology tested:** 6 participle forms (present/past/future × active/passive)

---

### 7. ELIDED ARTICLE (PR #19)

#### l' before vowels
```
INPUT:  l'urbo esas granda
EXPECT: la urbo estas granda

INPUT:  l'homo venas
EXPECT: la homo venas
```

**Feature tested:** Recognition of elided article `l'`

---

### 8. NEW VOCABULARY (PR #19, #22, #17)

#### Common words
```
INPUT:  La domo esas tre granda
EXPECT: La domo estas tre granda

INPUT:  Segun la legi
EXPECT: Laŭ la leĝo

INPUT:  La himno di Francia
EXPECT: La himno de Francio

INPUT:  En la Mezepoko
EXPECT: En la Mezepoko
```

#### Geographic/quantitative
```
INPUT:  La chefurbo di Francia esas Paris
EXPECT: La ĉefurbo de Francio estas Parizo

INPUT:  La distanco esas cent kilometri
EXPECT: La distanco estas cent kilometroj

INPUT:  La teritorio esas vasta
EXPECT: La teritorio estas vasta

INPUT:  La habitanti di la urbo
EXPECT: La loĝantoj de la urbo
```

**Words tested:** tre, segun, himno, Mezepoko, chefurbo, kilometro, teritorio, habitanto

---

### 9. FUNCTION WORDS - PREPOSITIONS (PR #5)

```
INPUT:  La libro dil me
EXPECT: La libro de mi

INPUT:  De la matino til la vespero
EXPECT: De la matino ĝis la vespero

INPUT:  Granda kom elefanto
EXPECT: Granda kiel elefanto

INPUT:  Ye la horo tri
EXPECT: Je la horo tri

INPUT:  Su la tablo
EXPECT: Sub la tablo
```

**Mappings tested:** dil→de, til→ĝis, kom→kiel, ye→je, su→sub

---

### 10. FUNCTION WORDS - CONJUNCTION & ADVERBS (PR #5)

```
INPUT:  La kato ed la hundo
EXPECT: La kato kaj la hundo

INPUT:  Me anke venas
EXPECT: Mi ankaŭ venas

INPUT:  Mem la regi savas
EXPECT: Eĉ la reĝo scias
```

**Mappings tested:** ed→kaj, anke→ankaŭ, mem→eĉ

---

### 11. DIRECTIONAL ADVERBS (PR #5)

```
INPUT:  Germania jacas este
EXPECT: Germanio kuŝas oriente

INPUT:  Oceano jacas weste
EXPECT: Oceano kuŝas okcidente

INPUT:  Belgia jacas norde
EXPECT: Belgio kuŝas norde

INPUT:  Francia jacas sude
EXPECT: Francio kuŝas sude
```

**Mappings tested:** este→oriente, weste→okcidente, norde→norde, sude→sude

---

### 12. CORE ADVERBS (PR #6)

```
INPUT:  Il laboras forte
EXPECT: Li laboras forte

INPUT:  Il venis itere
EXPECT: Li venis denove

INPUT:  Quale ol esas
EXPECT: Kiel ĝi estas

INPUT:  Ordinare me trinkas kafeo
EXPECT: Ordinare mi trinkas kafeon
```

**Critical fix:** Stem-based mappings (fort→forte, iter→denove, qual→kiel, ordinar→ordinare)

**Impact:** Fixed 71% of "missing" words in one PR

---

### 13. COORDINATION (PR #8)

```
INPUT:  La kato kaj la hundo kuras
EXPECT: La kato kaj la hundo kuras (subjects stay nominative)

INPUT:  Me vidas la kato e la hundo
EXPECT: Mi vidas la katon kaj la hundon (objects get accusative)
```

**Grammar tested:** Coordinated elements receive same case marking

---

## Summary Statistics

- **Total test sentences:** 54
- **Grammar rules tested:** 11 major fixes
- **Productive suffixes tested:** 2 (-eso→-eco, -ala→-a)
- **Vocabulary items tested:** 30+
- **Function words tested:** 15+

---

## Notes

1. **Markers in output:**
   - `*` = unknown word (not in monolingual dictionary)
   - `#` = ambiguous reading
   - `@` = generation error

2. **Some tests may show markers** for words not yet in monolingual dictionaries, but the TRANSFORMATIONS should still be correct.

3. **Priority:** Grammar fixes > Suffix rules > Vocabulary

---

## Recommendation

Add these as a new test suite: `test/ido-epo-pr-regression-input.txt`

Purpose: Prevent regression on fixes from the 20 most recent PRs.

