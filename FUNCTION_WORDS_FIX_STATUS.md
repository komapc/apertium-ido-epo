# Function Words Fix - Status Report

**Date:** October 9, 2025  
**Action:** Attempted to fix missing Ido function words

---

## ✅ What Was Fixed

### 1. Added Function Words to Ido Monolingual Dictionary (`apertium-ido.ido.dix`)

**Paradigms Added:**
- `__cnjcoo` - Coordinating conjunctions
- `__cnjsub` - Subordinating conjunctions
- `__pr` - Prepositions  
- `__prn` - Pronouns
- `__det` - Determiners
- `__ij` - Interjections

**Entries Added (~40 function words):**

**Conjunctions:**
- e, od, ma (coordinating)
- dum, kad, kam, se, pro, nam, pos, ko (subordinating)

**Prepositions:**
- a, ad, al, ante, da, de, di, en, inter, kontre, kun, per, por, pos, pri, pro, sen, sur, tra, trans, ultra

**Pronouns:**
- qua, qui, quo, qual, ka, yen

**Determiner:**
- la

**Interjections:**
- yes, no

**Result:** ✅ Morphological analyzer now recognizes all these words!

```bash
$ echo "e od en de la qua" | lt-proc ido-epo.automorf.bin
^e/e<cnjcoo>$ ^od/od<cnjcoo>$ ^en/en<pr>$ ^de/de<pr>$ ^la/la<det><def><sp>$ ^qua/qua<prn>$
```

---

### 2. Added Function Words to Bilingual Dictionary (`apertium-ido-epo.ido-epo.dix`)

**Mappings Added:**
- e → kaj
- od → aŭ  
- ma → sed
- dum → dum
- de → de
- di → de
- da → de
- en → en
- qua → kiu
- la → la
- etc. (~40 mappings)

**Result:** ⚠️ **PARTIAL SUCCESS** - Some work, some don't

```bash
# These work:
$ echo "^e<cnjcoo>$" | lt-proc -b ido-epo.autobil.bin
^e<cnjcoo>/kaj<cnjcoo>$  ✅

$ echo "^de<pr>$" | lt-proc -b ido-epo.autobil.bin  
^de<pr>/de<pr>$  ✅

# But with surface form, they fail:
$ echo "^e/e<cnjcoo>$" | lt-proc -b ido-epo.autobil.bin
^e/@e$  ❌
```

---

## ❌ What Still Doesn't Work

### Issue: Bilingual Transfer Failing

**Problem:** When the morphological analyzer outputs lexical units with surface forms `^word/lemma<tags>$`, the bilingual dictionary doesn't match them.

**Evidence:**
```bash
$ echo "e" | lt-proc ido-epo.automorf.bin
^e/e<cnjcoo>$

$ echo "e" | lt-proc ido-epo.automorf.bin | lt-proc -b ido-epo.autobil.bin
^e/@e$  ← Transfer fails! Shows @ (unknown)
```

**But manual test works:**
```bash
$ echo "^e<cnjcoo>$" | lt-proc -b ido-epo.autobil.bin
^e<cnjcoo>/kaj<cnjcoo>$  ← This works!
```

---

## 🔍 Root Cause Analysis

### Hypothesis: Surface Form vs Lemma Issue

The bilingual dictionary entries are defined as:
```xml
<e>
  <p>
    <l>e<s n="cnjcoo"/></l>
    <r>kaj<s n="cnjcoo"/></r>
  </p>
</e>
```

This matches `e<cnjcoo>` but the morphological analyzer outputs `e/e<cnjcoo>` where:
- First `e` = surface form
- Second `e` = lemma
- `<cnjcoo>` = tags

**The bilingual dictionary might be trying to match the surface form + tags, not lemma + tags.**

---

## 💡 Possible Solutions

### Option 1: Use Identity Paradigm

Many bilingual dictionaries use identity/equivalence entries for function words that are identical in both languages:

```xml
<e><i>e<s n="cnjcoo"/></i></e>
```

This might handle both surface and lemma forms.

### Option 2: Check Existing Working Entries

Look at how other function words in the dictionary work (if any) and copy that format exactly.

### Option 3: Add Surface Form Entries

Maybe need entries like:
```xml
<e>
  <p>
    <l>e/e<s n="cnjcoo"/></l>
    <r>kaj/kaj<s n="cnjcoo"/></r>
  </p>
</e>
```

### Option 4: Check if lt-proc -b needs different flags

Maybe the -b flag expects a different format or there's a preprocessing step missing.

---

## 🧪 Tests to Run

### Test 1: Check existing function words
```bash
grep -A5 "cnjcoo\|<pr>" apertium-ido-epo.ido-epo.dix | head -50
```

See if there are any existing function words and how they're formatted.

### Test 2: Test with identity entries
Add one identity entry and test if it works better.

### Test 3: Compare with working content words
```bash
echo "abelar" | lt-proc ido-epo.automorf.bin | lt-proc -b ido-epo.autobil.bin
```

See if content words transfer properly and check their format.

---

## 📊 Current Translation Quality

### Before Fix:
```
Gaza Strip (Ido → Esperanto):
#dum #la #Ses-@dia *milito #kaj ... #de ... #al ... #kiu
           ↑      ↑       ↑        ↑       ↑       ↑
        ALL FAILED
```

### After Monolingual Fix:
```
Morphological analysis works:
^dum/dum<cnjsub>$ ^la/la<det><def><sp>$ ^e/e<cnjcoo>$ ^de/de<pr>$ ^qua/qua<prn>$
        ✅               ✅                    ✅           ✅           ✅
```

### After Bilingual Attempt:
```
Transfer still failing:
^dum/@dum$ ^la/@la$ ^e/@e$ ^de/@de$ ^qua/@qua$
      ❌         ❌       ❌       ❌         ❌
```

---

## 🎯 Next Steps

1. **PRIORITY 1:** Figure out why bilingual transfer isn't working
   - Check format of existing entries
   - Try identity entries
   - Test with working content words

2. **PRIORITY 2:** Once transfer works, fix Esperanto generator
   - Some Esperanto forms like `la<det>` and `kiu<prn>` show # in generation
   - Need to ensure Esperanto monolingual has these

3. **PRIORITY 3:** Re-run Wikipedia translations
   - Test with Gaza and France articles
   - Measure error rate improvement

---

## 📝 Files Modified

1. ✅ `/home/mark/apertium-ido-epo/apertium-ido-epo/apertium-ido.ido.dix`
   - Added paradigms
   - Added ~40 function word entries
   
2. ✅ `/home/mark/apertium-ido-epo/apertium-ido-epo/apertium-ido-epo.ido-epo.dix`
   - Added ~40 bilingual mappings
   
3. ✅ Compilation successful
   - `make clean && make` completed without errors

---

## ✅ Verified Working

- ✅ Morphological analysis of Ido function words
- ✅ Compilation of all dictionaries
- ✅ Bilingual transfer works with manual tag-only input

## ❌ Not Working Yet

- ❌ Bilingual transfer with lexical units from morphological analyzer
- ❌ Full translation pipeline for function words
- ❌ Expected error rate improvement not yet achieved

---

**Status:** Partial fix complete. Investigation ongoing into bilingual transfer issue.

