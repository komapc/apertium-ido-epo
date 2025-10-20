# Suffix Transformation Rules for Ido-Esperanto

## Overview
This document describes the productive suffix paradigms and transformation rules between Ido and Esperanto.

---

## ✅ Implemented Suffix Paradigms

### 1. -oza Paradigm (Adjectives: "Full of, Characterized by")

**Status:** ✅ Fully Implemented

**Ido → Esperanto:** `-oza` → `-oza` (same form)

**Paradigm Definition (`apertium-ido.ido.dix`):**
```xml
<pardef n="oza__adj">
  <e><p><l>oza</l><r><s n="adj"/></r></p></e>
  <e><p><l>oze</l><r><s n="adv"/></r></p></e>
</pardef>
```

**Coverage:** 30 adjectives
- nervoza → nervoza (nervous)
- grandioza → grandioza (grandiose)
- famoza → famoza (famous)
- etc.

**Implementation Notes:**
- Fixed 10 adjectives that were using wrong paradigms (o__n, e__adv, a__adj)
- Added 4 missing bilingual mappings (brizoza, frenezioza, precoza, stonetoza)
- All -oza adjectives now correctly use `oza__adj` paradigm

---

### 2. -ajo Paradigm (Nouns: "Concrete thing made from X")

**Status:** ✅ Paradigm Implemented, Bilingual Mappings In Progress

**Ido → Esperanto:** `-ajo` → `-aĵo`

**Paradigm Definition (`apertium-ido.ido.dix`):**
```xml
<pardef n="ajo__n">
  <e><p><l>ajo</l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
  <e><p><l>aji</l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>
  <e><p><l>ajon</l><r><s n="n"/><s n="sg"/><s n="acc"/></r></p></e>
  <e><p><l>ajin</l><r><s n="n"/><s n="pl"/><s n="acc"/></r></p></e>
</pardef>
```

**Coverage:** 50 nouns identified
- fromajo → fromaĵo (cheese/cheese dish)
- bagajo → bagaĵo (luggage item)
- skribajo → skribaĵo (something written)
- etc.

**Example Entry:**
```xml
<e lm="fromajo">
  <i>from</i>
  <par n="ajo__n"/>
</e>
```

**Bilingual Mapping:**
```xml
<e>
  <p>
    <l>from<s n="n"/></l>
    <r>fromaĵo<s n="n"/></r>
  </p>
</e>
```

**Implementation Status:**
- ✅ Paradigm created
- ✅ 22 words converted to use new paradigm
- ⚠️ 37 words still need bilingual mappings added

**Remaining Work:**
Words needing bilingual mappings: almonajo, aquafortajo, avantajo, averajo, bagajo, brulajo, cedratajo, certajo, chasajo, cirajo, debajo, derivajo, drinkajo, etajo, fiktivajo, fromajo, imajo, kajo, kavajo, koagulajo, konfitajo, koruptajo, mariajo, menajo, mirajo, nutrajo, pasturajo, peizajo, plajo, projektajo, proprietajo, requizitajo, restajo, skribajo, subsidiajo, vicinajo, vilajo

---

### 3. -iva Paradigm (Adjectives: "Capable of, Able to")

**Status:** ⚠️ Partially Implemented - Needs Clarification

**Ido → Esperanto:** `-iva` → `-ebla` (for productive formations)

**Important Distinction:**
- **International adjectives** (borrowings): aktiva, pasiva, negativa, pozitiva, etc. 
  - These are NOT using the productive -iva suffix
  - They map to the SAME form in Esperanto: aktiva → aktiva
  - Currently: 17 such adjectives, all correctly mapped
  
- **Productive -iva formations** (from verb roots): 
  - Meaning: "capable of doing X" or "able to become X"
  - Should map to `-ebla` in Esperanto
  - Example: konstruiva (capable of constructing) → konstruebla
  - Currently: NOT implemented

**Paradigm Definition (`apertium-ido.ido.dix`):**
```xml
<pardef n="iva__adj">
  <e><p><l>iva</l><r><s n="adj"/></r></p></e>
  <e><p><l>ive</l><r><s n="adv"/></r></p></e>
</pardef>
```

**Current Status:**
- ✅ `iva__adj` paradigm exists but is NOT being used
- ✅ International adjectives use `a__adj` paradigm with stem ending in `-iv` (correct)
- ⚠️ No transfer rule exists for `-iva` → `-ebla` transformation
- ⚠️ No productive -iva words currently in dictionary

