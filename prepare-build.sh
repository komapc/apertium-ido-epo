#!/bin/bash
# Prepare build environment by copying required files from worktrees

echo "Preparing build environment..."

# Copy transfer rules and constraint grammar from CI worktree
echo "  -> Copying transfer rules..."
cp .worktrees/ci-clean/apertium-ido-epo.epo-ido.t1x apertium/apertium-ido-epo/ 2>/dev/null || echo "    Warning: epo-ido.t1x not found in worktree"
cp .worktrees/ci-clean/apertium-ido-epo.ido-epo.t1x apertium/apertium-ido-epo/ 2>/dev/null || echo "    Warning: ido-epo.t1x not found in worktree"

# Copy constraint grammar
echo "  -> Copying constraint grammar..."
cp .worktrees/ci-clean/apertium-epo.epo.rlx apertium/apertium-ido-epo/epo-ido.rlx 2>/dev/null || echo "    Warning: epo.epo.rlx not found in worktree"

# Copy post-generation dictionaries  
echo "  -> Copying post-generation dictionaries..."
cp .worktrees/ci-clean/apertium-ido-epo.post-epo.dix apertium/apertium-ido-epo/ 2>/dev/null || echo "    Warning: post-epo.dix not found in worktree"
cp .worktrees/ci-clean/apertium-ido-epo.post-ido.dix apertium/apertium-ido-epo/ 2>/dev/null || echo "    Warning: post-ido.dix not found in worktree"

# Validate dictionaries for required paradigms
echo "  -> Validating dictionaries..."

# Check if ordinal paradigm exists in Ido dictionary
if ! grep -q "pardef n=\"ordinal\"" apertium/apertium-ido-epo/apertium-ido.ido.dix; then
    echo "    Warning: Missing 'ordinal' paradigm in Ido dictionary"
    echo "    This will cause compilation to fail"
    echo "    Consider adding ordinal paradigm or using vendor Ido dictionary"
fi

# Check timestamps and warn if binaries are outdated
echo "  -> Checking binary timestamps..."
for bin in apertium/apertium-ido-epo/*.bin; do
    if [ -f "$bin" ]; then
        bin_time=$(stat -c %Y "$bin" 2>/dev/null || echo "0")
        dix_time=$(stat -c %Y "apertium/apertium-ido-epo/apertium-ido-epo.ido-epo.dix" 2>/dev/null || echo "0")
        if [ "$bin_time" -lt "$dix_time" ]; then
            echo "    Warning: $bin is outdated (compiled $(date -d @$bin_time) vs dictionary $(date -d @$dix_time))"
        fi
    fi
done

echo "Build preparation complete!"
echo ""

# Use vendor Ido dictionary instead of incomplete local one
echo "  -> Using vendor Ido dictionary (local is incomplete)..."
cp apertium/vendor/apertium-ido/apertium-ido.ido.dix apertium/apertium-ido-epo/apertium-ido.ido.dix 2>/dev/null || echo "    Warning: Could not copy vendor Ido dictionary"

