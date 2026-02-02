"""
Quick Network Test - Copy/Paste in KADAS Python Console

Test di connettività rapido da eseguire direttamente nella console Python di KADAS.
Copia e incolla tutto questo codice nella console.
"""

print("=" * 70)
print("KADAS STAC Plugin - Quick Network Test")
print("=" * 70)

# Test 1: QgsNetworkAccessManager
print("\n1. Testing QgsNetworkAccessManager...")
try:
    from qgis.core import QgsNetworkAccessManager, QgsSettings
    from qgis.PyQt.QtCore import QUrl
    from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply
    
    nam = QgsNetworkAccessManager.instance()
    print(f"   ✓ QgsNetworkAccessManager available: {type(nam).__name__}")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    import sys
    sys.exit(1)

# Test 2: QGIS Proxy Settings
print("\n2. Testing QGIS Proxy Settings...")
try:
    settings = QgsSettings()
    proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)
    proxy_host = settings.value("proxy/proxyHost", "", type=str)
    proxy_port = settings.value("proxy/proxyPort", 8080, type=int)
    
    print(f"   Proxy Enabled: {proxy_enabled}")
    if proxy_enabled:
        print(f"   Proxy: {proxy_host}:{proxy_port}")
    print(f"   ✓ Settings accessible")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# Test 3: Connection to data.geo.admin.ch
print("\n3. Testing connection to data.geo.admin.ch...")
try:
    url = QUrl("https://data.geo.admin.ch/api/stac/v1/")
    request = QNetworkRequest(url)
    request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
    
    # Add Referer header (KADAS pattern)
    referer = settings.value("search/referer", "http://localhost")
    request.setRawHeader(b"Referer", referer.encode())
    
    print(f"   Requesting: {url.toString()}")
    reply = nam.blockingGet(request)
    
    error = reply.error()
    status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
    
    if error == QNetworkReply.NoError:
        content = bytes(reply.content()).decode('utf-8')
        print(f"   Status: {status}")
        print(f"   Content Length: {len(content)} bytes")
        print(f"   ✓ Connection successful!")
    else:
        print(f"   ✗ Connection failed: {reply.errorString()}")
        print(f"   Error Code: {error}")
except Exception as e:
    print(f"   ✗ Exception: {e}")

# Test 4: QgisStacApiIO (if plugin installed)
print("\n4. Testing QgisStacApiIO module...")
try:
    import sys
    import os
    
    # Try to find plugin directory
    plugin_paths = [
        'c:/tmp/kadas-plugins/kadas-stac-plugin/src',
        os.path.expanduser('~/.qgis3/python/plugins/kadas_stac'),
        os.path.expanduser('~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/kadas_stac'),
    ]
    
    plugin_found = False
    for path in plugin_paths:
        if os.path.exists(path):
            if path not in sys.path:
                sys.path.insert(0, path)
            plugin_found = True
            print(f"   Plugin path: {path}")
            break
    
    if not plugin_found:
        print(f"   ⚠ Plugin not found in standard locations")
        print(f"   Searched: {plugin_paths}")
    else:
        from kadas_stac.api.qgis_stac_io import QgisStacApiIO
        
        stac_io = QgisStacApiIO()
        response = stac_io.request("https://data.geo.admin.ch/api/stac/v1/", method='GET')
        
        import json
        data = json.loads(response)
        
        print(f"   Response Type: {data.get('type')}")
        print(f"   STAC Version: {data.get('stac_version')}")
        print(f"   ✓ QgisStacApiIO working!")
        
except ImportError as e:
    print(f"   ⚠ Module not available: {e}")
    print(f"   (This is OK if plugin not installed yet)")
except Exception as e:
    print(f"   ✗ Failed: {e}")

# Summary
print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\nIf all tests passed (✓), network connectivity is working correctly!")
print("The plugin uses identical network patterns to KADAS Albireo 2.")
print("=" * 70)
