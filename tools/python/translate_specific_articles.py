#!/usr/bin/env python3
"""
Fetch and translate specific Wikipedia articles between Ido and Esperanto,
then analyze translation errors without fixing them.
"""

import requests
import subprocess
import json
import re
from typing import Dict, List, Tuple
from collections import Counter

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

def translate_text(text: str, direction: str, apertium_dir: str) -> str:
    """Translate text using Apertium."""
    cmd = ['apertium', '-d', apertium_dir, direction]
    
    try:
        result = subprocess.run(
            cmd,
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=120
        )
        return result.stdout.decode('utf-8')
    except Exception as e:
        return f"Translation error: {str(e)}"

def analyze_translation_errors(original: str, translated: str, direction: str) -> Dict:
    """Analyze errors in the translation."""
    
    # Find different types of error markers
    at_words = re.findall(r'@\w+', translated)
    hash_words = re.findall(r'#\w+', translated)
    star_words = re.findall(r'\*\w+', translated)
    
    # Find specific patterns
    prpers_matches = re.findall(r'@prpers\b', translated)
    double_patterns = re.findall(r'(\w+#)\s+\1', translated)
    untranslated_phrases = re.findall(r'@\([^)]+@\)', translated)
    
    # Count error markers
    at_count = translated.count('@')
    hash_count = translated.count('#')
    star_count = translated.count('*')
    total_errors = at_count + hash_count + star_count
    
    # Calculate statistics
    orig_words = len(original.split())
    trans_words = len(translated.split())
    error_rate = (total_errors / trans_words * 100) if trans_words > 0 else 0
    
    # Sample errors with context
    error_contexts = []
    lines = translated.split('\n')
    for i, line in enumerate(lines):
        if '@' in line or '#' in line or '*' in line:
            # Get context (line before and after if available)
            context_start = max(0, i - 1)
            context_end = min(len(lines), i + 2)
            context = '\n'.join(lines[context_start:context_end])
            error_contexts.append({
                'line_num': i + 1,
                'context': context[:200]  # First 200 chars
            })
            if len(error_contexts) >= 10:  # Limit to 10 samples
                break
    
    return {
        'error_markers': {
            'at_symbol_count': at_count,
            'hash_symbol_count': hash_count,
            'star_symbol_count': star_count,
            'total_error_markers': total_errors
        },
        'unique_errors': {
            'unknown_at': list(set(at_words))[:20],  # First 20 unique
            'unknown_hash': list(set(hash_words))[:20],
            'unknown_star': list(set(star_words))[:20]
        },
        'specific_issues': {
            'prpers_count': len(prpers_matches),
            'double_prepositions': double_patterns[:10],
            'untranslated_phrases': untranslated_phrases[:10]
        },
        'statistics': {
            'original_words': orig_words,
            'translated_words': trans_words,
            'error_rate_percent': round(error_rate, 2),
            'word_ratio': round(trans_words / orig_words, 2) if orig_words > 0 else 0
        },
        'error_samples': error_contexts
    }

