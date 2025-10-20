#!/usr/bin/env python3
"""
Fetch Ido Wikipedia articles, translate them phrase-by-phrase,
and analyze translation errors focusing on core vocabulary and grammar.
"""

import requests
import json
import subprocess
import re
from bs4 import BeautifulSoup
from collections import defaultdict

# List of articles to analyze
ARTICLES = [
    "https://io.wikipedia.org/wiki/Nederlando",
    "https://io.wikipedia.org/wiki/Belgia",
    "https://io.wikipedia.org/wiki/Homo",
    "https://io.wikipedia.org/wiki/Mamo",
    "https://io.wikipedia.org/wiki/Komputero",
]

def fetch_wikipedia_content(url):
    """Fetch and extract text content from Wikipedia article."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get title
        title = soup.find('h1', class_='firstHeading') or soup.find('h1')
        title_text = title.get_text() if title else url.split('/')[-1]
        
        # Get main content
        content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            return None, None
            
        # Extract paragraphs
        paragraphs = []
        for p in content_div.find_all('p', recursive=False):
            text = p.get_text().strip()
            if text and len(text) > 10:  # Skip very short paragraphs
                paragraphs.append(text)
        
        return title_text, paragraphs
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None, None

def translate_text(text, mode='ido-epo'):
    """Translate text using apertium."""
    try:
        result = subprocess.run(
            ['apertium', '-d', '/home/mark/apertium-ido-epo/apertium-ido-epo', mode],
            input=text,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Translation error: {e}")
        return f"[ERROR: {e}]"

def split_into_phrases(text):
    """Split text into phrases for detailed analysis."""
    # Split on sentence boundaries and major punctuation
    sentences = re.split(r'([.!?;:])', text)
    
    phrases = []
    current = ""
    for part in sentences:
        if part in '.!?;:':
            if current:
                phrases.append(current + part)
                current = ""
        else:
            current = part.strip()
    
    if current:
        phrases.append(current)
    
    return [p.strip() for p in phrases if p.strip()]

def analyze_translation_errors(ido_text, epo_text):
    """Analyze translation for common error patterns."""
    errors = []
    
    # Common patterns to check
    patterns = {
        'untranslated_words': r'\*\w+',
        'grammar_markers': r'#\w+',
        'missing_translations': r'@\w+',
    }
    
    for error_type, pattern in patterns.items():
        matches = re.findall(pattern, epo_text)
        if matches:
            errors.append({
                'type': error_type,
                'matches': matches,
                'ido': ido_text[:100],
                'epo': epo_text[:100]
            })
    
    # Check for common Ido-specific issues
    ido_words = ido_text.lower().split()
    epo_words = epo_text.lower().split()
    
    # Common Ido function words that should translate
    ido_function_words = {
        'esas': 'estas',
        'esos': 'estos', 
        'esis': 'estis',
        'di': 'de',
        'en': 'en',
        'por': 'por',
        'kad': 'ke',
        'qua': 'kiu',
        'quo': 'kio',
        'ca': 'ĉi tiu',
        'su': 'sub',
        'ye': 'je',
    }
    
    # Check if function words are translated or left untranslated
    for ido_word, expected_epo in ido_function_words.items():
        if ido_word in ido_words:
            if ido_word in epo_words:  # Word wasn't translated
                errors.append({
                    'type': 'untranslated_function_word',
                    'word': ido_word,
                    'expected': expected_epo,
                    'ido': ido_text[:100],
                    'epo': epo_text[:100]
                })
    
    return errors

def analyze_articles():
    """Main analysis function."""
    results = {
        'articles': [],
        'error_summary': defaultdict(lambda: defaultdict(int)),
        'examples': defaultdict(list)
    }
    
    print("Fetching and analyzing articles...\n")
    
    for url in ARTICLES:
        article_name = url.split('/')[-1]
        print(f"\n{'='*80}")
        print(f"Processing: {article_name}")
        print('='*80)
        
        title, paragraphs = fetch_wikipedia_content(url)
        if not paragraphs:
            print(f"Could not fetch content for {article_name}")
            continue
        
        article_data = {
            'url': url,
            'title': title,
            'paragraphs': []
        }
        
        print(f"\nTitle: {title}")
        print(f"Found {len(paragraphs)} paragraphs\n")
        
        for i, paragraph in enumerate(paragraphs[:5], 1):  # Analyze first 5 paragraphs
            print(f"\n--- Paragraph {i} ---")
            print(f"Ido: {paragraph[:150]}...")
            
            # Translate full paragraph
            epo_paragraph = translate_text(paragraph)
            print(f"Epo: {epo_paragraph[:150]}...")
            
            # Split into phrases and analyze each
            phrases = split_into_phrases(paragraph)
            phrase_data = []
            
            for phrase in phrases[:10]:  # Analyze first 10 phrases per paragraph
                epo_phrase = translate_text(phrase)
                errors = analyze_translation_errors(phrase, epo_phrase)
                
                phrase_data.append({
                    'ido': phrase,
                    'epo': epo_phrase,
                    'errors': errors
                })
                
                # Collect error statistics
                for error in errors:
                    error_type = error['type']
                    results['error_summary'][article_name][error_type] += 1
                    
                    if len(results['examples'][error_type]) < 10:  # Keep max 10 examples per type
                        results['examples'][error_type].append({
                            'article': article_name,
                            'ido': phrase,
                            'epo': epo_phrase,
                            'details': error
                        })
            
            article_data['paragraphs'].append({
                'ido': paragraph,
                'epo': epo_paragraph,
                'phrases': phrase_data
            })
        
        results['articles'].append(article_data)
    
    return results

def generate_summary_report(results):
    """Generate a comprehensive summary report."""
    print("\n\n" + "="*80)
    print("SUMMARY REPORT: Translation Error Analysis")
    print("="*80)
    
    # Overall statistics
    print("\n## Overall Error Statistics by Article\n")
    for article, errors in results['error_summary'].items():
        print(f"\n### {article}")
        total_errors = sum(errors.values())
        print(f"Total errors: {total_errors}")
        for error_type, count in sorted(errors.items(), key=lambda x: -x[1]):
            print(f"  - {error_type}: {count}")
    
    # Error type breakdown with examples
    print("\n\n## Error Types and Examples\n")
    for error_type, examples in results['examples'].items():
        print(f"\n### {error_type.upper().replace('_', ' ')}")
        print(f"Total occurrences: {sum(results['error_summary'][a].get(error_type, 0) for a in results['error_summary'])}")
        print("\nExamples:")
        
        for i, example in enumerate(examples[:5], 1):
            print(f"\n{i}. Article: {example['article']}")
            print(f"   Ido: {example['ido'][:100]}")
            print(f"   Epo: {example['epo'][:100]}")
            if 'word' in example['details']:
                print(f"   Problem word: '{example['details']['word']}' → expected '{example['details'].get('expected', '?')}'")
            elif 'matches' in example['details']:
                print(f"   Matches: {example['details']['matches'][:5]}")
    
    # Save detailed results
    with open('ido_articles_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n\nDetailed results saved to: ido_articles_analysis.json")
    
    # Generate text report
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("IDO WIKIPEDIA ARTICLES - TRANSLATION ERROR ANALYSIS")
    report_lines.append("="*80)
    report_lines.append("")
    
    for article_data in results['articles']:
        report_lines.append(f"\n{'='*80}")
        report_lines.append(f"ARTICLE: {article_data['title']}")
        report_lines.append(f"URL: {article_data['url']}")
        report_lines.append('='*80)
        
        for i, para in enumerate(article_data['paragraphs'], 1):
            report_lines.append(f"\n--- Paragraph {i} ---")
            report_lines.append(f"\nIDO: {para['ido']}")
            report_lines.append(f"\nEPO: {para['epo']}")
            
            if para['phrases']:
                report_lines.append("\nPhrase-by-phrase analysis:")
                for j, phrase in enumerate(para['phrases'], 1):
                    if phrase['errors']:
                        report_lines.append(f"\n  Phrase {j}:")
                        report_lines.append(f"    Ido: {phrase['ido']}")
                        report_lines.append(f"    Epo: {phrase['epo']}")
                        report_lines.append(f"    Errors: {len(phrase['errors'])}")
                        for error in phrase['errors']:
                            report_lines.append(f"      - {error['type']}")
    
    with open('ido_articles_error_report.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print("Text report saved to: ido_articles_error_report.txt")

if __name__ == '__main__':
    print("Starting Ido Wikipedia Articles Analysis")
    print("="*80)
    
    results = analyze_articles()
    generate_summary_report(results)
    
    print("\n\n✓ Analysis complete!")

