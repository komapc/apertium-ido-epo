# Error Analysis Report - December 9, 2025

## Overview
Analysis of translation output from `ido-epo-test-sentences.txt` after fixes.

## Fixes Implemented (Dec 9, 2025)

### 1. Tense Errors (FIXED)
Past tense verbs in Ido are now correctly translated to past tense in Esperanto.
- `partoprenis` (past) → `partoprenis` (past) ✅
- `diskutis` (past) → `diskutis` (past) ✅

**Cause:**
1. Garbage entries in dictionary (e.g., `partoprenis` defined as a lemma).
2. Mismatch between `pardefs.xml` tags (`past`, `pres`) and Apertium transfer rules (`pii`, `pri`).

**Fix:**
1. Filtered out conjugated verb forms from merging process.
2. Updated `pardefs.xml` to use standard Apertium tags (`pri`, `pii`, `fti`, `cni`).

### 2. Data Corruption (FIXED)
Metadata markers like arrows and parenthetical hints are gone.
- Old: `#de ↓ (indikante aganton)`
- New: `#de`

**Cause:**
`io_wiktionary` extraction included metadata in translation strings.

**Fix:**
Added cleaning logic to `merge_sources.py` to strip arrows and parenthetical hints.

## Remaining Issues

### 1. Unknown Words (`*`)
Significant number of unknown words remain:
- **Function Words:** `*maxim` (plej), `*quin` (kiujn), `*od` (aŭ)
- **Verbs:** `*remplacigar` (anstataŭigi), `*nomizas` (nomas), `*kreesis` (kreiĝis)
- **Adjectives/Adverbs:** `*saturdia` (sabata), `*facil` (facile)

### 2. Morphology & Derivation
- **Passive Voice:** `kreesis` is not handled.
- **Suffixes:** `-ebl` (`lernebla`, `uzebla`) is not recognized.
- **Compounds:** `video-konfero` → `Video-#keonfer`

### 3. Preposition/Particle Noise
- `da` → `#de` (Marked as #, likely because of case handling or missing definition in one direction)
- `di` → `@di`
- `kom` → `#keom`

## Next Steps
1. Add missing high-frequency words (`maxim`, `quin`, `od`).
2. Improve morphology handling for passives and suffixes.
3. Investigate preposition transfer rules.

