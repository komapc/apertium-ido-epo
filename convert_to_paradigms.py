#!/usr/bin/env python3
"""
Convert bilingual dictionary entries to use paradigms.

This script fixes the critical issue where lt-trim was creating empty transducers
because bilingual entries (e.g., hund<n>) didn't match morphological analyzer
output (e.g., hund<n><sg><nom>).

The fix adds paradigm definitions that expand entries to include all inflection tags.
"""

import re
import sys

def convert_dictionary(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add paradigm definitions after </sdefs>
    paradigms = '''<pardefs>
  <!-- Noun paradigm: pass through number and case tags -->
  <pardef n="noun__n">
    <e><p><l><s n="n"/><s n="sg"/><s n="nom"/></l><r><s n="n"/><s n="sg"/><s n="nom"/></r></p></e>
    <e><p><l><s n="n"/><s n="sg"/><s n="acc"/></l><r><s n="n"/><s n="sg"/><s n="acc"/></r></p></e>
    <e><p><l><s n="n"/><s n="pl"/><s n="nom"/></l><r><s n="n"/><s n="pl"/><s n="nom"/></r></p></e>
    <e><p><l><s n="n"/><s n="pl"/><s n="acc"/></l><r><s n="n"/><s n="pl"/><s n="acc"/></r></p></e>
    <e><p><l><s n="n"/><s n="sp"/><s n="nom"/></l><r><s n="n"/><s n="sp"/><s n="nom"/></r></p></e>
    <e><p><l><s n="n"/><s n="sp"/><s n="acc"/></l><r><s n="n"/><s n="sp"/><s n="acc"/></r></p></e>
    <e><p><l><s n="n"/><s n="sg"/></l><r><s n="n"/><s n="sg"/></r></p></e>
    <e><p><l><s n="n"/><s n="pl"/></l><r><s n="n"/><s n="pl"/></r></p></e>
    <e><p><l><s n="n"/><s n="sp"/></l><r><s n="n"/><s n="sp"/></r></p></e>
    <e><p><l><s n="n"/></l><r><s n="n"/></r></p></e>
  </pardef>

  <!-- Verb paradigm: pass through tense tags -->
  <pardef n="verb__vblex">
    <e><p><l><s n="vblex"/><s n="inf"/></l><r><s n="vblex"/><s n="inf"/></r></p></e>
    <e><p><l><s n="vblex"/><s n="pri"/></l><r><s n="vblex"/><s n="pri"/></r></p></e>
    <e><p><l><s n="vblex"/><s n="pii"/></l><r><s n="vblex"/><s n="pii"/></r></p></e>
    <e><p><l><s n="vblex"/><s n="fti"/></l><r><s n="vblex"/><s n="fti"/></r></p></e>
    <e><p><l><s n="vblex"/><s n="cni"/></l><r><s n="vblex"/><s n="cni"/></r></p></e>
    <e><p><l><s n="vblex"/><s n="imp"/></l><r><s n="vblex"/><s n="imp"/></r></p></e>
    <e><p><l><s n="vblex"/></l><r><s n="vblex"/></r></p></e>
  </pardef>

  <!-- Adjective paradigm: pass through number and case tags -->
  <pardef n="adj__adj">
    <e><p><l><s n="adj"/><s n="sg"/><s n="nom"/></l><r><s n="adj"/><s n="sg"/><s n="nom"/></r></p></e>
    <e><p><l><s n="adj"/><s n="sg"/><s n="acc"/></l><r><s n="adj"/><s n="sg"/><s n="acc"/></r></p></e>
    <e><p><l><s n="adj"/><s n="pl"/><s n="nom"/></l><r><s n="adj"/><s n="pl"/><s n="nom"/></r></p></e>
    <e><p><l><s n="adj"/><s n="pl"/><s n="acc"/></l><r><s n="adj"/><s n="pl"/><s n="acc"/></r></p></e>
    <e><p><l><s n="adj"/><s n="sp"/><s n="nom"/></l><r><s n="adj"/><s n="sp"/><s n="nom"/></r></p></e>
    <e><p><l><s n="adj"/><s n="sp"/><s n="acc"/></l><r><s n="adj"/><s n="sp"/><s n="acc"/></r></p></e>
    <e><p><l><s n="adj"/><s n="sg"/></l><r><s n="adj"/><s n="sg"/></r></p></e>
    <e><p><l><s n="adj"/><s n="pl"/></l><r><s n="adj"/><s n="pl"/></r></p></e>
    <e><p><l><s n="adj"/><s n="sp"/></l><r><s n="adj"/><s n="sp"/></r></p></e>
    <e><p><l><s n="adj"/></l><r><s n="adj"/></r></p></e>
  </pardef>

  <!-- Adverb paradigm: simple passthrough -->
  <pardef n="adv__adv">
    <e><p><l><s n="adv"/></l><r><s n="adv"/></r></p></e>
  </pardef>

  <!-- Pronoun paradigm: pass through case tags -->
  <pardef n="prn__prn">
    <e><p><l><s n="prn"/><s n="nom"/></l><r><s n="prn"/><s n="nom"/></r></p></e>
    <e><p><l><s n="prn"/><s n="acc"/></l><r><s n="prn"/><s n="acc"/></r></p></e>
    <e><p><l><s n="prn"/></l><r><s n="prn"/></r></p></e>
  </pardef>
</pardefs>'''
    
    # Replace the old <pardefs> section or add it if missing
    if '<pardefs>' in content:
        # Find and replace existing pardefs
        content = re.sub(r'<pardefs>.*?</pardefs>', paradigms, content, flags=re.DOTALL)
    else:
        # Insert paradigms after </sdefs>
        content = content.replace('</sdefs>', '</sdefs>\n' + paradigms)
    
    # Convert entries to use paradigms
    # Pattern: <e>\n      <p>\n        <l>STEM<s n="POS"/></l>\n        <r>TRANSL<s n="POS"/></r>\n      </p>\n    </e>
    
    # Nouns
    content = re.sub(
        r'<e>\s*<p>\s*<l>([^<]+)<s n="n"/></l>\s*<r>([^<]+)<s n="n"/></r>\s*</p>\s*</e>',
        r'<e r="LR">\n      <p>\n        <l>\1</l>\n        <r>\2</r>\n      </p>\n      <par n="noun__n"/>\n    </e>',
        content
    )
    
    # Verbs
    content = re.sub(
        r'<e>\s*<p>\s*<l>([^<]+)<s n="vblex"/></l>\s*<r>([^<]+)<s n="vblex"/></r>\s*</p>\s*</e>',
        r'<e r="LR">\n      <p>\n        <l>\1</l>\n        <r>\2</r>\n      </p>\n      <par n="verb__vblex"/>\n    </e>',
        content
    )
    
    # Adjectives
    content = re.sub(
        r'<e>\s*<p>\s*<l>([^<]+)<s n="adj"/></l>\s*<r>([^<]+)<s n="adj"/></r>\s*</p>\s*</e>',
        r'<e r="LR">\n      <p>\n        <l>\1</l>\n        <r>\2</r>\n      </p>\n      <par n="adj__adj"/>\n    </e>',
        content
    )
    
    # Adverbs
    content = re.sub(
        r'<e>\s*<p>\s*<l>([^<]+)<s n="adv"/></l>\s*<r>([^<]+)<s n="adv"/></r>\s*</p>\s*</e>',
        r'<e r="LR">\n      <p>\n        <l>\1</l>\n        <r>\2</r>\n      </p>\n      <par n="adv__adv"/>\n    </e>',
        content
    )
    
    # Pronouns
    content = re.sub(
        r'<e>\s*<p>\s*<l>([^<]+)<s n="prn"/></l>\s*<r>([^<]+)<s n="prn"/></r>\s*</p>\s*</e>',
        r'<e r="LR">\n      <p>\n        <l>\1</l>\n        <r>\2</r>\n      </p>\n      <par n="prn__prn"/>\n    </e>',
        content
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Converted dictionary written to {output_file}")
    print(f"  All noun, verb, adjective, adverb, and pronoun entries now use paradigms")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 convert_to_paradigms.py input.dix output.dix")
        sys.exit(1)
    
    convert_dictionary(sys.argv[1], sys.argv[2])

