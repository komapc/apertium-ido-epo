# Apertium Ido–Esperanto Translation Pair

Bidirectional machine translation between **Ido** and **Esperanto** on the
[Apertium](https://www.apertium.org) platform.

Translation quality (curated gold sets, October 2026):

| Direction | Curated gold | Tatoeba sample (300) |
|-----------|--------------|----------------------|
| Ido → Esperanto | chrF 97.9, coverage 98.6% | chrF 81.1, coverage 93.5% |
| Esperanto → Ido | chrF 95.4, coverage 99.0% | chrF 73.6, coverage 92.1% |

The Tatoeba samples are random real sentences with a single free-translation reference, so
chrF there is much lower than on the curated sets; read the trend, not the level.

## How it works

A shallow-transfer pipeline: morphological analysis → bilingual lexicon lookup →
constraint-grammar disambiguation → structural transfer → generation.

- `apertium-ido-epo.ido-epo.dix` — bilingual dictionary (~92,000 entries)
- `apertium-ido-epo.ido-epo.t1x` / `apertium-ido-epo.epo-ido.t1x` — transfer rules
- `apertium-ido-epo.ido.ido.rlx` / `apertium-ido-epo.epo.epo.rlx` — constraint-grammar
  disambiguation, both generated from the pair (`make regen-disambig`,
  `make regen-disambig-epo`; rerun after a bidix, transfer or Ido monodix change)
- Ido monodix: provided by the separate [apertium-ido](https://github.com/komapc/apertium-ido) package

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

Work toward making this an official Apertium pair (started 2026-06-15; status as of 2026-10-06).

**Retired blockers:**
- Readable `.dix` files — `apertium-ido-epo.ido-epo.dix` is plain multi-line lttoolbox XML
  (not minified).
- Provenance documentation — see [`PROVENANCE.md`](PROVENANCE.md) for per-source licensing
  and attribution.

**Open blockers:**
- Repository ownership/hosting — still under a personal account, not the `apertium` org
  (neither `apertium-ido` nor `apertium-ido-epo` exists there yet).
- No page on wiki.apertium.org yet (a search for Ido pages returns nothing); `configure.ac`
  already points at `Apertium-ido-epo`.
- Language-specific `der_*` derivation sdefs (23 in the bidix: `der_act`, `der_aj`, `der_ala`,
  `der_aro`, `der_oz`, `der_ppra`, … ) drive Ido's productive derivational morphology
  (participles, `-ar-`/`-oz-`/`-al-` derivations, etc.). They are not a blocker as such: official
  `apertium` pairs (e.g. `apertium-myv-fin`, `apertium-kpv-koi`, `apertium-sme-nob`) also use
  `der_*` sdefs in bilingual dictionaries. Every sdef carries a `c="…"` description and is
  listed in the `.dix` header. Open question for Apertium maintainers: whether the participle
  tags should be aligned with standard `pp`/`pprs`/`ger` (which cover only 3 of the 12
  participle/gerund forms).
- One `sed` pre/post-processing pair remains in `modes.xml`: the epo→ido mode detaches a
  period from the preceding word and re-joins it afterwards, because apertium-epo keeps `.`
  in its alphabet (for decimals like `3.14`) so `domo.` is read as one token. Fixing it means
  changing apertium-epo's alphabet. The ido→epo `l'` sed is gone: the elided article is a
  clitic unit of the Ido analyser (`type="postblank"` section, as in apertium-fra/cat/ita).
- epo→ido has its own evaluation: a curated gold set and a Tatoeba-sampled benchmark in the
  extractor (`data/gold/epo_ido*.tsv`, trend reports in `reports/`), see #188 and the closing
  note on #189. Remaining epo→ido gaps are mostly apertium-epo lexical coverage (participle
  forms, `-en` adverbs, `kian`); a first apertium-epo PR for the `-anta` participle is open
  ([apertium-epo#5](https://github.com/apertium/apertium-epo/pull/5)).

## License

GNU General Public License v3.0 (see `COPYING`). Dictionary data derives from Wiktionary,
Wikipedia, and Wikidata; see [`PROVENANCE.md`](PROVENANCE.md) for the full per-source
breakdown, licensing (CC BY-SA / CC0 → GPL-3.0) and attribution.
