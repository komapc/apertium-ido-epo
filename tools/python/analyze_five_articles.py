#!/usr/bin/env python3
"""
Analyze 5 specific Ido Wikipedia articles by translating phrase-by-phrase
and focusing on core vocabulary and grammatical errors.
"""

import requests
import subprocess
import json
import re
from collections import defaultdict
from typing import List, Dict, Tuple

# -------------------------------
# Number/Date normalizer helpers
# -------------------------------

MONTH_MAP_IDO_TO_EO = {
    # Ido → Esperanto
    'januaro': 'januaro',
    'februaro': 'februaro',
    'marzo': 'marto',
    'abril': 'aprilo',
    'mayo': 'majo',
    'junio': 'junio',
    'julio': 'julio',
    'agosto': 'aŭgusto',
    'septembro': 'septembro',
    'oktobro': 'oktobro',
    'novembro': 'novembro',
    'decembro': 'decembro',
}

def normalize_ido_dates(text: str) -> str:
    """Best-effort normalization of common Ido date/ordinal patterns before translation.

    Goals:
    - 26ma → 26-a
    - la 26ma di julio → la 26-a de julio
    - map Ido month variants to Esperanto forms (mayo→majo, marzo→marto, abril→aprilo, agosto→aŭgusto)
    - yarcento → jarcento; 17ma yarcento → 17-a jarcento
    - 35-yara → 35-jara; yara → jara
    Only affects date/number tokens; leaves other tokens intact.
    """
    s = text

    # 1) Ordinals: 26ma → 26-a (standalone)
    s = re.sub(r"\b(\d{1,2})ma\b", r"\1-a", s)

    # 2) Day + 'di' + month → ensure 'de' and EO month
    def _day_di_month(m: re.Match) -> str:
        day = m.group(1)
        month = m.group(2).lower()
        eo_month = MONTH_MAP_IDO_TO_EO.get(month, month)
        return f"{day} de {eo_month}"

    # patterns like: 26-a di julio / 26-a di mayo / 26-a di marzo
    s = re.sub(r"\b(\d{1,2}-?a)\s+di\s+(januaro|februaro|marzo|abril|mayo|junio|julio|agosto|septembro|oktobro|novembro|decembro)\b",
               _day_di_month, s, flags=re.IGNORECASE)

    # 3) Month-only mapping when present (keep casing as in source for simplicity)
    for ido, eo in MONTH_MAP_IDO_TO_EO.items():
        s = re.sub(rf"\b{ido}\b", eo, s, flags=re.IGNORECASE)

    # 4) yarcento/yara → EO jarcento/jara; also ordinal centurie: 17ma yarcento → 17-a jarcento
    s = re.sub(r"\byarcento\b", "jarcento", s, flags=re.IGNORECASE)
    s = re.sub(r"\b(\d{1,2})ma\s+jarcento\b", r"\1-a jarcento", s)
    s = re.sub(r"\b(\d{1,2})ma\s+yarcento\b", r"\1-a jarcento", s, flags=re.IGNORECASE)

    # 5) -yara → -jara (e.g., 35-yara → 35-jara) and standalone 'yara' → 'jara'
    s = re.sub(r"\b(\d+)-yara\b", r"\1-jara", s)
    s = re.sub(r"\byara\b", "jara", s, flags=re.IGNORECASE)

    # 6) If pattern like: la 26-a di → la 26-a de (limit to this date shape)
    s = re.sub(r"\b(\d{1,2}-?a)\s+di\b", r"\1 de", s)

    return s

def normalize_esperanto_numbers(text: str) -> str:
    """Post-translation cleanup of numeric forms to remove generation markers.

    - Remove leading '*' from pure numbers or number+suffix tokens: *1806 → 1806; *26-a → 26-a; *35-jara → 35-jara
    - Collapse multiple spaces introduced by replacements.
    """
    s = text
    # 1) Remove '*' before numbers and common suffixed numeric forms
    s = re.sub(r"\*(\d{3,4})\b", r"\1", s)            # years like *1806
    s = re.sub(r"\*(\d{1,2}-a)\b", r"\1", s)          # ordinals like *26-a
    s = re.sub(r"\*(\d{1,3}-jara)\b", r"\1", s)       # age/duration like *35-jara

    # 2) Also remove stray '*' before month/day tokens if any slipped through
    s = re.sub(r"\*(\d{1,2})\b", r"\1", s)

    # 3) Normalize double spaces
    s = re.sub(r"\s{2,}", " ", s)

    return s.strip()
