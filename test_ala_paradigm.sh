#!/bin/bash
# Test script for -ala adjective paradigm

echo "=== Testing -ala Adjective Paradigm ==="
echo ""

echo "Scientific/Technical:"
echo "  sunala (solar):" $(echo "sunala" | apertium -d . ido-epo)
echo "  astronomiala:" $(echo "astronomiala" | apertium -d . ido-epo)
echo "  molekulala:" $(echo "molekulala" | apertium -d . ido-epo)
echo "  atomala:" $(echo "atomala" | apertium -d . ido-epo)
echo ""

echo "Social/Political:"
echo "  nasionala:" $(echo "nasionala" | apertium -d . ido-epo)
echo "  internasionala:" $(echo "internasionala" | apertium -d . ido-epo)
echo "  kulturala:" $(echo "kulturala" | apertium -d . ido-epo)
echo "  legala:" $(echo "legala" | apertium -d . ido-epo)
echo ""

echo "General:"
echo "  naturala:" $(echo "naturala" | apertium -d . ido-epo)
echo "  totala:" $(echo "totala" | apertium -d . ido-epo)
echo "  formala:" $(echo "formala" | apertium -d . ido-epo)
echo "  normala:" $(echo "normala" | apertium -d . ido-epo)
echo ""

echo "Adverb forms (stem + ale):"
echo "  sunale (solarly):" $(echo "sunale" | apertium -d . ido-epo)
echo "  naturale:" $(echo "naturale" | apertium -d . ido-epo)
echo ""

echo "=== All tests completed ==="
