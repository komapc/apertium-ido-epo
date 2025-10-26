#!/bin/bash

# Regression Tests for Apertium Ido-Esperanto Translation
# This script tests critical functionality that was previously fixed but got lost

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to run a test
run_test() {
    local test_name="$1"
    local input="$2"
    local expected="$3"
    local direction="$4"
    
    echo -n "Testing $test_name... "
    
    # Run the translation
    local result=$(echo "$input" | apertium -d . "$direction" 2>/dev/null)
    
    # Check if result matches expected
    if [[ "$result" == "$expected" ]]; then
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}FAIL${NC}"
        echo "  Input:    '$input'"
        echo "  Expected: '$expected'"
        echo "  Got:      '$result'"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Function to run a test that should NOT contain asterisks
run_test_no_asterisk() {
    local test_name="$1"
    local input="$2"
    local direction="$3"
    
    echo -n "Testing $test_name (no asterisks)... "
    
    # Run the translation
    local result=$(echo "$input" | apertium -d . "$direction" 2>/dev/null)
    
    # Check if result contains asterisks
    if [[ "$result" == *"@"* ]]; then
        echo -e "${RED}FAIL${NC}"
        echo "  Input:    '$input'"
        echo "  Result:   '$result' (contains @ symbols)"
        ((TESTS_FAILED++))
        return 1
    else
        echo -e "${GREEN}PASS${NC}"
        ((TESTS_PASSED++))
        return 0
    fi
}

echo "=========================================="
echo "Apertium Ido-Esperanto Regression Tests"
echo "=========================================="
echo

# Test 1: Number Recognition (Critical Issue #1)
echo "=== NUMBER RECOGNITION TESTS ==="
run_test_no_asterisk "Number 1782" "1782" "epo-ido"
run_test_no_asterisk "Number 5" "5" "epo-ido"
run_test_no_asterisk "Number 60%" "60%" "epo-ido"
run_test_no_asterisk "Number 2023" "2023" "epo-ido"
run_test_no_asterisk "Number 3.14" "3.14" "epo-ido"

# Test 2: -ala Suffix Handling (Critical Issue #2)
echo
echo "=== -ALA SUFFIX TESTS ==="
run_test_no_asterisk "-ala suffix: naturala" "naturala" "epo-ido"
run_test_no_asterisk "-ala suffix: originala" "originala" "epo-ido"
run_test_no_asterisk "-ala suffix: sociala" "sociala" "epo-ido"

# Test 3: Basic Translation Quality
echo
echo "=== BASIC TRANSLATION TESTS ==="
run_test "Basic: me amas vu" "mi amas vi" "ido-epo"
run_test "Basic: saluton" "saluto" "epo-ido"

# Test 4: Historical Text (Original Problem)
echo
echo "=== HISTORICAL TEXT TESTS ==="
run_test_no_asterisk "Historical: En oktobro 1782" "En oktobro 1782" "epo-ido"
run_test_no_asterisk "Historical: naturala kauzi" "naturala kauzi" "epo-ido"

# Test 5: Reverse Direction
echo
echo "=== REVERSE DIRECTION TESTS ==="
run_test_no_asterisk "Reverse: 1782" "1782" "ido-epo"
run_test_no_asterisk "Reverse: naturala" "naturala" "ido-epo"

echo
echo "=========================================="
echo "TEST SUMMARY"
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "Total Tests: $((TESTS_PASSED + TESTS_FAILED))"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed! 🎉${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed! 😞${NC}"
    exit 1
fi