**Implementation Needed:**
1. Add transfer rule in `apertium-ido-epo.ido-epo.t1x` to handle -iva → -ebla
2. OR document that this is for future/productive use only

**Reference:** [Esperanto Wiktionary -iva entry](https://eo.wiktionary.org/wiki/-iva)  
_"kapabla fari (kun verba radikalo transitiva) aŭ farigi (kun verba radikalo netransitiva)"_  
_"capable of doing (with transitive verb root) or becoming (with intransitive verb root)"_

---

## Transformation Rules Summary

| Ido Suffix | Esperanto Suffix | Type | Status | Words |
|------------|------------------|------|--------|-------|
| **-oza** | -oza | Adj | ✅ Complete | 30 |
| **-ajo** | -aĵo | Noun | ⚠️ In Progress | 50 |
| **-iva** (productive) | -ebla | Adj | ❌ Not Implemented | TBD |
| **-iva** (international) | -iva | Adj | ✅ Complete | 17 |

---

## Technical Implementation Details

### Morphological Analysis Pipeline

1. **Ido Analysis:** `fromajo` → `from<n><sg><nom>`
2. **Bilingual Transfer:** `from<n>` → `fromaĵo<n>`
3. **Esperanto Generation:** `fromaĵo<n><sg><nom>` → `fromaĵo`

### Paradigm Usage Pattern

**Before (individual entries):**
```xml
<e lm="fromajo">
  <i>fromaj</i>
  <par n="o__n"/>
</e>
```

**After (paradigm-based):**
```xml
<e lm="fromajo">
  <i>from</i>
  <par n="ajo__n"/>
</e>
```

**Benefits:**
- ✅ DRY principle - define suffix once
- ✅ Easier to maintain
- ✅ Consistent morphology
- ✅ Smaller dictionary size (stem vs. stem+suffix)

---

## Related Paradigms (For Reference)

### -ala Paradigm (Already Implemented)
- **Coverage:** 108 adjectives
- **Pattern:** Various mappings to Esperanto (-a, -ia, -ea)
- **Status:** ✅ Fully implemented

### Other Candidates (Not Yet Implemented)
- **-ebla:** 25 adjectives (Ido -ebla → Esperanto -ebla)
- **-ema:** 9 adjectives (Ido -ema → Esperanto -ema)

---

## Fixes Applied

### 1. Fixed Incorrect Paradigms in -oza Adjectives
Corrected 10 adjectives using wrong paradigms:
- saloza, saporoza, sukoza, truoza (were using `o__n` noun paradigm)
- vaporoza, vigoroza, vinkoza, violentoza (were using `o__n` noun paradigm)
- stonetoza (was using `e__adv` adverb paradigm)
- viskoza (was using generic `a__adj` instead of `oza__adj`)

### 2. Added Missing Bilingual Mappings for -oza
Added 4 missing mappings:
- brizoz → brizoza
- frenezioz → frenezioza  
- precoz → precoza
- stonetoz → ŝtonetoza

### 3. Created and Deployed -ajo Paradigm
- Defined `ajo__n` paradigm with full noun inflection
- Converted 22 existing words to use new paradigm
- Documented 37 words needing bilingual mappings

---

## Testing

### Verify Paradigms
```bash
# Test -oza adjective
echo "nervoza" | apertium -d . ido-epo
# Expected: nervoza

# Test -ajo noun  
echo "fromajo" | apertium -d . ido-epo
# Expected: fromaĵo (once bilingual mapping added)
```

### Compile Dictionary
```bash
cd /home/mark/apertium-ido-epo/apertium-ido-epo
make
```

---

## References

- [Ido Grammar - Suffixes](http://www.romaniczo.com/ido/gramatiko/grammar_17.html)
- [Esperanto Wiktionary: -iva](https://eo.wiktionary.org/wiki/-iva)
- [Esperanto Wiktionary: -aĵo](https://eo.wiktionary.org/wiki/-a%C4%B5o)
- [Apertium Dictionary Format](https://wiki.apertium.org/wiki/Dictionaries)

---

**Document created:** October 10, 2025  
**Last updated:** October 10, 2025  
**Author:** Apertium Ido-Esperanto Development Team


