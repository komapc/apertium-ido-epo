#!/bin/bash

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              BEFORE/AFTER COMPARISON                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

for suite in ido-epo-basic ido-epo-grammar ido-epo-wikipedia ido-epo-accusative; do
    INPUT="test/${suite}-input.txt"
    OUTPUT=$(cat "$INPUT" | apertium -d . ido-epo)
    
    PASSTHROUGH=$(echo "$OUTPUT" | grep -o '\*[^ ]*' | wc -l)
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Test: $suite"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "* Passthrough words: $PASSTHROUGH"
    echo ""
    echo "Top passthrough issues:"
    echo "$OUTPUT" | grep -o '\*[a-zA-Z-]*' | sort | uniq -c | sort -rn | head -3
    echo ""
done
