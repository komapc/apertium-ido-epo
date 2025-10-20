#!/usr/bin/env python3
"""
Fetch large Wikipedia articles from Ido and Esperanto Wikipedia,
translate them using Apertium, and analyze translation problems.
"""

import requests
import subprocess
import json
from typing import Dict, List, Tuple

def get_wikipedia_article(lang: str, title: str) -> str:
    """Fetch a Wikipedia article in the specified language."""
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'extracts',
        'explaintext': True,
        'exsectionformat': 'plain'
    }
    
    try:
        headers = {
            'User-Agent': 'Apertium Translation Analysis/1.0 (https://github.com/apertium)'
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"  HTTP Error: {response.status_code}")
            return ""
        
        if not response.text:
            print(f"  Empty response from Wikipedia API")
            return ""
            
        data = response.json()
        
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        
        if page_id == '-1':
            print(f"  Article '{title}' not found")
            return ""
        
        return pages[page_id].get('extract', '')
    except Exception as e:
        print(f"  Error fetching article: {str(e)}")
        return ""

def get_large_articles(lang: str, limit: int = 10) -> List[Dict]:
    """Get a list of large articles from Wikipedia."""
    url = f"https://{lang}.wikipedia.org/w/api.php"
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'allpages',
        'aplimit': limit,
        'apfilterredir': 'nonredirects'
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    articles_with_sizes = []
    for page in data['query']['allpages']:
        title = page['title']
        # Get article size
        size_params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'size'
        }
        size_response = requests.get(url, params=size_params)
        size_data = size_response.json()
        pages = size_data['query']['pages']
        page_id = list(pages.keys())[0]
        size = pages[page_id]['revisions'][0]['size']
        articles_with_sizes.append({'title': title, 'size': size})
    
    # Sort by size and return
    articles_with_sizes.sort(key=lambda x: x['size'], reverse=True)
    return articles_with_sizes

def translate_text(text: str, direction: str, apertium_dir: str) -> str:
    """Translate text using Apertium."""
    cmd = ['apertium', '-d', apertium_dir, direction]
    
    try:
        result = subprocess.run(
            cmd,
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=60
        )
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Translation error: {str(e)}"

def analyze_translation_problems(original: str, translated: str, direction: str) -> List[str]:
    """Analyze problems in the translation."""
    problems = []
    
    # Check for untranslated words (marked with @)
    if '@' in translated:
        count = translated.count('@')
        problems.append(f"Found {count} untranslated/unknown words marked with '@'")
    
    # Check for asterisks (generation errors)
    if '*' in translated:
        count = translated.count('*')
        problems.append(f"Found {count} generation errors marked with '*'")
    
    # Check for hash symbols (other errors)
    if '#' in translated:
        count = translated.count('#')
        problems.append(f"Found {count} analysis errors marked with '#'")
    
    # Check length ratio
    orig_words = len(original.split())
    trans_words = len(translated.split())
    ratio = trans_words / orig_words if orig_words > 0 else 0
    
    if ratio < 0.5 or ratio > 2.0:
        problems.append(f"Unusual length ratio: {ratio:.2f} (original: {orig_words} words, translated: {trans_words} words)")
    
    # Check for repeated patterns (might indicate rule issues)
    lines = translated.split('\n')
    if len(lines) < len(original.split('\n')) / 2:
        problems.append("Translation produced significantly fewer lines than original")
    
    return problems

