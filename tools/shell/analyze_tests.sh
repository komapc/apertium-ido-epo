#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              COMPREHENSIVE TEST ANALYSIS                         ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

for suite in ido-epo-basic ido-epo-grammar ido-epo-wikipedia ido-epo-accusative; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📊 Test Suite: $suite"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    INPUT="test/${suite}-input.txt"
    LINES=$(wc -l < "$INPUT")
    OUTPUT=$(cat "$INPUT" | apertium -d . ido-epo)
    
    UNKNOWN=$(echo "$OUTPUT" | grep -o '@[^ ]*' | wc -l)
    GENERATION=$(echo "$OUTPUT" | grep -o '#[^ ]*' | wc -l)
    PASSTHROUGH=$(echo "$OUTPUT" | grep -o '\*[^ ]*' | wc -l)
    
    TOTAL_WORDS=$(echo "$OUTPUT" | wc -w)
    CLEAN=$((TOTAL_WORDS - UNKNOWN - GENERATION - PASSTHROUGH))
    
    CLEAN_PCT=$((CLEAN * 100 / TOTAL_WORDS))
    UNKNOWN_PCT=$((UNKNOWN * 100 / TOTAL_WORDS))
    GEN_PCT=$((GENERATION * 100 / TOTAL_WORDS))
    PASS_PCT=$((PASSTHROUGH * 100 / TOTAL_WORDS))
    
    echo "Sentences: $LINES"
    echo "Total words: $TOTAL_WORDS"
    echo ""
    echo "✅ Clean:      $CLEAN_PCT% ($CLEAN words)"
    echo "@ Unknown:    $UNKNOWN_PCT% ($UNKNOWN words)"
    echo "# Generation: $GEN_PCT% ($GENERATION words)"
    echo "* Passthrough: $PASS_PCT% ($PASSTHROUGH words)"
    echo ""
    
    # Top issues
    echo "Top 5 issues:"
    echo "$OUTPUT" | grep -o -E '@[a-zA-Z]+|#[a-zA-Z]+|\*[a-zA-Z]+' | sort | uniq -c | sort -rn | head -5
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
