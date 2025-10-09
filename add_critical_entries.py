#!/usr/bin/env python3
"""
Add critical missing dictionary entries for Kristanismo translation fixes
"""

import re

# Read the bilingual dictionary
with open('apertium-ido-epo.ido-epo.dix', 'r') as f:
    content = f.read()

# Find the end of the dictionary (before </section></dictionary>)
end_marker = '</section></dictionary>'

if end_marker not in content:
    print("ERROR: Could not find end marker in dictionary")
    exit(1)

# Entries to add
new_entries = [
    # Critical: Impersonal pronoun "oni" → "on"
    '<e><p><l>on<s n="prn" /></l><r>oni<s n="prn" /></r></p></e>',
    
    # Religious vocabulary
    '<e><p><l>kristanismo<s n="n" /></l><r>kristanismo<s n="n" /></r></p></e>',
    '<e><p><l>kristano<s n="n" /></l><r>kristano<s n="n" /></r></p></e>',
    '<e><p><l>kristana<s n="adj" /></l><r>kristana<s n="adj" /></r></p></e>',
    '<e><p><l>religio<s n="n" /></l><r>religio<s n="n" /></r></p></e>',
    '<e><p><l>religioza<s n="adj" /></l><r>religia<s n="adj" /></r></p></e>',
    
    # Jesus/Christ
    '<e><p><l>Iesu<s n="np" /></l><r>Jesuo<s n="np" /></r></p></e>',
    '<e><p><l>Kristo<s n="np" /></l><r>Kristo<s n="np" /></r></p></e>',
    
    # Religious terms
    '<e><p><l>eklezio<s n="n" /></l><r>eklezio<s n="n" /></r></p></e>',
    '<e><p><l>Biblio<s n="n" /></l><r>Biblio<s n="n" /></r></p></e>',
    '<e><p><l>biblio<s n="n" /></l><r>biblio<s n="n" /></r></p></e>',
    '<e><p><l>testamento<s n="n" /></l><r>testamento<s n="n" /></r></p></e>',
    
    # Common verbs
    '<e><p><l>bazita<s n="adj" /></l><r>bazita<s n="adj" /></r></p></e>',
    '<e><p><l>instruado<s n="n" /></l><r>instruoj<s n="n" /></r></p></e>',
    '<e><p><l>instruar<s n="vblex" /></l><r>instrui<s n="vblex" /></r></p></e>',
    '<e><p><l>existar<s n="vblex" /></l><r>ekzisti<s n="vblex" /></r></p></e>',
    '<e><p><l>kontar<s n="vblex" /></l><r>kalkuli<s n="vblex" /></r></p></e>',
    '<e><p><l>orinjinar<s n="vblex" /></l><r>origini<s n="vblex" /></r></p></e>',
    
    # Adjectives
    '<e><p><l>tut-mondala<s n="adj" /></l><r>tutmonda<s n="adj" /></r></p></e>',
    '<e><p><l>tutmondala<s n="adj" /></l><r>tutmonda<s n="adj" /></r></p></e>',
    
    # Geographic
    '<e><p><l>Judea<s n="np" /></l><r>Judujo<s n="np" /></r></p></e>',
    '<e><p><l>Judeana<s n="adj" /></l><r>juda<s n="adj" /></r></p></e>',
    
    # Numbers
    '<e><p><l>miliardo<s n="n" /></l><r>miliardo<s n="n" /></r></p></e>',
    '<e><p><l>miliardi<s n="n" /></l><r>miliardoj<s n="n" /></r></p></e>',
]

# Check which entries already exist
existing_entries = []
new_unique_entries = []

for entry in new_entries:
    # Extract the lemma (between <l> and <)
    match = re.search(r'<l>([^<]+)<', entry)
    if match:
        lemma = match.group(1)
        if f'<l>{lemma}<' in content:
            existing_entries.append(lemma)
        else:
            new_unique_entries.append(entry)

print(f"Found {len(existing_entries)} entries already in dictionary:")
for lemma in existing_entries:
    print(f"  ✓ {lemma}")

print(f"\nAdding {len(new_unique_entries)} new entries:")
for entry in new_unique_entries:
    match = re.search(r'<l>([^<]+)<', entry)
    if match:
        print(f"  + {match.group(1)}")

# Add new entries before the end marker
if new_unique_entries:
    insert_point = content.find(end_marker)
    new_content = (
        content[:insert_point] +
        ''.join(new_unique_entries) +
        content[insert_point:]
    )
    
    # Write back
    with open('apertium-ido-epo.ido-epo.dix', 'w') as f:
        f.write(new_content)
    
    print(f"\n✅ Successfully added {len(new_unique_entries)} entries to dictionary")
else:
    print("\n✅ All entries already exist in dictionary")

