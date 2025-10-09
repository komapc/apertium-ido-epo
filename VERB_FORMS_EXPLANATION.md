# Understanding Verb Forms in Apertium Dictionaries

**Date:** 2025-10-09  
**Question:** Why do we need multiple entries for the same verb?

---

## ✅ **YES - You Understand Correctly!**

There are **two approaches** to handling verb forms in Apertium:

---

## **APPROACH 1: Stem-Based (Paradigm System)** ⭐ RECOMMENDED

This is what Apertium **already does** and what we're using!

### How It Works:

**Step 1: Monolingual Dictionary** (Esperanto)
```xml
<!-- Define the verb paradigm once -->
<pardef n="i__vblex">
  <e><p><l>i</l><r>i<s n="vblex"/><s n="inf"/></r></p></e>
  <e><p><l>as</l><r>i<s n="vblex"/><s n="pres"/></r></p></e>
  <e><p><l>is</l><r>i<s n="vblex"/><s n="past"/></r></p></e>
  <e><p><l>os</l><r>i<s n="vblex"/><s n="fti"/></r></p></e>
  <!-- ... etc for all conjugations -->
</pardef>

<!-- Apply paradigm to verb stem -->
<e lm="ekzisti"><i>ekzist</i><par n="i__vblex"/></e>
```

**Result:**
- `ekzisti` (infinitive) → `ekzist + i` → `ekzisti<vblex><inf>`
- `ekzistas` (present) → `ekzist + as` → `ekzisti<vblex><pres>`
- `ekzistis` (past) → `ekzist + is` → `ekzisti<vblex><past>`

**ONE entry generates ALL forms!** ✅

---

**Step 2: Bilingual Dictionary**

You only need **ONE entry** for the lemma (base form):

```xml
<!-- Map lemmas only - not every conjugation -->
<e><p><l>existar<s n="vblex"/></l><r>ekzisti<s n="vblex"/></r></p></e>
```

This matches:
- `ekzisti<vblex><inf>` → `existar<vblex><inf>`
- `ekzisti<vblex><pres>` → `existar<vblex><pres>`
- `ekzisti<vblex><past>` → `existar<vblex><past>`

**Tag wildcarding:** The bilingual lookup matches the base lemma and preserves tense tags!

---

**Step 3: Transfer Rules**

Convert Esperanto tense tags → Ido tense tags:

```xml
<rule>
  <when>
    <test><equal><clip pos="1" part="temps"/><lit-tag v="pres"/></equal></test>
    <out>
      <clip pos="1" part="lem"/>
      <clip pos="1" part="a_vblex"/>
      <lit-tag v="pri"/>  <!-- Esperanto 'pres' → Ido 'pri' -->
    </out>
  </when>
</rule>
```

---

**Step 4: Target Language Dictionary** (Ido)

```xml
<!-- Ido verb paradigm -->
<e lm="existar"><i>exist</i><par n="ar__vblex"/></e>
```

Generates:
- `existar<vblex><pri>` → `existar`
- `existar<vblex><pii>` → `existis`
- `existar<vblex><fti>` → `existos`

---

### **Why This Is Beautiful:**

**ONE entry per verb in each dictionary = INFINITE conjugations!**

```
Monolingual Esperanto: 1 entry (ekzisti) → 50+ forms
Bilingual:             1 entry (ekzisti↔existar)
Monolingual Ido:       1 entry (existar) → 50+ forms
Transfer:              Rules handle tag conversion

TOTAL: 3 entries + paradigms = ALL VERB FORMS ✅
```

---

## **APPROACH 2: Exhaustive Listing** ❌ NOT RECOMMENDED

Adding every single form manually:

```xml
<!-- BAD: Would need hundreds of entries per verb! -->
<e><p><l>existar<s n="vblex"/><s n="inf"/></l><r>ekzisti<s n="vblex"/><s n="inf"/></r></p></e>
<e><p><l>existar<s n="vblex"/><s n="pres"/></l><r>ekzisti<s n="vblex"/><s n="pres"/></r></p></e>
<e><p><l>existar<s n="vblex"/><s n="past"/></l><r>ekzisti<s n="vblex"/><s n="past"/></r></p></e>
<!-- ... hundreds more for every tense/mood/aspect -->
```

