# Test Results - December 8, 2025

**Test Corpus Location:** `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/ido-epo-test-sentences.txt`

This document contains the current translation results for all test sentences in the corpus file, along with a detailed error analysis.

---

## Sentence 1: Historical/Linguistic Description of Ido

### Input (Ido)
```
Ido esas konstruktita linguo derivante de Reformita Esperanto (reformita linguo konstruktita de Esperanto, facita da la originala kreinto di Esperanto) adoptita kom Esperanto reformita en Paris da la Delegitaro (Délégation pour l'adoption d'une langue auxiliaire internationale) ye la 24ma di oktobro 1907. Ido kreesis por havar poka polisemio, esas sat konciza, facile lernebla e uzebla. Ol kreesis por esar Internaciona auxiliara linguo por personi de diversa origini e esas la maxim sucesoza de la multa Esperanto-derivaji, quin on nomizas Esperantidoj.
```

### Current Output (Esperanto)
```
Ido estas #Konstruita lingvo *derivante @de Reformita Esperanton (reformita lingvon konstruas @de Esperanto, faras #de ↓ (indikante aganton) #la ↓ #originalo #kereint @di Esperanto) adoptas #keom Esperanto reformas #en ↓ #Parizo #de ↓ (indikante aganton) #la ↓ #Delegitaro, delegacio (*Délégation *pour #L'*adoption #D'*une *langue *auxiliaire *internationale) #jee #la ↓ #24-a de oktobro *1907. Ido *kreesis @por havi malmultan #Polisemio, estas #sate konciza, @facil *lernebla kaj *uzebla. @Ol *kreesis @por esti #Internacia planlingvo @por personoj @de diversaj originoj kaj estas #la ↓ *maxim #seucecoz @de #la ↓ multa Esperanto-derivaĵoj, *quin @on *nomizas *Esperantidoj@.
```

### Expected Translation (Reference)
```
Ido estas konstruita lingvo derivanta de Reformita Esperanto (reformita lingvo konstruita de Esperanto, farita de la originala kreinto de Esperanto) adoptita kiel Esperanto reformita en Parizo de la Delegitaro (Délégation pour l'adoption d'une langue auxiliaire internationale) je la 24-a de oktobro 1907. Ido kreiĝis por havi malmultan polisemion, estas sufiĉe konciza, facile lernebla kaj uzebla. Ĝi kreiĝis por esti Internacia helpa lingvo por personoj de diversaj originoj kaj estas la plej sukcesa de la multaj Esperanto-derivaĵoj, kiujn oni nomas Esperantidoj.
```

### Error Analysis

#### Unknown Words (marked with `*`)
1. `*derivante` → should be "derivanta" (present participle)
2. `*kreesis` → should be "kreiĝis" (past tense, reflexive)
3. `*lernebla` → should be "lernebla" (learnable - missing from dictionary)
4. `*uzebla` → should be "uzebla" (usable - missing from dictionary)
5. `*maxim` → should be "plej" (most, superlative)
6. `*quin` → should be "kiujn" (which, relative pronoun accusative)
7. `*on` → should be "oni" (one, impersonal pronoun)
8. `*nomizas` → should be "nomas" (names, calls)
9. `*Esperantidoj` → should be "Esperantidoj" (proper noun)
10. `*1907` → year not recognized

#### Translation Rule Issues (marked with `#`)
1. `#Konstruita` → incorrect capitalization, should be "konstruita"
2. `#de ↓` → incorrect handling of "da" (by/from agent marker)
3. `#la ↓` → incorrect handling of "la" (definite article)
4. `#originalo #kereint` → incorrect handling of "originala kreinto" (original creator)
   - Should be: "originala kreinto" → "originala kreinto"
   - Issue: Split incorrectly, "kereint" should be "kreinto"
5. `#keom` → incorrect handling of "kom" (as/like)
   - Should be: "kom" → "kiel"
6. `#jee` → incorrect handling of "ye" (on/at)
   - Should be: "ye" → "je"
7. `#Polisemio` → incorrect capitalization, should be "polisemion"
8. `#sate` → incorrect handling of "sat" (quite/enough)
   - Should be: "sat" → "sufiĉe"
9. `#seucecoz` → incorrect handling of "sucesoza" (successful)
   - Should be: "sucesoza" → "sukcesa"
   - Issue: Typo in analysis result

