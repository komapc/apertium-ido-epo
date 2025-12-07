# TODO - Apertium Ido-Esperanto Translation Pair

**Last Updated:** December 6, 2025

## 🚨 Critical & Immediate

### 0. 🔤 Fix Case Sensitivity for Proper Nouns (EASY FIX - 15-30 min)
**Priority:** HIGH  
**Time:** 15-30 minutes  
**Status:** Not Started

**Issue:** Proper nouns like `Ido`, `Paris`, `Idisti` exist in JSON as lowercase but appear capitalized in text. Morphological analyzer requires exact case match.

**Solution:**
- [x] Removed `source_manual.json` - all dictionaries regenerated from sources only
- [x] Added automatic `np__np` paradigm assignment in `merge_sources.py` for entries with `pos: "np"`
- [x] Proper nouns from `source_io_wikipedia.json` now automatically get `np__np` paradigm
- [ ] Regenerate dictionaries: `cd projects/data && python3 scripts/regenerate_all.py`
- [ ] Copy generated files to apertium directories
- [ ] Recompile and test

**IMPORTANT:** 
- Do NOT manually edit .dix files. Always regenerate from JSON sources.
- All source JSON files are generated automatically. No manual entries needed.

**Files:**
- `projects/data/scripts/merge_sources.py` (updated - assigns `np__np` paradigm automatically)
- `projects/data/pardefs.xml` (contains `np__np` paradigm)

**Documentation:** `corpus/EASY_FIX_CASE_SENSITIVITY.md`

---

### 1. 🔧 Fix Missing Dictionary Entries
**Priority:** HIGH  
**Time:** 1-2 hours  
**Status:** Not Started

**Missing Words:**
- [ ] `kreinto` - Add to monodix and bidix (exists in JSON)
- [ ] `remplacigar` - Add to JSON sources, then monodix and bidix
- [ ] `existant` - Add to JSON sources, then monodix and bidix

**Documentation:** `corpus/MISSING_WORDS_ANALYSIS.md`

---

### 2. ⏰ Fix Tense Translation Errors
**Priority:** HIGH  
**Time:** 15-30 minutes  
**Status:** Not Started

**Issue:** Past tense verbs (`partoprenis`, `diskutis`) translated as present tense.

**Root Causes:**
1. Wrong tags in paradigm (`pres`/`past`/`fut` instead of `pri`/`pii`/`fti`)
2. Wrong stem in static entry (`partoprenis` instead of `partopren`)

**Solution:**
- [ ] Fix `ar__vblex` paradigm tags in `../apertium-ido/pardefs.xml`: `pres`→`pri`, `past`→`pii`, `fut`→`fti`
- [ ] Fix static entry stem in `../apertium-ido/apertium-ido.ido.dix` or remove entry
- [ ] Recompile and test

**Documentation:** `corpus/TENSE_ERRORS_FIX.md`

---

## 📊 Translation Quality Issues

### 3. Fix Grammar/Agreement Errors
**Priority:** MEDIUM  
**Time:** 2-4 hours

**Issues Found:**
- Case errors: `lingvon` (accusative) should be `lingvo` (nominative)
- Tense errors: Past participles translated as present tense verbs
- Agreement errors: Adjective agreement issues (`nova` → `novaj`)

**Documentation:** `corpus/TRANSLATION_ERRORS_ANALYSIS.md`

---

### 4. Fix Compound Word Recognition
**Priority:** MEDIUM  
**Time:** 1-2 hours

**Issues:**
- `video-konfero` not recognized
- `Ido-renkontro` not recognized
- `google-grupo` not recognized

**Solution:** Add compound word handling rules or dictionary entries.

---

### 5. Fix Function Word Translations
**Priority:** MEDIUM  
**Time:** 1 hour

**Issues:**
- `di` → `@di` (should be `de`)
- `ye` → `@ye` (should be `je`)
- `dil` → `#de l'` (should be `de la`)
- `da` → `#de ↓ (indikante aganton)` (agent marker)

---

## 📈 Improvements

### 6. Add More Test Sentences
**Priority:** LOW  
**Time:** 1 hour

- [ ] Add test cases for all verb tenses
- [ ] Add test cases for various noun cases
- [ ] Add test cases for various adjective forms
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

- **Error Analysis:** `corpus/TRANSLATION_ERRORS_ANALYSIS.md`
- **Missing Words:** `corpus/MISSING_WORDS_ANALYSIS.md`
- **Tense Errors:** `corpus/TENSE_ERRORS_FIX.md`
- **Easy Fix:** `corpus/EASY_FIX_CASE_SENSITIVITY.md`
- **Summary:** `corpus/ANALYSIS_SUMMARY.md`

