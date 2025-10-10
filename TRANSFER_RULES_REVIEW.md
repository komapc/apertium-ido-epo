# Ido-Esperanto Transfer Rules Review

**Review Date:** October 10, 2025  
**Files Reviewed:**
- `apertium-ido-epo.ido-epo.t1x` (Ido → Esperanto, 752 lines)
- `apertium-ido-epo.epo-ido.t1x` (Esperanto → Ido, 390 lines)

---

## Executive Summary

The transfer rules have been comprehensively reviewed and annotated with detailed comments. Several critical issues and optimization opportunities were identified. The rules are functional for basic translation but have significant design flaws that affect accuracy in specific grammatical contexts.

---

## Critical Issues Found

### 1. ⚠️ **BROKEN: Context-Insensitive Conjunction Rules** (Ido→Esperanto)
**Location:** Lines 375-449 in `ido-epo.t1x`  
**Severity:** HIGH

**Problem:**
The conjunction rules blindly apply accusative case to ALL nouns following coordinating conjunctions, regardless of whether they're subjects or objects.

**Examples of Incorrect Translation:**
```
✗ WRONG: "La kato kaj la hundo kuras" → "La kato kaj la hundon kuras"
         (Coordinated subjects incorrectly marked as objects)

✓ RIGHT: Should only apply accusative in object contexts:
         "Mi vidas la katon kaj la hundon"
```

**Root Cause:**
The rules use a 2-token pattern `[conjunction + noun]` without tracking whether we're in an object context (after a transitive verb).

**Recommended Solution:**
1. **Short-term:** Add longer patterns that include the verb: `[verb + noun + conjunction + noun]`
2. **Long-term:** Implement variables to track transitivity context or use chunking/two-stage transfer

---

### 2. ⚠️ **Missing Copula Check for Proper Nouns** (Ido→Esperanto)
**Location:** Lines 718-749 in `ido-eeo.t1x`  
**Severity:** MEDIUM

**Problem:**
The rule `[Verb + ProperNoun]` applies accusative to ALL proper nouns after verbs, but doesn't check if the verb is "esar" (to be).

**Example:**
```
✗ WRONG: "Li esas Petron" (He is Peter-ACC)
✓ RIGHT: "Li esas Petro" (He is Peter-NOM)
```

**Recommended Solution:**
Add a conditional check similar to the common noun rules (lines 212-249) to distinguish copula from transitive verbs.

---

### 3. ⚠️ **Aggressive Pronoun Tag Stripping** (Esperanto→Ido)
**Location:** Lines 204-226 in `epo-ido.t1x`  
**Severity:** MEDIUM

**Problem:**
The pronoun rule strips ALL morphological features (case, number, gender), outputting only `lemma + prn`.

**Risk:**
Both Esperanto and Ido distinguish pronoun cases:
- Esperanto: mi/min (I/me), ni/nin (we/us)
- Ido: me/mi (I/me), nos/ni (we/us)

Stripping case information may cause incorrect pronoun forms in the output.

**Recommended Solution:**
Preserve case tags: `<clip pos="1" side="tl" part="cas"/>`

---

## Design Issues & Optimizations

### 4. 📋 **Redundant Code: Separate Handling of Same Verb** (Ido→Esperanto)
**Location:** Lines 88-159 (vbser) vs. Lines 161-373 (vblex with "esar" checks)  
**Severity:** LOW (code quality)

**Problem:**
The copula "esar" is handled in two separate rule sets:
1. Category `vbser` specifically for "esar" (lines 88-159)
2. Generic `vblex` with conditional checks for "esar" (lines 161-373)

**Impact:**
- Code duplication
- Maintenance burden (changes must be synchronized)
- Potential for inconsistencies

**Recommended Solution:**
Consolidate into one approach. Either:
- Remove vbser category and handle everything in vblex with conditionals, OR
- Ensure vbser catches all "esar" patterns so vblex rules never see it

---

### 5. 📋 **Default Tense Assumption** (Ido→Esperanto)
**Location:** Lines 570-578 in `ido-epo.t1x`  
**Severity:** LOW (potential error masking)

**Problem:**
When no tense tag is found on a verb, the rule defaults to present tense.

**Risk:**
This might hide errors in morphological analysis, making debugging harder.

**Recommended Solution:**
Add logging/warning mechanism, or output a special error marker when tense is missing.

