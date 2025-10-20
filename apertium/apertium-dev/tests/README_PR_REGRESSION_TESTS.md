# PR Regression Tests

**Created:** October 15, 2025  
**Purpose:** Prevent regression on fixes from the 20 most recent PRs

## Test File

- **Input:** `ido-epo-pr-regression-input.txt`
- **Expected output:** `ido-epo-pr-regression-postgen-expected.txt`

## What These Tests Cover

### 1. Critical Bug Fixes (PR #24)
- Line 1: Ido language name (was translating to "tradukar")
- Lines 2-3: Possessive pronouns lua/sua → ĝia
- Line 4: himno (anthem) vocabulary

### 2. Suffix Transformations (PR #22)
- Lines 5-8: -ala → -a transformation (parlamentala, mondala, kulturala, demografiala)
- Note: -eso → -eco is handled by post-generator

### 3. Historical/Geographic Vocabulary (PR #22, #17)
- Line 9: Mezepoko (Middle Ages)
- Line 10: chefurbo (capital city)
- Line 11: cent, kilometri (numbers, distance units)

### 4. Function Words (PR #5, #6)
- Line 12: ed → kaj (conjunction)
- Lines 13-14: forte, itere (core adverbs)
- Lines 15-19: dil→de, til→ĝis, kom→kiel, ye→je, su→sub (prepositions)
- Line 20: anke → ankaŭ (adverb)

### 5. Directional Adverbs (PR #5)
- Lines 21-24: este, weste, norde, sude → oriente, okcidente, norde, sude

### 6. Elided Article (PR #19)
- Line 25: l'urbo recognition

### 7. High-Confidence Mappings (PR #17)
- Lines 26-30: granda, nova, alta, centro, vilajo, urbo (common words)

## Key Transformations Being Tested

✅ **Working:**
- lua/sua → ĝia (possessive pronouns)
- -ala → -a suffix (parlamentala → parlamenta, kulturala → kultura)
- ed → kaj (conjunction)
- kom → kiel (comparison)
- til → ĝis (preposition)
- anke → ankaŭ (adverb)

⚠️ **Partial/Unknown words marked with * or #:**
- Some words show markers because they're not in monolingual dictionaries yet
- Markers don't mean the TRANSFORMATION failed - just that the base word is unknown
- This is expected and documents current system state

## Markers in Output

- `*` = unknown word (not in monolingual dictionary)
- `#` = ambiguous reading (multiple possible analyses)
- `@` = generation error

## Usage

Run with `make test` or manually:

```bash
cat test/ido-epo-pr-regression-input.txt | apertium -d . ido-epo > output.txt
diff test/ido-epo-pr-regression-postgen-expected.txt output.txt
```

## Purpose

These tests serve as a regression safety net. If any of these translations change unexpectedly, it indicates a potential bug or regression in one of the 20 recent PR fixes.

## Related Documentation

- `/home/mark/apertium-dev/PR_REVIEW_AND_TESTS_SUMMARY.md` - Full PR review
- `/home/mark/apertium-dev/PROPOSED_TEST_SENTENCES.md` - Detailed test explanations

## Note

This test suite captures the CURRENT state after 20 PRs. Future improvements should:
1. Keep these tests passing (no regression)
2. Add additional tests for new fixes
3. Update expectations when intentionally improving translations

