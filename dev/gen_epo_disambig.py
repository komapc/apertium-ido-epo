#!/usr/bin/env python3
"""Generate the Esperanto disambiguation grammar (apertium-ido-epo.epo.epo.rlx).

epo->ido has no tagger, so after cg-proc the transfer takes the FIRST reading
the analyser lists. apertium-epo lists them in dictionary order, not by
likelihood: `ke` comes out as <adv> before <cnjsub>, `por` as <cnjadv> before
<pr>, `Li` as a surname <np> before the pronoun, `venonta` as <vbser><pp2>
before <vblex><pp2>. Those first readings have no bidix entry (or no Ido
generation), so the most frequent function words surfaced as @ke, @por, @Li...

This script resolves that against the pair itself, at build time: every
surface of the Esperanto dictionary with more than one reading has each reading
pushed through the rest of the epo->ido pipeline (bidix, transfer, generator).
A reading that comes out as an @/# gap is REMOVEd, but only in cohorts that
also hold a reading of the same surface that translates cleanly -- so the rule
can never turn a translation into a gap, and never touches a word whose
readings all fail (those stay visible as gaps to fix in the dictionaries).

Everything is derived from the dictionaries and the compiled pair, so the
grammar is regeneratable and auditable, not hand-curated. Rerun it (make
regen-disambig-epo) after any bidix, epo-ido.t1x or Ido monodix change.

Usage:
  python3 dev/gen_epo_disambig.py \\
      --monodix ../apertium-epo/apertium-epo.epo.dix \\
      --bidix epo-ido.autobil.bin --t1x apertium-ido-epo.epo-ido.t1x \\
      --t1x-bin epo-ido.t1x.bin --gen epo-ido.autogen.bin \\
      --out apertium-ido-epo.epo.epo.rlx
"""
import argparse
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def expand(monodix: Path) -> dict[str, list[str]]:
    """{surface: [reading, ...]} in analyser order, from lt-expand.

    Lines are `surface:reading` (both ways), `surface:>:reading` (analysis
    only) or `surface:<:reading` (generation only, skipped)."""
    p = subprocess.run(["lt-expand", str(monodix)], capture_output=True,
                       text=True, check=True)
    readings = defaultdict(list)
    for line in p.stdout.splitlines():
        if ":<:" in line:
            continue
        surf, _, reading = line.replace(":>:", ":", 1).partition(":")
        if reading and reading not in readings[surf]:
            readings[surf].append(reading)
    return readings


def probe(readings: list[str], args) -> dict[str, bool]:
    """True when a reading, alone, comes out of bidix+transfer+generation with
    no @ (no bidix entry), # (not generatable) or * (unknown) mark.

    (No -n on apertium-pretransfer: it hangs on a stream of bare lexical units.)

    Readings are separated by a sentence token so no multi-word transfer rule
    (plej+adj, nom+da+nom) can join two neighbours."""
    ok = {}
    CHUNK = 20000
    for i in range(0, len(readings), CHUNK):
        chunk = readings[i:i + CHUNK]
        stream = "".join(f"^{r}$^.<sent>$\n" for r in chunk)
        p = subprocess.run(
            f"apertium-pretransfer | lt-proc -b {args.bidix} | "
            f"apertium-transfer -b {args.t1x} {args.t1x_bin} | "
            f"lt-proc -g {args.gen}",
            shell=True, input=stream, capture_output=True, text=True, check=True)
        lines = p.stdout.split("\n")
        if len(lines) < len(chunk):
            raise SystemExit(f"probe: {len(lines)} output lines for {len(chunk)} readings")
        for r, out in zip(chunk, lines):
            out = out.strip()
            if out.endswith("."):
                out = out[:-1].strip()
            ok[r] = bool(out) and not re.search(r"(^|\s)[@#*]", out)
    return ok


def tags(reading: str) -> tuple[str, ...]:
    return tuple(re.findall(r"<([^>]+)>", reading))


def lemma(reading: str) -> str:
    return reading.split("<", 1)[0]


def cg_lemmas(lemmas) -> str:
    """CG base-form tags for these lemmas, lowercase and capitalised: the
    analyser capitalises the lemma of a capitalised surface (Li -> Prpers).
    Plain tags, not "x"i -- vislcg3 cannot index case-insensitive tags."""
    out = []
    for lm in sorted(lemmas):
        for v in dict.fromkeys([lm, lm[:1].upper() + lm[1:]]):
            out.append('"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"')
    return " ".join(out)


