# Function Words Pipeline Issue

**Date:** December 6, 2025  
**Status:** Threshold updated to 0.9, pipeline issue identified

---

## 1. Threshold Updated ✅

**Changed:** `projects/data/scripts/regenerate_all.py`
- **Old default:** `--min-confidence 0.0`
- **New default:** `--min-confidence 0.9`

This will filter out low-confidence BERT embeddings (0.85) while keeping high-confidence sources (1.0 from wiktionary).

---

## 2. Function Words Missing from Pipelines

### Current Status

**Function words needed:** `por`, `de`, `en`, `e`, `od`, `per`, `ye`, `kom`

**Where they exist:**
- ✅ **BERT embeddings:** All 8 words exist, but with wrong translations (confidence 0.85)
- ❌ **Wiktionary:** Filtered out (single-letter words rejected)
- ❌ **Wikipedia:** Not found
- ❌ **EN pivot:** Not found

### Root Cause: Wiktionary Parser Filtering

**File:** `projects/extractor/scripts/wiktionary_parser.py`  
**Function:** `is_valid_title()` (lines 97-106)

```python
def is_valid_title(title: str) -> bool:
    if not title:
        return False
    t = title.strip()
    if len(t) < 2:  # ← THIS FILTERS OUT SINGLE-LETTER WORDS
        return False
    # ...
```

**Impact:**
- Single-letter words like "e" are rejected
- Short function words may be filtered if they're < 2 characters

### BERT Embeddings Issue

**All function words have confidence 0.85 with wrong translations:**
- `od` → `ke`, `per`, `deputitoj` (should be `aŭ`)
- `kom` → `komarko`, `kun`, `ke` (should be `kiel`)
- `ye` → `en`, `ke`, `ene` (should be `je`)

**With threshold 0.9, these will be filtered out** (0.85 < 0.9).

---

## 3. Solutions (Pipeline-Based Only)

### Option A: Fix Wiktionary Parser (Recommended)

**Modify:** `projects/extractor/scripts/wiktionary_parser.py`

**Change:**
```python
def is_valid_title(title: str) -> bool:
    if not title:
        return False
    t = title.strip()
    # Allow single-letter words that are known function words
    if len(t) < 2:
        # Allow common function words
        if t.lower() in {'e', 'a', 'o', 'i', 'u'}:  # Add more as needed
            return True
        return False
    # ... rest of function
```

**Then re-run extraction pipeline** to get function words from Wiktionary.

### Option B: Improve BERT Embeddings

**Fix translations in BERT alignment:**
- Improve the alignment algorithm to better handle function words
- Use context-aware embeddings for short words
- Post-process function words with known translations

**Requires:** Modifying `projects/embedding-aligner/` scripts.

### Option C: Add to ido_lexicon.yaml

**If `apdata/ido_lexicon.yaml` is part of the pipeline:**
- Add function words to the lexicon
- Ensure they're exported to JSON during lexicon processing
- This would be pipeline-generated, not manual

**Check:** Does `ido_lexicon.yaml` → JSON conversion exist?

---

## 4. Current State After Threshold Change

**With threshold 0.9:**
- ✅ High-confidence wiktionary entries (1.0) → **INCLUDED**
- ❌ Low-confidence BERT embeddings (0.85) → **FILTERED OUT**
- ❌ Function words from BERT → **FILTERED OUT** (wrong translations anyway)

**Result:** Function words will be missing from generated dictionaries until pipeline is fixed.

---

## 5. Next Steps

1. **Immediate:** Threshold is updated (done)
2. **Short-term:** Fix wiktionary parser to allow single-letter function words
3. **Medium-term:** Improve BERT embeddings for function words OR add to lexicon pipeline
4. **Long-term:** Re-run extraction pipeline to get function words from sources

---

## 6. Verification

After fixing pipeline, verify:
```bash
cd projects/data
python3 scripts/regenerate_all.py --min-confidence 0.9

# Check generated dictionaries
grep -E "(por|de|en|e|od|per|ye|kom)" generated/ido.ido.dix
grep -E "(por|de|en|e|od|per|ye|kom)" generated/ido-epo.ido-epo.dix
```

---

## Notes

- **No manual sources:** All words must come from pipelines
- **Threshold 0.9:** Filters bad BERT translations but also removes function words
- **Wiktionary filter:** Single-letter words rejected, needs fix
- **BERT quality:** Function word translations are poor (0.85 confidence, wrong terms)

