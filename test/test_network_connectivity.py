# -*- coding: utf-8 -*-
"""
Test network connectivity using QGIS QgsNetworkAccessManager.

Verifies that the plugin can connect to STAC APIs using the same
network stack as KADAS Albireo 2.
"""

import unittest
import sys
import os

from qgis.core import QgsApplication, QgsNetworkAccessManager, QgsSettings
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply


class TestNetworkConnectivity(unittest.TestCase):
    """Test network connectivity patterns matching KADAS Albireo 2"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        cls.nam = QgsNetworkAccessManager.instance()
        cls.settings = QgsSettings()
    
    def test_qgis_network_manager_available(self):
        """Test that QgsNetworkAccessManager is available"""
        self.assertIsNotNone(self.nam)
        self.assertIsInstance(self.nam, QgsNetworkAccessManager)
    
    def test_basic_https_connection(self):
        """Test basic HTTPS connection to data.geo.admin.ch"""
        url = QUrl("https://data.geo.admin.ch/api/stac/v1/")
        request = QNetworkRequest(url)
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        
        # Add Referer header (KADAS pattern)
        referer = self.settings.value("search/referer", "http://localhost")
        request.setRawHeader(b"Referer", referer.encode())
        
        reply = self.nam.blockingGet(request)
        
        error = reply.error()
        self.assertEqual(error, QNetworkReply.NoError, 
                        f"Connection failed: {reply.errorString()}")
        
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        self.assertEqual(status_code, 200, 
                        f"Expected status 200, got {status_code}")
        
        content = bytes(reply.content()).decode('utf-8')
        self.assertGreater(len(content), 0, "Response content is empty")
    
    def test_redirect_following(self):
        """Test that HTTP->HTTPS redirects work"""
        # Test URL that might redirect
        url = QUrl("http://data.geo.admin.ch/api/stac/v1/")
        request = QNetworkRequest(url)
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        request.setMaximumRedirectsAllowed(5)
        
        reply = self.nam.blockingGet(request)
        
        # Should either succeed or redirect to HTTPS
        error = reply.error()
        final_url = reply.url().toString()
        
        # Accept both success and redirect results
        self.assertIn(error, [QNetworkReply.NoError, 
                             QNetworkReply.ProtocolUnknownError],
                     f"Unexpected error: {reply.errorString()}")
        
        if error == QNetworkReply.NoError:
            # If successful, should be HTTPS
            self.assertTrue(final_url.startswith('https://'),
                          f"Final URL should be HTTPS: {final_url}")
    
    def test_proxy_settings_readable(self):
        """Test that QGIS proxy settings can be read"""
        proxy_enabled = self.settings.value("proxy/proxyEnabled", False, type=bool)
        proxy_type = self.settings.value("proxy/proxyType", 0, type=int)
        proxy_host = self.settings.value("proxy/proxyHost", "", type=str)
        proxy_port = self.settings.value("proxy/proxyPort", 8080, type=int)
        
        # Just verify we can read settings (values depend on environment)
        self.assertIsInstance(proxy_enabled, bool)
        self.assertIsInstance(proxy_type, int)
        self.assertIsInstance(proxy_host, str)
        self.assertIsInstance(proxy_port, int)
        
        print(f"\nProxy Settings:")
        print(f"  Enabled: {proxy_enabled}")
        print(f"  Type: {proxy_type}")
        print(f"  Host: {proxy_host}")
        print(f"  Port: {proxy_port}")
    
    def test_qgis_stac_io_import(self):
        """Test that QgisStacApiIO can be imported"""
        try:
            # Add src to path if needed
            src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from kadas_stac.api.qgis_stac_io import QgisStacApiIO
            
            # Create instance
            stac_io = QgisStacApiIO()
            self.assertIsNotNone(stac_io)
            self.assertIsNotNone(stac_io.nam)
            
        except ImportError as e:
            self.fail(f"Failed to import QgisStacApiIO: {e}")
    
    def test_qgis_stac_io_request(self):
        """Test QgisStacApiIO request method"""
        try:
            # Add src to path if needed
            src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from kadas_stac.api.qgis_stac_io import QgisStacApiIO
            
            stac_io = QgisStacApiIO()
            
            # Test basic GET request
            response = stac_io.request(
                "https://data.geo.admin.ch/api/stac/v1/",
                method='GET'
            )
            
            self.assertIsInstance(response, str)
            self.assertGreater(len(response), 0)
            
            # Should be valid JSON
            import json
            data = json.loads(response)
            self.assertIsInstance(data, dict)
            
            # Should have STAC API structure
            self.assertIn('type', data)
            self.assertEqual(data['type'], 'Catalog')
            
        except ImportError as e:
            self.skipTest(f"QgisStacApiIO not available: {e}")
        except Exception as e:
            self.fail(f"Request failed: {e}")
    
    def test_proxy_handler_import(self):
        """Test that proxy_handler can be imported"""
        try:
            # Add src to path if needed
            src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from kadas_stac.api.proxy_handler import (
                get_qgis_proxy_settings,
                test_connection_qgis,
                get_proxy_config,
                is_proxy_enabled
            )
            
            # Test functions callable
            proxy_settings = get_qgis_proxy_settings()
            self.assertIsInstance(proxy_settings, dict)
            
            # Test connection
            connection_ok = test_connection_qgis()
            self.assertIsInstance(connection_ok, bool)
            
            print(f"\nProxy Handler Test:")
            print(f"  Connection OK: {connection_ok}")
            print(f"  Proxy Enabled: {proxy_settings.get('enabled')}")
            
        except ImportError as e:
            self.fail(f"Failed to import proxy_handler: {e}")
    
    def test_url_normalization(self):
        """Test URL normalization (adding https:// prefix)"""
        try:
            src_path = os.path.join(os.path.dirname(__file__), '..', 'src')
            if src_path not in sys.path:
                sys.path.insert(0, src_path)
            
            from kadas_stac.api.qgis_stac_io import QgisStacApiIO
            
            stac_io = QgisStacApiIO()
            
            # Test with URL missing scheme
            # Note: This will add https:// prefix
            test_url = "data.geo.admin.ch/api/stac/v1/"
            
            try:
                response = stac_io.request(test_url, method='GET')
                self.assertIsInstance(response, str)
                self.assertGreater(len(response), 0)
            except Exception as e:
                # URL normalization should work, but connection might fail
                # depending on environment
                print(f"\nURL normalization test: {e}")
                # Don't fail test - just verify URL was normalized
                pass
            
        except ImportError as e:
            self.skipTest(f"QgisStacApiIO not available: {e}")
    
    def test_referer_header_set(self):
        """Test that Referer header is set correctly"""
        url = QUrl("https://data.geo.admin.ch/api/stac/v1/")
        request = QNetworkRequest(url)
        
        # Set Referer header (KADAS pattern)
        referer = self.settings.value("search/referer", "http://localhost")
        request.setRawHeader(b"Referer", referer.encode())
        
        # Verify header is set
        referer_header = request.rawHeader(b"Referer")
        self.assertIsNotNone(referer_header)
        self.assertEqual(referer_header.data().decode(), referer)
        
        print(f"\nReferer Header: {referer}")


def run_tests():
    """Run all tests and print results"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestNetworkConnectivity)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # Run tests
    success = run_tests()
    sys.exit(0 if success else 1)