def group(ambiguous: dict[str, list[str]], ok: dict[str, bool]):
    """One rule per (failing tags A, translating tags B) pair, with the lemma
    lists it applies to: REMOVE Lbad + (A) IF (0 Lgood + (B)).

    vislcg3 tries every rule on every window, so 18k per-reading rules made
    cg-proc ~100x slower; grouped there are a few hundred. A list can match a
    lemma/tag combination that never co-occurred in the dictionary, so each
    group is checked against every ambiguous surface: a lemma whose reading
    would be removed while it translates is taken out of the group, and its
    failing readings get exact rules of their own. Returns
    ({(A, B): (bad lemmas, good lemmas)}, [(bad reading, good readings)])."""
    groups = defaultdict(lambda: (set(), set()))
    for rs in ambiguous.values():
        good = [r for r in rs if ok[r]]
        if not good:
            continue
        for r in rs:
            if ok[r]:
                continue
            g = good[0]
            key = (tags(r), tags(g))
            groups[key][0].add(lemma(r))
            groups[key][1].add(lemma(g))

    def fl(x):
        return x[:1].lower() + x[1:]

    by_lemma = defaultdict(list)          # lowercased lemma -> surfaces
    for surf, rs in ambiguous.items():
        for r in rs:
            by_lemma[fl(lemma(r))].append(surf)

    ejected = defaultdict(set)            # key -> bad lemmas taken out
    for key, (lb, lg) in groups.items():
        a, b = set(key[0]), set(key[1])
        extra = b - a    # subtracted from the target, see rule_sets()
        lbl = {fl(x) for x in lb}
        lgl = {fl(x) for x in lg}
        while True:
            bad = set()
            for surf in {s for x in lgl for s in by_lemma[x]}:
                rs = ambiguous[surf]
                if not any(fl(lemma(r)) in lgl and b <= set(tags(r)) for r in rs):
                    continue
                for r in rs:
                    if ok[r] and fl(lemma(r)) in lbl and a <= set(tags(r)) \
                            and not extra & set(tags(r)):
                        bad.add(fl(lemma(r)))
            if not bad:
                break
            lbl -= bad
            ejected[key] |= bad
        groups[key] = ({x for x in lb if fl(x) in lbl}, lg)

    residue = []
    if any(ejected.values()):
        for rs in ambiguous.values():
            good = [r for r in rs if ok[r]]
            for r in rs:
                if not ok[r] and good and \
                   fl(lemma(r)) in ejected.get((tags(r), tags(good[0])), ()):
                    residue.append((r, tuple(good)))
    return {k: v for k, v in groups.items() if v[0]}, sorted(set(residue))


def exact(reading: str, minus=()) -> str:
    """A CG set matching this reading: lemma (both cases) + its tags, minus
    readings carrying any tag in `minus`."""
    t = " ".join(tags(reading))
    core = " OR ".join(f"({v} {t})" for v in cg_lemmas([lemma(reading)]).split(" "))
    if not minus:
        return core
    return f"({core})" + "".join(f" - ({m})" for m in sorted(minus))


