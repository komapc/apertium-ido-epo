# Function Words in Wiktionary - Status Report

**Date:** December 6, 2025  
**Words Checked:** `por`, `de`, `en`, `e`, `od`, `per`, `ye`, `kom`

---

## Summary

✅ **All 8 words exist in Ido Wiktionary** (verified via HTTP 200 responses)

❌ **Only 4 out of 8 are extracted** in `io_wiktionary_processed.json`

❌ **None have proper POS tags or paradigms** (so they're skipped during DIX generation)

---

## Detailed Status

### ✅ Words Found in Processed Wiktionary

| Word | Status | POS | EO Translation | Notes |
|------|--------|-----|----------------|-------|
| `de` | ✅ FOUND | None | Missing in sense 1 | Has EN/FR translations |
| `en` | ✅ FOUND | None | `en ↓` | Has EO translation |
| `per` | ✅ FOUND | None | Missing | Has EN/FR translations |
| `ye` | ✅ FOUND | None | `je` | Has EO translation |

### ❌ Words NOT Found in Processed Wiktionary

| Word | Status | Wiktionary Page | Reason |
|------|--------|-----------------|--------|
| `por` | ❌ NOT FOUND | ✅ Exists | **Parser issue** - not extracted |
| `e` | ❌ NOT FOUND | ✅ Exists | **Parser filter** - single-letter (FIXED) |
| `od` | ❌ NOT FOUND | ✅ Exists | **Parser issue** - not extracted |
| `kom` | ✅ FOUND in HTML | ❌ Not in processed | **Parser issue** - not extracted properly |

**Note:** `kom` exists in Wiktionary HTML with Esperanto translation "kiel", but is not in processed JSON.

---

## Why Words Are Missing

### 1. Parser Filtering (FIXED for "e")

**File:** `projects/extractor/scripts/wiktionary_parser.py`  
**Function:** `is_valid_title()`

**Before fix:**
- All single-letter words rejected (`if len(t) < 2: return False`)
- "e" was filtered out

**After fix:**
- Single-letter function words allowed: `e`, `a`, `o`, `i`, `u`
- "e" will now be extracted (needs re-run of extraction)

### 2. Missing EO Translations

Some words are extracted but don't have Esperanto translations in the expected format:

- `de`: Has EN/FR translations, but EO translation missing or in wrong format
- `per`: Has EN/FR translations, but EO translation missing

**Parser looks for:**
- `* {{eo}}: translation`
- `{{t|eo|translation}}`
- `{{l|eo|translation}}`

**If these patterns aren't found**, the word is extracted but without EO translation.

### 3. Missing POS Tags

**All extracted words have `POS: None`**

**Why:**
- Parser tries to extract POS from:
  - POS headers (=== Preposition ===)
  - Templates ({{head|io|preposition}})
  - Heuristics

**For function words:**
- Wiktionary pages may not have clear POS headers
- Templates may be missing or unclear
- Heuristics fail for short words

**Result:** No POS → No paradigm → Skipped during DIX generation

---

## What Needs to Be Fixed

### 1. Re-run Extraction (After Parser Fix)

**Action:** Re-run wiktionary extraction to get "e" (and potentially others)

```bash
cd projects/extractor
python3 scripts/01_parse_io_wiktionary.py
```

### 2. Fix Missing Words (`por`, `od`, `kom`)

**Investigation needed:**
- Check why `por`, `od`, `kom` are not extracted
- Check if they have EO translations in Wiktionary
- Check if parser patterns match their Wiktionary format

**Possible issues:**
- Translation format not matching parser patterns
- Page structure different from expected
- Filtering logic rejecting them

### 3. Add POS Tags

**For extracted words without POS:**
- Add POS inference for function words
- Known function words → POS mapping:
  - `por`, `de`, `en`, `per`, `ye`, `kom` → `pr` (preposition)
  - `od`, `e` → `cnjcoo` (coordinating conjunction)

### 4. Add Paradigms

**After POS is assigned:**
- Convert POS → paradigm:
  - `pr` → `__pr`
  - `cnjcoo` → `__cnjcoo`

**This will allow words to be included in generated DIX.**

---

## Verification

### Check Wiktionary Pages Directly

All pages exist and are accessible:
- ✅ https://io.wiktionary.org/wiki/por
- ✅ https://io.wiktionary.org/wiki/de
- ✅ https://io.wiktionary.org/wiki/en
- ✅ https://io.wiktionary.org/wiki/e
- ✅ https://io.wiktionary.org/wiki/od
- ✅ https://io.wiktionary.org/wiki/per
- ✅ https://io.wiktionary.org/wiki/ye
- ✅ https://io.wiktionary.org/wiki/kom

### Check Processed Data

**File:** `projects/extractor/work/io_wiktionary_processed.json`

**Found:**
- `de` - ✅ (no POS, no EO in sense 1)
- `en` - ✅ (no POS, has EO: "en ↓")
- `per` - ✅ (no POS, no EO)
- `ye` - ✅ (no POS, has EO: "je")

**Missing:**
- `por` - ❌
- `e` - ❌ (will be fixed after re-extraction)
- `od` - ❌
- `kom` - ❌

---

## Next Steps

1. **Re-run extraction** to get "e" (parser fix applied)
2. **Investigate** why `por`, `od`, `kom` aren't extracted
3. **Add POS inference** for function words
4. **Add paradigm assignment** based on POS
5. **Re-generate dictionaries** to include function words

---

## Notes

- All words **DO exist** in Wiktionary (as expected)
- Parser **needs improvement** to extract all of them
- Even when extracted, **POS/paradigm assignment** is needed
- Without paradigms, words are **skipped during DIX generation**

The issue is not that words don't exist in Wiktionary - they do. The issue is:
1. Parser not extracting them all
2. Missing POS tags when extracted
3. Missing paradigms (even with POS)

