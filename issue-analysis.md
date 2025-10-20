# Critical Analysis: Why Verbs, Elision, and Plurals Don't Work

## Issue #1: Verb Generation Failure

### The Problem
```bash
esas → @es (should be "estas")
havas → @hav (should be "havas")
```

### Root Cause: STEM vs LEMMA Mismatch

**What happens:**

1. **Morphological Analyzer** (apertium-ido.ido.dix):
   ```xml
   <e lm="esar">
     <i>es</i>           ← STEM only
     <par n="ar__vblex"/>
   </e>
   ```
   - Input: "esas"
   - Output: `^esas/es<vblex><pri>$`  ← STEM is "es"

2. **Bilingual Dictionary** (apertium-ido-epo.ido-epo.dix):
   ```xml
   <e><p><l>esar<s n="vblex"/></l><r>esti<s n="vblex"/></r></p></e>
   ```
   - Expects: "esar<vblex>..." ← FULL LEMMA
   - Gets: "es<vblex><pri>" ← STEM only
   - **MISMATCH! No translation happens!**

3. **Generator**:
   - Gets: `^es<vblex><pri>$` (untranslated)
   - Esperanto dict doesn't have "es" stem
   - Output: `#es` or `@es`

### The Fix

Change bilingual dictionary entries from:
```xml
❌ <l>esar<s n="vblex"/></l><r>esti<s n="vblex"/></r>
```

To:
```xml
✅ <l>es<s n="vblex"/></l><r>est<s n="vblex"/></r>
```

**This affects ALL VERBS in the dictionary!**

---

## Issue #2: Elision Not Handled (l' → la)

### The Problem
```
l'Uniono → @l '*Uniono (should be "la Uniono")
l'euro → @l '@eur (should be "la eŭron")
```

### Root Cause: Apostrophe Elision Not Processed

**What happens:**

1. **Input text**: `l'Uniono`

2. **Tokenizer** treats this as TWO tokens:
   - `l'` (not recognized as "la")
   - `Uniono`

3. **Morphological Analyzer**:
   - Input: "l'"
   - Output: `^l'/*l'$` ← Unknown word

### The Fix

**Option A: Pretransfer Processing**
Add rule before morphological analysis to expand elisions:
```bash
l' → la 
L' → La
```

**Option B: Add to Monolingual Dictionary**
```xml
<e lm="la">
  <i>l'</i>
  <par n="__det"/>
</e>
```

**Option C: Transfer Rule**
Handle in transfer rules (not ideal, should be earlier)

---

## Issue #3: Noun Plurals Not Converting (-i → -j)

### The Problem
```
lingui → *lingui (should be "lingvoj")
stati → @stat (should be "ŝtatoj")
aferi → @afer (should be "aferoj")
```

### Root Cause: Multiple Issues

**Issue 3A: Morphological Analysis**

```bash
echo "lingui" | lt-proc ido-epo.automorf.bin
```

Need to check if:
- "lingui" is recognized as plural
- Output includes `<pl>` tag

**Issue 3B: Bilingual Dictionary**

Even if analyzed correctly, bilingual dict needs STEM mapping:
```xml
<e><p><l>lingu<s n="n"/></l><r>lingv<s n="n"/></r></p></e>
```

Not lemma mapping:
```xml
❌ <e><p><l>linguo<s n="n"/></l><r>lingvo<s n="n"/></r></p></e>
```

**Issue 3C: Generator**

Esperanto generator must have paradigm that generates:
- `lingv<n><sg>` → "lingvo"
- `lingv<n><pl>` → "lingvoj"

**Issue 3D: Transfer Rules**

Transfer rules might need to add plural tags or convert case.

---

## Testing Each Issue

### Test #1: Verify Stem Output

```bash
cd /home/mark/apertium-ido-epo/apertium-ido-epo

# Check what analyzer outputs
echo "esas" | lt-proc ido-epo.automorf.bin
# Expected: ^esas/es<vblex><pri>$
# ^---- stem is "es" not "esar"

echo "havas" | lt-proc ido-epo.automorf.bin  
# Expected: ^havas/hav<vblex><pri>$
# ^---- stem is "hav" not "havar"
```

### Test #2: Check Elision

```bash
echo "l'" | lt-proc ido-epo.automorf.bin
# Current: ^l'/*l'$  ← unknown
# Expected: ^l'/la<det><def><sp>$
```

### Test #3: Check Plural Analysis

```bash
echo "lingui" | lt-proc ido-epo.automorf.bin
# Need to see if <pl> tag is present

echo "kati" | lt-proc ido-epo.automorf.bin  
# Simpler test with "kato"
```

---

## Impact Assessment

### Issue #1 (Verbs): **CRITICAL - WIDESPREAD**
- Affects: ALL verbs (~1000+ entries)
- Impact: ~60% of translation failures
- Difficulty: EASY FIX (sed/awk to strip -ar/-i suffix)

### Issue #2 (Elision): **HIGH - COMMON**
- Affects: ~15 instances in test text
- Impact: ~10% of failures
- Difficulty: EASY FIX (add elided forms to dict)

### Issue #3 (Plurals): **HIGH - COMPLEX**
- Affects: All plural nouns (~500+ instances)
- Impact: ~20% of failures  
- Difficulty: MEDIUM (need to diagnose which stage fails)

---

## Recommended Fix Order

1. **Fix Issue #1 first** - Verb stems in bilingual dict
   - Single find/replace operation
   - Fixes majority of problems

2. **Fix Issue #2** - Add elision support
   - Add l'/L' to monolingual dict
   - Quick win

3. **Diagnose Issue #3** - Test each stage
   - Morphological analysis
   - Bilingual lookup
   - Generation
   - Then fix based on diagnosis


