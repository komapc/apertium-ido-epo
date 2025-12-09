# Test Corpus for Ido-Esperanto Translation

This directory contains test sentences for evaluating translation quality and improvements.

## File Structure

- `ido-epo-test-sentences.txt` - Test sentences in Ido for translation to Esperanto
  - **Full Path:** `/home/mark/apertium-dev/apertium/apertium-ido-epo/corpus/ido-epo-test-sentences.txt`
  - **Purpose:** Contains test sentences for evaluating translation quality and improvements
  - **Format:** Plain text with comments (lines starting with `#`)
  - **Current Content:** 2 test sentences (as of December 8, 2025)
- `README.md` - This file
- `TEST_RESULTS_2025-12-08.md` - Latest detailed test results and error analysis

## Usage

### Test a single sentence:
```bash
cat corpus/ido-epo-test-sentences.txt | grep -v "^#" | apertium ido-epo
```

### Test all sentences:
```bash
# Extract sentences (skip comments and empty lines)
grep -v "^#" corpus/ido-epo-test-sentences.txt | grep -v "^$" | apertium ido-epo
```

### Test with verbose output:
```bash
echo "Ido sentence here" | apertium -d . ido-epo
```

## Adding Test Sentences

When adding new test sentences:
1. Add them to `ido-epo-test-sentences.txt`
2. Include a comment describing what the sentence tests
3. Test both directions (Ido→Esperanto and Esperanto→Ido) when relevant
4. Document any known issues or expected behaviors

## Test Categories

- **Historical/Linguistic**: Complex sentences about Ido's history and characteristics
- **Community**: Sentences about Ido community activities
- **Grammar**: Test specific grammatical constructions
- **Vocabulary**: Test specific word translations
- **Edge Cases**: Unusual or challenging translations

## Bidirectional Testing

Remember to test both directions:
- Ido → Esperanto: `echo "text" | apertium ido-epo`
- Esperanto → Ido: `echo "text" | apertium epo-ido`

