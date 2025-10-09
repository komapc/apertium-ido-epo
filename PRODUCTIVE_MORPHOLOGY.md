# Productive Morphology in Ido-Esperanto Translation

## Overview

This document describes the productive morphology paradigms implemented in the Ido monolingual dictionary to enable scalable translation of derived forms.

---

## ✅ Implemented: -ala Paradigm (Relational Adjectives)

### Usage
The `-ala` suffix creates relational adjectives from nouns (similar to English "-al"):
- `suno` (sun) → `sunala` (solar)
- `astronomio` (astronomy) → `astronomiala` (astronomical)
- `naturo` (nature) → `naturala` (natural)

### Implementation
**Paradigm definition:**
```xml
<pardef n="ala__adj">
  <e><p><l>ala</l><r><s n="adj"/></r></p></e>
  <e><p><l>ale</l><r><s n="adv"/></r></p></e>
</pardef>
```

**Example entries:**
```xml
<e lm="sunala">
  <i>sun</i>
  <par n="ala__adj"/>
</e>
```

### Coverage
- **108 adjectives** implemented
- **Esperanto equivalents:** Various patterns (`-a`, `-ia`, `-ea`)
- **Examples:** `sunala→suna`, `astronomiala→astronomia`, `naturala→natura`

### Benefits
✅ DRY principle - add stem, get adjective + adverb automatically  
✅ Scalable - easy to add new adjectives  
✅ Maintainable - single paradigm definition

---

## 🔄 Candidates for Future Implementation

### 1. -oza Suffix (Full of, Rich in)
**Count:** 29 adjectives  
**Examples:**
- `famoza` (famous) → Epo: `fama`
- `glorioza` (glorious) → Epo: `glora`
- `populoza` (populous) → Epo: `popola`

**Pattern:** Usually `-oza` → `-a` in Esperanto

**Priority:** Medium  
**Effort:** 2-3 hours

---

### 2. -iva Suffix (Having the nature/quality of)
**Count:** 31 adjectives  
**Examples:**
- `aktiva` (active) → Epo: `aktiva`
- `produktiva` (productive) → Epo: `produktiva`
- `defensiva` (defensive) → Epo: `defenda`

**Pattern:** Often same in Esperanto, but some variation

**Priority:** Medium  
**Effort:** 3-4 hours (requires checking each mapping)

---

### 3. -ebla Suffix (Able to be, -able)
**Count:** 25 adjectives  
**Examples:**
- `posibla` (possible) → Epo: `ebla`
- `videbla` (visible) → Epo: `videbla`
- `amebla` (lovable) → Epo: `amebla`

**Pattern:** Mixed - some regular, some exceptions

**Priority:** Medium  
**Effort:** 2-3 hours

---

### 4. -ema Suffix (Having a tendency to)
**Count:** 9 adjectives  
**Examples:**
- `kredema` (credulous) → Epo: `kredema`
- `timema` (timid) → Epo: `timema`

**Pattern:** Usually same in Esperanto

**Priority:** Low (only 9 words)  
**Effort:** 1 hour

---

## Implementation Guidelines

### Step 1: Analyze the Suffix
```bash
# Extract all adjectives with the suffix
grep -o "<l>[^<]*SUFFIX<s n=\"adj\"/>" apertium-ido-epo.ido-epo.dix \
  | sed 's/<l>//; s/<s n="adj"\/>//' | sort -u > stems.txt

# Check how they map to Esperanto
grep -B1 -A1 "SUFFIX" apertium-ido-epo.ido-epo.dix | grep "<r>"
```

### Step 2: Create Paradigm
```xml
<pardef n="SUFFIX__adj">
  <e><p><l>SUFFIX</l><r><s n="adj"/></r></p></e>
  <e><p><l>SUFFIXe</l><r><s n="adv"/></r></p></e>
</pardef>
```

**Important:** Use compact format (no whitespace in tags) to avoid pipeline issues!

### Step 3: Add Entries
```xml
<e lm="stemSUFFIX">
  <i>stem</i>
  <par n="SUFFIX__adj"/>
</e>
```

### Step 4: Update Bilingual Dictionary
Change from: `<l>stemSUFFIX<s n="adj"/></l>`  
To: `<l>stem<s n="adj"/></l>`

### Step 5: Remove Duplicates
Check for and remove old full-word entries that conflict with the new paradigm.

### Step 6: Test
```bash
echo "stemSUFFIX" | apertium -d . ido-epo
```

---

## Technical Notes

### Whitespace Issue
**Problem:** lttoolbox includes XML formatting in analysis output  
**Solution:** Use compact tag format without newlines:
```xml
<!-- ❌ Don't do this -->
<r>
  <s n="adj"/>
</r>

<!-- ✅ Do this -->
<r><s n="adj"/></r>
```

### Pipeline
1. **Analysis:** `stemSUFFIX` → `^stemSUFFIX/stem<adj>$`
2. **Bilingual:** `stem<adj>` → `esperantostem<adj>`
3. **Generation:** `esperantostem<adj>` → `esperantostema`

---

## Statistics

| Paradigm | Status | Entries | Esperanto Patterns | Priority |
|----------|--------|---------|-------------------|----------|
| **-ala** | ✅ Implemented | 108 | Mixed | - |
| **-iva** | 🔄 Candidate | 31 | Mostly regular | Medium |
| **-oza** | 🔄 Candidate | 29 | Regular | Medium |
| **-ebla** | 🔄 Candidate | 25 | Mixed | Medium |
| **-ema** | 🔄 Candidate | 9 | Regular | Low |

---

## References

- [Ido Grammar - Suffixes](http://www.romaniczo.com/ido/gramatiko/grammar_17.html)
- [Apertium Dictionary Format](https://wiki.apertium.org/wiki/Dictionaries)
- Commit: 74a3eea "Implement productive -ala adjective paradigm"

---

**Document created:** October 10, 2025  
**Last updated:** October 10, 2025