def main():
    print("Fetching large articles from Ido and Esperanto Wikipedia...\n")
    
    # Manually select well-known large articles
    ido_articles = [
        "Tero",  # Earth
        "Europa",  # Europe
    ]
    
    epo_articles = [
        "Tero",  # Earth
        "Eŭropo",  # Europe
    ]
    
    apertium_dir = "/home/mark/apertium-dev/apertium-ido-epo"
    results = []
    
    # Process Ido articles (translate to Esperanto)
    print("=" * 80)
    print("IDO → ESPERANTO TRANSLATIONS")
    print("=" * 80)
    
    for title in ido_articles:
        print(f"\nFetching Ido article: {title}")
        original = get_wikipedia_article('io', title)
        
        if not original or len(original) < 100:
            print(f"  Article too short or not found, skipping...")
            continue
        
        # Take first 2000 characters for analysis
        original_excerpt = original[:2000]
        print(f"  Article length: {len(original)} characters")
        print(f"  Using first 2000 characters for translation")
        
        print(f"  Translating to Esperanto...")
        translated = translate_text(original_excerpt, 'ido-epo', apertium_dir)
        
        print(f"  Analyzing problems...")
        problems = analyze_translation_problems(original_excerpt, translated, 'ido-epo')
        
        result = {
            'source_lang': 'ido',
            'target_lang': 'esperanto',
            'title': title,
            'original_length': len(original),
            'excerpt_length': len(original_excerpt),
            'translated_length': len(translated),
            'original_excerpt': original_excerpt,
            'translated': translated,
            'problems': problems
        }
        results.append(result)
        
        print(f"\n  Problems found: {len(problems)}")
        for i, problem in enumerate(problems, 1):
            print(f"    {i}. {problem}")
    
    # Process Esperanto articles (translate to Ido)
    print("\n" + "=" * 80)
    print("ESPERANTO → IDO TRANSLATIONS")
    print("=" * 80)
    
    for title in epo_articles:
        print(f"\nFetching Esperanto article: {title}")
        original = get_wikipedia_article('eo', title)
        
        if not original or len(original) < 100:
            print(f"  Article too short or not found, skipping...")
            continue
        
        # Take first 2000 characters for analysis
        original_excerpt = original[:2000]
        print(f"  Article length: {len(original)} characters")
        print(f"  Using first 2000 characters for translation")
        
        print(f"  Translating to Ido...")
        translated = translate_text(original_excerpt, 'epo-ido', apertium_dir)
        
        print(f"  Analyzing problems...")
        problems = analyze_translation_problems(original_excerpt, translated, 'epo-ido')
        
        result = {
            'source_lang': 'esperanto',
            'target_lang': 'ido',
            'title': title,
            'original_length': len(original),
            'excerpt_length': len(original_excerpt),
            'translated_length': len(translated),
            'original_excerpt': original_excerpt,
            'translated': translated,
            'problems': problems
        }
        results.append(result)
        
        print(f"\n  Problems found: {len(problems)}")
        for i, problem in enumerate(problems, 1):
            print(f"    {i}. {problem}")
    
    # Save results to JSON
    output_file = '/home/mark/apertium-dev/wikipedia_translation_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {output_file}")
    print(f"Total translations analyzed: {len(results)}")
    
    # Create a summary report
    summary_file = '/home/mark/apertium-dev/wikipedia_translation_summary.txt'
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("WIKIPEDIA TRANSLATION ANALYSIS SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        
        for result in results:
            f.write(f"Article: {result['title']}\n")
            f.write(f"Direction: {result['source_lang']} → {result['target_lang']}\n")
            f.write(f"Original excerpt length: {result['excerpt_length']} chars\n")
            f.write(f"Translated length: {result['translated_length']} chars\n")
            f.write(f"Problems found: {len(result['problems'])}\n")
            
            if result['problems']:
                f.write("\nProblems:\n")
                for i, problem in enumerate(result['problems'], 1):
                    f.write(f"  {i}. {problem}\n")
            
            f.write("\n" + "-" * 80 + "\n")
            f.write("ORIGINAL EXCERPT:\n")
            f.write("-" * 80 + "\n")
            f.write(result['original_excerpt'][:500] + "...\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("TRANSLATION:\n")
            f.write("-" * 80 + "\n")
            f.write(result['translated'][:500] + "...\n\n")
            
            f.write("=" * 80 + "\n\n")
    
    print(f"Summary report saved to: {summary_file}")

if __name__ == '__main__':
    main()

