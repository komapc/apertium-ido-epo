# Pull Request Links

**Date:** December 6, 2025

---

## Created PRs

### 1. apertium-ido
**PR #14:** feat: Add function words (por, de, en, od, per, ye, kom) with POS and paradigms  
**URL:** https://github.com/komapc/apertium-ido/pull/14

**Changes:**
- Added 7 function words to monodix
- Correct POS tags and paradigms
- Generated from unified JSON pipeline

---

### 2. apertium-ido-epo
**PR #65:** feat: Add function words and update dictionaries  
**URL:** https://github.com/komapc/apertium-ido-epo/pull/65

**Changes:**
- Updated monodix with function words
- Updated bidix with improved translations
- Added corpus test sentences and documentation

---

### 3. ido-esperanto-extractor
**PR #45:** feat: Fix parser to extract function words from numbered sections  
**URL:** https://github.com/komapc/ido-esperanto-extractor/pull/45

**Changes:**
- Fixed parser to extract function words from numbered sections
- Extract POS from section headers
- Allow single-letter function words

---

## Improvement Summary

**Function Words Recognition:**
- Before: 0/8 (0%)
- After: 7/8 (87.5%)
- Improvement: +87.5%

**Test Results:**
- Function words: `*por *de *en *e *od *per *ye *kom` → `@por @de @en *e @od @per @ye @kom`
- Corpus sentences show reduced unknown word count

---

## Next Steps

1. Review PRs
2. Merge when approved
3. Continue work on remaining issues:
   - "e" still needs extraction
   - Translation rule refinements

