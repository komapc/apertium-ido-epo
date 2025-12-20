# TODO - Apertium Ido-Esperanto Translation Pair

**Last Updated:** December 20, 2025

## ✅ Recently Completed

### ✅ Transfer Rules for New Morphology (Dec 20, 2025)
**Status:** COMPLETED

- [x] **Passive voice**: Ido synthetic passive (`-esar`, `-esis`) → Esperanto periphrastic (`esti` + participle)
  - `kreesis` → `estis kreita` (was created)
  - `kreesas` → `estas kreita` (is created)
  - `kreesar` → `esti kreita` (to be created)
- [x] **Participles**: Ido `-ante` → Esperanto `-ante` (adverbial participle)
  - `derivante` → `derivante`

### ✅ Morphological Paradigm Extensions (Dec 20, 2025)
**Status:** COMPLETED

- [x] **Accusative case for nouns** (`o__n`): Added `-on` (sg) and `-in` (pl) forms
- [x] **Accusative case for adjectives** (`a__adj`, `ebl__adj`): Added `-an` forms  
- [x] **Passive voice for verbs** (`ar__vblex`): Added `-esar`, `-esas`, `-esis`, `-esos`, `-esus`, `-esez`
- [x] **Participles for verbs** (`ar__vblex`): Added `-ante` (present), `-inte` (past active), `-onte` (future), `-ata`, `-ita`, `-ota` (passive)
- [x] **Elided article l'**: Fixed to be parsed as determiner (was preposition)

---

## 🚨 Critical & Immediate

### 1. 🎯 Add CG3 Disambiguation Rules
**Priority:** HIGH  
**Time:** 2-4 hours  
**Status:** Not Started

**Issue:** The `ido-epo` mode has NO disambiguation step. When words have multiple readings (e.g., `la` → `l<adj>` or `la<det>`), the first reading is picked, which is often wrong.

**Evidence:**
- `#la` in translation output suggests `la` is being misparsed or mistranslated because of ambiguity.
- `@l` errors in previous tests.

**Solution:**
- [ ] Create `apertium-ido-epo.ido.rlx` with CG3 disambiguation rules
- [ ] Add `cg-proc` step to `modes.xml` for `ido-epo` mode
- [ ] Add rules to select correct readings (e.g., SELECT det IF next is noun/adj)

**Documentation:** `docs/FIX_PLAN_TRANSLATION_ERRORS.md`

---

### 2. 🔧 Add Missing Dictionary Entries
**Priority:** HIGH  
**Time:** 1-2 hours  
**Status:** Partially Complete

**Missing Words Identified:**
- [ ] `maxim` - Superlative marker (adverb) → `plej`
- [ ] `nomizar` - "to name" (verb) → `nomi`
- [ ] `Esperantidoj` - Proper noun plural handling
- [x] Cardinal numbers (1907, etc.) - Added num_regex paradigm and bidix handling

**Documentation:** `docs/FIX_PLAN_TRANSLATION_ERRORS.md`

---

## 📊 Translation Quality Issues

### 3. Fix Case Sensitivity for Proper Nouns
**Priority:** MEDIUM  
**Time:** 15-30 minutes  
**Status:** In Progress

**Issue:** Proper nouns like `Ido`, `Paris`, `Idisti` exist in JSON as lowercase but appear capitalized in text.

**Solution:**
- [x] Added automatic `np__np` paradigm assignment in `merge_sources.py`
- [x] Proper nouns from `source_io_wikipedia.json` now automatically get `np__np` paradigm
- [x] Regenerate dictionaries: `cd projects/data && python3 scripts/regenerate_all.py`
- [x] Copy generated files to apertium directories
- [x] Recompile and test

---

### 4. Fix Grammar/Agreement Errors
**Priority:** MEDIUM  
**Time:** 2-4 hours

**Issues Found:**
- Case errors: `lingvon` (accusative) should be `lingvo` (nominative) in certain contexts
- Agreement errors: Adjective agreement issues (`nova` → `novaj`)

---

### 5. Fix Compound Word Recognition
**Priority:** MEDIUM  
**Time:** 1-2 hours

**Issues:**
- `video-konfero` not recognized
- `Ido-renkontro` not recognized
- `google-grupo` not recognized

**Solution:** Add compound word handling rules or dictionary entries.

---

## 📈 Improvements

### 6. Add More Test Sentences
**Priority:** LOW  
**Time:** 1 hour

- [ ] Add test cases for all verb tenses
- [ ] Add test cases for accusative case
- [ ] Add test cases for passive voice
- [ ] Add test cases for participles
- [ ] Add test cases for compound words

**File:** `corpus/ido-epo-test-sentences.txt`

---

### 7. Improve Error Reporting
**Priority:** LOW  
**Time:** 1-2 hours

- [ ] Add verbose mode to show morphological analysis
- [ ] Add error logging for unknown words
- [ ] Add statistics on translation quality

---

## 📚 Documentation

### 8. Update Translation Rule Documentation
**Priority:** LOW  
**Time:** 2-3 hours

- [ ] Document all translation rules with examples
- [ ] Add linguistic justification for complex rules
- [ ] Cross-reference related rules

**File:** `apertium-ido-epo.ido-epo.t1x`

---

## 🔗 Related Documentation

- **Fix Plan:** `docs/FIX_PLAN_TRANSLATION_ERRORS.md`
- **Error Analysis:** `corpus/TRANSLATION_ERRORS_ANALYSIS.md`
- **Missing Words:** `corpus/MISSING_WORDS_ANALYSIS.md`
- **Tense Errors:** `corpus/TENSE_ERRORS_FIX.md`
- **Easy Fix:** `corpus/EASY_FIX_CASE_SENSITIVITY.md`
- **Summary:** `corpus/ANALYSIS_SUMMARY.md`
