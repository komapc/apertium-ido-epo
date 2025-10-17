#!/usr/bin/env python3
import argparse
import json
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple

import xml.etree.ElementTree as ET


def normalize_space(value: Optional[str]) -> str:
    if value is None:
        return ""
    return "".join(value.split()) if ("\n" in value or "\t" in value or "  " in value) else value.strip()


def get_text(elem: Optional[ET.Element]) -> str:
    if elem is None:
        return ""
    text = (elem.text or "").strip()
    return text


def extract_tags_from_r(r_elem: ET.Element) -> List[str]:
    tags: List[str] = []
    for s in r_elem.findall(".//s"):
        n = s.attrib.get("n", "").strip()
        if n:
            tags.append(n)
    return tags


def infer_pos_from_par_name(par_name: str) -> Optional[str]:
    # Map common Ido paradigms to POS
    mapping = {
        "o__n": "n",
        "a__adj": "adj",
        "e__adv": "adv",
        "ar__vblex": "vblex",
        "ir__vblex": "vblex",
        "or__vblex": "vblex",
        "__inv_n": "n",
        "__pr": "pr",
        "__cnjcoo": "cnjcoo",
        "__cnjsub": "cnjsub",
    }
    return mapping.get(par_name)


def iter_entries(dix_path: Path) -> Iterable[Dict[str, object]]:
    # Support two common monodix entry styles under <section id="main">:
    # 1) Pair style: <e><p><l>lemma</l><r>...<s n="POS"/></r></p></e>
    # 2) Paradigm style: <e lm="lemma"><i>stem</i><par n="paradigm"/></e>
    # IMPORTANT: Only yield entries within <section id="main">, never from <pardefs>
    in_main_section: bool = False
    for event, elem in ET.iterparse(str(dix_path), events=("start", "end")):
        if event == "start":
            if elem.tag == "section" and elem.attrib.get("id") == "main":
                in_main_section = True
        elif event == "end":
            if elem.tag == "e" and in_main_section:
                yield parse_entry(elem)
                elem.clear()  # free memory
            elif elem.tag == "section" and elem.attrib.get("id") == "main":
                in_main_section = False


def parse_entry(e_elem: ET.Element) -> Dict[str, object]:
    # Try pair style first
    p = e_elem.find("p")
    if p is not None:
        l_elem = p.find("l")
        r_elem = p.find("r")
        lemma = normalize_space(get_text(l_elem))
        tags: List[str] = extract_tags_from_r(r_elem) if r_elem is not None else []
        return {
            "lemma": lemma,
            "pos_tags": tags,
            "source": "pair",
        }

    # Try paradigm style
    lemma = e_elem.attrib.get("lm", "").strip()
    i_elem = e_elem.find("i")
    par_elem = e_elem.find("par")
    stem = normalize_space(get_text(i_elem))
    par_name = par_elem.attrib.get("n") if par_elem is not None else None
    pos = infer_pos_from_par_name(par_name or "")
    tags = [pos] if pos else []
    return {
        "lemma": lemma,
        "pos_tags": tags,
        "source": "paradigm",
        "paradigm": par_name or "",
        "stem": stem,
    }