**Problems:**
- Unmaintainable (thousands of entries)
- Error-prone
- Doesn't scale
- Defeats the purpose of paradigms

---

## **THE REAL ISSUE: vbser vs vblex**

The problem with `ekzistas` → `@ekzisti` is **NOT** about missing forms.

### What's Happening:

**Current Situation:**
```bash
# Esperanto morphology produces:
ekzistas → ekzisti<vbser><pres>  (copula verb)

# Our bilingual dictionary has:
existar<vblex> ↔ ekzisti<vblex>

# Mismatch:
ekzisti<vbser> ≠ ekzisti<vblex>
# No match → @ekzisti
```

### Why the Mismatch?

Esperanto has **two verb categories**:
- `vblex` - regular verbs (havi, fari, iri)
- `vbser` - copula "to be" verbs (esti, esti as auxiliary)

Some verbs like `ekzisti` can be **BOTH**:
- `ekzisti<vblex>` - "to exist" (normal verb)
- `ekzisti<vbser>` - "there exists" (copula usage)

### The Solution:

**Add TWO bilingual entries** - one for each tag:

```xml
<!-- Regular verb usage -->
<e><p><l>existar<s n="vblex"/></l><r>ekzisti<s n="vblex"/></r></p></e>

<!-- Copula verb usage -->
<e><p><l>existar<s n="vblex"/></l><r>ekzisti<s n="vbser"/></r></p></e>
```

**Total:** 2 entries, still handles ALL conjugations of both types!

---

## **YOUR UNDERSTANDING IS CORRECT!**

You wrote:
> "find the basic form and than add needed suffixes and postfixes of the language (translate stem+suffix if the word does not exist)"

**Exactly!** This is the paradigm system:

```
ekzist (stem) + as (suffix) = ekzistas
   ↓              ↓
existar (stem) + as (suffix) = existas

The bilingual dictionary maps STEMS
The paradigms add SUFFIXES  
The transfer rules convert TAG SETS
```

---

## **PRACTICAL EXAMPLE**

### Current State:

```bash
echo "ekzistas" | apertium -d . epo-ido
# Output: @ekzisti

# Why:
# 1. Morphology: ekzist + as → ekzisti<vbser><pres> ✅
# 2. Bilingual: ekzisti<vbser> → NO MATCH ❌ (only has vblex)
# 3. Output: @ekzisti
```

### After Adding vbser Entry:

```bash
echo "ekzistas" | apertium -d . epo-ido
# Output: existas

# How:
# 1. Morphology: ekzist + as → ekzisti<vbser><pres> ✅
# 2. Bilingual: ekzisti<vbser> → existar<vblex> ✅
# 3. Transfer: <pres> → <pri> ✅
# 4. Generator: exist + as → existas ✅
```

**ONE additional entry fixes ALL conjugations of that verb type!** 🎯

---

## **KEY INSIGHT**

Apertium's power comes from **paradigm-based morphology**:

- **NOT:** Add every word form manually
- **YES:** Add stem once, paradigm handles inflections
- **NOT:** Add every tag combination in bilingual
- **YES:** Add lemma, let wildcarding handle tags

This is why we can have:
- **88,000+ word forms** from just **5,000 entries** in Ido dictionary
- **Infinite verb conjugations** from a few paradigm definitions

---

## **WHAT YOU NEED TO DO**

For the problematic verb cases:

1. ✅ **Already working:** Stem-based system in place
2. ❌ **Need to add:** Missing tag variants (vbser entries)
3. ✅ **Don't need:** Every single conjugated form

**Solution:** Add ~10-20 bilingual entries for tag mismatches, NOT thousands!

---

## **SUMMARY**

✅ **Your understanding is correct!**
- Apertium uses stem + paradigm approach (smart!)
- We DON'T add every form manually (would be crazy!)
- The issue is tag category mismatches (vbser vs vblex)
- Solution: Add entries for each tag category variant

The system is already doing what you described - we just need to handle the edge cases where Esperanto and Ido categorize the same verb differently! 🎉

