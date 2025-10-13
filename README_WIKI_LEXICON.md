## Ido Wikipedia Lexicon Builder

This pipeline downloads the Ido Wikipedia dump, extracts main-namespace article text (templates, tables, and blockquotes removed), removes quoted spans, tokenizes per agreed rules, and produces a word-frequency TSV.

### Install

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-wiki.txt
```

### Run

```bash
python scripts/build_ido_wiki_lexicon.py --min-count 1
```

Outputs:
- `outputs/iowiki_word_frequency.tsv` — `token<TAB>count` sorted by count desc

Optional flags:
- `--dump-url` override dump (default latest iowiki pages-articles)
- `--processes` parallel extraction processes (default 4)
- `--base-dir` working root (default: repo root)

Tokenization rules:
- Unicode NFC, lowercase
- Keep letters and internal apostrophes/hyphens
- Exclude tokens containing digits or URL-like patterns

Ignored content:
- Templates (via WikiExtractor `--no_templates`)
- Tables and blockquotes (via `--discardElements`)
- Quoted spans (", ', “”, ‘’, «»)



