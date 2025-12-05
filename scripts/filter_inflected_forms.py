#!/usr/bin/env python3
"""
Filter out inflected forms that were mistakenly included as lemmas.

For example, "homi" (plural of "homo") should not be a separate lemma entry.
"""

import json
import sys
from pathlib import Path
import re

# Patterns for inflected forms that should be filtered out
INFLECTED_PATTERNS = [
    r'.*i$',  # Ido plural nouns ending in -i (should be -o)
    r'.*n$',  # Esperanto accusative forms ending in -n
]

# Compile regex patterns
COMPILED_PATTERNS = [re.compile(pattern) for pattern in INFLECTED_PATTERNS]


def is_inflected_form(lemma: str, pos: str) -> bool:
    """Check if a lemma is likely an inflected form rather than a true lemma."""
    
    # For nouns, lemmas should end in -o in both Ido and Esperanto
    if pos == 'n':
        if lemma.endswith('i') and not lemma.endswith('i' * 2):
            # Likely plural form
            base = lemma[:-1] + 'o'
            return True
        if lemma.endswith('n') and not lemma.endswith('n' * 2):
            # Likely accusative form
            return True
    
    return False


def filter_merged_json(input_file: Path, output_file: Path):
    """Filter out inflected forms from merged JSON."""
    
    print(f"Loading {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    metadata = data.get('metadata', {})
    
    print(f"Original entries: {len(entries)}")
    
    filtered_entries = []
    skipped_inflected = []
    
    for entry in entries:
        lemma = entry.get('lemma', '')
        pos = entry.get('pos', '')
        
        if is_inflected_form(lemma, pos):
            skipped_inflected.append(lemma)
            continue
        
        filtered_entries.append(entry)
    
    print(f"Filtered entries: {len(filtered_entries)}")
    print(f"Skipped inflected forms: {len(skipped_inflected)}")
    
    if skipped_inflected:
        print(f"\nExamples of skipped forms:")
        for lemma in skipped_inflected[:10]:
            print(f"  - {lemma}")
    
    # Update metadata
    metadata['filtered_inflected_forms'] = len(skipped_inflected)
    metadata['statistics'] = metadata.get('statistics', {})
    metadata['statistics']['total_entries'] = len(filtered_entries)
    
    # Write output
    output_data = {
        'metadata': metadata,
        'entries': filtered_entries
    }
    
    print(f"\nWriting to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Done!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Filter inflected forms from merged JSON'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Input merged JSON file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        required=True,
        help='Output filtered JSON file'
    )
    
    args = parser.parse_args()
    
    filter_merged_json(args.input, args.output)


if __name__ == '__main__':
    main()

