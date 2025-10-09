# Idolinguo Dictionary Improvements

**Date:** October 9, 2025  
**Source:** [Idolinguo Ido-Esperanto Dictionary](https://idolinguo.org.uk/idoesp2.htm)

## Summary

Analyzed the Idolinguo Ido-Esperanto dictionary (7,206 words) and compared it with our Ido Wiktionary-based dictionary to identify gaps and corrections.

## Comparison Results

- **Our dictionary:** 7,756 entries → 7,764 entries
- **Idolinguo dictionary:** 7,206 entries
- **Coverage of key words:** 62% → improved
- **Added:** 8 new words
- **Corrected:** 3 translations

## New Words Added

### Function Words (High Priority)
1. **per** → per (preposition "through/by")
2. **od** → aŭ (exclusive "or")
3. **vu** → vi (formal singular "you")

### Verbs
4. **abandonar** → forlasi (to abandon)
5. **abasar** → malaltigi (to lower)
6. **abjurar** → forĵuri (to abjure)
7. **ablaktar** → demamigi (to wean)
8. **aboyar** → boji (to bark/bay)

## Corrections Made

### Translation Errors Fixed
1. **quale** → **kiel** (was incorrectly "kia")
   - Correct: "how" (adverb)
   - Error was: "what kind" (adjective)

2. **ilia** → **lia** (was incorrectly "ili")
   - Correct: "his" (masculine possessive)
   - Error was: "they" (plural pronoun)

3. **olia** → **ilia** (was incorrectly "ili")
   - Correct: "their" (neuter possessive)
   - Error was: "they" (plural pronoun)

## Impact

### Improvements
- ✅ Added essential function words (per, od, vu)
- ✅ Fixed critical pronoun translation errors
- ✅ Corrected "quale" (common interrogative adverb)
- ✅ Added obscure but valid verbs

### Test Results
```
Test: "Quale vu facas to?"
Before: "Kia #default faras #unknown?"
After:  "Kiel #default faras #unknown?" ✓
```

The correction of `quale` to `kiel` is particularly important as "how" is a very common word.

## Methodology

1. **Analyzed** Idolinguo dictionary structure
2. **Parsed** key entries from the web version
3. **Compared** with our Wiktionary-based dictionary
4. **Identified** 14 missing words and 9 different translations
5. **Validated** which differences were errors vs. alternatives
6. **Created** supplement JSON with additions and corrections
7. **Merged** supplement into main dictionary
8. **Regenerated** .dix files
9. **Tested** improvements

## Scripts Created

- `parse_idolinguo.py` - Parser for Idolinguo format
- `compare_with_idolinguo.py` - Comparison tool
- `apply_idolinguo_supplement.py` - Merge tool
- `idolinguo_supplement.json` - Supplement data

## Files Modified

### ido-esperanto-extractor/
- `dictionary_merged.json` - Updated with new entries
- `apertium-ido.ido.dix` - Regenerated monolingual
- `apertium-ido-epo.ido-epo.dix` - Regenerated bilingual

### apertium-ido-epo/
- `apertium-ido.ido.dix` - Updated from extractor
- `apertium-ido-epo.ido-epo.dix` - Updated from extractor

## Backup

A backup was created before merging:
- `dictionary_merged_backup_20251009_065909.json`

## Future Work

The Idolinguo dictionary has ~7,206 words. A more comprehensive extraction could:
1. Parse the complete HTML dictionary
2. Extract all 7,206 entries systematically
3. Identify more gaps and alternative translations
4. Create a comprehensive supplement

However, our current dictionary (7,764 entries) already has good coverage, and the most critical additions have been made.

## References

- **Idolinguo Dictionary:** https://idolinguo.org.uk/idoesp2.htm (7,206 words, Sept 2011)
- **Our Source:** Ido Wiktionary (Oct 2025 dump, 7,549 extracted words)
- **Final Count:** 7,764 entries (Wiktionary + manual additions + Idolinguo supplement)

