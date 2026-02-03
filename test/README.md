# KADAS STAC Plugin - Testing Documentation

Comprehensive testing guide for developers and advanced users.

---

## Test Structure

```
test/
├── README.md                      ← This file
├── quick_network_test.py          ← Quick connectivity test (KADAS Console)
├── test_network.py                ← Standalone network tests
├── test_suite.py                  ← Full plugin test suite
├── test_network_connectivity.py   ← Network patterns (unittest)
├── test_qgis_environment.py       ← QGIS environment validation
├── test_settings_manager.py       ← Settings persistence tests
├── test_stac_api_client_*.py      ← API client tests
├── test_translations.py           ← i18n tests
├── test_maxar_structure.py        ← Maxar catalog hierarchy analysis
├── test_collection_ids.py         ← Collection filter tests
├── run-network-tests.ps1          ← PowerShell test runner
├── run-network-tests.sh           ← Bash test runner
└── mock/                          ← Mock STAC API server
    ├── stac_api_server_app.py
    ├── stac_api_auth_server_app.py
    └── data/                      ← Mock catalog responses
```

---

## Quick Tests

### 1. Quick Network Test (Recommended)

**Purpose**: Verify KADAS network stack and STAC connectivity

**Usage** (copy/paste in KADAS Python Console):

```python
exec(open('test/quick_network_test.py').read())
```

**Tests**:
1. ✓ QgsNetworkAccessManager available
2. ✓ QGIS proxy settings readable
3. ✓ Basic HTTPS connection to data.geo.admin.ch
4. ✓ QgisStacApiIO module import
5. ✓ STAC catalog access (Swiss Federal Geodata)

**Expected Output**:
```
======================================================================
KADAS STAC Plugin - Quick Network Test
======================================================================

1. Testing QgsNetworkAccessManager...
   ✓ QgsNetworkAccessManager available

2. Testing QGIS Proxy Settings...
   Proxy Type: NoProxy
   ✓ Proxy settings readable

3. Testing Basic HTTPS Connection...
   URL: https://data.geo.admin.ch/api/stac/v1/
   Status: 200
   ✓ Connection successful!

4. Testing QgisStacApiIO module...
   ✓ QgisStacApiIO imported successfully

5. Testing STAC Catalog Access...
   Catalog Type: Catalog
   STAC Version: 1.0.0
   ✓ STAC catalog accessible

======================================================================
All tests PASSED ✓
======================================================================
```

**Troubleshooting**:
- **Test 1 fails**: QGIS not properly initialized
- **Test 3 fails**: Network/proxy/firewall issues
- **Test 4 fails**: Plugin not installed correctly
- **Test 5 fails**: STAC API down or proxy blocks request

---

### 2. Standalone Network Test

**Purpose**: Detailed network diagnostics without KADAS GUI

**Usage**:

```powershell
# Windows PowerShell
cd test
& "C:\Program Files\QGIS 3.40.7\apps\Python312\python.exe" test_network.py
```

```bash
# Linux/Mac
cd test
python test_network.py
```

**Tests**:
1. QgsNetworkAccessManager
2. QGIS Settings
3. Basic HTTPS Connection
4. QgisStacApiIO Implementation
5. Proxy Handler
6. URL Normalization

**Expected Output**:
```
======================================================================
TEST RESULTS SUMMARY
======================================================================
  ✓ PASS  QgsNetworkAccessManager
  ✓ PASS  QGIS Settings
  ✓ PASS  Basic HTTPS Connection
  ✓ PASS  QgisStacApiIO
  ✓ PASS  Proxy Handler
  ✓ PASS  URL Normalization

======================================================================
Total: 6 tests
Passed: 6
Failed: 0
Success Rate: 100%
======================================================================
```

---

## Full Test Suite

### 3. Complete Plugin Tests

**Purpose**: Comprehensive functionality testing

**Usage**:

```powershell
cd test
python test_suite.py
```

