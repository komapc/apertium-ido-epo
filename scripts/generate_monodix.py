#!/usr/bin/env python3
"""
Generate Apertium monodix (.dix) file from merged JSON.

Reads: projects/data/merged/merged_monodix.json
Outputs: Apertium monolingual dictionary XML file

Usage:
    python3 generate_monodix.py --input merged_monodix.json --output ido.ido.dix
"""

import json
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
import re


# POS mapping from JSON to Apertium symbol definitions
POS_MAP = {
    'n': 'n',           # noun
    'v': 'vblex',       # verb
    'adj': 'adj',       # adjective
    'adv': 'adv',       # adverb
    'pr': 'pr',         # preposition
    'prn': 'prn',       # pronoun
    'det': 'det',       # determiner
    'num': 'num',       # numeral
    'cnjcoo': 'cnjcoo', # coordinating conjunction
    'cnjsub': 'cnjsub', # subordinating conjunction
    'ij': 'ij',         # interjection
}


def extract_stem_ido(lemma: str, pos: Optional[str], paradigm: Optional[str]) -> str:
    """
    Extract the stem from an Ido lemma based on POS and paradigm.
    
    For Ido:
    - Nouns ending in -o → remove -o (persono → person)
    - Verbs ending in -ar → remove -ar (irar → ir)
    - Adjectives ending in -a → remove -a (bona → bon)
    - Adverbs ending in -e → remove -e (bone → bon)
    - Others → return as-is
    """
    if not lemma:
        return ""
    
    # If paradigm is specified, use it
    if paradigm:
        if paradigm.startswith('o__'):  # noun paradigm
            return lemma.rstrip('o') if lemma.endswith('o') else lemma
        elif paradigm.startswith('ar__'):  # verb paradigm
            return lemma.rstrip('ar') if lemma.endswith('ar') else lemma
        elif paradigm.startswith('a__'):  # adjective paradigm
            return lemma.rstrip('a') if lemma.endswith('a') else lemma
        elif paradigm.startswith('e__'):  # adverb paradigm
            return lemma.rstrip('e') if lemma.endswith('e') else lemma
        elif paradigm.startswith('__'):  # invariable (no suffix)
            return lemma
    
    # Fallback: use POS
    if pos == 'n' and lemma.endswith('o'):
        return lemma[:-1]
    elif pos in ('v', 'vblex') and lemma.endswith('ar'):
        return lemma[:-2]
    elif pos == 'adj' and lemma.endswith('a'):
        return lemma[:-1]
    elif pos == 'adv' and lemma.endswith('e'):
        return lemma[:-1]
    
    # Return as-is for other cases
    return lemma


def create_entry_element(lemma: str, stem: str, paradigm: str) -> ET.Element:
    """
    Create a monodix entry element.
    
    Format:
    <e lm="lemma">
      <i>stem</i>
      <par n="paradigm"/>
    </e>
    """
    entry = ET.Element('e')
    entry.set('lm', lemma)
    
    i_elem = ET.SubElement(entry, 'i')
    i_elem.text = stem
    
    par_elem = ET.SubElement(entry, 'par')
    par_elem.set('n', paradigm)
    
    return entry


