#!/usr/bin/env python3
"""
Generate Apertium bidix (.dix) file from merged JSON.

Reads: projects/data/merged/merged_bidix.json
Outputs: Apertium bilingual dictionary XML file

Usage:
    python3 generate_bidix.py --input merged_bidix.json --output ido-epo.ido-epo.dix
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
    'noun': 'n',
    'v': 'vblex',       # verb
    'verb': 'vblex',
    'vblex': 'vblex',   # verb (already mapped)
    'adj': 'adj',       # adjective
    'adjective': 'adj',
    'adv': 'adv',       # adverb
    'adverb': 'adv',
    'pr': 'pr',         # preposition -> pr in bidix
    'prep': 'pr',       # preposition
    'preposition': 'pr',
    'prn': 'prn',       # pronoun
    'pronoun': 'prn',
    'det': 'det',       # determiner
    'determiner': 'det',
    'num': 'num',       # numeral
    'numeral': 'num',
    'cnjcoo': 'cnjcoo', # coordinating conjunction
    'conjunction': 'cnjcoo', # generic conjunction maps to cnjcoo
    'coordinating conjunction': 'cnjcoo',
    'cnjsub': 'cnjsub', # subordinating conjunction
    'subordinating conjunction': 'cnjsub',
    'ij': 'ij',         # interjection
    'interjection': 'ij',
    'proper noun': 'np',
    'np': 'np',
}


def guess_pos_ido(word: str) -> Optional[str]:
    """Guess POS from Ido word ending."""
    if not word:
        return None
    
    word = word.lower().strip()
    
    if word.endswith('o'):
        return 'n'
    elif word.endswith('ar'):
        return 'vblex'
    elif word.endswith('a') and not word.endswith('ar'):
        return 'adj'
    elif word.endswith('e'):
        return 'adv'
    
    return None


def guess_pos_esperanto(word: str) -> Optional[str]:
    """Guess POS from Esperanto word ending."""
    if not word:
        return None
    
    word = word.lower().strip()
    
    if word.endswith('o'):
        return 'n'
    elif word.endswith('i'):
        return 'vblex'
    elif word.endswith('a') and not word.endswith('i'):
        return 'adj'
    elif word.endswith('e'):
        return 'adv'
    
    return None


def extract_lemma_ido(word: str, pos: Optional[str] = None) -> str:
    """
    Extract lemma (stem) from Ido word.
    
    For Ido:
    - Nouns ending in -o → remove -o (persono → person)
    - Verbs ending in -ar → remove -ar (irar → ir)
    - Adjectives ending in -a → remove -a (bona → bon)
    - Adverbs ending in -e → remove -e (bone → bon)
    - Others → return as-is
    """
    if not word:
        return word
    
    word = word.strip()
    
    # If POS not provided, guess it
    if not pos:
        pos = guess_pos_ido(word)
    
    pos_lower = pos.lower() if pos else ''
    
    if (pos_lower in ('n', 'noun', 'np') or 'proper' in pos_lower) and word.endswith('o'):
        return word[:-1]
    elif pos_lower in ('v', 'vblex', 'verb') and word.endswith('ar'):
        return word[:-2]
    elif pos_lower in ('adj', 'adjective') and word.endswith('a'):
        return word[:-1]
    elif pos_lower in ('adv', 'adverb') and word.endswith('e'):
        return word[:-1]
    
    return word


def extract_lemma_esperanto(word: str, pos: Optional[str] = None) -> str:
    """
    Extract lemma (stem) from Esperanto word.
    
    For Esperanto:
    - Nouns ending in -o → remove -o (homo → hom)
    - Verbs ending in -i → remove -i (iri → ir)
    - Adjectives ending in -a → remove -a (bona → bon)
    - Adverbs ending in -e → remove -e (bone → bon)
    - Others → return as-is
    """
    if not word:
        return word
    
    word = word.strip()
    
    # If POS not provided, guess it
    if not pos:
        pos = guess_pos_esperanto(word)
    
    pos_lower = pos.lower() if pos else ''
    
    if pos_lower in ('n', 'noun') and word.endswith('o'):
        return word[:-1]
    elif pos_lower in ('v', 'vblex', 'verb') and word.endswith('i'):
        return word[:-1]
    elif pos_lower in ('adj', 'adjective') and word.endswith('a'):
        return word[:-1]
    elif pos_lower in ('adv', 'adverb') and word.endswith('e'):
        return word[:-1]
    
    return word


def create_bidix_entry(ido_lemma: str, epo_lemma: str, confidence: float, 
                       pos: Optional[str] = None, add_pos: bool = True) -> ET.Element:
    """
    Create a bidix entry element.
    
    Format without POS:
    <e>
      <p>
        <l>ido_lemma</l>
        <r>epo_lemma</r>
      </p>
    </e>
    
    Format with POS:
    <e>
      <!-- confidence: 1.0000 -->
      <p>
        <l>ido_lemma<s n="pos"/></l>
        <r>epo_lemma<s n="pos"/></r>
      </p>
    </e>
    """
    entry = ET.Element('e')
    
    # Add confidence comment
    comment = ET.Comment(f' confidence: {confidence:.4f} ')
    entry.append(comment)
    
    pair = ET.SubElement(entry, 'p')
    left = ET.SubElement(pair, 'l')
    right = ET.SubElement(pair, 'r')
    
    # Decide whether to add POS tags
    if add_pos and pos and pos in POS_MAP:
        # With POS tags
        left.text = ido_lemma
        s_left = ET.SubElement(left, 's')
        s_left.set('n', POS_MAP[pos])
        
        right.text = epo_lemma
        s_right = ET.SubElement(right, 's')
        s_right.set('n', POS_MAP[pos])
    else:
        # Without POS tags
        left.text = ido_lemma
        right.text = epo_lemma
    
    return entry


def generate_bidix(input_file: Path, output_file: Path, min_confidence: float = 0.0,
                   add_pos: bool = True):
    """
    Generate Apertium bidix from merged JSON.
    
    Args:
        input_file: Path to merged_bidix.json
        output_file: Path to output .dix file
        min_confidence: Minimum confidence threshold for including translations
        add_pos: Whether to add POS tags to entries
    """
    print(f"Loading merged bidix from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    metadata = data.get('metadata', {})
    stats = metadata.get('statistics', {})
    
    print(f"Total entries: {len(entries)}")
    print(f"Statistics: {stats}")
    print(f"Min confidence: {min_confidence}")
    print(f"Add POS tags: {add_pos}")
    
    # Create root element
    root = ET.Element('dictionary')
    
    # Add alphabet
    alphabet = ET.SubElement(root, 'alphabet')
    # Empty alphabet for bidix is standard
    
    # Add symbol definitions
    sdefs = ET.SubElement(root, 'sdefs')
    
    # Standard symbol definitions for bidix
    sdef_list = ['n', 'vblex', 'adj', 'adv', 'prn', 'det', 'pr', 
                 'cnjcoo', 'cnjsub', 'num', 'np', 'ij']
    
    for sdef_name in sdef_list:
        sdef = ET.SubElement(sdefs, 'sdef')
        sdef.set('n', sdef_name)
    
    # Add section with entries
    section = ET.SubElement(root, 'section')
    section.set('id', 'main')
    section.set('type', 'standard')
    
    # Track statistics
    entries_added = 0
    entries_skipped_no_translation = 0
    entries_skipped_low_confidence = 0
    entries_skipped_no_lemma = 0
    
    for entry in entries:
        lemma = entry.get('lemma', '').strip()
        
        if not lemma:
            entries_skipped_no_lemma += 1
            continue
        
        translations = entry.get('translations', [])
        
        if not translations:
            entries_skipped_no_translation += 1
            continue
        
        pos = entry.get('pos')
        
        # Process each translation
        for trans in translations:
            term = trans.get('term', '').strip()
            lang = trans.get('lang', '')
            confidence = trans.get('confidence', 0.0)
            
            # Skip if not Esperanto
            if lang != 'eo':
                continue
            
            # Skip if below confidence threshold
            if confidence < min_confidence:
                entries_skipped_low_confidence += 1
                continue
            
            if not term:
                continue
            
            # Extract lemmas (stems)
            # For Ido: extract stem (homo → hom)
            # For Esperanto: keep full lemma (homo → homo) because Esperanto generator expects full lemmas
            ido_lemma = extract_lemma_ido(lemma, pos)
            epo_lemma = term  # Keep full Esperanto lemma, don't extract stem
            
            # Create entry
            entry_elem = create_bidix_entry(ido_lemma, epo_lemma, confidence, pos, add_pos)
            section.append(entry_elem)
            entries_added += 1
    
    # Write output
    print(f"\nWriting bidix to {output_file}...")
    print(f"  Entries added: {entries_added}")
    print(f"  Entries skipped (no translation): {entries_skipped_no_translation}")
    print(f"  Entries skipped (low confidence): {entries_skipped_low_confidence}")
    print(f"  Entries skipped (no lemma): {entries_skipped_no_lemma}")
    
    # Format XML with proper indentation
    indent_xml(root)
    
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)
    
    print(f"✅ Successfully generated bidix: {output_file}")


def indent_xml(elem, level=0):
    """
    Add proper indentation to XML for readability.
    
    CRITICAL: Do NOT add whitespace inside <r> or <l> tags in bidix because 
    it breaks morphological analysis! Tags must stay on one line.
    """
    indent = "\n" + "  " * level
    
    # Skip formatting inside <r> and <l> tags - they must stay on one line
    if elem.tag in ('r', 'l'):
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
        description='Generate Apertium bidix from merged JSON'
    )
    parser.add_argument(
        '--input',
        type=Path,
        default=Path(__file__).parent.parent / 'merged' / 'merged_bidix.json',
        help='Input merged_bidix.json file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path(__file__).parent.parent / 'generated' / 'ido-epo.ido-epo.dix',
        help='Output .dix file'
    )
    parser.add_argument(
        '--min-confidence',
        type=float,
        default=0.0,
        help='Minimum confidence threshold for including translations'
    )
    parser.add_argument(
        '--no-pos',
        action='store_true',
        help='Do not add POS tags to entries'
    )
    
    args = parser.parse_args()
    
    # Create output directory if needed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    
    generate_bidix(args.input, args.output, args.min_confidence, add_pos=not args.no_pos)


if __name__ == '__main__':
    main()
