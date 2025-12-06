# Why Words from Wiktionary Don't Appear in Final Dictionary

**Date:** December 6, 2025

---

## The Problem

Words that exist in Wiktionary (like `en`, `ye`) are extracted and appear in:
- ✅ `source_io_wiktionary.json` 
- ✅ `merged_monodix.json`

But they **DO NOT** appear in:
- ❌ `generated/ido.ido.dix` (final monodix)

---

## Root Cause: Missing Paradigms

### The Filtering Step

**File:** `projects/data/scripts/generate_monodix.py`  
**Lines:** 199-201

```python
if not paradigm:
    entries_skipped_no_paradigm += 1
    continue
```

**What this means:**
- Every entry MUST have a `paradigm` in `morphology.paradigm`
- Entries without paradigms are **SKIPPED** during DIX generation
- They never make it into the final dictionary

### Statistics

From `merged_monodix.json`:
- **Total entries:** 16,402
- **Entries WITH paradigm:** 13,002 (79.3%) ✅ → Included in DIX
- **Entries WITHOUT paradigm:** 3,400 (20.7%) ❌ → **SKIPPED**

**Examples of skipped entries:**
- `en` (from wiktionary) - NO paradigm
- `por`, `de`, `od`, `per`, `ye`, `kom` (from BERT) - NO paradigm
- Many other function words and short words

---

## Why Are Paradigms Missing?

### 1. Wiktionary Parser Doesn't Always Extract POS

**File:** `projects/extractor/scripts/wiktionary_parser.py`

The parser tries to extract POS using:
- POS headers (=== Noun ===, === Preposition ===)
- Template detection ({{head|io|preposition}})
- Fallback heuristics

**Problem:** For function words like `en`:
- Wiktionary page might not have clear POS headers
- Template might be missing or unclear
- Heuristics fail for short words

**Result:** `pos` field is `None` or missing

### 2. No Paradigm Assignment Without POS

**The pipeline:**
1. Parser extracts word → `lemma: "en"`, `pos: None`
2. No POS → No paradigm assignment
3. Entry saved with `morphology: {}` (empty)
4. During DIX generation → `paradigm` is `None` → **SKIPPED**

### 3. BERT Embeddings Never Have Paradigms

BERT embeddings only provide:
- Lemma
- Translations (with confidence scores)
- **NO POS tags**
- **NO paradigms**

So ALL BERT entries are missing paradigms unless they're merged with other sources that have them.

---

## Example: "en" Entry Journey

### Step 1: Wiktionary Extraction
```json
{
  "lemma": "en",
  "source": "io_wiktionary",
  "pos": null,  // ← NOT EXTRACTED
  "morphology": {},  // ← EMPTY (no paradigm)
  "translations": [{"term": "en ↓", "lang": "eo", "confidence": 1.0}]
}
```

### Step 2: Merged JSON
```json
{
  "lemma": "en",
  "source": "io_wiktionary",  // or bert_embeddings
  "pos": null,  // ← STILL MISSING
  "morphology": {},  // ← STILL EMPTY
  "translations": [...]
}
```

### Step 3: DIX Generation
```python
paradigm = morphology.get('paradigm')  # → None
if not paradigm:  # → True
    entries_skipped_no_paradigm += 1  # ← SKIPPED!
    continue  # ← Entry never added to DIX
```

**Result:** "en" never appears in `generated/ido.ido.dix`

---

## Why This Happens

### Design Decision

The monodix generator requires paradigms because:
1. **Apertium needs paradigms** to generate morphological forms
2. **Paradigms define** how words inflect (singular/plural, verb tenses, etc.)
3. **Without paradigms**, entries can't be properly analyzed

### The Gap

**Missing link:** There's no step that:
- Infers POS from word form when parser fails
- Assigns appropriate paradigms based on POS
- Handles function words (prepositions, conjunctions) that need `__pr`, `__cnjcoo` paradigms

---

## Solutions

### Option 1: Improve POS Extraction (Recommended)

**Enhance wiktionary parser:**
- Better heuristics for function words
- Lookup table for common function words → POS mapping
- Template pattern improvements

### Option 2: Add Paradigm Inference

**Add step after merging:**
- If `pos` is missing, infer from word form/context
- If `paradigm` is missing but `pos` exists, assign appropriate paradigm:
  - `pr` (preposition) → `__pr`
  - `cnjcoo` (coordinating conjunction) → `__cnjcoo`
  - `n` (noun) → `o__n`
  - etc.

### Option 3: Function Word Lookup Table

**Add to merge/generation pipeline:**
- Known function words → POS → Paradigm mapping
- Apply during merge or generation step
- Ensures function words get proper paradigms

---

## Current State

**After threshold change to 0.9:**
- BERT embeddings (0.85 confidence) → **FILTERED OUT** from bidix
- BERT entries (no paradigms) → **SKIPPED** from monodix
- Wiktionary entries (no paradigms) → **SKIPPED** from monodix
- **Result:** Function words missing from both monodix and bidix

**After wiktionary parser fix:**
- Single-letter words like "e" → **WILL BE EXTRACTED**
- But still need POS/paradigm assignment → **STILL MISSING from DIX**

---

## Summary

**Why words don't appear in final dictionary:**

1. ✅ Words ARE extracted from Wiktionary
2. ✅ Words ARE in merged JSON
3. ❌ Words DON'T have paradigms
4. ❌ `generate_monodix.py` SKIPS entries without paradigms
5. ❌ Words never make it to final DIX

**The fix needed:**
- Not just allowing single-letter words (done)
- Also need to assign POS tags and paradigms to function words
- Otherwise they'll still be skipped during DIX generation