---

### 6. 📋 **Hardcoded Singular for Proper Nouns** (Ido→Esperanto)
**Location:** Line 744 in `ido-epo.t1x`  
**Severity:** LOW

**Problem:**
The rule hardcodes `<lit-tag v="sg"/>` for all proper nouns, but some proper nouns can be plural (e.g., "Usono" = United States, geographic regions).

**Recommended Solution:**
Preserve the original number tag: `<clip pos="2" side="tl" part="nbr"/>`

---

### 7. ✅ **Missing Degree Constructions** (Esperanto→Ido)
**Location:** Lines 324-352 in `epo-ido.t1x`  
**Severity:** LOW (missing functionality)

**Problem:**
Only the superlative "plej + ADJ → maxim + ADJ" is handled. Missing:
- Superlative with adverbs: "plej rapide" → "maxim rapide"
- Comparative: "pli bela" → "plu bela"
- Comparative with adverbs: "pli rapide" → "plu rapide"

**Recommended Solution:**
Add rules for:
```xml
<!-- plej + adverb -->
<pattern>
  <pattern-item n="plej"/>
  <pattern-item n="adv"/>
</pattern>

<!-- pli + adjective -->
<pattern>
  <pattern-item n="pli"/>
  <pattern-item n="adj"/>
</pattern>
```

---

## Correct and Well-Designed Rules

### ✅ Adjective-Noun Agreement (Ido→Esperanto)
**Location:** Lines 451-476 in `ido-epo.t1x`

Correctly propagates number and case from nouns to adjectives in Esperanto, where adjectives must agree.

---

### ✅ Tense Conversion (Both Directions)
**Location:** 
- Lines 527-582 in `ido-epo.t1x`
- Lines 156-202 in `epo-ido.t1x`

Clean bidirectional mapping:
- pri ↔ pres (present)
- pii ↔ past (past)
- fti ↔ fti (future)

---

### ✅ Adjective Invariability (Esperanto→Ido)
**Location:** Lines 120-140 in `epo-ido.t1x`

Correctly strips number/case agreement from adjectives when translating to Ido, where adjectives are invariable.

---

### ✅ Partitive/Genitive Preposition (Esperanto→Ido)
**Location:** Lines 354-387 in `epo-ido.t1x`

Correctly transforms Esperanto partitive "da" to Ido genitive "di":
- "glaso da akvo" → "glaso di aquo"

---

## Summary Statistics

| Metric | Ido→Esperanto | Esperanto→Ido |
|--------|---------------|---------------|
| **Total Rules** | 25 | 12 |
| **Critical Issues** | 2 | 1 |
| **Medium Issues** | 1 | 0 |
| **Low Issues** | 3 | 1 |
| **Well-Designed** | 19 | 10 |

---

## Recommendations Priority

### High Priority (Fix Immediately)
1. **Fix conjunction rules** - Major source of incorrect translations
2. **Add copula check for proper nouns** - Causes grammatical errors

### Medium Priority
3. **Preserve pronoun case information** - Risk of pronoun errors

### Low Priority (Code Quality)
4. Consolidate redundant copula handling
5. Add logging for default tense assumption
6. Preserve proper noun number tags
7. Add missing degree constructions

---

## Testing Recommendations

To validate fixes, test with:

1. **Coordinated subjects:**
   - "La kato kaj la hundo kuras" (subjects)
   - "Mi vidas la katon kaj la hundon" (objects)

2. **Copula with proper nouns:**
   - "Li esas Petro" (predicate nominative)
   - "Mi konocas Petron" (direct object)

3. **Pronouns with case:**
   - "Mi vidas lin" → "Me vidas il" (accusative)
   - "Li estas bela" → "Il esas bela" (nominative)

4. **Degree constructions:**
   - "plej bela" → "maxim bela"
   - "plej rapide" → "maxim rapide"
   - "pli bela" → "plu bela"

---

## Conclusion

The transfer rules are **functionally adequate for simple sentences** but have **critical design flaws** that cause errors in:
- Coordinated noun phrases
- Predicate nominatives with proper nouns
- Potentially pronoun case agreement

The most urgent fix is the conjunction rule redesign, as it affects a common grammatical pattern and produces clearly incorrect output.

All identified issues have been documented with inline comments in the source files for future maintenance.