#### Proper Noun Issues (marked with `@`)
1. `@de` → should be "de" (preposition)
2. `@di Esperanto` → should be "de Esperanto" (of Esperanto)
3. `@por` (multiple) → should be "por" (for)
4. `@facil` → should be "facile" (easily)
5. `@Ol` → should be "Ĝi" (It)
6. `@on` → should be "oni" (one/they)

#### Grammar Issues
1. `lingvon` → should be "lingvo" (incorrect accusative case)
2. `konstruas` → should be "konstruita" (should be past participle, not present)
3. `faras` → should be "farita" (should be past participle, not present)
4. `adoptas` → should be "adoptita" (should be past participle, not present)
5. `reformas` → should be "reformita" (should be past participle, not present)
6. `multa` → should be "multaj" (many, plural form)
7. `Esperanton` → should be "Esperanto" (proper noun, incorrect accusative)

#### Word Order Issues (marked with `↓`)
- Multiple instances where word order is incorrect
- Marker `↓` indicates position issues

---

## Sentence 2: Discussion About Ido Community Meeting

### Input (Ido)
```
Hodie partoprenis kin Idisti la saturdiala video-konfero. Ni diskutis inter altro kelka detali dil internaciona Ido-renkontro 2025 e la nova vorti dil google-grupo Linguo. Restas la questiono kad esas bona remplacigar od adjuntar ja existanta vorti per nova vorti por la sama kozo.
```

### Current Output (Esperanto)
```
Hodiaŭ partoprenas #kvin Idistoj #la ↓ *saturdia Video-#keonfer. #Ni diskutas inter #alio kelkaj detaloj #de l'internacia Ido-@renkontr *2025 kaj #la ↓ #nova ↓ vortoj #de la #Google-#grupo ↓ Lingvo. Restas #la ↓ demandon #ĉu estas bona *remplacigar @od aldoni #jam #kajxistant vortoj @per #nova ↓ vortoj @por #la ↓ sama aĵo@.
```

### Expected Translation (Reference)
```
Hodiaŭ partoprenis kvin Idistoj la sabata videokonferenco. Ni diskutis inter alie kelkajn detalojn de la internacia Ido-renkontro 2025 kaj la novajn vortojn de la google-grupo Lingvo. Restas la demando ĉu estas bona anstataŭigi aŭ aldoni jam ekzistantajn vortojn per novaj vortoj por la sama afero.
```

### Error Analysis

#### Unknown Words (marked with `*`)
1. `*saturdia` → should be "sabata" (Saturday)
2. `*2025` → year not recognized
3. `*remplacigar` → should be "anstataŭigi" (to replace)

#### Translation Rule Issues (marked with `#`)
1. `#kvin` → should be "kvin" (five) - analysis issue, not unknown
2. `#la ↓` → incorrect handling of "la" (definite article)
3. `#keonfer` → incorrect handling of "konfero" (conference)
   - Should be: "video-konfero" → "videokonferenco"
   - Issue: Split and incorrectly analyzed
4. `#Ni` → should be "Ni" (We) - capitalization preserved, but tense wrong
5. `#alio` → incorrect handling of "altro" (other)
   - Should be: "altro" → "alie"
6. `#de l'internacia` → should be "de la internacia" (of the international)
7. `#nova ↓` → incorrect handling of "nova" (new)
8. `#Google-#grupo` → incorrect handling of compound "google-grupo"
9. `#demandon` → should be "demando" (question, nominative not accusative)
10. `#ĉu` → correctly translated from "kad", but formatting issue
11. `#jam` → should be "jam" (already) - correct but formatting issue
12. `#kajxistant` → typo, should be "ekzistantajn" (existing, accusative plural)

#### Proper Noun Issues (marked with `@`)
1. `@renkontr` → should be "renkontro" (meeting/encounter)
2. `@od` → should be "aŭ" (or)
3. `@per` → should be "per" (by/with)

#### Grammar Issues
1. `partoprenas` → should be "partoprenis" (wrong tense: present vs past)
2. `diskutas` → should be "diskutis" (wrong tense: present vs past)
3. `detaloj` → should be "detalojn" (missing accusative case)
4. `vortoj` → should be "vortojn" (missing accusative case)
5. `demandon` → should be "demando" (incorrect accusative, should be nominative)
6. `ekzistantajn` → missing, shows as `#kajxistant` (typo + missing accusative plural)

#### Compound Word Issues
1. `video-konfero` → split into `Video-#keonfer`
   - Should be: "videokonferenco" (one word)
   - Issue: Compound split incorrectly
