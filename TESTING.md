# Testing Guide

Network connectivity testing for KADAS STAC Plugin.

---

## 🎯 Overview

The plugin includes comprehensive tests to verify that network connectivity works identically to KADAS Albireo 2.

**What is tested**:
- QgsNetworkAccessManager pattern compatibility
- QGIS Settings integration (proxy configuration)
- HTTPS connections to STAC APIs
- Qt SSL stack functionality
- URL normalization and redirect handling
- Referer header support

---

## 🧪 Test Levels

### 1. Quick Test ⚡ (Recommended for Users)

**File**: `test/quick_network_test.py`

**How to run**:
```python
# Copy and paste into KADAS Python Console:
exec(open('c:/path/to/kadas-stac-plugin/test/quick_network_test.py').read())
```

**What it tests**:
- ✓ QgsNetworkAccessManager availability
- ✓ QGIS Settings readable (proxy configuration)
- ✓ HTTPS connection to data.geo.admin.ch
- ✓ QgisStacApiIO module (if plugin installed)

**Duration**: ~5 seconds

**Expected output**:
```
======================================================================
KADAS STAC Plugin - Quick Network Test
======================================================================

1. Testing QgsNetworkAccessManager...
   ✓ QgsNetworkAccessManager available: QgsNetworkAccessManager

2. Testing QGIS Proxy Settings...
   Proxy Enabled: True
   Proxy: prp01.adb.intra.admin.ch:8080
   ✓ Settings accessible

3. Testing connection to data.geo.admin.ch...
   Requesting: https://data.geo.admin.ch/api/stac/v1/
   Status: 200
   Content Length: 1234 bytes
   ✓ Connection successful!

4. Testing QgisStacApiIO module...
   Response Type: Catalog
   STAC Version: 1.0.0
   ✓ QgisStacApiIO working!
```

---

### 2. Standalone Test 🔍 (Recommended for Developers)

**File**: `test_network.py`

**How to run**:
```bash
# From terminal (with QGIS/KADAS Python in PATH):
python test_network.py

# Or from KADAS Python Console:
exec(open('c:/path/to/test_network.py').read())
```

**What it tests**:
1. QgsNetworkAccessManager Availability
2. QGIS Settings (Proxy Configuration)
3. Basic HTTPS Connection
4. QgisStacApiIO Implementation
5. Proxy Handler
6. URL Normalization

**Duration**: ~10 seconds

**Expected output**:
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
Success Rate: 100.0%
======================================================================

✓ ALL TESTS PASSED - Network connectivity is working correctly!
  Plugin uses identical network patterns to KADAS Albireo 2
```

---

### 3. Unit Test Suite 🧪 (Recommended for CI/CD)

**File**: `test/test_network_connectivity.py`

**How to run**:
```bash
# Run all unit tests:
python -m unittest test.test_network_connectivity -v

# Run specific test:
python -m unittest test.test_network_connectivity.TestNetworkConnectivity.test_basic_https_connection -v
```

**What it tests**:
- `test_qgis_network_manager_available` - QgsNetworkAccessManager singleton
- `test_basic_https_connection` - HTTPS to data.geo.admin.ch
- `test_redirect_following` - HTTP→HTTPS redirects
- `test_proxy_settings_readable` - QGIS Settings proxy reading
- `test_qgis_stac_io_import` - QgisStacApiIO import
- `test_qgis_stac_io_request` - QgisStacApiIO request method
- `test_proxy_handler_import` - Proxy handler import
- `test_url_normalization` - https:// auto-prefix
- `test_referer_header_set` - Referer header setting

**Duration**: ~15 seconds

---

## 🔧 Network Patterns Tested

All tests verify **identical patterns** to KADAS Albireo 2:

### Pattern 1: QgsNetworkAccessManager
```python
# KADAS C++:
# QNetworkReply *reply = QgsNetworkAccessManager::instance()->get(req);

# Plugin Python (identical):
nam = QgsNetworkAccessManager.instance()
reply = nam.blockingGet(request)
```

### Pattern 2: Referer Header
```python
# KADAS C++ (catalog providers):
# req.setRawHeader("Referer", QgsSettings().value(...).toByteArray());

# Plugin Python (identical):
settings = QgsSettings()
referer = settings.value("search/referer", "http://localhost")
request.setRawHeader(b"Referer", referer.encode())
```

### Pattern 3: Redirect Following
```python
# KADAS: Qt automatic redirects

# Plugin (explicit configuration):
request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
request.setMaximumRedirectsAllowed(5)
```

### Pattern 4: Proxy from QGIS Settings
```python
# Both KADAS and plugin read from same location:
settings = QgsSettings()
proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)
proxy_host = settings.value("proxy/proxyHost", "", type=str)
proxy_port = settings.value("proxy/proxyPort", 8080, type=int)
```

---

## 🚨 Troubleshooting

### Tests Fail: "QGIS not available"

**Symptom**:
```
ERROR: QGIS not found in PATH
```

**Solution**:
- Run tests in QGIS/KADAS Python environment
- Or add QGIS Python to PATH before running tests

---

### Tests Fail: "Connection failed"

**Symptom**:
```
✗ Connection failed: Connection refused
```

**Possible causes**:
1. **No internet connection**: Ping test.geo.admin.ch
2. **Firewall blocking**: Check firewall allows HTTPS (port 443)
3. **Proxy not configured**: Configure in QGIS Settings → Network
4. **VPN required**: Connect VPN before testing

**Solution**:
```bash
# Test basic connectivity:
ping data.geo.admin.ch

