# Complete Error List - December 8, 2025

**Test Corpus:** `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/ido-epo-test-sentences.txt`

This document lists all translation errors found in the test sentences.

---

## Sentence 1 Errors

### Unknown Words (`*` marker) - 10 errors
1. `*derivante` → should be "derivanta"
2. `*kreesis` → should be "kreiĝis"
3. `*lernebla` → should be "lernebla" (missing from dictionary)
4. `*uzebla` → should be "uzebla" (missing from dictionary)
5. `*maxim` → should be "plej"
6. `*quin` → should be "kiujn"
7. `*on` → should be "oni"
8. `*nomizas` → should be "nomas"
9. `*Esperantidoj` → should be "Esperantidoj"
10. `*1907` → year not recognized

### Translation Rule Issues (`#` marker) - 9 errors
1. `#Konstruita` → incorrect capitalization
2. `#de ↓` → incorrect handling of "da" (by/from agent)
3. `#la ↓` (multiple) → incorrect handling of "la" (definite article)
4. `#originalo #kereint` → should be "originala kreinto"
5. `#keom` → should be "kiel" (from "kom")
6. `#jee` → should be "je" (from "ye")
7. `#Polisemio` → incorrect capitalization, should be "polisemion"
8. `#sate` → should be "sufiĉe" (from "sat")
9. `#seucecoz` → should be "sukcesa" (from "sucesoza", typo in analysis)

### Proper Noun Issues (`@` marker) - 6 errors
1. `@de` → should be "de"
2. `@di Esperanto` → should be "de Esperanto"
3. `@por` (multiple) → should be "por"
4. `@facil` → should be "facile"
5. `@Ol` → should be "Ĝi"
6. `@on` → should be "oni"

### Grammar Errors - 7 errors
1. `lingvon` → should be "lingvo" (incorrect accusative)
2. `konstruas` → should be "konstruita" (present → past participle)
3. `faras` → should be "farita" (present → past participle)
4. `adoptas` → should be "adoptita" (present → past participle)
5. `reformas` → should be "reformita" (present → past participle)
6. `multa` → should be "multaj" (singular → plural)
7. `Esperanton` → should be "Esperanto" (incorrect accusative on proper noun)

### Word Order Issues - Multiple
- Multiple `↓` markers indicating word order problems

**Sentence 1 Total Errors: ~32 errors**

---

## Sentence 2 Errors

### Unknown Words (`*` marker) - 3 errors
1. `*saturdia` → should be "sabata"
2. `*2025` → year not recognized
3. `*remplacigar` → should be "anstataŭigi"

### Translation Rule Issues (`#` marker) - 12 errors
1. `#kvin` → should be "kvin" (analysis issue, word is known)
2. `#la ↓` (multiple) → incorrect handling of "la"
3. `#keonfer` → should be "konferenco" (from "video-konfero")
4. `#Ni` → capitalization ok, but tense wrong
5. `#alio` → should be "alie" (from "altro")
6. `#de l'internacia` → should be "de la internacia"
7. `#nova ↓` (multiple) → incorrect handling of "nova"
8. `#Google-#grupo` → incorrect compound handling
9. `#demandon` → should be "demando" (incorrect accusative)
10. `#ĉu` → correct translation but formatting issue
11. `#jam` → correct but formatting issue
12. `#kajxistant` → typo, should be "ekzistantajn"

### Proper Noun Issues (`@` marker) - 3 errors
1. `@renkontr` → should be "renkontro"
2. `@od` → should be "aŭ"
3. `@per` → should be "per"

### Grammar Errors - 6 errors
1. `partoprenas` → should be "partoprenis" (present → past) **CRITICAL**
2. `diskutas` → should be "diskutis" (present → past) **CRITICAL**
3. `detaloj` → should be "detalojn" (missing accusative)
4. `vortoj` → should be "vortojn" (missing accusative)
5. `demandon` → should be "demando" (incorrect accusative)
6. Missing accusative plural on `ekzistantajn` (shows as typo `kajxistant`)

### Compound Word Errors - 3 errors
1. `video-konfero` → incorrectly split to `Video-#keonfer`
   - Should be: "videokonferenco" (one word)
2. `Ido-renkontro` → incorrectly split to `Ido-@renkontr`
   - Should preserve hyphenated compound
3. `google-grupo` → incorrectly split to `#Google-#grupo`
   - Should preserve hyphenated compound

### Tense Errors - 2 errors (CRITICAL)
1. `partoprenas` (present) → should be `partoprenis` (past)
2. `diskutas` (present) → should be `diskutis` (past)

**Sentence 2 Total Errors: ~26 errors**

---

## Summary

### Total Errors by Category

| Category | Sentence 1 | Sentence 2 | Total |
|----------|-----------|------------|-------|
| Unknown Words | 10 | 3 | 13 |
| Translation Rules | 9 | 12 | 21 |
| Proper Noun Issues | 6 | 3 | 9 |
| Grammar Errors | 7 | 6 | 13 |
| Compound Words | 0 | 3 | 3 |
| Tense Errors | 0 | 2 | 2 |
| Word Order | Multiple | Multiple | Multiple |
| **TOTAL** | **~32** | **~26** | **~58** |

### Critical Errors (Must Fix)

1. **Tense recognition failure** (Sentence 2)
   - `partoprenas` → `partoprenis`
   - `diskutas` → `diskutis`

2. **Missing dictionary entries**
   - `lernebla`, `uzebla`, `saturdia`, `remplacigar`

3. **Compound word splitting**
   - `video-konfero`, `Ido-renkontro`, `google-grupo`

4. **Accusative case marking**
   - Missing: `detalojn`, `vortojn`
   - Incorrect: `demandon` → `demando`

### Error Rate

- **Sentence 1:** ~38% error rate (32 errors / ~85 words)
- **Sentence 2:** ~74% error rate (26 errors / ~35 words)
- **Overall:** ~56% error rate (58 errors / ~120 words)

---

## Improvements Needed

### High Priority
1. Fix verb tense recognition (present vs past)
2. Add missing dictionary entries
3. Fix compound word handling
4. Fix accusative case marking

### Medium Priority
5. Fix preposition translations (`kom` → `kiel`, `ye` → `je`)
6. Fix plural forms (`multa` → `multaj`)
7. Fix word order issues

### Low Priority
8. Improve proper noun handling
9. Fix capitalization issues
10. Clean up formatting markers

---

**Generated:** December 8, 2025

