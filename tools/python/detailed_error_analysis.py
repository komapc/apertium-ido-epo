#!/usr/bin/env python3
"""
Deep analysis of translation errors - categorize by type
"""

import re
from collections import defaultdict

def categorize_errors(filename):
    """Categorize errors by type"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    categories = {
        'numbers': [],
        'proper_names': [],
        'function_words': [],
        'verbs': [],
        'nouns': [],
        'adjectives': [],
        'pronouns': [],
        'prepositions': [],
        'conjunctions': [],
        'unknown_category': []
    }
    
    # Extract all error markers
    at_words = re.findall(r'@(\w+)', content)
    hash_words = re.findall(r'#(\w+)', content)
    star_words = re.findall(r'\*(\w+)', content)
    
    all_errors = list(set(at_words + hash_words + star_words))
    
    for word in all_errors:
        # Categorize
        if word.isdigit() or re.match(r'\d+', word):
            categories['numbers'].append(word)
        elif word[0].isupper():  # Proper names
            categories['proper_names'].append(word)
        elif word in ['kaj', 'ol', 'sed', 'ktp', 'o', 'u', 'aŭ']:
            categories['conjunctions'].append(word)
        elif word in ['prpers', 'si', 'li', 'ili', 'el', 'elu', 'ol', 'Lo', 'Olia', 'Ilia']:
            categories['pronouns'].append(word)
        elif word in ['al', 'de', 'en', 'kun', 'por', 'pri', 'pro', 'di', 'che']:
            categories['prepositions'].append(word)
        elif word.endswith('ar') or word.endswith('ir') or word.endswith('or') or word.endswith('i'):
            categories['verbs'].append(word)
        elif word.endswith('o') or word.endswith('in') or word.endswith('ino'):
            categories['nouns'].append(word)
        elif word.endswith('a') or word.endswith('ala') or word.endswith('ema'):
            categories['adjectives'].append(word)
        else:
            categories['unknown_category'].append(word)
    
    return categories, all_errors

def analyze_specific_patterns(filename):
    """Analyze specific error patterns"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    patterns = {
        'prpers_pronoun': len(re.findall(r'@prpers', content)),
        'doubled_prepositions': len(re.findall(r'#al#\s+#al#|@di@\s+@di@', content)),
        'untranslated_parentheses': len(re.findall(r'@\([^)]+@\)', content)),
        'untranslated_quotes': len(re.findall(r'@"[^"]+@"', content)),
        'broken_compounds': len(re.findall(r'@\w+-@\w+', content)),
        'number_issues': len(re.findall(r'@\d+', content)),
        'reveni_al_al': len(re.findall(r'reveni#\s+al#\s+al#', content)),
    }
    
    return patterns

def main():
    files = {
        'tolkien_ido.txt': 'Tolkien (epo→ido)',
        'egipta_mitologio_ido.txt': 'Egyptian Mythology (epo→ido)',
        'austria_esperanto.txt': 'Austria (ido→epo)',
        'euro_esperanto.txt': 'Euro (ido→epo)',
    }
    
    print("=" * 80)
    print("DETAILED ERROR CATEGORIZATION")
    print("=" * 80)
    
    for filename, name in files.items():
        print(f"\n\n{'='*80}")
        print(f"{name}")
        print(f"File: {filename}")
        print(f"{'='*80}\n")
        
        categories, all_errors = categorize_errors(filename)
        patterns = analyze_specific_patterns(filename)
        
        print(f"Total unique errors: {len(all_errors)}\n")
        
        print("ERROR CATEGORIES:\n")
        
        for category, words in categories.items():
            if words:
                print(f"  {category.upper().replace('_', ' ')} ({len(words)}):")
                for word in sorted(set(words))[:15]:  # Show first 15
                    print(f"    - {word}")
                if len(words) > 15:
                    print(f"    ... and {len(words) - 15} more")
                print()
        
        print("\nSPECIFIC ERROR PATTERNS:\n")
        for pattern_name, count in patterns.items():
            if count > 0:
                print(f"  {pattern_name.replace('_', ' ').title()}: {count} occurrences")
        
        print()

if __name__ == '__main__':
    main()