**Tests**:
- Settings manager (connection CRUD)
- STAC API client functions
- Authentication mechanisms
- Translation files
- QGIS environment compatibility

**Expected Output**:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 2.34s

OK
```

---

## Specialized Tests

### 4. Network Connectivity Patterns

**File**: `test_network_connectivity.py`

**Purpose**: Test network patterns matching KADAS Albireo 2

```powershell
python -m unittest test_network_connectivity
```

**Tests**:
- Basic HTTPS connection
- Proxy configuration handling
- SSL certificate validation
- Timeout handling
- Error recovery

---

### 5. Static Catalog Structure Analysis

**File**: `test_maxar_structure.py`

**Purpose**: Analyze hierarchical static catalog structure

```powershell
python test_maxar_structure.py
```

**Output**:
```
=== Maxar Open Data Catalog Structure ===

Root Catalog: Maxar Open Data
URL: https://maxar-opendata.s3.amazonaws.com/events/catalog.json

Level 0: Root Catalog
  └─ Links: 55 collections

Level 1: Event Collections
  ├─ Emilia-Romagna-Italy-flooding-may23
  │  └─ Links: 11 sub-collections
  ├─ Turkey-Syria-earthquake-23
  └─ ...

Level 2: Acquisition Collections
  ├─ 10300100BF164000
  │  └─ Items: 10
  └─ ...

Total Items Found: 120 (limited to 100 for safety)
```

---

### 6. Collection Filter Tests

**File**: `test_collection_ids.py`

**Purpose**: Verify collection filtering works correctly

```powershell
python test_collection_ids.py
```

---

## Mock STAC API Server

### Purpose

Test plugin against local STAC API without internet connection.

### Setup

```powershell
# Install dependencies
pip install flask

# Start mock server
cd test/mock
python stac_api_server_app.py
```

**Server runs on**: `http://localhost:5001`

### Mock Data

Located in `test/mock/data/`:
- `catalog.json` - Root catalog
- `collections.json` - Collection list
- `collection.json` - Single collection
- `search.json` - Search results
- `*_item.json` - Individual items

### Test Against Mock

1. Start mock server (above)
2. Add connection in plugin:
   ```
   Name: Mock STAC
   URL: http://localhost:5001
   Type: API Catalog
   ```
3. Search and verify results

---

## Test Runners

### PowerShell Runner

**File**: `run-network-tests.ps1`

```powershell
.\run-network-tests.ps1
```

Runs all network tests in sequence.

### Bash Runner

**File**: `run-network-tests.sh`

```bash
chmod +x run-network-tests.sh
./run-network-tests.sh
```

---

## Debugging Tests

### Enable Debug Logging

**In Test Scripts**:

```python
from kadas_stac.logger import get_logger

logger = get_logger(level="DEBUG")
logger.debug("Test message")
```

**Log Location**: `~/.kadas/stac.log`

### Increase Verbosity

```python
# In test files
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Pytest Integration

```powershell
# Install pytest
pip install pytest

# Run with verbose output
pytest test/ -v

# Run specific test
pytest test/test_network_connectivity.py::TestNetworkConnectivity::test_basic_connection -v
```

---

## Continuous Integration

### GitHub Actions (Future)

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install QGIS
        run: |
          sudo apt-get install qgis qgis-plugin-grass
      - name: Run Tests
        run: |
          cd test
          python test_network.py
          python test_suite.py
```

---

## Test Coverage

### Measure Coverage

```powershell
pip install coverage

# Run tests with coverage
coverage run --source=../src/kadas_stac -m pytest test/

# Generate report
coverage report
coverage html  # HTML report in htmlcov/
```

### Expected Coverage

| Module | Coverage | Status |
|--------|----------|--------|
| `api/network.py` | 85% | ✓ Good |
| `api/qgis_stac_io.py` | 90% | ✓ Excellent |
| `api/models.py` | 70% | ⚠ Needs work |
| `gui/*.py` | 60% | ⚠ GUI testing hard |
| `conf.py` | 80% | ✓ Good |
| **Overall** | **75%** | **✓ Acceptable** |

