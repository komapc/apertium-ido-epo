#!/usr/bin/env python3
"""
Step 6: Systematic Pattern Analysis for Kristanismo Translation
Analyzes the Esperanto Wikipedia article on Kristanismo to extract patterns
"""

import re
import sys
from collections import Counter, defaultdict

def analyze_partitive_da(text):
    """Extract all 'da' partitive constructions"""
    # Pattern: NUMBER/QUANTITY da NOUN
    pattern = r'(\S+)\s+da\s+(\S+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def analyze_superlative_plej(text):
    """Extract all 'plej + ADJECTIVE' constructions"""
    pattern = r'plej\s+(\S+)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def analyze_pronoun_gxi(text):
    """Extract 'ĝi' pronouns and context"""
    # Find ĝi, ĝin, ĝia, etc
    pattern = r'(\S*ĝi\S*)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def analyze_pronoun_oni(text):
    """Extract 'oni' pronouns and usage"""
    pattern = r'(\boni\w*)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches

def analyze_ordinals(text):
    """Extract ordinal numbers (1-a, 2-a, etc.)"""
    pattern = r'(\d+)-a\b'
    matches = re.findall(pattern, text)
    return matches

def analyze_circumflex_letters(text):
    """Count circumflex letters that need conversion"""
    counts = {
        'ĉ': text.count('ĉ') + text.count('Ĉ'),
        'ĝ': text.count('ĝ') + text.count('Ĝ'),
        'ĥ': text.count('ĥ') + text.count('Ĥ'),
        'ĵ': text.count('ĵ') + text.count('Ĵ'),
        'ŝ': text.count('ŝ') + text.count('Ŝ'),
        'ŭ': text.count('ŭ') + text.count('Ŭ'),
    }
    return counts

def analyze_compound_words(text):
    """Find potential compound words"""
    # Look for common compound patterns
    compounds = re.findall(r'\b[a-zĉĝĥĵŝŭ]{4,}(?:ismo|isto|ejo|eco|ado|ato|ido)\b', text, re.IGNORECASE)
    return compounds

def main():
    # Sample text from Kristanismo article
    sample_text = """
    Kristanismo estas tutmonda religio bazita sur la instruoj de Jesuo Kristo.
    Ĝi estas la plej granda religio en la mondo.
    Oni kalkulas, ke ekzistas ĉirkaŭ 2,4 miliardoj da kristanoj en la mondo.
    Kristanismo originas en Judujo en la 1-a jarcento.
    
    La kristana religio havas tri ĉefajn branĉojn: katolikismo, ortodoksismo kaj protestantismo.
    Ĝi estas bazita sur la vivo kaj instruoj de Jesuo Kristo, kiun kristanoj kredas esti la Filo de Dio.
    La sankta libro de kristanoj estas la Biblio, kiu konsistas el la Malnova Testamento kaj la Nova Testamento.
    
    Oni kredas, ke Jesuo naskiĝis en Bet-Le hem ĉirkaŭ la jaro 4 a.K.
    La plej gravaj kristanaj festoj estas Pasko kaj Kristnasko.
    Miloj da homoj ĉiujare pilgrimadas al sanktaj lokoj.
    """
    
    print("=" * 70)
    print("KRISTANISMO PATTERN ANALYSIS - Step 6")
    print("=" * 70)
    print()
    
    # Analyze partitive 'da'
    da_constructions = analyze_partitive_da(sample_text)
    print("1. PARTITIVE 'da' CONSTRUCTIONS")
    print("-" * 70)
    print(f"   Total found: {len(da_constructions)}")
    if da_constructions:
        print("   Examples:")
        for quant, noun in Counter(da_constructions).most_common(10):
            print(f"     • {quant} da {noun}")
    print()
    
    # Analyze superlative 'plej'
    plej_constructions = analyze_superlative_plej(sample_text)
    print("2. SUPERLATIVE 'plej + ADJECTIVE'")
    print("-" * 70)
    print(f"   Total found: {len(plej_constructions)}")
    if plej_constructions:
        print("   Examples:")
        for adj, count in Counter(plej_constructions).most_common(10):
            print(f"     • plej {adj} (× {count})")
    print()
    
    # Analyze pronoun 'ĝi'
    gxi_uses = analyze_pronoun_gxi(sample_text)
    print("3. NEUTER PRONOUN 'ĝi' FORMS")
    print("-" * 70)
    print(f"   Total found: {len(gxi_uses)}")
    if gxi_uses:
        print("   Forms:")
        for form, count in Counter(gxi_uses).most_common():
            print(f"     • {form} (× {count})")
    print()
    
    # Analyze pronoun 'oni'
    oni_uses = analyze_pronoun_oni(sample_text)
    print("4. IMPERSONAL PRONOUN 'oni'")
    print("-" * 70)
    print(f"   Total found: {len(oni_uses)}")
    if oni_uses:
        print("   Forms:")
        for form, count in Counter(oni_uses).most_common():
            print(f"     • {form} (× {count})")
    print()
    
    # Analyze ordinals
    ordinals = analyze_ordinals(sample_text)
    print("5. ORDINAL NUMBERS (N-a format)")
    print("-" * 70)
    print(f"   Total found: {len(ordinals)}")
    if ordinals:
        print("   Examples:")
        for num, count in Counter(ordinals).most_common(10):
            print(f"     • {num}-a → {num}ma (× {count})")
    print()
    
    # Analyze circumflex letters
    circumflex = analyze_circumflex_letters(sample_text)
    print("6. CIRCUMFLEX LETTERS (to remove/convert)")
    print("-" * 70)
    total_circumflex = sum(circumflex.values())
    print(f"   Total circumflexed characters: {total_circumflex}")
    for letter, count in circumflex.items():
        if count > 0:
            print(f"     • {letter}: {count} occurrences")
    print()
    
    # Analyze compounds
    compounds = analyze_compound_words(sample_text)
    print("7. COMPOUND WORDS (potential patterns)")
    print("-" * 70)
    print(f"   Total found: {len(compounds)}")
    if compounds:
        print("   Examples:")
        for word, count in Counter(compounds).most_common(15):
            print(f"     • {word} (× {count})")
    print()
    
    # Summary
    print("=" * 70)
    print("SUMMARY - IMPACT ASSESSMENT")
    print("=" * 70)
    print(f"Partitive 'da':        {len(da_constructions)} instances (HIGH priority)")
    print(f"Superlative 'plej':    {len(plej_constructions)} instances (HIGH priority)")
    print(f"Pronoun 'ĝi':          {len(gxi_uses)} instances (HIGH priority)")
    print(f"Pronoun 'oni':         {len(oni_uses)} instances (HIGH priority)")
    print(f"Ordinal numbers:       {len(ordinals)} instances (HIGH priority)")
    print(f"Circumflex letters:    {total_circumflex} characters (handled by dict)")
    print(f"Compound words:        {len(set(compounds))} unique (MEDIUM priority)")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

