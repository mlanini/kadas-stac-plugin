#!/usr/bin/env pwsh
# Run all network connectivity tests for KADAS STAC Plugin

Write-Host "=" * 70
Write-Host "KADAS STAC Plugin - Network Connectivity Test Suite"
Write-Host "=" * 70
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion"
} catch {
    Write-Host "ERROR: Python not found in PATH"
    Write-Host "Please ensure QGIS/KADAS Python is in your PATH"
    exit 1
}

Write-Host ""
Write-Host "Running tests..."
Write-Host ""

# Run standalone test
Write-Host "=" * 70
Write-Host "Running Standalone Test (test_network.py)"
Write-Host "=" * 70
Write-Host ""

python test_network.py

$standaloneResult = $LASTEXITCODE

Write-Host ""
Write-Host "=" * 70
Write-Host "Running Unit Test Suite (test/test_network_connectivity.py)"
Write-Host "=" * 70
Write-Host ""

# Run unit tests
python -m unittest test.test_network_connectivity -v

$unittestResult = $LASTEXITCODE

# Summary
Write-Host ""
Write-Host "=" * 70
Write-Host "TEST SUITE RESULTS"
Write-Host "=" * 70
Write-Host ""

if ($standaloneResult -eq 0) {
    Write-Host "✓ Standalone Test: PASSED"
} else {
    Write-Host "✗ Standalone Test: FAILED"
}

if ($unittestResult -eq 0) {
    Write-Host "✓ Unit Test Suite: PASSED"
} else {
    Write-Host "✗ Unit Test Suite: FAILED"
}

Write-Host ""

if ($standaloneResult -eq 0 -and $unittestResult -eq 0) {
    Write-Host "✓ ALL TESTS PASSED!"
    Write-Host "  Network connectivity is working correctly."
    Write-Host "  Plugin uses identical patterns to KADAS Albireo 2."
    exit 0
} else {
    Write-Host "✗ SOME TESTS FAILED!"
    Write-Host "  Please check the errors above."
    Write-Host "  See test/NETWORK_TESTS.md for troubleshooting."
    exit 1
}
