#!/bin/bash
# Fix missing paradigms in dictionaries

echo "Fixing dictionary paradigms..."

# Check if ordinal paradigm exists in vendor Ido dictionary
if grep -q "pardef n=\"ordinal\"" apertium/vendor/apertium-ido/apertium-ido.ido.dix; then
    echo "  -> Found ordinal paradigm in vendor Ido dictionary"
    
    # Extract and copy the ordinal paradigm from vendor dictionary
    grep -A 20 "pardef n=\"ordinal\"" apertium/vendor/apertium-ido/apertium-ido.ido.dix | head -21 > /tmp/ordinal_paradigm.tmp
    
    # Check if it already exists in local dictionary
    if ! grep -q "pardef n=\"ordinal\"" apertium/apertium-ido-epo/apertium-ido.ido.dix; then
        echo "  -> Adding missing ordinal paradigm to local Ido dictionary..."
        
        # Find where to insert it (after the last pardef)
        last_pardef_line=$(grep -n "</pardef>" apertium/apertium-ido-epo/apertium-ido.ido.dix | tail -1 | cut -d: -f1)
        if [ -n "$last_pardef_line" ]; then
            # Insert the paradigm after the last existing paradigm
            sed -i "${last_pardef_line}r /tmp/ordinal_paradigm.tmp" apertium/apertium-ido-epo/apertium-ido.ido.dix
            echo "  -> Ordinal paradigm added successfully"
        else
            echo "  -> Could not find insertion point for ordinal paradigm"
        fi
    else
        echo "  -> Ordinal paradigm already exists in local dictionary"
    fi
else
    echo "  -> Ordinal paradigm not found in vendor dictionary either"
    echo "  -> Attempting to add ordinal paradigm..."
    ./add-ordinal-paradigm.sh
fi

# Clean up
rm -f /tmp/ordinal_paradigm.tmp

echo "Dictionary paradigm fixes complete!"
echo ""
