#!/usr/bin/env python3
"""
Generate number entries for Apertium Ido-Esperanto dictionary
Handles: 0-9999, ordinals, and bidirectional conversion
"""

def generate_numbers():
    """Generate cardinal number entries 0-9999"""
    entries = []
    
    # Cardinal numbers 0-9999
    for i in range(10000):
        entry = f'<e><p><l>{i}<s n="num"/></l><r>{i}<s n="num"/></r></p></e>'
        entries.append(entry)
    
    return entries

def generate_ordinals():
    """Generate ordinal number entries"""
    entries = []
    
    # Ordinals: 1ma-100ma (Ido) <-> 1-a through 100-a (Esperanto)
    for i in range(1, 101):
        # Ido ordinal (1ma, 2ma, etc.) <-> Esperanto ordinal (unua, dua, etc.)
        # For numbers, we use the digit form
        # Ido: 1ma, 2ma, 3ma, etc.
        # Esperanto: 1-a, 2-a, 3-a, etc.
        
        # Nominative form
        entry_nom = f'<e><p><l>{i}ma<s n="num"/></l><r>{i}-a<s n="num"/></r></p></e>'
        entries.append(entry_nom)
        
        # Accusative form (only in Esperanto)
        entry_acc = f'<e><p><l>{i}ma<s n="num"/></l><r>{i}-an<s n="num"/></r></p></e>'
        entries.append(entry_acc)
    
    # Special ordinals with word forms
    special_ordinals = [
        ('1ma', 'unua'),
        ('2ma', 'dua'),
        ('3ma', 'tria'),
        ('4ma', 'kvara'),
        ('5ma', 'kvina'),
        ('6ma', 'sesa'),
        ('7ma', 'sepa'),
        ('8ma', 'oka'),
        ('9ma', 'naŭa'),
        ('10ma', 'deka'),
    ]
    
    for ido, epo in special_ordinals:
        # Nominative
        entries.append(f'<e><p><l>{ido}<s n="adj"/></l><r>{epo}<s n="adj"/></r></p></e>')
        # Accusative (Esperanto adds -n)
        entries.append(f'<e><p><l>{ido}<s n="adj"/></l><r>{epo}n<s n="adj"/></r></p></e>')
    
    return entries

def main():
    print('<?xml version="1.0" encoding="UTF-8"?>')
    print('<!-- Generated number entries for Apertium Ido-Esperanto -->')
    print('<!-- Cardinals: 0-9999, Ordinals: 1ma-100ma with accusative forms -->')
    print('<section id="numbers" type="standard">')
    
    # Generate cardinal numbers
    print('  <!-- Cardinal numbers 0-9999 -->')
    for entry in generate_numbers():
        print(f'  {entry}')
    
    # Generate ordinal numbers  
    print('\n  <!-- Ordinal numbers -->')
    for entry in generate_ordinals():
        print(f'  {entry}')
    
    print('</section>')

if __name__ == '__main__':
    main()

