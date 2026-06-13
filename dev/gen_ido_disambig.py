#!/usr/bin/env python3
"""Generate the Ido disambiguation grammar (apertium-ido-epo.ido.ido.rlx).

The "der-shadow" problem: Ido noun paradigms auto-generate productive
derivational forms (-ajo/der_aj, -aro/der_aro, ...) for EVERY root, so a surface
like `vilajo` analyses BOTH as the phantom `vil`+der_aj AND as the real
lexicalized word `vilaj` (= village). With no disambiguation the phantom wins
and the real word is lost (-> @vil).

"Prefer the lexicalized reading" is correct ONLY when that reading is actually
translatable -- otherwise we would turn a usable approximation into a visible
@-gap (e.g. `muzikajo`: the lexical reading `muzikaj` has no bidix entry, so the
der reading's `muziko` is the better fallback). That decision depends on
BILINGUAL coverage, which a Constraint Grammar cannot see. So we resolve it here
at build time, against the compiled bidix, and emit a CG that fires only on the
verified-safe lexemes.

The emitted SAFE_LEX list is derived entirely from the dictionaries (monodix +
compiled bidix) -- it is regeneratable and auditable, not hand-curated.

Usage:
  python3 dev/gen_ido_disambig.py \
      --morf ido-epo.automorf.bin \
      --bidix ido-epo.autobil.bin \
      --monodix ../apertium-ido/apertium-ido.ido.dix \
      --out apertium-ido-epo.ido.ido.rlx
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

# Productive nominal derivation tags whose phantom forms shadow real lexemes.
# der_aj (-ajo) / der_aro (-aro): the LEXICAL reading is the real word and the
# derivation is the phantom -> always prefer lexical when it translates.
# Verbal derivations (der_esar passive, der_pres agents) are excluded: there the
# derived reading is frequently the correct one (prezidanto, uzesar).
DEFAULT_SCOPE_TAGS = ("der_aj", "der_aro")


def citation_forms(monodix: Path) -> list[str]:
    forms = {m for m in re.findall(r'lm="([^"]+)"', monodix.read_text())
             if m and " " not in m}
    return sorted(forms)


def analyse(forms: list[str], morf: Path) -> dict[str, list[str]]:
    """Return {surface: [reading, ...]} from the analyser, chunked (a single
    huge stream truncates lt-proc)."""
    out_parts = []
    CHUNK = 1000
    for i in range(0, len(forms), CHUNK):
        chunk = "\n".join(forms[i:i + CHUNK])
        p = subprocess.run(["lt-proc", str(morf)], input=chunk,
                           capture_output=True, text=True)
        out_parts.append(p.stdout)
    analysis = {}
    for tok in re.findall(r"\^([^$]*)\$", "".join(out_parts)):
        parts = tok.split("/")
        if len(parts) > 1:
            analysis[parts[0]] = parts[1:]
    return analysis


def baseform(reading: str) -> str:
    m = re.match(r"([^<]+)", reading)
    return m.group(1) if m else ""


def translatable_batch(readings: list[str], bidix: Path) -> dict[str, bool]:
    """Probe each full reading through the bidix; True if it yields a
    non-gap right side."""
    stream = "".join(f"^{r}$ " for r in readings)
    p = subprocess.run(["lt-proc", "-b", str(bidix)], input=stream,
                       capture_output=True, text=True)
    res = {}
    toks = re.findall(r"\^([^$]*)\$", p.stdout)
    for reading, tok in zip(readings, toks):
        parts = tok.split("/")
        # lt-proc -b marks an untranslatable lemma with a leading '@'
        right = parts[1] if len(parts) > 1 else "@"
        res[reading] = not right.startswith("@")
    return res


def collisions(analysis: dict[str, list[str]], scope_tags):
    """Yield (surface, der_reading, lexical_reading) where the first reading is
    an in-scope derivation and a later reading is a plain lexicalized one."""
    want = tuple(f"<{x}>" for x in scope_tags)
    for surf, readings in analysis.items():
        if len(readings) < 2:
            continue
        first = readings[0]
        if not any(t in first for t in want):
            continue
        for r in readings[1:]:
            if "<der_" not in r:
                yield surf, first, r
                break


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--morf", type=Path, default=here.parent / "ido-epo.automorf.bin")
    ap.add_argument("--bidix", type=Path, default=here.parent / "ido-epo.autobil.bin")
    ap.add_argument("--monodix", type=Path,
                    default=here.parent.parent / "apertium-ido" / "apertium-ido.ido.dix")
    ap.add_argument("--out", type=Path,
                    default=here.parent / "apertium-ido-epo.ido.ido.rlx")
    # Two policy groups (per measured behaviour):
    #  full-tags: the LEXICAL reading is the real word, the derivation is the
    #    phantom -> prefer lexical whenever it translates (der_aj/der_aro).
    #  gap-tags:  the DERIVATION is usually the real word -> prefer lexical ONLY
    #    when the derivation reading is itself an @-gap (pure upside). Preferring
    #    lexical unconditionally here regresses (saneso: saneco->sano), so it is
    #    restricted to the @-gap cases (der_qual/der_act).
    ap.add_argument("--full-tags", default="der_aj,der_aro,der_izar",
                    help="prefer lexical whenever it translates "
                         "(tags where the lexical reading is the real word)")
    ap.add_argument("--gap-tags", default="der_qual,der_act,der_pres",
                    help="prefer lexical only when the derivation is an @-gap "
                         "(tags where the derivation reading is usually correct)")
    args = ap.parse_args()
    full_tags = tuple(t.strip() for t in args.full_tags.split(",") if t.strip())
    gap_tags = tuple(t.strip() for t in args.gap_tags.split(",") if t.strip())

    for f in (args.morf, args.bidix, args.monodix):
        if not f.exists():
            print(f"ERROR: missing input {f}", file=sys.stderr)
            return 1

    forms = citation_forms(args.monodix)
    print(f"[gen-disambig] {len(forms)} citation forms", file=sys.stderr)
    analysis = analyse(forms, args.morf)

    def safe_lexemes(tags, gap_only):
        if not tags:
            return set()
        cols = list(collisions(analysis, tags))
        trans = translatable_batch(sorted({lex for _, _, lex in cols}), args.bidix)
        der_trans = (translatable_batch(sorted({der for _, der, _ in cols}),
                                        args.bidix) if gap_only else {})
        sset = {baseform(lex) for _, der, lex in cols
                if trans.get(lex) and (not gap_only or not der_trans.get(der))}
        print(f"[gen-disambig] {'/'.join(tags)}"
              f"{' (gap-only)' if gap_only else ''}: {len(cols)} collisions -> "
              f"{len(sset)} safe lexemes", file=sys.stderr)
        return sset

    safe = safe_lexemes(full_tags, False) | safe_lexemes(gap_tags, True)
    # keep only baseforms that are CG-literal-safe (plain word chars / hyphen)
    safe = sorted(s for s in safe if re.fullmatch(r"[\w’'-]+", s))
    scope_tags = full_tags + gap_tags
    print(f"[gen-disambig] {len(safe)} total safe lexemes -> {args.out.name}",
          file=sys.stderr)

    listing = "\n".join(f'\t"{s}"' for s in safe)
    rlx = f'''# Constraint Grammar for Ido (ido)  --  GENERATED FILE, DO NOT EDIT.
# Regenerate with: python3 dev/gen_ido_disambig.py
# (built by the Makefile from the monodix + compiled bidix).
#
# Resolves the "der-shadow" ambiguity: Ido paradigms auto-generate productive
# derivations ({", ".join(scope_tags)}) for every root, so a surface like vilajo
# analyses both as the phantom root+suffix AND as the real lexicalized word.
# With no disambiguation in ido->epo the phantom wins (-> @vil). A baseform is
# listed in SAFELEX (and its derivation reading dropped) only when verified at
# build time against the bidix, so we never turn a usable fallback into a visible
# @-gap. Two policies: for {", ".join(full_tags)} the lexical reading is the real
# word, so prefer it whenever it translates; for {", ".join(gap_tags)} the
# derivation is usually correct, so prefer lexical ONLY when the derivation
# reading is itself an @-gap. Mirrors the cg-proc stage epo-ido already uses.

DELIMITERS = "<.>" "<!>" "<?>" "<...>" ;

# In-scope productive derivation tags.
LIST DER = {" ".join(scope_tags)} ;

# Lexicalized baseforms whose lexical reading is bidix-translatable, i.e. safe
# to prefer over the phantom derivation. Generated from bidix coverage.
LIST SAFELEX =
{listing} ;

# SAFELEX restricted to NON-derivation readings: a derivation whose own lemma
# happens to be in SAFELEX (e.g. popular<der_qual>, lemma "popular") must not
# satisfy the condition and remove itself.
SET SAFELEXLEX = SAFELEX - DER ;

SECTION

# Drop the phantom derivation when a verified-translatable lexicalized reading
# for the same surface exists in the cohort.
REMOVE DER IF (0 SAFELEXLEX) ;
'''
    args.out.write_text(rlx)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
