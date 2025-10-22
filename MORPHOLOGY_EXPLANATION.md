# Morphology Issue Explanation

## What Files Am I Looking At?

I'm examining: `/home/mark/apertium-ido-epo/apertium/apertium-ido-epo/apertium-ido.ido.dix`

This is the **Ido monolingual morphological dictionary** that tells Apertium:
- How Ido words inflect (conjugate, pluralize, etc.)
- What grammatical forms exist for each word

## What Rules (Paradigms) DO We Have?

### Current Paradigms in apertium-ido.ido.dix:

```xml
1. o__n (noun)
   - Defines: "o" → singular nominative
   - Example: "kato" → cat (singular)
   - Missing: plural (-i), accusative (-n, -i-n)

2. a__adj (adjective)  
   - Defines: "a" → adjective form
   - Example: "granda" → big
   - Missing: plural (-i), accusative (-n, -i-n)

3. e__adv (adverb)
   - Defines: "e" → adverb form
   - Example: "rapide" → quickly
   - Complete (adverbs don't inflect in Ido)

4. ar__vblex (verb) **← THE PROBLEM!**
   - Defines: "ar" → infinitive only
   - Example: "esar" → to be
   - Missing: ALL conjugations!

5. __pr, __det, __prn, __cnjcoo, __cnjsub (function words)
   - Defines: empty inflection (invariable)
   - Example: "la" (the), "me" (I), "e" (and)
   - Complete (don't inflect)
```

## The Problem Illustrated

### What We Have: ar__vblex
```xml
<pardef n="ar__vblex">
  <e>
    <p>
      <l>ar</l>  <!-- input: "ar" -->
      <r>
        <s n="vblex" />
        <s n="inf" />  <!-- output: verb infinitive -->
      </r>
    </p>
  </e>
</pardef>
```

**Dictionary entry:**
```xml
<e lm="esar">
  <i>esar</i>  <!-- stem: "es" -->
  <par n="ar__vblex" />  <!-- paradigm adds: "ar" → infinitive -->
</e>
```

**What Apertium recognizes:**
- ✅ `esar` → `es` + `ar` → verb, infinitive ✅

**What Apertium DOESN'T recognize:**
- ❌ `esas` → `es` + `as` → ??? (no rule for "as")
- ❌ `esis` → `es` + `is` → ??? (no rule for "is")
- ❌ `esos` → `es` + `os` → ??? (no rule for "os")

**Result:** Can't translate `"Me esas bona"` because `esas` is unknown!

---

## What We NEED: Complete ar__vblex Paradigm

```xml
<pardef n="ar__vblex">
  <!-- Infinitive -->
  <e><p><l>ar</l><r><s n="vblex"/><s n="inf"/></r></p></e>
  
  <!-- Present tense -->
  <e><p><l>as</l><r><s n="vblex"/><s n="pri"/></r></p></e>
  
  <!-- Past tense -->
  <e><p><l>is</l><r><s n="vblex"/><s n="pii"/></r></p></e>
  
  <!-- Future tense -->
  <e><p><l>os</l><r><s n="vblex"/><s n="fti"/></r></p></e>
  
  <!-- Conditional -->
  <e><p><l>us</l><r><s n="vblex"/><s n="cni"/></r></p></e>
  
  <!-- Imperative -->
  <e><p><l>ez</l><r><s n="vblex"/><s n="imp"/></r></p></e>
</pardef>
```

**With this, the dictionary entry for "esar" would recognize:**
- ✅ `esar` → es+ar → to be (infinitive)
- ✅ `esas` → es+as → is/are (present)
- ✅ `esis` → es+is → was/were (past)
- ✅ `esos` → es+os → will be (future)
- ✅ `esus` → es+us → would be (conditional)
- ✅ `esez` → es+ez → be! (imperative)

---

## Similarly for Nouns (o__n)

### Current:
```xml
<pardef n="o__n">
  <e><p><l>o</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
</pardef>
```
- Only recognizes: `kato` (cat, singular, nominative)

### Needed:
```xml
<pardef n="o__n">
  <!-- Singular nominative -->
  <e><p><l>o</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
  
  <!-- Singular accusative -->
  <e><p><l>on</l><r><s n="n"/><s n="sg"/><s n="acc"/></r></p></e>
  
  <!-- Plural nominative -->
  <e><p><l>i</l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>
  
  <!-- Plural accusative -->
  <e><p><l>in</l><r><s n="n"/><s n="pl"/><s n="acc"/></r></p></e>
</pardef>
```

**With this, "kato" would recognize:**
- ✅ `kato` → cat (singular)
- ✅ `katon` → cat (singular, accusative)
- ✅ `kati` → cats (plural)
- ✅ `katin` → cats (plural, accusative)

---

## The Answer

**WHERE am I looking?**
→ In `apertium-ido.ido.dix` (lines 29-91) - the `<pardefs>` section

**WHAT rules do we have?**
→ Only **skeleton rules** (infinitive, singular, base forms only)

**WHAT's missing?**
→ **All inflections** (verb conjugations, noun plurals, adjective agreement)

**WHY doesn't translation work?**
→ Because Apertium can't recognize inflected forms like `esas`, `katon`, `grandi`

---

## Solution

We need to either:
1. **Find existing complete paradigms** from official Apertium Ido repos
2. **Create paradigms manually** based on Ido grammar rules (simple, regular)
3. **Import from another Apertium language** and adapt (Esperanto paradigms are similar)

Ido is very regular, so creating paradigms is straightforward once we have the grammar rules!
