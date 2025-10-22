#!/bin/bash
# Add missing ordinal paradigm to Ido dictionary

echo "Adding ordinal paradigm to Ido dictionary..."

# Check if ordinal paradigm already exists
if grep -q "pardef n=\"ordinal\"" apertium/apertium-ido-epo/apertium-ido.ido.dix; then
    echo "  -> Ordinal paradigm already exists"
    exit 0
fi

# Find where to insert the paradigm (after the last existing paradigm)
last_pardef_end=$(grep -n "</pardef>" apertium/apertium-ido-epo/apertium-ido.ido.dix | tail -1 | cut -d: -f1)

if [ -z "$last_pardef_end" ]; then
    echo "  -> Could not find insertion point for ordinal paradigm"
    exit 1
fi

# Create the ordinal paradigm
cat > /tmp/ordinal_paradigm.tmp << 'EOF_PARD'
    <pardef n="ordinal">
      <e>
        <p>
          <l></l>
          <r>ma</r>
        </p>
      </e>
    </pardef>
EOF_PARD

# Insert the paradigm
sed -i "${last_pardef_end}r /tmp/ordinal_paradigm.tmp" apertium/apertium-ido-epo/apertium-ido.ido.dix

if [ $? -eq 0 ]; then
    echo "  -> Ordinal paradigm added successfully"
    echo "  -> Dictionary should now compile correctly"
else
    echo "  -> Failed to add ordinal paradigm"
fi

# Clean up
rm -f /tmp/ordinal_paradigm.tmp

echo "Ordinal paradigm addition complete!"
echo ""
