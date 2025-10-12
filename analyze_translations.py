#!/usr/bin/env python3
"""
Analyze translation errors and issues in the Wikipedia article translations
"""

import re
import json
from collections import defaultdict, Counter

def analyze_file(filename, direction):
    """Analyze a single translation file for issues"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = {
        'unknown_words_at': [],      # Words marked with @
        'unknown_words_hash': [],    # Words marked with #
        'unknown_words_star': [],    # Words marked with *
        'prpers_usage': [],           # Incorrect pronoun "prpers"
        'double_prepositions': [],   # Doubled prepositions like "al# al#"
        'untranslated_phrases': [],  # Phrases that weren't translated
        'formatting_issues': [],     # Formatting problems
        'capitalization_issues': [], # Improper capitalization
    }
    
    stats = {
        'total_chars': len(content),
        'total_lines': len(content.split('\n')),
        'total_words': len(content.split()),
    }
    
    # Find words with @ symbol
    at_words = re.findall(r'@\w+', content)
    issues['unknown_words_at'] = list(set(at_words))
    
    # Find words with # symbol  
    hash_words = re.findall(r'#\w+', content)
    issues['unknown_words_hash'] = list(set(hash_words))
    
    # Find words with * symbol
    star_words = re.findall(r'\*\w+', content)
    issues['unknown_words_star'] = list(set(star_words))
    
    # Find @prpers (incorrect pronoun handling)
    prpers_matches = re.findall(r'@prpers\b', content)
    issues['prpers_usage'] = prpers_matches
    
    # Find doubled words/prepositions
    double_patterns = re.findall(r'(\w+#)\s+\1', content)
    issues['double_prepositions'] = double_patterns
    
    # Find @(...@) patterns (untranslated parenthetical content)
    untranslated = re.findall(r'@\([^)]+@\)', content)
    issues['untranslated_phrases'] = untranslated
    
    # Count frequency of error markers
    stats['at_symbol_count'] = content.count('@')
    stats['hash_symbol_count'] = content.count('#')
    stats['star_symbol_count'] = content.count('*')
    stats['total_error_markers'] = stats['at_symbol_count'] + stats['hash_symbol_count'] + stats['star_symbol_count']
    
    # Calculate error rate
    if stats['total_words'] > 0:
        stats['error_rate_percent'] = (stats['total_error_markers'] / stats['total_words']) * 100
    else:
        stats['error_rate_percent'] = 0
    
    return issues, stats

def count_word_frequencies(issues):
    """Count how often each unknown word appears"""
    all_words = (
        issues['unknown_words_at'] + 
        issues['unknown_words_hash'] + 
        issues['unknown_words_star']
    )
    return Counter(all_words)

def main():
    print("=" * 80)
    print("TRANSLATION ERROR ANALYSIS")
    print("=" * 80)
    print()
    
    files_to_analyze = [
        {
            'name': 'Tolkien (Esperanto→Ido)',
            'file': 'tolkien_ido.txt',
            'direction': 'epo-ido',
            'original': 'tolkien_esperanto.txt'
        },
        {
            'name': 'Egyptian Mythology (Esperanto→Ido)',
            'file': 'egipta_mitologio_ido.txt',
            'direction': 'epo-ido',
            'original': 'egipta_mitologio_esperanto.txt'
        },
        {
            'name': 'Austria (Ido→Esperanto)',
            'file': 'austria_esperanto.txt',
            'direction': 'ido-epo',
            'original': 'austria_ido.txt'
        },
        {
            'name': 'Euro (Ido→Esperanto)',
            'file': 'euro_esperanto.txt',
            'direction': 'ido-epo',
            'original': 'euro_ido.txt'
        }
    ]
    
    all_results = {}
    
    for article in files_to_analyze:
        print(f"\n{'='*80}")
        print(f"Analyzing: {article['name']}")
        print(f"File: {article['file']}")
        print(f"Direction: {article['direction']}")
        print(f"{'='*80}\n")
        
        issues, stats = analyze_file(article['file'], article['direction'])
        all_results[article['name']] = {'issues': issues, 'stats': stats}
        
        # Print statistics
        print(f"STATISTICS:")
        print(f"  Total characters: {stats['total_chars']:,}")
        print(f"  Total words: {stats['total_words']:,}")
        print(f"  Total lines: {stats['total_lines']:,}")
        print(f"  Error markers (@): {stats['at_symbol_count']}")
        print(f"  Error markers (#): {stats['hash_symbol_count']}")
        print(f"  Error markers (*): {stats['star_symbol_count']}")
        print(f"  Total error markers: {stats['total_error_markers']}")
        print(f"  Error rate: {stats['error_rate_percent']:.2f}%")
        print()
        
        # Print issues
        print(f"ISSUES FOUND:")
        
        if issues['unknown_words_at']:
            print(f"\n  @ Unknown words ({len(issues['unknown_words_at'])} unique):")
            for word in sorted(issues['unknown_words_at'])[:20]:  # Show first 20
                print(f"    - {word}")
            if len(issues['unknown_words_at']) > 20:
                print(f"    ... and {len(issues['unknown_words_at']) - 20} more")
        
        if issues['unknown_words_hash']:
            print(f"\n  # Unknown words ({len(issues['unknown_words_hash'])} unique):")
            for word in sorted(issues['unknown_words_hash'])[:20]:
                print(f"    - {word}")
            if len(issues['unknown_words_hash']) > 20:
                print(f"    ... and {len(issues['unknown_words_hash']) - 20} more")
        
        if issues['unknown_words_star']:
            print(f"\n  * Unknown words ({len(issues['unknown_words_star'])} unique):")
            for word in sorted(issues['unknown_words_star'])[:20]:
                print(f"    - {word}")
            if len(issues['unknown_words_star']) > 20:
                print(f"    ... and {len(issues['unknown_words_star']) - 20} more")
        
        if issues['prpers_usage']:
            print(f"\n  @prpers issues: {len(issues['prpers_usage'])} occurrences")
        
        if issues['double_prepositions']:
            print(f"\n  Double prepositions: {issues['double_prepositions']}")
        
        if issues['untranslated_phrases']:
            print(f"\n  Untranslated phrases: {len(issues['untranslated_phrases'])}")
            for phrase in issues['untranslated_phrases'][:5]:
                print(f"    - {phrase}")
    
    # Overall summary
    print(f"\n\n{'='*80}")
    print("OVERALL SUMMARY")
    print(f"{'='*80}\n")
    
    total_words = sum(r['stats']['total_words'] for r in all_results.values())
    total_errors = sum(r['stats']['total_error_markers'] for r in all_results.values())
    overall_error_rate = (total_errors / total_words) * 100 if total_words > 0 else 0
    
    print(f"Total words translated: {total_words:,}")
    print(f"Total error markers: {total_errors:,}")
    print(f"Overall error rate: {overall_error_rate:.2f}%")
    print()
    
    print("Error rate by article:")
    for name, data in all_results.items():
        print(f"  {name}: {data['stats']['error_rate_percent']:.2f}%")
    
    print("\nError rate by direction:")
    epo_ido_errors = sum(
        r['stats']['error_rate_percent'] 
        for name, r in all_results.items() 
        if 'Esperanto→Ido' in name
    ) / 2
    ido_epo_errors = sum(
        r['stats']['error_rate_percent'] 
        for name, r in all_results.items() 
        if 'Ido→Esperanto' in name
    ) / 2
    
    print(f"  Esperanto→Ido: {epo_ido_errors:.2f}%")
    print(f"  Ido→Esperanto: {ido_epo_errors:.2f}%")
    
    # Save detailed results to JSON
    output_data = {}
    for name, data in all_results.items():
        output_data[name] = {
            'stats': data['stats'],
            'issues': {
                'unknown_at_count': len(data['issues']['unknown_words_at']),
                'unknown_hash_count': len(data['issues']['unknown_words_hash']),
                'unknown_star_count': len(data['issues']['unknown_words_star']),
                'prpers_count': len(data['issues']['prpers_usage']),
                'sample_unknown_at': data['issues']['unknown_words_at'][:10],
                'sample_unknown_hash': data['issues']['unknown_words_hash'][:10],
                'sample_unknown_star': data['issues']['unknown_words_star'][:10],
            }
        }
    
    with open('translation_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nDetailed results saved to: translation_analysis_results.json")

if __name__ == '__main__':
    main()

