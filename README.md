# Apertium Ido–Esperanto Translation Pair

Bidirectional machine translation between **Ido** and **Esperanto** on the
[Apertium](https://www.apertium.org) platform.

Translation quality (163-sentence gold set, `ido-epo`): **chrF 96.5, coverage 98.4%**.

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

## Officialization status

Work toward making this an official Apertium pair (tracked informally; target 2026-06-15).

**Retired blockers:**
- Readable `.dix` files — `apertium-ido-epo.ido-epo.dix` is plain multi-line lttoolbox XML
  (not minified).
- Provenance documentation — see [`PROVENANCE.md`](PROVENANCE.md) for per-source licensing
  and attribution.

**Open blockers:**
- Repository ownership/hosting — still under a personal account, not the `apertium` org.
- 15 non-standard `der_*` sdefs in the bidix (`der_act`, `der_aj`, `der_ala`, `der_aro`,
  `der_esar`, `der_izar`, `der_oz`, `der_past`, `der_pfut`, `der_ppa`, `der_ppas`,
  `der_ppra`, `der_pprs`, `der_pres`, `der_qual`) drive derivational morphology
  (participles, `-igi`/`-iĝi` derivations, etc.) — upstream review would likely ask for
  these to follow more conventional Apertium symbol naming or be folded into standard tags.
- `sed`-based pre/post-processing hacks in `modes.xml` (apostrophe contraction spacing,
  period spacing) — functional but non-standard; an upstream-quality pair would handle
  these in the FST rather than shell pipeline hacks.
- epo→ido transfer-rule coverage lags ido→epo (`epo-ido.t1x` has 14 rules vs.
  `ido-epo.t1x`'s 70) and has no dedicated evaluation corpus — see #188, #189.

## License

GNU General Public License v3.0 (see `COPYING`). Dictionary data derives from Wiktionary,
Wikipedia, and Wikidata; see [`PROVENANCE.md`](PROVENANCE.md) for the full per-source
breakdown, licensing (CC BY-SA / CC0 → GPL-3.0) and attribution.
