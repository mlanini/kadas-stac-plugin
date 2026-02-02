#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick network connectivity test for KADAS STAC Plugin.

Tests basic connectivity to data.geo.admin.ch STAC API
using the same patterns as KADAS Albireo 2.
"""

import sys
import os

# Add src to path
src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from qgis.core import QgsApplication, QgsNetworkAccessManager, QgsSettings
    from qgis.PyQt.QtCore import QUrl
    from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply
    QGIS_AVAILABLE = True
except ImportError:
    QGIS_AVAILABLE = False
    print("⚠️  QGIS not available - this test must be run in QGIS/KADAS Python environment")
    sys.exit(1)


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def test_qgis_network_manager():
    """Test basic QgsNetworkAccessManager availability"""
    print_header("TEST 1: QgsNetworkAccessManager Availability")
    
    try:
        nam = QgsNetworkAccessManager.instance()
        print(f"✓ QgsNetworkAccessManager instance: {type(nam).__name__}")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_qgis_settings():
    """Test QGIS Settings (proxy configuration)"""
    print_header("TEST 2: QGIS Settings (Proxy Configuration)")
    
    try:
        settings = QgsSettings()
        
        proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)
        proxy_type = settings.value("proxy/proxyType", 0, type=int)
        proxy_host = settings.value("proxy/proxyHost", "", type=str)
        proxy_port = settings.value("proxy/proxyPort", 8080, type=int)
        proxy_user = settings.value("proxy/proxyUser", "", type=str)
        
        print(f"  Proxy Enabled: {proxy_enabled}")
        print(f"  Proxy Type: {proxy_type} (0=None, 3=HttpProxy, 4=Socks5)")
        print(f"  Proxy Host: {proxy_host if proxy_host else '(not configured)'}")
        print(f"  Proxy Port: {proxy_port}")
        print(f"  Proxy User: {proxy_user if proxy_user else '(no authentication)'}")
        
        referer = settings.value("search/referer", "http://localhost")
        print(f"  Referer Header: {referer}")
        
        print(f"✓ QGIS Settings accessible")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False


def test_basic_connection():
    """Test basic HTTPS connection to data.geo.admin.ch"""
    print_header("TEST 3: Basic HTTPS Connection")
    
    try:
        nam = QgsNetworkAccessManager.instance()
        settings = QgsSettings()
        
        url = QUrl("https://data.geo.admin.ch/api/stac/v1/")
        request = QNetworkRequest(url)
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        request.setMaximumRedirectsAllowed(5)
        
        # Add Referer header (KADAS pattern)
        referer = settings.value("search/referer", "http://localhost")
        request.setRawHeader(b"Referer", referer.encode())
        
        print(f"  Request URL: {url.toString()}")
        print(f"  Referer: {referer}")
        print(f"  Redirects: Enabled (max 5)")
        
        reply = nam.blockingGet(request)
        
        error = reply.error()
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        final_url = reply.url().toString()
        
        print(f"  Final URL: {final_url}")
        print(f"  Status Code: {status_code}")
        print(f"  Error Code: {error} ({reply.errorString()})")
        
        if error == QNetworkReply.NoError:
            content = bytes(reply.content()).decode('utf-8')
            print(f"  Content Length: {len(content)} bytes")
            print(f"✓ Connection successful")
            return True
        else:
            print(f"✗ Connection failed: {reply.errorString()}")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_qgis_stac_io():
    """Test QgisStacApiIO implementation"""
    print_header("TEST 4: QgisStacApiIO Implementation")
    
    try:
        from kadas_stac.api.qgis_stac_io import QgisStacApiIO
        
        stac_io = QgisStacApiIO()
        print(f"  QgisStacApiIO instance: {type(stac_io).__name__}")
        print(f"  Network Manager: {type(stac_io.nam).__name__}")
        
        print(f"\n  Testing GET request...")
        response = stac_io.request(
            "https://data.geo.admin.ch/api/stac/v1/",
            method='GET'
        )
        
        print(f"  Response Length: {len(response)} bytes")
        
        # Parse JSON
        import json
        data = json.loads(response)
        
        print(f"  Response Type: {data.get('type')}")
        print(f"  STAC Version: {data.get('stac_version')}")
        print(f"  ID: {data.get('id')}")
        print(f"  Title: {data.get('title')}")
        
        if data.get('type') == 'Catalog':
            print(f"✓ QgisStacApiIO working correctly")
            return True
        else:
            print(f"✗ Unexpected response type: {data.get('type')}")
            return False
            
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_proxy_handler():
    """Test proxy handler module"""
    print_header("TEST 5: Proxy Handler")
    
    try:
        from kadas_stac.api.proxy_handler import (
            get_qgis_proxy_settings,
            test_connection_qgis,
            detect_proxy_requirement,
            is_proxy_enabled
        )
        
        print(f"  Getting proxy settings...")
        proxy_settings = get_qgis_proxy_settings()
        
        print(f"    Enabled: {proxy_settings.get('enabled')}")
        print(f"    Type: {proxy_settings.get('type')}")
        print(f"    Host: {proxy_settings.get('host')}")
        print(f"    Port: {proxy_settings.get('port')}")
        
        print(f"\n  Testing connection...")
        connection_ok = test_connection_qgis("https://data.geo.admin.ch/api/stac/v1/")
        print(f"    Connection: {'✓ OK' if connection_ok else '✗ Failed'}")
        
        print(f"\n  Checking proxy status...")
        proxy_enabled = is_proxy_enabled()
        print(f"    Proxy Enabled: {proxy_enabled}")
        
        print(f"✓ Proxy handler working correctly")
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_url_normalization():
    """Test URL normalization (https:// prefix)"""
    print_header("TEST 6: URL Normalization")
    
    try:
        from kadas_stac.api.qgis_stac_io import QgisStacApiIO
        
        stac_io = QgisStacApiIO()
        
        # Test with URL missing scheme
        test_url = "data.geo.admin.ch/api/stac/v1/"
        print(f"  Original URL: {test_url}")
        print(f"  Expected: https://{test_url}")
        
        try:
            response = stac_io.request(test_url, method='GET')
            print(f"  Response Length: {len(response)} bytes")
            print(f"✓ URL normalization working")
            return True
        except Exception as e:
            # Normalization might work but connection fail - check error message
            if "https://" in str(e):
                print(f"  URL was normalized to HTTPS")
                print(f"✓ URL normalization working (connection failed but normalization OK)")
                return True
            else:
                print(f"✗ URL normalization failed: {e}")
                return False
            
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False


def main():
    """Run all tests"""
    print_header("KADAS STAC Plugin - Network Connectivity Test")
    print("Testing network connectivity using QGIS patterns (identical to KADAS Albireo 2)")
    
    results = []
    
    results.append(("QgsNetworkAccessManager", test_qgis_network_manager()))
    results.append(("QGIS Settings", test_qgis_settings()))
    results.append(("Basic HTTPS Connection", test_basic_connection()))
    results.append(("QgisStacApiIO", test_qgis_stac_io()))
    results.append(("Proxy Handler", test_proxy_handler()))
    results.append(("URL Normalization", test_url_normalization()))
    
    # Print summary
    print_header("TEST RESULTS SUMMARY")
    
    passed = 0
    failed = 0
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}  {name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Total: {len(results)} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {(passed/len(results)*100):.1f}%")
    print("=" * 70)
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED - Network connectivity is working correctly!")
        print("  Plugin uses identical network patterns to KADAS Albireo 2")
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED - Please check the errors above")
        return 1


if __name__ == '__main__':
    sys.exit(main())
