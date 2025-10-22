#!/bin/bash
# Properly fix the ordinal paradigm insertion

echo "Fixing ordinal paradigm insertion..."

# Remove the incorrectly inserted paradigm at the end
sed -i '/<pardef n="ordinal">/,/<\/pardef>/d' apertium/apertium-ido-epo/apertium-ido.ido.dix

# Find the end of the pardefs section
pardefs_end=$(grep -n "</pardefs>" apertium/apertium-ido-epo/apertium-ido.ido.dix | head -1 | cut -d: -f1)

if [ -n "$pardefs_end" ]; then
    # Insert before the closing </pardefs> tag
    sed -i "${pardefs_end}i\\
    <pardef n=\"ordinal\">\\
      <e>\\
        <p>\\
          <l></l>\\
          <r>ma</r>\\
        </p>\\
      </e>\\
    </pardef>" apertium/apertium-ido-epo/apertium-ido.ido.dix
    
    echo "  -> Ordinal paradigm inserted in correct location"
else
    echo "  -> Could not find pardefs section"
    exit 1
fi

echo "Ordinal paradigm fix complete!"