# Articles to analyze (extract title from URL)
ARTICLES = [
    ("Nederlando", "https://io.wikipedia.org/wiki/Nederlando"),
    ("Belgia", "https://io.wikipedia.org/wiki/Belgia"),
    ("Homo", "https://io.wikipedia.org/wiki/Homo"),
    ("Mamo", "https://io.wikipedia.org/wiki/Mamo"),
    ("Komputero", "https://io.wikipedia.org/wiki/Komputero"),
]

# Common Ido function words and their Esperanto equivalents
IDO_FUNCTION_WORDS = {
    'esas': 'estas',
    'esos': 'estos',
    'esis': 'estis',
    'esus': 'estus',
    'eser': 'esti',
    'di': 'de',
    'en': 'en',
    'por': 'por',
    'kad': 'ke',
    'qua': 'kiu',
    'quo': 'kio',
    'qual': 'kia',
    'quan': 'kiam',
    'qube': 'kie',
    'su': 'sub',
    'ye': 'je',
    'ca': 'ĉi tiu',
    'ica': 'tiu ĉi',
    'to': 'tio',
    'ico': 'tio',
    'ta': 'tiu',
    'ita': 'tiu',
    'tre': 'tre',
    'plu': 'pli',
    'plua': 'plia',
    'maxim': 'plej',
    'nek': 'nek',
    'od': 'aŭ',
    'ma': 'sed',
    'nam': 'ĉar',
}

# Common Ido suffixes and their Esperanto equivalents
IDO_SUFFIXES = {
    '-ar': '-ar',
    '-aro': '-aro',
    '-erio': '-ejo',
    '-eso': '-eco',
    '-uro': '-aĵo',
    '-uro': '-uro',
}

def get_wikipedia_article(title: str) -> Tuple[str, str]:
    """Fetch Ido Wikipedia article text using the API."""
    url = "https://io.wikipedia.org/w/api.php"
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
            'User-Agent': 'Apertium Translation Analysis/1.0'
        }
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return "", f"HTTP Error: {response.status_code}"
        
        data = response.json()
        pages = data['query']['pages']
        page_id = list(pages.keys())[0]
        
        if page_id == '-1':
            return "", "Article not found"
        
        text = pages[page_id].get('extract', '')
        return text, None
    except Exception as e:
        return "", str(e)

def translate_text(text: str) -> str:
    """Translate Ido text to Esperanto using Apertium."""
    try:
        result = subprocess.run(
            ['apertium', '-d', '/home/mark/apertium-ido-epo/apertium-ido-epo', 'ido-epo'],
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=60
        )
        return result.stdout.decode('utf-8').strip()
    except Exception as e:
        return f"[TRANSLATION ERROR: {e}]"