# Test HTTPS access:
curl https://data.geo.admin.ch/api/stac/v1/

# Check proxy in QGIS:
# Settings → Options → Network → Proxy
```

---

### Tests Fail: "SSL module not available"

**Symptom**:
```
SSLError: Can't connect to HTTPS URL because the SSL module is not available
```

**Solution**:
✅ **This should NOT happen** - the plugin uses Qt SSL stack (always available).

If you see this error, the plugin is incorrectly using Python SSL. Check:
1. Plugin is using `QgisStacApiIO` (not requests library)
2. No import of Python `ssl` module
3. All HTTP done via `QgsNetworkAccessManager`

---

### Tests Fail: "Protocol unknown"

**Symptom**:
```
Exception: HTTP None: Il protocollo "" è sconosciuto
```

**Solution**:
✅ **This should NOT happen** - URL normalization auto-adds `https://`.

If you see this error:
1. Check `QgisStacApiIO.request()` normalizes URLs
2. Verify QUrl validation works
3. Check redirect attribute is set

---

### Tests Fail: Proxy not working

**Symptom**:
```
✗ Connection test failed
Proxy Enabled: True
```

**Solution**:
1. **Check QGIS Settings**:
   - Open QGIS → Settings → Options → Network
   - Verify "Use proxy for web access" is checked
   - Verify Host and Port are correct
   
2. **Test proxy manually**:
   ```python
   from qgis.core import QgsSettings
   settings = QgsSettings()
   print(settings.value("proxy/proxyEnabled"))  # Should be True
   print(settings.value("proxy/proxyHost"))     # Should show host
   ```

3. **Restart QGIS** after changing proxy settings

4. **Corporate proxy**: May require authentication:
   - Add Username and Password in QGIS Settings
   - Format: `http://user:pass@host:port`

---

### Tests Fail: VPN Issues

**Symptom**:
```
✗ Connection successful without SSL verification only
✓ VPN Connection: Detected
```

**Solution**:
✅ **This is NORMAL** for corporate VPN with SSL inspection.

The plugin:
- Uses Qt SSL stack (handles VPN certificates)
- Automatically detects VPN
- Works correctly with VPN

**Action**: No action needed - plugin is working correctly!

---

## 📊 Test Results Interpretation

### 100% Pass Rate (Expected)

```
Total: 6 tests
Passed: 6
Failed: 0
Success Rate: 100.0%
```

✅ **Plugin is ready for production use**
- Network connectivity identical to KADAS
- All patterns verified
- Proxy/VPN working correctly

### Partial Pass (Investigate)

```
Total: 6 tests
Passed: 4
Failed: 2
Success Rate: 66.7%
```

⚠️ **Check failed tests**:
- Look at specific error messages
- Common: Proxy misconfiguration
- Common: Network/firewall issues
- Unlikely: Code bugs (patterns are simple)

### All Fail (Environment Issue)

```
Total: 6 tests
Passed: 0
Failed: 6
Success Rate: 0.0%
```

🔴 **Environment problem**:
- QGIS not properly installed
- Python environment incorrect
- No network access at all
- Tests running outside QGIS

---

## 🎬 Running Tests in Different Environments

### KADAS Albireo 2 (Target Environment)

```python
# Open KADAS Albireo 2
# Plugins → Python Console
# Copy/paste:
exec(open('c:/path/to/test/quick_network_test.py').read())
```

### QGIS Desktop

```python
# Open QGIS
# Plugins → Python Console
# Copy/paste:
exec(open('c:/path/to/test/quick_network_test.py').read())
```

### Terminal (with QGIS Python)

```bash
# Windows (PowerShell):
& "C:\Program Files\QGIS 3.40.7\apps\Python312\python.exe" test_network.py

# Linux:
/usr/bin/python3 test_network.py

# macOS:
/Applications/QGIS.app/Contents/MacOS/bin/python3 test_network.py
```

---

## 📋 Test Checklist

Before releasing plugin version:

- [ ] Quick test passes (console)
- [ ] Standalone test passes (terminal)
- [ ] Unit tests pass (unittest)
- [ ] Proxy configuration tested
- [ ] VPN configuration tested
- [ ] HTTPS connection verified
- [ ] Redirect handling verified
- [ ] QgisStacApiIO tested
- [ ] Proxy Handler tested
- [ ] KADAS Albireo 2 tested

---

## 📞 Support

If tests consistently fail:

1. **Check environment**: QGIS/KADAS installed correctly?
2. **Check network**: Can you access https://data.geo.admin.ch/?
3. **Check proxy**: Is proxy configured in QGIS Settings?
4. **Report issue**: https://github.com/mlanini/kadas-stac-plugin/issues

Include in report:
- Test output (full)
- QGIS/KADAS version
- Operating System
- Proxy configuration (yes/no, don't include credentials)
- VPN active (yes/no)
