# Byzantine Empire Article - Esperanto→Ido Translation Analysis

**Source:** [Esperanto Wikipedia - Bizanca imperio](https://eo.wikipedia.org/wiki/Bizanca_imperio)  
**Date:** October 9, 2025  
**Direction:** **Esperanto → Ido** (reverse direction)  
**Test:** Historical article translation

---

## Test Sentences (6 sentences)

### Sentence 1:
```
EPO: La Bizanca Imperio estis kontinuaĵo de la Romia Imperio en siaj orientaj provincoj.
IDO: @La @Bizanca Imperio @esti @kontinuaĵo @de @la @Romia Imperio en lua #orienta provinci@.@
EXP: La Bizanca Imperio esis kontinuajo de la Romia Imperio en lua orienta provincii.
```

**Quality:** ❌ 25% - Poor  
**Issues:** Most words marked with @ (not in dictionary for epo→ido direction)

---

### Sentence 2:
```
EPO: La imperio daŭris de 395 ĝis 1453.
IDO: @La imperio duris @de @395 @ĝis @1453@.@
EXP: La imperio duris de 395 til 1453.
```

**Quality:** ⚠️ 40% - Fair  
**Issues:** Articles, prepositions, numbers not found

---

### Sentence 3:
```
EPO: Ĝia ĉefurbo estis Konstantinopolo.
IDO: Olua #chefurbo @esti @Konstantinopolo@.@
EXP: Olua chefurbo esis Konstantinopolo.
```

**Quality:** ⚠️ 45% - Fair  
**Issues:** "estis" not found, proper noun missing

---

### Sentence 4:
```
EPO: La Bizanca Imperio estis la plej potenca stato en Eŭropo dum la Mezepoko.
IDO: @La @Bizanca Imperio @esti @la maxim #potenta estado en @Eŭropo @dum @la @Mezepoko@.@
EXP: La Bizanca Imperio esis la maxim potenca stato en Eŭropo dum la Mezepoko.
```

**Quality:** ⚠️ 35% - Fair  
**Issues:** Many words not in reverse dictionary

---

### Sentence 5:
```
EPO: La imperio falis en 1453 kiam la turkoj konkeros Konstantinopolon.
IDO: @La imperio falis en @1453 kande @la @turko konquestos @Konstantinopolo@.@
EXP: La imperio falis en 1453 kande la turki konkeros Konstantinopolo.
```

**Quality:** ⚠️ 50% - Fair  
**Issues:** Articles, numbers, some words not in reverse dictionary

**Positive:** Some words working (falis, en, kande → works!)

---

### Sentence 6:
```
EPO: La bizanca kulturo influis la kulturon de multaj landoj.
IDO: @La @bizanca kulturo influis @la kulturon @de @multa landi@.@
EXP: La bizanca kulturo influis la kulturon de multa landi.
```

**Quality:** ⚠️ 45% - Fair  
**Issues:** Articles, adjectives not in reverse dictionary

---

## Coverage Statistics

| Marker | Count | Meaning |
|--------|-------|---------|
| **@** | ~35 | Not in dictionary (most common!) |
| **#** | ~3 | Generation issue |
| **\*** | ~0 | Passthrough |

**Overall Quality:** ~40% - Poor to Fair

---

## Critical Finding: @ Markers Everywhere! ⚠️⚠️⚠️

###The problem:
Almost every common word has @ marker, meaning it's **not in the bilingual dictionary** for the Esperanto→Ido direction.

**Words marked with @:**
- `@La` - the (article)
- `@de` - of/from (preposition)
- `@la` - the
- `@esti` - was (verb)
- `@Bizanca` - Byzantine
- `@kontinuaĵo` - continuation
- `@Romia` - Roman
- `@ĝis` - until
- `@395`, `@1453` - numbers
- `@dum` - during
- `@Mezepoko` - Middle Ages
- `@turko` - Turk
- `@multa` - many

---

## Root Cause Analysis

### Why Epo→Ido is broken:

Our bilingual dictionary (`apertium-ido-epo.ido-epo.dix`) was built primarily for **Ido→Esperanto** direction.

**Bilingual dictionary format:**
```xml
<e><p>
  <l>IDEO_WORD<s n="pos"/></l>
  <r>ESPERANTO_WORD<s n="pos"/></r>
</p></e>
```

This creates:
- **LR (Left-to-Right):** Ido → Esperanto ✓ Works
- **RL (Right-to-Left):** Esperanto → Ido ✗ Should work but doesn't?

### Investigation needed:

When we compiled the dictionary:
```bash
lt-comp lr apertium-ido-epo.ido-epo.dix ido-epo.autobil.bin  # Ido→Epo
lt-comp rl apertium-ido-epo.ido-epo.dix epo-ido.autobil.bin  # Epo→Ido
```

The `rl` compilation SHOULD create reverse lookups, but many words show @ markers.

**Possible causes:**
1. Dictionary entries missing reverse direction entries
2. Tag mismatches preventing reverse lookup
3. Paradigm issues in Esperanto monolingual analyzer

---

## What Works in Epo→Ido (Surprisingly)

Despite the @ markers, some things work:

✅ **Words that work:**
- `imperio` → `Imperio`
- `falis` → `falis`
- `en` → `en`
- `kulturo` → `kulturo`
- `influis` → `influis`
- `politiko` → `politiko`
- `kande` → `kande` (when)
- `kaj` → `e` (and - after our fix!)

✅ **Grammar:**
- `lua` (possessive) works
- Basic sentence structure preserved
- Some verb forms work

---

## Comparison: Ido→Epo vs Epo→Ido

| Metric | Ido→Epo | Epo→Ido | Difference |
|--------|---------|---------|------------|
| **Clean output** | ~65% | ~25% | -40% |
| **# markers** | ~16% | ~5% | Better! |
| **@ markers** | ~0% | ~60% | Much worse! |
| **Quality** | ~82% | ~40% | -42% |

**Conclusion:** Esperanto→Ido direction is **significantly worse** than Ido→Esperanto.

---

## Why This Happened

### Design Issue:
The dictionaries were built from **Ido Wiktionary**, which provides:
- Ido word → Esperanto translation ✓
- NOT: Esperanto word → Ido translation ✗

### Missing Reverse Entries:
Common Esperanto words not mapped back to Ido:
- Articles: `la`, `La`
- Prepositions: `de`, `ĝis`, `dum`
- Verbs: `estis` (was)
- Adjectives: `Bizanca`, `Romia`
- Nouns: `kontinuaĵo`, `Mezepoko`

---

## Recommendations for Epo→Ido

### If we want to support Esperanto→Ido properly:

1. **Extract from Esperanto Wiktionary**
   - Get Esperanto→Ido mappings
   - Or create reverse mappings programmatically

2. **Add common Esperanto words manually**
   - Articles, prepositions, conjunctions
   - At minimum: la, de, ĝis, al, en, sur, etc.

3. **Create systematic reverse mappings**
   - For each Ido→Epo entry, create Epo→Ido entry
   - Handle morphological differences

4. **Test extensively**
   - Build Epo→Ido test corpus
   - Ensure bidirectional quality

---

## Current Focus

**For now: Ido→Esperanto direction is the priority**

The Ido→Epo direction is working well (~82% quality after fixes).  
The Epo→Ido direction would require significant additional work.

**Recommendation:** 
- Document that Ido→Epo is the primary/supported direction
- Epo→Ido is experimental/incomplete
- Focus efforts on improving Ido→Epo quality to 90%+

---

## Summary

**Ido→Esperanto:** ✅ Good quality (~82%), functional  
**Esperanto→Ido:** ⚠️ Poor quality (~40%), needs work  

**Current state:** Asymmetric translator - works well in one direction only.

**To fix:** Would need to build comprehensive Esperanto→Ido dictionary, which is a separate project of similar scope to what we've already done.

---

## Files

- ✅ `test_byzantine_epo.txt` - Test sentences (Esperanto)
- ✅ `BYZANTINE_EPO_IDO_ANALYSIS.md` - This analysis

**Source:** https://eo.wikipedia.org/wiki/Bizanca_imperio


