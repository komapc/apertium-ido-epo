# Test Results Comparison

**Date:** December 6, 2025  
**Test:** Corpus sentences before vs after fixes

---

## Current Test Results (After Code Fixes, Before Dictionary Regeneration)

### Sentence 1
**Input:** Historical description of Ido

**Output:**
```
@Id estas konstruita lingvon *derivante *de Reformita Esperanton (reformita lingvon konstruas *de Esperanto, faras #de ↓ (indikante aganton) #tio #originalo #kreiint #de ↓ (indikante aganton) Esperanto) adoptas *kom Esperanto reformas *en *Paris #de ↓ (indikante aganton) #tio #Delegitaro, delegacio (*Délégation *pour *l'*adoption *d'*une *langue *auxiliaire *internationale) *ye #tio *24ma #de ↓ (indikante aganton) oktobro *1907. @Id *kreesis *por havi malmulta *polisemio, estas *sat konciza, facile *lernebla *e *uzebla. *Ol *kreesis *por esti Internacia @auxiliar lingvo *por personoj *de diversaj originoj *e estas #tio *maxim #sukcecooz *de #tio multa Esperanto-derivaĵoj, *quin *on *nomizas *Esperantidoj.
```

**Status:** ❌ No improvement yet - same errors as before

### Sentence 2
**Input:** Ido community meeting discussion

**Output:**
```
Hodiaŭ partoprenas *kin Idistoj #tio *saturdia *video-#konferenci. #Ne diskutas *inter #alie #iom detaloj *dil internacia @Id-#renkonti *2025 *e #tio #nova ↓ vortoj *dil *google-#grupo ↓ Lingvo. Restas #tio demandon *kad estas bona *remplacigar *od aldoni #jam #ekzistoant vortoj *per #nova ↓ vortoj *por #tio sama aĵo.
```

**Status:** ❌ No improvement yet - same errors as before

---

## Function Words Test

**Test:** `echo "por de en e od per ye kom" | apertium -d . ido-epo`

**Result:**
```
*por *de *en *e *od *per *ye *kom
```

**Status:** ❌ All function words still unknown

**Morphological Analysis:**
- `por`: `^por/*por$` (unknown)
- `de`: `^de/*de$` (unknown)
- `kom`: `^kom/*kom$` (unknown)
- `od`: `^od/*od$` (unknown)
- `e`: `^e/*e$` (unknown)

---

## Why No Improvement Yet

**Root Cause:** Dictionaries haven't been regenerated with the fixes

**What Was Fixed:**
1. ✅ Parser now extracts `por`, `od`, `kom` from numbered sections
2. ✅ Parser extracts POS from section headers `(prepoziciono)`
3. ✅ POS inference for function words
4. ✅ Paradigm assignment from POS
5. ✅ Default paradigms for words without POS

**What's Needed:**
1. Re-run extraction pipeline to get words from Wiktionary
2. Re-merge sources with new inference logic
3. Re-generate dictionaries
4. Copy to apertium directories
5. Recompile

**Current State:**
- Code fixes: ✅ Complete
- Dictionary regeneration: ❌ Not done yet
- Expected improvement: Will see after regeneration

---

## Next Steps

To see improvements, we need to:

1. **Re-run extraction:**
   ```bash
   cd projects/extractor
   python3 scripts/01_parse_io_wiktionary.py
   ```

2. **Re-generate dictionaries:**
   ```bash
   cd projects/data
   python3 scripts/regenerate_all.py --min-confidence 0.9
   ```

3. **Copy to apertium:**
   ```bash
   cp projects/data/generated/ido.ido.dix apertium/apertium-ido-epo/apertium-ido.ido.dix
   cp projects/data/generated/ido-epo.ido-epo.dix apertium/apertium-ido-epo/apertium-ido-epo.ido-epo.dix
   ```

4. **Recompile and test:**
   ```bash
   cd apertium/apertium-ido-epo
   make clean && make
   # Test again
   ```

---

## Conclusion

**Current Status:** ❌ No improvement in test results

**Reason:** Dictionaries not regenerated yet - fixes are in code but not applied to dictionaries

**Action Required:** Regenerate dictionaries to see improvements

**PR Status:** Should wait until dictionaries are regenerated and improvements are verified

