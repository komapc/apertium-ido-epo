#!/usr/bin/env python3
"""
Safe fixer for obvious errors in Ido monodix.

Rules (100% confidence only):
- If an entry is pair-style and has lemma ending with 'o', is single-word lowercase (no spaces, hyphens, or caps), and is tagged as adv, convert it to noun (n) by changing <r> tags to n sg/nom only.
  Rationale: Lowercase, single-word lemmas ending in -o are prototypically nouns; 'adv' is highly likely wrong. We do NOT touch multi-word or capitalized items.

Operations are conservative and reversible; original file is backed up.
"""

import argparse
import shutil
import sys
from pathlib import Path
from typing import List
import xml.etree.ElementTree as ET


def is_singleword_lower_o(lemma: str) -> bool:
    if not lemma:
        return False
    if " " in lemma or "\t" in lemma or "-" in lemma:
        return False
    if not lemma.endswith("o"):
        return False
    # Lowercase check: if any cased char is uppercase, skip
    if any(ch.isalpha() and ch != ch.lower() for ch in lemma):
        return False
    return True


def fix_file(input_path: Path, output_path: Path) -> int:
    tree = ET.parse(str(input_path))
    root = tree.getroot()
    section_main = None
    for section in root.findall("section"):
        if section.attrib.get("id") == "main":
            section_main = section
            break

    if section_main is None:
        print("No <section id=\"main\"> found; no changes.", file=sys.stderr)
        return 0

    changes = 0
    for e in section_main.findall("e"):
        p = e.find("p")
        if p is None:
            continue
        l = p.find("l")
        r = p.find("r")
        if l is None or r is None:
            continue
        lemma = (l.text or "").strip()
        if not is_singleword_lower_o(lemma):
            continue

        # collect tags
        tags = [s.attrib.get("n", "") for s in r.findall(".//s")]
        tags_set = set([t for t in tags if t])

        # If currently marked adv and not already noun/proper
        if "adv" in tags_set and "n" not in tags_set and "np" not in tags_set:
            # Replace r content with noun sg/nom
            r.clear()
            s_n = ET.SubElement(r, "s")
            s_n.attrib["n"] = "n"
            s_sg = ET.SubElement(r, "s")
            s_sg.attrib["n"] = "sg"
            s_nom = ET.SubElement(r, "s")
            s_nom.attrib["n"] = "nom"
            changes += 1

    if changes > 0:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        tree.write(str(output_path), encoding="UTF-8", xml_declaration=True)

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply safe fixes to Ido monodix")
    parser.add_argument("--input", required=True, help="Path to apertium-ido.ido.dix")
    parser.add_argument("--output", required=True, help="Path to write fixed dictionary")
    parser.add_argument("--backup", required=False, help="Optional path to backup original")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    if args.backup:
        backup_path = Path(args.backup)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(input_path), str(backup_path))

    changes = fix_file(input_path, output_path)
    print({"changes": changes, "output": str(output_path)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


