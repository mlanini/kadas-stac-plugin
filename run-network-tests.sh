#!/bin/bash
# Run all network connectivity tests for KADAS STAC Plugin

echo "======================================================================"
echo "KADAS STAC Plugin - Network Connectivity Test Suite"
echo "======================================================================"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "ERROR: Python not found in PATH"
    echo "Please ensure QGIS/KADAS Python is in your PATH"
    exit 1
fi

PYTHON_VERSION=$(python --version 2>&1)
echo "Python: $PYTHON_VERSION"
echo ""

echo "Running tests..."
echo ""

# Run standalone test
echo "======================================================================"
echo "Running Standalone Test (test_network.py)"
echo "======================================================================"
echo ""

python test_network.py
STANDALONE_RESULT=$?

echo ""
echo "======================================================================"
echo "Running Unit Test Suite (test/test_network_connectivity.py)"
echo "======================================================================"
echo ""

# Run unit tests
python -m unittest test.test_network_connectivity -v
UNITTEST_RESULT=$?

# Summary
echo ""
echo "======================================================================"
echo "TEST SUITE RESULTS"
echo "======================================================================"
echo ""

if [ $STANDALONE_RESULT -eq 0 ]; then
    echo "✓ Standalone Test: PASSED"
else
    echo "✗ Standalone Test: FAILED"
fi

if [ $UNITTEST_RESULT -eq 0 ]; then
    echo "✓ Unit Test Suite: PASSED"
else
    echo "✗ Unit Test Suite: FAILED"
fi

echo ""

if [ $STANDALONE_RESULT -eq 0 ] && [ $UNITTEST_RESULT -eq 0 ]; then
    echo "✓ ALL TESTS PASSED!"
    echo "  Network connectivity is working correctly."
    echo "  Plugin uses identical patterns to KADAS Albireo 2."
    exit 0
else
    echo "✗ SOME TESTS FAILED!"
    echo "  Please check the errors above."
    echo "  See test/NETWORK_TESTS.md for troubleshooting."
    exit 1
fi