def main() -> int:
    here = Path(__file__).resolve().parent
    root = here.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--monodix", type=Path,
                    default=root.parent / "apertium-epo" / "apertium-epo.epo.dix")
    ap.add_argument("--bidix", type=Path, default=root / "epo-ido.autobil.bin")
    ap.add_argument("--t1x", type=Path, default=root / "apertium-ido-epo.epo-ido.t1x")
    ap.add_argument("--t1x-bin", type=Path, default=root / "epo-ido.t1x.bin")
    ap.add_argument("--gen", type=Path, default=root / "epo-ido.autogen.bin")
    ap.add_argument("--out", type=Path, default=root / "apertium-ido-epo.epo.epo.rlx")
    args = ap.parse_args()

    for f in (args.monodix, args.bidix, args.t1x, args.t1x_bin, args.gen):
        if not f.exists():
            print(f"ERROR: missing input {f}", file=sys.stderr)
            return 1

    analyses = expand(args.monodix)
    # A capitalised token (sentence start) gets the readings of its own entry
    # AND those of the lowercase word: `Li` is the surname Li<np> plus the
    # pronoun li. Merge them so those cohorts are seen as the analyser builds
    # them. (Lemmas stay as in the dictionary; rules list both cases.)
    for surf in list(analyses):
        cap = surf[:1].upper() + surf[1:]
        if cap != surf:
            merged = analyses.get(cap, []) + analyses[surf]
            analyses[cap] = list(dict.fromkeys(merged))
    ambiguous = {s: rs for s, rs in analyses.items() if len(rs) > 1}
    todo = sorted({r for rs in ambiguous.values() for r in rs})
    print(f"[gen-epo-disambig] {len(analyses)} surfaces, {len(ambiguous)} ambiguous, "
          f"{len(todo)} readings to probe", file=sys.stderr)
    ok = probe(todo, args)

    groups, residue = group(ambiguous, ok)
    lists, rules = [], []
    for n, ((a, b), (lb, lg)) in enumerate(sorted(groups.items())):
        lists.append(f"LIST BAD{n} = {cg_lemmas(lb)} ;")
        lists.append(f"LIST GOOD{n} = {cg_lemmas(lg)} ;")
        # vislcg3 matches a set by tag inclusion, so (vblex pp3) would also
        # hit the translating (vblex pp3 sg): subtract the condition's extra tags.
        minus = "".join(f" - ({m})" for m in sorted(set(b) - set(a)))
        tgt = f"BAD{n} + ({' '.join(a)})" if a else f"BAD{n}"
        cnd = f"GOOD{n} + ({' '.join(b)})" if b else f"GOOD{n}"
        lists.append(f"SET BADT{n} = {tgt}{minus} ;")
        rules.append(f"REMOVE BADT{n} IF (0 {cnd}) ;")
    for bad, goods in residue:
        cond = " OR ".join(exact(g) for g in goods)
        minus = {t for g in goods for t in tags(g)} - set(tags(bad))
        rules.append(f"REMOVE {exact(bad, minus)} IF (0 {cond}) ;")
    nrules = len(groups) + len(residue)
    print(f"[gen-epo-disambig] {len(groups)} grouped + {len(residue)} exact "
          f"REMOVE rules -> {args.out.name}", file=sys.stderr)

    args.out.write_text(f'''# Constraint Grammar for Esperanto (epo)  --  GENERATED FILE, DO NOT EDIT.
# Regenerate with: make regen-disambig-epo  (dev/gen_epo_disambig.py)
#
# epo->ido has no tagger, so transfer takes the first reading the analyser
# lists, and apertium-epo's order often puts an untranslatable reading first
# (ke<adv> before ke<cnjsub>, Li<np> before the pronoun). Each rule below drops
# readings that come out of bidix+transfer+generation as an @/# gap, and fires
# only when the cohort also holds a reading verified at build time to
# translate. Rules are grouped by tag pattern with lemma lists (vislcg3 tries
# every rule on every window, so one rule per word was ~100x slower); each
# group was checked against the whole dictionary never to remove a reading
# that translates.

DELIMITERS = "<.>" "<!>" "<?>" "<...>" "<¶>" ;

LIST nom = (n) ;
LIST det = (det) ;
LIST prntn = (prn tn) ;
SET nominal = (n) OR (adj) OR (np) ;

# Lemma lists of the generated rules (BADn: lemmas whose reading is dropped,
# GOODn: lemmas whose translating reading must be present).
''' + "\n".join(lists) + f'''

SECTION

# Hand rule kept from the original grammar: a noun reading loses to any other
# reading of the same cohort (La, Mi analyse as nouns first).
REMOVE nom IF (0 nom) ;

# Generated: {nrules} rules.
''' + "\n".join(rules) + '''

SECTION

# Hand rules, after the generated ones (which condition on the first
# translating reading, often the pronoun): a correlative that is both
# determiner and pronoun (neniu, tiu, ĉiu) is the determiner before a noun or
# adjective and the pronoun elsewhere -- Ido tells them apart (nula homo /
# nulu venis).
REMOVE prntn IF (0 det) (1 nominal) ;
REMOVE det IF (0 prntn) (NOT 1 nominal) ;
''')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
