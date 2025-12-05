# Dictionary Generation Scripts

This directory contains scripts for regenerating the Ido and Ido-Esperanto dictionaries from source data.

## Scripts

### `generate_monodix.py`
Generates the Ido monolingual dictionary (`apertium-ido.ido.dix`) from merged JSON data and paradigm definitions.

**Critical fixes:**
- XML indentation does NOT add whitespace inside `<r>` tags
- Paradigm tags must remain on single line to prevent morphological analyzer from outputting tags with newlines

### `generate_bidix.py`
Generates the Ido-Esperanto bilingual dictionary (`apertium-ido-epo.ido-epo.dix`) from merged JSON data.

**Critical fixes:**
- Keeps Esperanto lemmas as full forms (e.g., "homo") instead of extracting stems (e.g., "hom")
- Extracts Ido stems for proper morphological analysis
- XML indentation does NOT add whitespace inside `<r>` or `<l>` tags

### `filter_inflected_forms.py`
Filters out inflected forms that were mistakenly included as lemmas in the source data.

**Example:** Filters "homi" (plural of "homo") which should not be a separate lemma.

## Regeneration Process

To regenerate the dictionaries:

```bash
# 1. Filter inflected forms from source data
python3 scripts/filter_inflected_forms.py \
    --input /path/to/merged_bidix.json \
    --output /path/to/merged_bidix_filtered.json

# 2. Generate monodix
python3 scripts/generate_monodix.py \
    --input /path/to/merged_monodix.json \
    --output apertium-ido.ido.dix

# 3. Generate bidix
python3 scripts/generate_bidix.py \
    --input /path/to/merged_bidix_filtered.json \
    --output apertium-ido-epo.ido-epo.dix \
    --no-pos \
    --min-confidence 1.0

# 4. Rebuild
make clean && make
```

## Important Notes

- **DO NOT** manually edit generated `.dix` files
- All changes should be made in source data or generation scripts
- Paradigm definitions in `../data/pardefs.xml` must have tags on single lines
- The `--no-pos` flag is used because morphological analysis handles POS tags
- Confidence threshold of 1.0 ensures only highest quality translations