def classify_mismatches(lemma: str, tags: Set[str]) -> List[str]:
    issues: List[str] = []
    lower = lemma.lower()

    # Helpers
    is_noun = "n" in tags
    is_adj = "adj" in tags
    is_adv = "adv" in tags
    is_v = "vblex" in tags
    is_proper = "np" in tags

    # Whitelist: function words often end with -e/-a; avoid flagging them
    function_word_whitelist = {
        "ke", "de", "se", "la", "o", "e", "ma", "ka", "tra", "pro", "po", "no", "lo",
    }

    # -o nouns
    if lower.endswith("o"):
        if not is_noun and not is_proper:
            issues.append("o_not_noun")
        # Optional: adjectives/adv tagged words ending with 'o'
        if (is_adj or is_adv) and not is_noun:
            issues.append("o_with_adj_or_adv")

    # -a adjectives
    if lower.endswith("a") and lower not in function_word_whitelist:
        # Exclude very short unknown symbols like "4a" (numbers with a suffix)
        if not is_adj and not is_proper:
            issues.append("a_not_adj")

    # -e adverbs
    if lower.endswith("e") and lower not in function_word_whitelist:
        # Many proper names end with -e too; don't flag proper
        if not is_adv and not is_proper:
            issues.append("e_not_adv")

    # Verb endings
    ends_like_verb = lower.endswith("ar") or lower.endswith("ir") or lower.endswith("or")
    if ends_like_verb and not is_v:
        issues.append("verb_ending_not_vblex")
    # Do not flag finite forms like as/is/os/ez/us when vblex is present
    finite_forms = {"as", "is", "os", "ez", "us"}
    if is_v and (not ends_like_verb) and (lower not in finite_forms):
        issues.append("vblex_wrong_ending")

    return issues


def analyze(dix_path: Path) -> Dict[str, object]:
    results: List[Dict[str, object]] = []
    counts = Counter()
    categories = defaultdict(list)

    for entry in iter_entries(dix_path):
        lemma = str(entry.get("lemma", "")).strip()
        if not lemma:
            continue
        pos_tags = set([t for t in entry.get("pos_tags", []) if t])

        issues = classify_mismatches(lemma, pos_tags)
        if issues:
            item = {
                "lemma": lemma,
                "pos_tags": sorted(pos_tags),
                "issues": issues,
                "source": entry.get("source"),
            }
            # Carry extra fields if present
            if "paradigm" in entry:
                item["paradigm"] = entry["paradigm"]
            if "stem" in entry:
                item["stem"] = entry["stem"]

            results.append(item)
            for i in issues:
                counts[i] += 1
                categories[i].append(item)

    summary = {
        "dix_path": str(dix_path),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_flagged": len(results),
        "issue_counts": dict(counts),
    }
    return {"summary": summary, "results": results, "categories": categories}


def write_outputs(analysis: Dict[str, object], out_json: Path, out_tsv: Path) -> None:
    # JSON
    serializable = {
        "summary": analysis["summary"],
        "results": analysis["results"],
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with out_json.open("w", encoding="utf-8") as f:
        json.dump(serializable, f, ensure_ascii=False, indent=2)

    # TSV
    with out_tsv.open("w", encoding="utf-8") as f:
        f.write("lemma\tpos_tags\tissues\tsource\tparadigm\tstem\n")
        for item in analysis["results"]:
            lemma = item.get("lemma", "")
            pos_tags = ",".join(item.get("pos_tags", []))
            issues = ",".join(item.get("issues", []))
            source = item.get("source", "")
            paradigm = item.get("paradigm", "")
            stem = item.get("stem", "")
            f.write(f"{lemma}\t{pos_tags}\t{issues}\t{source}\t{paradigm}\t{stem}\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze Ido monodix for lemma-ending vs POS mismatches")
    parser.add_argument("--input", required=True, help="Path to apertium-ido.ido.dix")
    parser.add_argument("--out", required=False, help="Output JSON path")
    parser.add_argument("--tsv", required=False, help="Output TSV path")
    args = parser.parse_args()

    dix_path = Path(args.input)
    if not dix_path.exists():
        print(f"Input not found: {dix_path}", file=sys.stderr)
        return 2

    analysis = analyze(dix_path)

    # Defaults for outputs
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%SZ")
    out_json = Path(args.out) if args.out else Path("outputs") / f"ido_monodix_analysis_{timestamp}.json"
    out_tsv = Path(args.tsv) if args.tsv else Path("outputs") / f"ido_monodix_analysis_{timestamp}.tsv"

    write_outputs(analysis, out_json, out_tsv)

    # Print concise summary to stdout
    print(json.dumps(analysis["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


