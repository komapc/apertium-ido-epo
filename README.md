# Apertium Ido–Esperanto Translation Pair

Bidirectional machine translation between **Ido** and **Esperanto** on the
[Apertium](https://www.apertium.org) platform.

Translation quality (130-sentence gold set, `ido-epo`): **chrF 93.2, coverage 99.4%**.

## How it works

A shallow-transfer pipeline: morphological analysis → bilingual lexicon lookup →
constraint-grammar disambiguation → structural transfer → generation.

- `apertium-ido-epo.ido-epo.dix` — bilingual dictionary (~103,600 entries)
- `apertium-ido-epo.ido-epo.t1x` / `apertium-ido-epo.epo-ido.t1x` — transfer rules
- `epo-ido.rlx` / `apertium-ido-epo.epo.epo.rlx` — constraint-grammar disambiguation
- `apertium-ido.ido.dix` — Ido monodix (from [apertium-ido](https://github.com/komapc/apertium-ido))

The dictionaries are **auto-generated** by the
[ido-esperanto-extractor](https://github.com/komapc/ido-esperanto-extractor) pipeline
(`bidix_big.json` → `export_apertium.py`) — edit the extractor, not the `.dix` files here.
The Esperanto morphology comes from [apertium-epo](https://github.com/komapc/apertium-epo).

## Requirements

- `apertium` (>= 3.6), `lttoolbox` (>= 3.5)
- `apertium-ido` and `apertium-epo` (monolingual packages)

## Build & use

```bash
./autogen.sh
./configure
make

echo "Il amas mea hundo." | apertium -d . ido-epo
# → Li amas mian hundon.

echo "Li amas mian hundon." | apertium -d . epo-ido
```

Modes: `ido-epo` (Ido → Esperanto) and `epo-ido` (Esperanto → Ido).

## Quality

Regressions are caught by the extractor's evaluation harness
(`scripts/eval_translation.py` → chrF + coverage on `data/gold/ido_epo.tsv`) and the
`conflict_winner_diff` / `dict_diff` gates, run before each regen is deployed here.

## License

GNU General Public License v3.0 (see `COPYING`). Dictionary data derives from Wiktionary,
Wikipedia, and Wikidata (CC BY-SA); see the extractor for full attribution.
