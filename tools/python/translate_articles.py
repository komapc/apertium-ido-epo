#!/usr/bin/env python3
"""
Script to extract and translate Wikipedia articles using Apertium
"""

import json
import subprocess
import sys

def extract_text_from_json(json_file):
    """Extract plain text from Wikipedia API JSON response"""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pages = data['query']['pages']
    page_id = list(pages.keys())[0]
    
    if 'extract' in pages[page_id]:
        return pages[page_id]['extract']
    else:
        return ""

def translate_text(text, direction):
    """
    Translate text using Apertium
    direction: 'epo-ido' or 'ido-epo'
    """
    try:
        # Use apertium from the built directory
        process = subprocess.Popen(
            ['apertium', '-d', '/home/mark/apertium-dev/apertium-ido-epo', direction],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        output, error = process.communicate(input=text.encode('utf-8'))
        
        if process.returncode != 0:
            print(f"Error translating: {error.decode('utf-8')}", file=sys.stderr)
            return text
        
        return output.decode('utf-8')
    except Exception as e:
        print(f"Exception during translation: {str(e)}", file=sys.stderr)
        return text

def main():
    # Article configurations
    articles = [
        {
            'name': 'Tolkien',
            'input': 'tolkien_raw.json',
            'direction': 'epo-ido',
            'output_text': 'tolkien_esperanto.txt',
            'output_translation': 'tolkien_ido.txt'
        },
        {
            'name': 'Egyptian Mythology',
            'input': 'egipta_mitologio_raw.json',
            'direction': 'epo-ido',
            'output_text': 'egipta_mitologio_esperanto.txt',
            'output_translation': 'egipta_mitologio_ido.txt'
        },
        {
            'name': 'Austria',
            'input': 'austria_raw.json',
            'direction': 'ido-epo',
            'output_text': 'austria_ido.txt',
            'output_translation': 'austria_esperanto.txt'
        },
        {
            'name': 'Euro',
            'input': 'euro_raw.json',
            'direction': 'ido-epo',
            'output_text': 'euro_ido.txt',
            'output_translation': 'euro_esperanto.txt'
        }
    ]
    
    for article in articles:
        print(f"\n{'='*60}")
        print(f"Processing: {article['name']}")
        print(f"{'='*60}")
        
        # Extract text
        print(f"Extracting text from {article['input']}...")
        text = extract_text_from_json(article['input'])
        
        if not text:
            print(f"Warning: No text extracted from {article['input']}")
            continue
        
        # Save original text
        with open(article['output_text'], 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Saved original text to {article['output_text']} ({len(text)} chars)")
        
        # Translate
        print(f"Translating {article['direction']}...")
        translation = translate_text(text, article['direction'])
        
        # Save translation
        with open(article['output_translation'], 'w', encoding='utf-8') as f:
            f.write(translation)
        print(f"Saved translation to {article['output_translation']} ({len(translation)} chars)")
    
    print(f"\n{'='*60}")
    print("All translations completed!")
    print(f"{'='*60}")

if __name__ == '__main__':
    main()