def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences."""
    # Split on sentence boundaries
    sentences = re.split(r'([.!?])\s+', text)
    
    # Recombine punctuation with sentences
    result = []
    for i in range(0, len(sentences) - 1, 2):
        if i + 1 < len(sentences):
            result.append(sentences[i] + sentences[i+1])
        else:
            result.append(sentences[i])
    
    if len(sentences) % 2 == 1:
        result.append(sentences[-1])
    
    return [s.strip() for s in result if s.strip()]

def analyze_errors(ido_text: str, epo_text: str) -> Dict:
    """Analyze translation errors focusing on vocabulary and grammar."""
    errors = {
        'untranslated_words': [],
        'generation_errors': [],
        'analysis_errors': [],
        'function_word_issues': [],
        'other_issues': []
    }
    
    # Find error markers
    untranslated = re.findall(r'@[\w-]+', epo_text)
    if untranslated:
        errors['untranslated_words'] = untranslated
    
    generation = re.findall(r'\*[\w-]+', epo_text)
    if generation:
        errors['generation_errors'] = generation
    
    analysis = re.findall(r'#[\w-]+', epo_text)
    if analysis:
        errors['analysis_errors'] = analysis
    
    # Check for function words that may not have translated properly
    ido_words_lower = ido_text.lower().split()
    epo_words_lower = epo_text.lower().split()
    
    for ido_word, expected_epo in IDO_FUNCTION_WORDS.items():
        if ido_word in ido_words_lower:
            # Check if the Ido word appears untranslated in output
            if ido_word in epo_words_lower:
                errors['function_word_issues'].append({
                    'ido_word': ido_word,
                    'expected': expected_epo,
                    'status': 'untranslated'
                })
    
    # Check for untranslated Ido-specific patterns
    ido_patterns = [
        r'\besas\b', r'\besis\b', r'\besos\b', r'\besus\b',
        r'\bqua\b', r'\bquo\b', r'\bqual\b', r'\bquan\b', r'\bqube\b',
        r'\bica\b', r'\bica\b', r'\bico\b', r'\bica\b'
    ]
    
    for pattern in ido_patterns:
        matches = re.findall(pattern, epo_text, re.IGNORECASE)
        if matches:
            errors['other_issues'].append(f"Ido pattern '{pattern}' found in Esperanto output: {matches}")
    
    return errors

def count_total_errors(errors: Dict) -> int:
    """Count total number of errors."""
    count = 0
    count += len(errors.get('untranslated_words', []))
    count += len(errors.get('generation_errors', []))
    count += len(errors.get('analysis_errors', []))
    count += len(errors.get('function_word_issues', []))
    count += len(errors.get('other_issues', []))
    return count

def analyze_article(title: str, url: str) -> Dict:
    """Analyze a single article."""
    print(f"\n{'='*80}")
    print(f"ANALYZING: {title}")
    print(f"URL: {url}")
    print('='*80)
    
    # Fetch article
    print("\nFetching article...")
    text, error = get_wikipedia_article(title)
    
    if error:
        print(f"ERROR: {error}")
        return None
    
    if not text or len(text) < 100:
        print("Article too short or empty")
        return None
    
    print(f"Article length: {len(text)} characters")
    print(f"Word count: {len(text.split())} words")
    
    # Take first 3000 characters for analysis
    excerpt = text[:3000]
    
    # Split into sentences
    sentences = split_into_sentences(excerpt)
    print(f"Analyzing {len(sentences)} sentences...")
    
    sentence_results = []
    all_errors = defaultdict(list)
    
    for i, sentence in enumerate(sentences[:30], 1):  # Analyze first 30 sentences
        if len(sentence) < 10:  # Skip very short sentences
            continue
        
        # Normalize common date/ordinal patterns pre-translation
        pre = normalize_ido_dates(sentence)

        # Translate
        translated = translate_text(pre)

        # Post-translation numeric cleanup
        translated = normalize_esperanto_numbers(translated)
        
        # Analyze errors
        errors = analyze_errors(sentence, translated)
        total_errors = count_total_errors(errors)
        
        result = {
            'sentence_num': i,
            'ido': sentence,
            'epo': translated,
            'errors': errors,
            'error_count': total_errors
        }
        sentence_results.append(result)
        
        # Aggregate errors
        if total_errors > 0:
            for key, value in errors.items():
                if value:
                    all_errors[key].extend(value if isinstance(value, list) else [value])
        
        # Print if there are errors
        if total_errors > 0:
            print(f"\n  Sentence {i}: {total_errors} error(s)")
            print(f"    Ido: {sentence[:80]}...")
            print(f"    Epo: {translated[:80]}...")
            if errors['untranslated_words']:
                print(f"    Untranslated: {errors['untranslated_words'][:5]}")
            if errors['generation_errors']:
                print(f"    Generation errors: {errors['generation_errors'][:5]}")
            if errors['function_word_issues']:
                print(f"    Function word issues: {len(errors['function_word_issues'])}")
    
    return {
        'title': title,
        'url': url,
        'full_text_length': len(text),
        'analyzed_excerpt_length': len(excerpt),
        'sentence_count': len(sentences),
        'sentences_analyzed': len(sentence_results),
        'sentence_results': sentence_results,
        'total_errors': dict(all_errors),
        'error_summary': {
            'untranslated_words': len(all_errors['untranslated_words']),
            'generation_errors': len(all_errors['generation_errors']),
            'analysis_errors': len(all_errors['analysis_errors']),
            'function_word_issues': len(all_errors['function_word_issues']),
            'other_issues': len(all_errors['other_issues']),
        }
    }

def generate_summary(results: List[Dict]):
    """Generate comprehensive summary report."""
    print("\n\n" + "="*80)
    print("SUMMARY OF TRANSLATION PROBLEMS")
    print("="*80)
    
    # Overall statistics
    total_articles = len(results)
    total_sentences = sum(r['sentences_analyzed'] for r in results)
    
    print(f"\nArticles analyzed: {total_articles}")
    print(f"Total sentences analyzed: {total_sentences}")
    
    # Error breakdown by article
    print("\n\n## ERROR BREAKDOWN BY ARTICLE\n")
    for result in results:
        print(f"\n### {result['title']}")
        print(f"  Sentences analyzed: {result['sentences_analyzed']}")
        print(f"  Error summary:")
        for error_type, count in result['error_summary'].items():
            if count > 0:
                print(f"    - {error_type.replace('_', ' ').title()}: {count}")
    
    # Aggregate all errors
    all_untranslated = set()
    all_generation = set()
    all_function_issues = []
    
    for result in results:
        if 'untranslated_words' in result['total_errors']:
            all_untranslated.update(result['total_errors']['untranslated_words'])
        if 'generation_errors' in result['total_errors']:
            all_generation.update(result['total_errors']['generation_errors'])
        if 'function_word_issues' in result['total_errors']:
            all_function_issues.extend(result['total_errors']['function_word_issues'])
    
    print("\n\n## CORE VOCABULARY ISSUES\n")
    print(f"\nUnique untranslated words: {len(all_untranslated)}")
    if all_untranslated:
        print("\nMost common untranslated words:")
        for word in sorted(all_untranslated)[:20]:
            print(f"  - {word}")
    
    print(f"\n\nUnique generation errors: {len(all_generation)}")
    if all_generation:
        print("\nMost common generation errors:")
        for word in sorted(all_generation)[:20]:
            print(f"  - {word}")
    
    print("\n\n## GRAMMATICAL ISSUES\n")
    print(f"\nFunction word translation problems: {len(all_function_issues)}")
    if all_function_issues:
        # Group by word
        word_counts = defaultdict(int)
        for issue in all_function_issues:
            if isinstance(issue, dict):
                word_counts[issue['ido_word']] += 1
        
        print("\nMost problematic function words:")
        for word, count in sorted(word_counts.items(), key=lambda x: -x[1])[:10]:
            expected = IDO_FUNCTION_WORDS.get(word, '?')
            print(f"  - '{word}' (should be '{expected}'): {count} occurrences")
    
    # Save detailed results
    output_file = 'ido_five_articles_analysis.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n\nDetailed results saved to: {output_file}")
    
    # Generate text report
    report_lines = []
    report_lines.append("="*80)
    report_lines.append("IDO WIKIPEDIA ARTICLES - PHRASE-BY-PHRASE TRANSLATION ANALYSIS")
    report_lines.append("Focus: Core Vocabulary and Grammatical Errors")
    report_lines.append("="*80)
    report_lines.append("")
    report_lines.append(f"Articles analyzed: {total_articles}")
    report_lines.append(f"Total sentences analyzed: {total_sentences}")
    report_lines.append("")
    
    for result in results:
        report_lines.append(f"\n{'='*80}")
        report_lines.append(f"ARTICLE: {result['title']}")
        report_lines.append(f"URL: {result['url']}")
        report_lines.append('='*80)
        report_lines.append(f"\nSentences analyzed: {result['sentences_analyzed']}")
        report_lines.append("\nError Summary:")
        for error_type, count in result['error_summary'].items():
            if count > 0:
                report_lines.append(f"  - {error_type.replace('_', ' ').title()}: {count}")
        
        report_lines.append("\n\nPROBLEMATIC SENTENCES:\n")
        for sent in result['sentence_results']:
            if sent['error_count'] > 0:
                report_lines.append(f"\nSentence {sent['sentence_num']} ({sent['error_count']} errors):")
                report_lines.append(f"  IDO: {sent['ido']}")
                report_lines.append(f"  EPO: {sent['epo']}")
                
                if sent['errors']['untranslated_words']:
                    report_lines.append(f"  Untranslated: {', '.join(sent['errors']['untranslated_words'][:10])}")
                if sent['errors']['generation_errors']:
                    report_lines.append(f"  Generation errors: {', '.join(sent['errors']['generation_errors'][:10])}")
                if sent['errors']['function_word_issues']:
                    issues = sent['errors']['function_word_issues'][:3]
                    for issue in issues:
                        if isinstance(issue, dict):
                            report_lines.append(f"  Function word: '{issue['ido_word']}' not translated (expected: '{issue['expected']}')")
                report_lines.append("")
    
    report_file = 'ido_five_articles_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"Text report saved to: {report_file}")

def main():
    print("="*80)
    print("IDO WIKIPEDIA ARTICLES - TRANSLATION ANALYSIS")
    print("="*80)
    print("\nArticles to analyze:")
    for title, url in ARTICLES:
        print(f"  - {title}")
    
    results = []
    
    for title, url in ARTICLES:
        result = analyze_article(title, url)
        if result:
            results.append(result)
    
    if results:
        generate_summary(results)
    
    print("\n\n✓ Analysis complete!")

if __name__ == '__main__':
    main()

