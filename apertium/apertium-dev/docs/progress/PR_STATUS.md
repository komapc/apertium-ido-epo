# Pull Request Status - Ido-Esperanto Translation Pair

**Date:** October 10, 2025  
**Repository:** https://github.com/komapc/apertium-ido-epo

---

## ✅ Active PRs Ready for Review

### 1. Feature: Add Coordination Patterns
**Branch:** `feature/add-coordination-patterns`  
**PR Link:** https://github.com/komapc/apertium-ido-epo/pull/new/feature/add-coordination-patterns  
**Status:** ✅ Built, tested, ready for review  

**Changes:**
- Added transfer rule: Verb + Det + Adj + Noun + Conj + Det + Adj + Noun (copula-aware)
- Added proper noun support: Petr<np> → Petro<np>
- Includes previous work: bilingual mappings for core vocabulary stems

**Tests:**
- ✅ "La kato kaj la hundo kuras" → "La kato kaj la hundo kuras" (subjects stay nominative)
- ✅ "Me vidas la kato kaj la hundo" → "Mi vidas la katon kaj la hundon" (objects get accusative)
- ✅ "forte itere konstante" → "forte denove konstante" (core vocab works)

**Commits:**
- ce5f92d Transfer: add Det+Adj coordination rule. Bilingual: Petr (np)→Petro (np).
- d96da2d Add bilingual mappings for core vocabulary stems

---

### 2. Feature: Add Bilingual Mappings and Core Vocab
**Branch:** `feature/add-bilingual-mappings-and-core-vocab`  
**PR Link:** Already merged as #6 ✅  
**Status:** ✅ Merged to main  

**Changes:**
- Added 28+ bilingual stem mappings
- Fixed asymmetric mappings (Ido stems → Esperanto full forms)
- Core adverbs: fort, iter, konstant, ordinar, cirkum, qual
- Core nouns: milit

**Impact:**
- 71% reduction in untranslated words (49 → 14)
- 7% reduction in generation errors (426 → 395)

---

## 📋 Other Feature Branches (No New Commits)

### 3. Feature: Add Pronouns, Fix Copula and Coordination
**Branch:** `feature/add-pronouns-fix-copula-and-coordination`  
**Status:** ⚠️ No commits ahead of main  
**Action:** This branch appears to be already merged or superseded

### 4. Feature: Add Verified Grammatical Words
**Branch:** `feature/add-verified-grammatical-words`  
**Status:** ⚠️ No commits ahead of main  
**Action:** This branch appears to be already merged or superseded

### 5. Feature: Enhance Rule Documentation
**Branch:** `feature/enhance-rule-documentation`  
**Status:** ⚠️ Already merged as #4  
**Action:** None needed

### 6. Feature: Date Normalizer CLI
**Branch:** `feature/date-normalizer-cli`  
**Status:** ⚠️ Points to same commit as feature/add-coordination-patterns  
**Action:** This was a mistaken branch name; use feature/add-coordination-patterns instead

---

## 🎯 Recommended Actions

### Immediate:
1. ✅ **Review and merge PR**: `feature/add-coordination-patterns`
   - This includes the proven-correct stem-based bilingual mappings
   - Coordination patterns tested and working
   - Proper noun support added

### Optional Cleanup:
2. Delete stale branches after confirming they're merged:
   - `feature/add-pronouns-fix-copula-and-coordination`
   - `feature/add-verified-grammatical-words`
   - `feature/date-normalizer-cli` (duplicate)

---

## 📊 Testing Summary

All branches built successfully with no errors:
- **Bilingual entries:** 13,279 (was 13,274)
- **Ido morphology:** 4,642 entries
- **Esperanto morphology:** 88,580 entries

**Key findings:**
- Asymmetric bilingual mappings (Ido stem → Esperanto full) are **correct and intentional**
- Pattern matches existing entries like `ank<adv>` → `ankaŭ<adv>`
- Both languages' analyzers output different forms (stems vs. full), requiring asymmetry

---

## 🔧 Technical Notes

### Bilingual Dictionary Pattern
The asymmetry `fort<s n="adv"/>` → `forte<s n="adv"/>` is correct because:
1. Ido monolingual: stores stem with paradigm (e.g., `fort` + `e__adv`)
2. Ido analyzer outputs: `forte` → `fort<adv>` (stem)
3. Bilingual maps: `fort<adv>` → `forte<adv>` (stem → full form)
4. Esperanto works with full forms

This matches the pattern used for adjectives:
- `bel<adj>` → `bela<adj>` (Ido stem → Esperanto full)
- `konstant<adj>` → `konstanta<adj>` (Ido stem → Esperanto full)

---

**Next Steps:** Review and merge the active PR, then continue with remaining improvements (copula consolidation, degree constructions, etc.)