2. `Ido-renkontro` → split into `Ido-@renkontr`
   - Should be: "Ido-renkontro" (hyphenated compound)
   - Issue: Second part analyzed incorrectly
3. `google-grupo` → split into `#Google-#grupo`
   - Should be: "google-grupo" (hyphenated compound)
   - Issue: Both parts analyzed separately

#### Tense Issues (Critical)
1. `partoprenas` (present) → should be `partoprenis` (past)
2. `diskutas` (present) → should be `diskutis` (past)

---

## Error Summary Statistics

### Sentence 1
- **Total words:** ~85 words
- **Unknown words:** 10 instances (12%)
- **Translation rule errors:** 9 instances (11%)
- **Proper noun handling issues:** 6 instances (7%)
- **Grammar errors:** 7 instances (8%)
- **Overall error rate:** ~38%

### Sentence 2
- **Total words:** ~35 words
- **Unknown words:** 3 instances (9%)
- **Translation rule errors:** 12 instances (34%)
- **Proper noun handling issues:** 3 instances (9%)
- **Grammar errors:** 6 instances (17%)
- **Tense errors:** 2 instances (6%)
- **Overall error rate:** ~75%

### Overall Corpus Statistics
- **Total sentences:** 2
- **Average error rate:** ~56%
- **Most common error type:** Translation rule issues
- **Critical errors:** Tense handling (present vs past)

---

## Error Categories

### 1. Missing Dictionary Entries
- `lernebla`, `uzebla` - Common adjectives missing
- `saturdia` → `sabata` - Day name missing
- `remplacigar` → `anstataŭigi` - Verb missing

### 2. Morphological Analysis Failures
- Verb tense not recognized (present vs past)
- Accusative case not applied correctly
- Compound words split incorrectly

### 3. Translation Rule Issues
- Prepositions: `kom` → `kiel`, `ye` → `je`
- Function words: `la` handling
- Word order issues (marked with `↓`)

### 4. Grammar Issues
- Case errors: accusative missing or incorrectly applied
- Tense errors: present vs past confusion
- Plural forms: `multa` → `multaj`

### 5. Compound Word Handling
- Hyphenated compounds incorrectly split
- Each part analyzed separately instead of as unit

---

## Comparison with Previous Results

### Improvements
- `hodiaŭ` correctly translated from `hodie`
- `kvin` correctly identified (though marked with `#`)
- `ĉu` correctly translated from `kad`
- `aldoni` correctly translated from `adjuntar`
- Some proper noun handling improved

### Regressions/Still Present
- Tense errors (present vs past) - **Critical issue**
- Compound word splitting
- Accusative case marking
- Some translation rule issues remain

---

## Recommendations

### High Priority
1. **Fix tense recognition** - Critical issue affecting sentence 2
   - `partoprenas` → `partoprenis`
   - `diskutas` → `diskutis`

2. **Fix compound word handling**
   - `video-konfero` → `videokonferenco`
   - `Ido-renkontro` → preserve hyphenated form
   - `google-grupo` → preserve hyphenated form

3. **Add missing dictionary entries**
   - `lernebla` → `lernebla`
   - `uzebla` → `uzebla`
   - `saturdia` → `sabata`

### Medium Priority
4. **Fix accusative case marking**
   - `detaloj` → `detalojn`
   - `vortoj` → `vortojn`
   - `demandon` → `demando` (should not be accusative)

5. **Fix translation rules for prepositions**
   - `kom` → `kiel`
   - `ye` → `je`

6. **Fix plural forms**
   - `multa` → `multaj`

### Low Priority
7. **Improve proper noun handling**
8. **Fix capitalization issues**
9. **Improve word order**

---

## File Location Documentation

**Test Corpus File:**
- **Path:** `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/ido-epo-test-sentences.txt`
- **Purpose:** Contains test sentences for evaluating translation quality
- **Format:** Plain text with comments (lines starting with `#`)
- **Directions:** Currently Ido → Esperanto
- **Last Updated:** Contains 2 sentences as of December 8, 2025

**Related Files:**
- `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/README.md` - Corpus documentation
- `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/TRANSLATIONS.md` - Previous translation results
- `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/test_results_current.txt` - Current test results
- `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/test_results_after_regeneration.txt` - Previous regeneration results

---

**Generated:** December 8, 2025
**Apertium Version:** Latest (tested with `apertium -d . ido-epo`)

