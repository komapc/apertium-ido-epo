#!/usr/bin/env python3
"""Tatoeba held-out quality gate for both directions of the pair.

Translates test/tatoeba/{ido_epo,epo_ido}_tatoeba.tsv with the built pair and
computes two chrF scores per direction:

  steering  -- the metric of extractor's scripts/eval_translation.py (the
               numbers in its reports/quality_trend*_tatoeba.md): lowercased,
               Apertium markers * @ # stripped, whitespace kept, chrF per
               sentence against the best ' | ' reference, mean over sentences.
  sacrebleu -- sacrebleu's standard corpus chrF (default settings, markers
               stripped, first reference), for comparison with other systems.

The run fails when either score of either direction drops more than
--tolerance below test/tatoeba/baseline.json, or when the gold sets do not
have the sentence counts the baseline was measured on. A PR that improves
quality updates baseline.json on purpose (--write-baseline prints the new one).

Usage, from the repo root after `make`:
  python3 dev/eval_tatoeba.py
  python3 dev/eval_tatoeba.py --write-baseline   # rewrite baseline.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from sacrebleu.metrics import CHRF

ROOT = Path(__file__).resolve().parent.parent
GOLD_DIR = ROOT / "test" / "tatoeba"
DIRECTIONS = ("ido-epo", "epo-ido")
MARKERS = {0x2A: None, 0x40: None, 0x23: None}  # * @ #


def load_gold(path: Path) -> list[tuple[str, list[str]]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            rows.append((parts[0].strip(), [r.strip() for r in parts[1].split(" | ")]))
    return rows


def translate(text: str, mode: str, pair_dir: Path) -> str:
    # Same call as extractor's eval_translation.py: one sentence per process.
    proc = subprocess.run(["apertium", "-d", str(pair_dir), mode], input=text,
                          capture_output=True, text=True, check=True)
    return proc.stdout.strip()


def _ngrams(text: str, n: int) -> list[str]:
    s = re.sub(r"\s+", " ", text.translate(MARKERS).strip().lower())
    return [s[i:i + n] for i in range(len(s) - n + 1)]


def steering_chrf(hyp: str, ref: str, max_n: int = 6, beta: float = 2.0) -> float:
    """Byte-for-byte the chrF of extractor/scripts/eval_translation.py."""
    if not hyp.strip() or not ref.strip():
        return 0.0
    scores = []
    for n in range(1, max_n + 1):
        h, r = _ngrams(hyp, n), _ngrams(ref, n)
        if not h or not r:
            continue
        hc, rc = Counter(h), Counter(r)
        overlap = sum(min(c, rc[g]) for g, c in hc.items())
        prec, rec = overlap / len(h), overlap / len(r)
        b2 = beta * beta
        scores.append(0.0 if prec + rec == 0 else (1 + b2) * prec * rec / (b2 * prec + rec))
    return 100.0 * sum(scores) / len(scores) if scores else 0.0


def evaluate(mode: str, jobs: int, pair_dir: Path) -> dict:
    gold = load_gold(GOLD_DIR / f"{mode.replace('-', '_')}_tatoeba.tsv")
    with ThreadPoolExecutor(jobs) as pool:
        hyps = list(pool.map(lambda row: translate(row[0], mode, pair_dir), gold))
    steering = sum(max(steering_chrf(h, r) for r in refs)
                   for h, (_, refs) in zip(hyps, gold)) / len(gold)
    metric = CHRF()
    sb = metric.corpus_score([h.translate(MARKERS) for h in hyps],
                             [[refs[0] for _, refs in gold]])
    return {"sentences": len(gold), "chrf_steering": round(steering, 2),
            "chrf_sacrebleu": round(sb.score, 2),
            "_sig": metric.get_signature().format(), "_hyps": hyps, "_gold": gold}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--baseline", type=Path, default=GOLD_DIR / "baseline.json")
    ap.add_argument("--tolerance", type=float, default=None,
                    help="allowed drop in chrF points (default: baseline.json's)")
    ap.add_argument("--pair-dir", type=Path, default=ROOT, help="built pair (default: this repo)")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--hyp-dir", type=Path, help="write each direction's output here")
    args = ap.parse_args()

    baseline = json.loads(args.baseline.read_text()) if args.baseline.exists() else {}
    tol = args.tolerance if args.tolerance is not None else baseline.get("tolerance", 0.5)
    results = {mode: evaluate(mode, args.jobs, args.pair_dir) for mode in DIRECTIONS}

    if args.hyp_dir:
        args.hyp_dir.mkdir(parents=True, exist_ok=True)
        for mode, res in results.items():
            (args.hyp_dir / f"{mode}.tsv").write_text("".join(
                f"{src}\t{hyp}\t{refs[0]}\n" for hyp, (src, refs) in zip(res["_hyps"], res["_gold"])),
                encoding="utf-8")

    sig = results["ido-epo"]["_sig"]
    failed = False
    lines = ["| Direction | Metric | Baseline | Now | Δ |", "|---|---|---|---|---|"]
    for mode, res in results.items():
        base = baseline.get("directions", {}).get(mode, {})
        if base and base.get("sentences") != res["sentences"]:
            print(f"FAIL {mode}: {res['sentences']} sentences, baseline was measured on "
                  f"{base.get('sentences')} -- update baseline.json with the gold set",
                  file=sys.stderr)
            failed = True
        for metric in ("chrf_steering", "chrf_sacrebleu"):
            now, was = res[metric], base.get(metric)
            delta = "" if was is None else f"{now - was:+.2f}"
            mark = ""
            if was is not None and now < was - tol:
                mark, failed = " **FAIL**", True
            lines.append(f"| {mode} | {metric} | {was if was is not None else '-'} | {now:.2f} | {delta}{mark} |")
    report = "\n".join(lines) + f"\n\nTolerance {tol} chrF. sacrebleu signature: `{sig}`\n"
    print(report)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write("### Tatoeba held-out chrF\n\n" + report)

    if args.write_baseline:
        out = {
            "_comment": "Tatoeba held-out chrF of this pair, checked by dev/eval_tatoeba.py in CI. "
                        "Raise it (python3 dev/eval_tatoeba.py --write-baseline) in the PR that "
                        "improves quality; never lower it to make a regression pass.",
            "tolerance": tol,
            "sacrebleu_signature": sig,
            "directions": {m: {k: v for k, v in r.items() if not k.startswith("_")}
                           for m, r in results.items()},
        }
        args.baseline.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n")
        print(f"wrote {args.baseline}")
        return 0
    if failed:
        print("Quality gate failed (see above); baseline: "
              f"{args.baseline}.", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
