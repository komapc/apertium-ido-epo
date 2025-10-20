#!/usr/bin/env python3
"""
Sort Ido dictionary entries alphabetically while preserving structure
"""

import xml.etree.ElementTree as ET
from xml.dom import minidom

def sort_dictionary(file_path):
    """Sort dictionary entries alphabetically"""
    
    # Parse with ElementTree
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Find main section
    main_section = root.find(".//section[@id='main']")
    if main_section is None:
        print("Error: Could not find main section")
        return None
    
    # Get all entries and comments
    entries = list(main_section)
    
    # Separate function words (first entries, usually have comments before them)
    # and regular entries
    function_words_section = []
    regular_entries = []
    
    in_function_words = True
    i = 0
    
    while i < len(entries):
        item = entries[i]
        
        # Check if this is a comment marking the end of function words
        if item.tag == ET.Comment:
            comment_text = item.text.strip() if item.text else ""
            if 'Noun' in comment_text or 'Adjective' in comment_text or 'Verb' in comment_text:
                in_function_words = False
        
        if in_function_words:
            function_words_section.append(item)
        else:
            regular_entries.append(item)
        
        i += 1
    
    # Sort regular entries by lemma (lm attribute)
    def get_sort_key(elem):
        if elem.tag == ET.Comment:
            return ""  # Comments stay with their following entry
        lm = elem.get('lm', '')
        # Case-insensitive sort, but keep proper nouns (starting with capital) after common nouns
        return (lm.lower(), lm)
    
    # Group comments with their following entries
    sorted_entries = []
    pending_comment = None
    
    for item in regular_entries:
        if item.tag == ET.Comment:
            pending_comment = item
        else:
            if pending_comment is not None:
                sorted_entries.append((get_sort_key(item), pending_comment, item))
                pending_comment = None
            else:
                sorted_entries.append((get_sort_key(item), None, item))
    
    # Sort by the key
    sorted_entries.sort(key=lambda x: x[0])
    
    # Clear main section
    main_section.clear()
    
    # Add function words section back
    for item in function_words_section:
        main_section.append(item)
    
    # Add sorted entries
    for _, comment, entry in sorted_entries:
        if comment is not None:
            main_section.append(comment)
        main_section.append(entry)
    
    return tree

def main():
    input_file = '/home/mark/apertium-dev/apertium-ido-epo/apertium-ido.ido.dix'
    output_file = '/home/mark/apertium-dev/apertium-ido-epo/apertium-ido.ido.dix'
    
    print("Sorting Ido dictionary alphabetically...")
    tree = sort_dictionary(input_file)
    
    if tree is None:
        print("Error: Could not sort dictionary")
        return
    
    # Write sorted dictionary
    tree.write(output_file, encoding='UTF-8', xml_declaration=True)
    
    print(f"\n✓ Dictionary sorted and saved to: {output_file}")
    print("\nEntries are now sorted alphabetically by lemma for better maintainability.")

if __name__ == '__main__':
    main()