---

## Performance Testing

### Benchmark Search Performance

```python
import time

# API Catalog
start = time.time()
# ... perform search ...
api_time = time.time() - start

# Static Catalog
start = time.time()
# ... perform search ...
static_time = time.time() - start

print(f"API: {api_time:.2f}s")
print(f"Static: {static_time:.2f}s")
```

**Expected**:
- API catalog: 1-3 seconds
- Static catalog: 3-10 seconds (recursive navigation)

### Load Test

```python
# Test 100 concurrent searches
import concurrent.futures

def search():
    # ... perform search ...
    pass

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(search) for _ in range(100)]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

print(f"Completed {len(results)} searches")
```

---

## Common Test Failures

### "ImportError: No module named 'qgis'"

**Cause**: Running tests outside QGIS Python environment

**Solution**:
```powershell
# Use QGIS Python
& "C:\Program Files\QGIS 3.40.7\apps\Python312\python.exe" test_network.py
```

### "SSL: CERTIFICATE_VERIFY_FAILED"

**Cause**: Corporate SSL inspection or firewall

**Solution**:
- Configure QGIS proxy settings
- OR: Set environment variable:
  ```powershell
  $env:REQUESTS_CA_BUNDLE = "C:\path\to\company-ca-bundle.crt"
  ```

### "Connection Timeout"

**Cause**: Network latency or catalog down

**Solution**:
- Check internet connection
- Try different catalog
- Increase timeout in test

---

## Writing New Tests

### Template

```python
# test_my_feature.py
import unittest
from qgis.core import QgsApplication
from kadas_stac.api.network import ContentFetcherTask

class TestMyFeature(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize QGIS application once"""
        cls.qgs = QgsApplication([], False)
        cls.qgs.initQgis()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up QGIS application"""
        cls.qgs.exitQgis()
    
    def setUp(self):
        """Run before each test"""
        self.task = ContentFetcherTask(...)
    
    def test_my_feature(self):
        """Test description"""
        # Arrange
        expected = "result"
        
        # Act
        actual = self.task.my_method()
        
        # Assert
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
```

### Best Practices

1. **One test, one assertion**: Each test should verify one thing
2. **Use descriptive names**: `test_search_returns_correct_item_count()`
3. **Mock external dependencies**: Don't rely on live catalogs
4. **Clean up**: Remove temp files/connections in `tearDown()`
5. **Document**: Add docstrings explaining what is tested

---

## Troubleshooting Test Environment

### QGIS Not Found

```powershell
# Find QGIS Python
Get-ChildItem "C:\Program Files" -Recurse -Filter "python.exe" | Where-Object { $_.Directory -like "*QGIS*" }
```

### Plugin Not Loadable

```python
# In KADAS Python Console
import sys
sys.path.append('c:/tmp/kadas-plugins/kadas-stac-plugin/src')

from kadas_stac import KadasStac
print("Plugin loaded successfully")
```

### Dependencies Missing

```powershell
# Install in QGIS Python
& "C:\Program Files\QGIS 3.40.7\apps\Python312\python.exe" -m pip install pytest coverage
```

---

## Test Maintenance

### Update Mock Data

When STAC spec changes, update `test/mock/data/`:

```python
# Download real catalog response
import requests
response = requests.get('https://data.geo.admin.ch/api/stac/v1/')
with open('test/mock/data/catalog.json', 'w') as f:
    f.write(response.text)
```

### Refresh Test Catalogs

Periodically check test catalogs are still online:

```python
python test/test_network.py --verify-catalogs
```

---

## Resources

- **pytest Documentation**: https://docs.pytest.org/
- **unittest Documentation**: https://docs.python.org/3/library/unittest.html
- **QGIS Testing**: https://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/testing.html
- **STAC API Validator**: https://github.com/stac-utils/stac-api-validator

---

**Last Updated**: 2026-02-03 | **Version**: 0.1.0