def main():
    print("=" * 80)
    print("TRANSLATING SPECIFIC WIKIPEDIA ARTICLES")
    print("=" * 80)
    print()
    
    # Articles to translate
    articles = [
        {
            'lang': 'eo',
            'title': 'Francio',
            'direction': 'epo-ido',
            'target_lang': 'Ido',
            'description': 'France (Esperanto → Ido)'
        },
        {
            'lang': 'io',
            'title': 'Francia',
            'direction': 'ido-epo',
            'target_lang': 'Esperanto',
            'description': 'France (Ido → Esperanto)'
        },
        {
            'lang': 'eo',
            'title': 'Israel-palestina konflikto',
            'direction': 'epo-ido',
            'target_lang': 'Ido',
            'description': 'Israel-Palestine conflict (Esperanto → Ido)'
        },
        {
            'lang': 'io',
            'title': 'Gaza-strio',
            'direction': 'ido-epo',
            'target_lang': 'Esperanto',
            'description': 'Gaza Strip (Ido → Esperanto)'
        }
    ]
    
    apertium_dir = "/home/mark/apertium-ido-epo/apertium-ido-epo"
    results = []
    
    for article in articles:
        print(f"\n{'=' * 80}")
        print(f"Processing: {article['description']}")
        print(f"Article: {article['title']}")
        print(f"Language: {article['lang']}")
        print(f"Direction: {article['direction']}")
        print(f"{'=' * 80}\n")
        
        print(f"Fetching article from {article['lang']}.wikipedia.org...")
        original = get_wikipedia_article(article['lang'], article['title'])
        
        if not original or len(original) < 100:
            print(f"  ⚠ Article too short or not found, skipping...")
            continue
        
        print(f"  ✓ Article fetched: {len(original)} characters")
        print(f"  ✓ Word count: {len(original.split())} words")
        
        # Use first 5000 characters for translation
        excerpt_length = 5000
        original_excerpt = original[:excerpt_length]
        
        print(f"\n  Translating to {article['target_lang']}...")
        translated = translate_text(original_excerpt, article['direction'], apertium_dir)
        
        if translated.startswith("Translation error:"):
            print(f"  ✗ {translated}")
            continue
        
        print(f"  ✓ Translation completed: {len(translated)} characters")
        
        print(f"\n  Analyzing translation errors...")
        error_analysis = analyze_translation_errors(original_excerpt, translated, article['direction'])
        
        result = {
            'source_lang': article['lang'],
            'target_lang': article['target_lang'],
            'title': article['title'],
            'description': article['description'],
            'direction': article['direction'],
            'original_full_length': len(original),
            'excerpt_length': len(original_excerpt),
            'translated_length': len(translated),
            'original_excerpt': original_excerpt,
            'translated': translated,
            'error_analysis': error_analysis
        }
        results.append(result)
        
        # Print summary
        stats = error_analysis['statistics']
        markers = error_analysis['error_markers']
        
        print(f"\n  ERROR ANALYSIS SUMMARY:")
        print(f"  ───────────────────────────────────────────")
        print(f"  Original words:      {stats['original_words']:,}")
        print(f"  Translated words:    {stats['translated_words']:,}")
        print(f"  Word ratio:          {stats['word_ratio']}")
        print(f"  Error rate:          {stats['error_rate_percent']:.2f}%")
        print(f"\n  Error Markers:")
        print(f"    @ symbols:         {markers['at_symbol_count']}")
        print(f"    # symbols:         {markers['hash_symbol_count']}")
        print(f"    * symbols:         {markers['star_symbol_count']}")
        print(f"    TOTAL:             {markers['total_error_markers']}")
        
        # Show sample errors
        if error_analysis['unique_errors']['unknown_at']:
            print(f"\n  Sample unknown words (@):")
            for word in error_analysis['unique_errors']['unknown_at'][:5]:
                print(f"    • {word}")
        
        if error_analysis['unique_errors']['unknown_hash']:
            print(f"\n  Sample unknown words (#):")
            for word in error_analysis['unique_errors']['unknown_hash'][:5]:
                print(f"    • {word}")
        
        if error_analysis['specific_issues']['prpers_count'] > 0:
            print(f"\n  ⚠ Pronoun issues (@prpers): {error_analysis['specific_issues']['prpers_count']}")
    
    # Save results to JSON
    output_file = '/home/mark/apertium-ido-epo/specific_articles_translation_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n{'=' * 80}")
    print(f"COMPLETE - Results saved to: {output_file}")
    print(f"{'=' * 80}\n")
    
    # Create detailed error report
    report_file = '/home/mark/apertium-ido-epo/specific_articles_error_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Translation Error Analysis Report\n\n")
        f.write("**Analysis Date:** October 9, 2025\n\n")
        f.write("## Overview\n\n")
        f.write(f"This report analyzes translation errors in {len(results)} Wikipedia articles ")
        f.write("translated between Ido and Esperanto using Apertium.\n\n")
        
        f.write("## Articles Analyzed\n\n")
        for i, result in enumerate(results, 1):
            f.write(f"{i}. **{result['description']}**\n")
            f.write(f"   - Title: {result['title']}\n")
            f.write(f"   - Direction: {result['direction']}\n\n")
        
        f.write("---\n\n")
        
        # Detailed analysis for each article
        for result in results:
            f.write(f"## {result['description']}\n\n")
            f.write(f"**Title:** {result['title']}  \n")
            f.write(f"**Source Language:** {result['source_lang']}  \n")
            f.write(f"**Target Language:** {result['target_lang']}  \n")
            f.write(f"**Direction:** `{result['direction']}`\n\n")
            
            stats = result['error_analysis']['statistics']
            markers = result['error_analysis']['error_markers']
            
            f.write("### Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Original Words | {stats['original_words']:,} |\n")
            f.write(f"| Translated Words | {stats['translated_words']:,} |\n")
            f.write(f"| Word Ratio | {stats['word_ratio']} |\n")
            f.write(f"| Error Rate | {stats['error_rate_percent']}% |\n")
            f.write(f"| @ Errors | {markers['at_symbol_count']} |\n")
            f.write(f"| # Errors | {markers['hash_symbol_count']} |\n")
            f.write(f"| * Errors | {markers['star_symbol_count']} |\n")
            f.write(f"| **Total Errors** | **{markers['total_error_markers']}** |\n\n")
            
            # Unknown words
            f.write("### Unknown Words and Error Patterns\n\n")
            
            if result['error_analysis']['unique_errors']['unknown_at']:
                f.write("#### Unknown Words (@ marker)\n\n")
                f.write("These words were not found in the dictionary:\n\n")
                for word in result['error_analysis']['unique_errors']['unknown_at'][:15]:
                    f.write(f"- `{word}`\n")
                if len(result['error_analysis']['unique_errors']['unknown_at']) > 15:
                    remaining = len(result['error_analysis']['unique_errors']['unknown_at']) - 15
                    f.write(f"\n*...and {remaining} more*\n")
                f.write("\n")
            
            if result['error_analysis']['unique_errors']['unknown_hash']:
                f.write("#### Analysis Errors (# marker)\n\n")
                f.write("These forms could not be analyzed:\n\n")
                for word in result['error_analysis']['unique_errors']['unknown_hash'][:15]:
                    f.write(f"- `{word}`\n")
                if len(result['error_analysis']['unique_errors']['unknown_hash']) > 15:
                    remaining = len(result['error_analysis']['unique_errors']['unknown_hash']) - 15
                    f.write(f"\n*...and {remaining} more*\n")
                f.write("\n")
            
            if result['error_analysis']['unique_errors']['unknown_star']:
                f.write("#### Generation Errors (* marker)\n\n")
                f.write("These forms could not be generated:\n\n")
                for word in result['error_analysis']['unique_errors']['unknown_star'][:15]:
                    f.write(f"- `{word}`\n")
                f.write("\n")
            
            # Specific issues
            issues = result['error_analysis']['specific_issues']
            if issues['prpers_count'] > 0 or issues['double_prepositions'] or issues['untranslated_phrases']:
                f.write("### Specific Translation Issues\n\n")
                
                if issues['prpers_count'] > 0:
                    f.write(f"- **Pronoun errors (@prpers):** {issues['prpers_count']} occurrences\n")
                
                if issues['double_prepositions']:
                    f.write(f"- **Double prepositions:** Found {len(issues['double_prepositions'])} cases\n")
                
                if issues['untranslated_phrases']:
                    f.write(f"- **Untranslated phrases:** {len(issues['untranslated_phrases'])} instances\n")
                
                f.write("\n")
            
            # Error context samples
            if result['error_analysis']['error_samples']:
                f.write("### Sample Errors in Context\n\n")
                f.write("Here are some examples of errors found in the translation:\n\n")
                
                for i, sample in enumerate(result['error_analysis']['error_samples'][:5], 1):
                    f.write(f"**Example {i}** (line {sample['line_num']}):\n\n")
                    f.write(f"```\n{sample['context']}\n```\n\n")
            
            # Original excerpt
            f.write("### Original Text Excerpt (first 500 characters)\n\n")
            f.write(f"```\n{result['original_excerpt'][:500]}...\n```\n\n")
            
            # Translation excerpt
            f.write("### Translation Excerpt (first 500 characters)\n\n")
            f.write(f"```\n{result['translated'][:500]}...\n```\n\n")
            
            f.write("---\n\n")
        
        # Overall summary
        f.write("## Overall Summary\n\n")
        
        total_orig_words = sum(r['error_analysis']['statistics']['original_words'] for r in results)
        total_trans_words = sum(r['error_analysis']['statistics']['translated_words'] for r in results)
        total_errors = sum(r['error_analysis']['error_markers']['total_error_markers'] for r in results)
        avg_error_rate = sum(r['error_analysis']['statistics']['error_rate_percent'] for r in results) / len(results) if results else 0
        
        f.write(f"- **Total articles analyzed:** {len(results)}\n")
        f.write(f"- **Total words translated:** {total_trans_words:,}\n")
        f.write(f"- **Total error markers:** {total_errors:,}\n")
        f.write(f"- **Average error rate:** {avg_error_rate:.2f}%\n\n")
        
        # By direction
        epo_ido = [r for r in results if r['direction'] == 'epo-ido']
        ido_epo = [r for r in results if r['direction'] == 'ido-epo']
        
        if epo_ido:
            avg_epo_ido = sum(r['error_analysis']['statistics']['error_rate_percent'] for r in epo_ido) / len(epo_ido)
            f.write(f"### Esperanto → Ido\n\n")
            f.write(f"- Articles: {len(epo_ido)}\n")
            f.write(f"- Average error rate: {avg_epo_ido:.2f}%\n\n")
        
        if ido_epo:
            avg_ido_epo = sum(r['error_analysis']['statistics']['error_rate_percent'] for r in ido_epo) / len(ido_epo)
            f.write(f"### Ido → Esperanto\n\n")
            f.write(f"- Articles: {len(ido_epo)}\n")
            f.write(f"- Average error rate: {avg_ido_epo:.2f}%\n\n")
        
        f.write("---\n\n")
        f.write("*Note: This is an error analysis only. No corrections have been made to the translation system.*\n")
    
    print(f"Detailed report saved to: {report_file}")
    print(f"\nTranslation analysis complete!")
    
    # Print summary table
    print(f"\n{'=' * 80}")
    print("SUMMARY TABLE")
    print(f"{'=' * 80}\n")
    print(f"{'Article':<40} {'Direction':<15} {'Error Rate':<15}")
    print(f"{'-' * 40} {'-' * 15} {'-' * 15}")
    
    for result in results:
        title_short = result['title'][:37] + "..." if len(result['title']) > 40 else result['title']
        direction = result['direction']
        error_rate = f"{result['error_analysis']['statistics']['error_rate_percent']:.2f}%"
        print(f"{title_short:<40} {direction:<15} {error_rate:<15}")
    
    print(f"\n{'=' * 80}")

if __name__ == '__main__':
    main()