def generate_monodix(input_file: Path, output_file: Path, min_confidence: float = 0.0):
    """
    Generate Apertium monodix from merged JSON.
    
    Args:
        input_file: Path to merged_monodix.json
        output_file: Path to output .dix file
        min_confidence: Minimum confidence threshold (not used for monodix, kept for consistency)
    """
    print(f"Loading merged monodix from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    metadata = data.get('metadata', {})
    stats = metadata.get('statistics', {})
    
    print(f"Total entries: {len(entries)}")
    print(f"Statistics: {stats}")
    
    # Create root element
    root = ET.Element('dictionary')
    
    # Add alphabet
    alphabet = ET.SubElement(root, 'alphabet')
    alphabet.text = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Add symbol definitions
    sdefs = ET.SubElement(root, 'sdefs')
    
    # Standard Ido symbol definitions
    sdef_list = [
        'n', 'adj', 'adv', 'vblex', 'pr', 'prn', 'det', 'num',
        'cnjcoo', 'cnjsub', 'ij', 'sg', 'pl', 'sp', 'nom', 'acc',
        'inf', 'pri', 'pii', 'fti', 'cni', 'imp',
        'p1', 'p2', 'p3', 'm', 'f', 'mf', 'nt',
        'np', 'ant', 'cog', 'top', 'al', 'ciph',
        'pres', 'past', 'fut', 'cond', 'pp',
        'pprs', 'pasv', 'act', 'pfut'
    ]
    
    for sdef_name in sdef_list:
        sdef = ET.SubElement(sdefs, 'sdef')
        sdef.set('n', sdef_name)
    
    # Add paradigm definitions
    pardefs = ET.SubElement(root, 'pardefs')
    
    # Load paradigms from external file if provided
    pardefs_file = input_file.parent.parent / 'pardefs.xml'
    if pardefs_file.exists():
        print(f"Loading paradigms from {pardefs_file}...")
        try:
            # Parse the pardefs file
            # We wrap it in a root element because the file might just be a list of <pardef>
            with open(pardefs_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # If it's not a full XML doc, wrap it
            if not content.strip().startswith('<?xml'):
                content = f"<root>{content}</root>"
            
            pardefs_root = ET.fromstring(content)
            
            # Append children to pardefs element
            for child in pardefs_root:
                pardefs.append(child)
                
            print(f"  ✅ Loaded {len(pardefs_root)} paradigms")
                
        except Exception as e:
            print(f"WARNING: Failed to load paradigms: {e}")
            comment = ET.Comment(f' Failed to load paradigms: {e} ')
            pardefs.append(comment)
    else:
        comment = ET.Comment(' Paradigm definitions should be included here ')
        pardefs.append(comment)
        print(f"WARNING: pardefs.xml not found at {pardefs_file}")
    
    # Add section with entries
    section = ET.SubElement(root, 'section')
    section.set('id', 'main')
    section.set('type', 'standard')
    
    # Track statistics
    entries_added = 0
    entries_skipped_no_paradigm = 0
    entries_skipped_no_lemma = 0
    
    for entry in entries:
        lemma = entry.get('lemma', '').strip()
        
        if not lemma:
            entries_skipped_no_lemma += 1
            continue
        
        # Get morphology
        morphology = entry.get('morphology', {})
        paradigm = morphology.get('paradigm')
        pos = entry.get('pos')
        
        if not paradigm:
            entries_skipped_no_paradigm += 1
            continue
        
        # Extract stem
        stem = extract_stem_ido(lemma, pos, paradigm)
        
        # Create entry
        entry_elem = create_entry_element(lemma, stem, paradigm)
        section.append(entry_elem)
        entries_added += 1
    
    # Write output
    print(f"\nWriting monodix to {output_file}...")
    print(f"  Entries added: {entries_added}")
    print(f"  Entries skipped (no paradigm): {entries_skipped_no_paradigm}")
    print(f"  Entries skipped (no lemma): {entries_skipped_no_lemma}")
    
    # Format XML with proper indentation
    indent_xml(root)
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    
    print(f"✅ Successfully generated monodix: {output_file}")


def indent_xml(elem, level=0):
    """
    Add proper indentation to XML for readability.
    
    CRITICAL: Do NOT add whitespace inside <r> tags because it breaks 
    morphological analysis! Tags like <s n="n"/><s n="pl"/> must be 
    on a single line without newlines or spaces between them.
    """
    indent = "\n" + "  " * level
    
    # Skip formatting inside <r> tags - they must stay on one line
    if elem.tag == 'r':
        # Just fix the tail (what comes after this element)
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent
        return
    
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent


def main():
    parser = argparse.ArgumentParser(
        description='Generate Apertium monodix from merged JSON'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path(__file__).parent.parent / 'merged' / 'merged_monodix.json',
        help='Input merged_monodix.json file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'generated' / 'ido.ido.dix',
        help='Output .dix file'
    )
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.0,
        help='Minimum confidence threshold (not used for monodix)'
    )
    
    args = parser.parse_args()
    
    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    generate_monodix(args.input, args.output, args.min_confidence)


if __name__ == '__main__':
    main()


