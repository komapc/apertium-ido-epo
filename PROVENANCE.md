# Data provenance & licensing

The dictionaries in this pair are **auto-generated** and fully regeneratable —
they are never edited by hand. This document records where the lexical data
comes from and under what terms it is redistributed, so the pair can be audited
for inclusion in official Apertium.

## What is generated, and from what

| File | Repo | Built by |
|------|------|----------|
| `apertium-ido-epo.ido-epo.dix` (bilingual) | this repo | `build_one_big_bidix_json.py` → `export_apertium.py` |
| `apertium-ido.ido.dix` (Ido morphology) | [apertium-ido](https://github.com/komapc/apertium-ido) | `export_apertium.py` |
| Esperanto morphology | [apertium-epo](https://github.com/apertium/apertium-epo) | upstream (official) |

The generator is the [ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor)
pipeline. Every entry carries per-entry `provenance` in the intermediate
`bidix_big.json`, so any translation pair can be traced back to its source.
**To change the dictionaries, edit the extractor and regenerate — do not edit
the `.dix` files here.**

## Sources

Entry counts below are translation-source tallies over the ~93k bilingual
entries (an entry may draw on more than one source).

| Source | Entries | What it is | License of source |
|--------|--------:|------------|-------------------|
| `io_wiktionary` | 44,343 | Ido Wiktionary translation tables and headwords | CC BY-SA 4.0 / GFDL |
| `eowiki_langlinks` | 16,519 | Esperanto Wikipedia interlanguage links (eo→io) | CC BY-SA 4.0 |
| `wikipedia_langlinks` | 16,300 | Ido Wikipedia interlanguage links (io→eo) | CC BY-SA 4.0 |
| `io_wikipedia` | 12,058 | Ido Wikipedia article titles / redirects | CC BY-SA 4.0 |
| `wikidata_labels` | 11,268 | Wikidata entity labels (io/eo) | CC0 1.0 (public domain) |
| `morphological_expansion` | 10,121 | Derived forms generated **by rule** from known io/eo roots via the shared Ido/Esperanto suffix system | rule-generated (no external source) |
| `en_wiktionary_via` | 4,508 | Pairs pivoted through English Wiktionary translation tables | CC BY-SA 4.0 / GFDL |
| `bert_embeddings` | 4,328 | Cognate pairs from a fine-tuned XLM-RoBERTa aligner (similarity ≥ 0.99 + a 4-character cognate guard) | model: MIT; pairs are factual correspondences |
| `fr_wiktionary_via` | 462 | Pairs pivoted through French Wiktionary | CC BY-SA 4.0 / GFDL |
| `eo_wiktionary` | 200 | Esperanto Wiktionary | CC BY-SA 4.0 / GFDL |
| `closed_class_tables` | 87 | Pronoun / correlative correspondences parsed from the io.wikipedia pages *"Komparo inter Ido ed Esperanto"* and *"Gramatiko di Ido"* (Esperanto side partly derived by rule from the correlative grid) | CC BY-SA 4.0 |
| `function_word_override` / `function_words_seed` | 17 | A deliberately minimal hand-curated list of closed-class function words that Wiktionary either omits or mis-parses | this project (GPL-3.0) |

## Licensing

- **Source data** is Wikimedia content under **CC BY-SA** (Wiktionary text is
  additionally GFDL) except **Wikidata, which is CC0** (public domain). The
  rule-generated and aligner-derived rows above are factual word
  correspondences rather than copied text.
- **This dictionary** and the rest of the pair are distributed under the
  **GNU General Public License v3.0** (see `COPYING`).
- Attribution to the Wikimedia projects is preserved through the per-entry
  provenance retained by the extractor; this file provides the project-level
  attribution required by CC BY-SA.

## Derivation symbols

The dictionaries use a small set of language-specific `der_*` symbols for Ido's
productive derivational morphology (e.g. `der_aro` = the Ido `-ar-` collective
suffix). Each symbol is documented, with its Ido → Esperanto mapping, in the
header comment of every generated `.dix` file.

## Regenerating

```bash
# in the extractor checkout, with work/ and dist/ already populated:
python3 scripts/export_apertium.py
bash core/deploy.sh        # copies dist/*.dix into this repo and apertium-ido
```

See the extractor's pipeline documentation for a full rebuild from the
Wiktionary/Wikipedia/Wikidata dumps.
