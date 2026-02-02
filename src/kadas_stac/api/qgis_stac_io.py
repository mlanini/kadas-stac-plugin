# -*- coding: utf-8 -*-
"""
QGIS-compatible StacApiIO using QgsNetworkAccessManager instead of requests.

This solves the SSL module availability issue in KADAS/QGIS Python environments.
"""

import json
import re
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.parse import urlparse

from qgis.core import (
    QgsNetworkAccessManager,
    QgsNetworkReplyContent,
    QgsSettings,
)
from qgis.PyQt.QtCore import QUrl, QEventLoop
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply

from ..lib.pystac.stac_io import DefaultStacIO
from ..lib.pystac.link import Link
from ..lib.pystac_client.conformance import ConformanceClasses, CONFORMANCE_URIS
from ..logger import get_logger

logger = get_logger(level="DEBUG")


class QgisStacApiIO(DefaultStacIO):
    """
    StacApiIO implementation using QGIS QgsNetworkAccessManager.
    
    This avoids Python SSL module dependency and uses Qt/QGIS network stack instead,
    which is properly configured in KADAS/QGIS environments.
    """
    
    def __init__(
        self,
        headers: Optional[Dict] = None,
        conformance: Optional[list] = None,
        parameters: Optional[Dict] = None,
    ):
        """
        Initialize QGIS-based API IO.
        
        Args:
            headers: Optional dictionary of headers to include in all requests
            conformance: Optional list of Conformance Classes
            parameters: Optional dictionary of query string parameters to include in all requests
        """
        self.headers = headers or {}
        self.parameters = parameters or {}
        self._conformance = conformance
        self.nam = QgsNetworkAccessManager.instance()
        
        logger.debug(f"QgisStacApiIO initialized with headers: {list(self.headers.keys())}")
    
    def set_conformance(self, conformance: Optional[list]):
        """Set conformance classes"""
        self._conformance = conformance
    
    def conforms_to(self, conformance_class: ConformanceClasses) -> bool:
        """
        Whether the API conforms to the given standard.
        
        This method only checks against the "conformsTo" property from the API 
        landing page and does not make any additional calls to a /conformance 
        endpoint even if the API provides such an endpoint.
        
        Args:
            conformance_class: The ConformanceClasses key to check conformance against.
            
        Returns:
            bool: Indicates if the API conforms to the given spec or URI.
        """
        # Conformance of None means ignore all conformance as opposed to an
        # empty array which would indicate the API conforms to nothing
        if self._conformance is None:
            return True
        
        class_regex = CONFORMANCE_URIS.get(conformance_class.name, None)
        
        if class_regex is None:
            raise Exception(f"Invalid conformance class {conformance_class}")
        
        pattern = re.compile(class_regex)
        
        if not any(re.match(pattern, uri) for uri in self._conformance):
            return False
        
        return True
    
    def assert_conforms_to(self, conformance_class: ConformanceClasses) -> None:
        """
        Raises a NotImplementedError if the API does not publish the given conformance class.
        
        This method only checks against the "conformsTo" property from the API 
        landing page and does not make any additional calls to a /conformance 
        endpoint even if the API provides such an endpoint.
        
        Args:
            conformance_class: The ConformanceClasses key to check conformance against.
            
        Raises:
            NotImplementedError: If the API does not conform to the given class.
        """
        if not self.conforms_to(conformance_class):
            raise NotImplementedError(f"{conformance_class} not supported")
    
    def get_pages(
        self, 
        url: str, 
        method: str = 'GET', 
        parameters: Optional[Dict] = None
    ) -> Iterator[Dict]:
        """
        Iterator that yields dictionaries for each page at a STAC paging endpoint.
        
        Follows STAC API pagination by following 'next' links in the response.
        Common endpoints: /collections, /search
        
        Args:
            url: The URL to request
            method: HTTP method (GET or POST)
            parameters: Optional query parameters or POST body
            
        Yields:
            Dict: JSON content from each page
        """
        parameters = parameters or {}
        
        # Get first page
        page = self.read_json(url, method=method, parameters=parameters)
        yield page
        
        # Follow 'next' links for pagination
        next_link = next((link for link in page.get('links', []) if link['rel'] == 'next'), None)
        while next_link:
            link = Link.from_dict(next_link)
            page = self.read_json(link, parameters=parameters)
            yield page
            
            # Get the next link for the next iteration
            next_link = next((link for link in page.get('links', []) if link['rel'] == 'next'), None)
    
    def read_text(
        self,
        source: Union[str, Link],
        *args: Any,
        parameters: Optional[dict] = None,
        **kwargs: Any
    ) -> str:
        """
        Read text from the given URI using QGIS network manager.
        
        Args:
            source: URL string or Link object
            parameters: Additional query parameters
            
        Returns:
            str: Response text content
        """
        parameters = parameters or {}
        
        if isinstance(source, str):
            href = source
            if bool(urlparse(href).scheme):
                return self.request(href, parameters=parameters, **kwargs)
            else:
                # Local file
                with open(href) as f:
                    return f.read()
                    
        elif isinstance(source, Link):
            link = source.to_dict()
            href = link['href']
            merge = bool(link.get('merge', False))
            method = link.get('method', 'GET')
            headers = link.get('headers', None)
            link_body = link.get('body', {})
            
            if method == 'POST':
                parameters = {**parameters, **link_body} if merge else link_body
            else:
                parameters = {}
                
            return self.request(
                href,
                method=method,
                headers=headers,
                parameters=parameters
            )
        
        return ""
    
    def request(
        self,
        href: str,
        method: str = 'GET',
        headers: Optional[Dict] = None,
        parameters: Optional[Dict] = None,
        **kwargs: Any
    ) -> str:
        """
        Make HTTP request using QGIS QgsNetworkAccessManager.
        
        Args:
            href: URL to request
            method: HTTP method (GET or POST)
            headers: Optional headers to add to request
            parameters: Optional parameters (query string for GET, body for POST)
            
        Returns:
            str: Response content
            
        Raises:
            Exception: If request fails
        """
        logger.debug(f"{method} {href}")
        
        # Normalize URL - ensure it has a proper scheme
        if not href.startswith(('http://', 'https://')):
            href = 'https://' + href
            logger.debug(f"Added https:// scheme to URL: {href}")
        
        # Build URL
        url = QUrl(href)
        
        # Validate URL
        if not url.isValid():
            error_msg = f"Invalid URL: {href}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        # Add query parameters for GET
        if method == 'GET' and parameters:
            from qgis.PyQt.QtCore import QUrlQuery
            query = QUrlQuery()
            for key, value in {**self.parameters, **parameters}.items():
                query.addQueryItem(str(key), str(value))
            url.setQuery(query)
        
        # Create request
        request = QNetworkRequest(url)
        
        # Enable redirect following
        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)
        request.setMaximumRedirectsAllowed(5)
        
        # Add Referer header (KADAS compatibility - used by all catalog providers)
        settings = QgsSettings()
        referer = settings.value("search/referer", "http://localhost")
        request.setRawHeader(b"Referer", referer.encode())
        
        # Add headers
        all_headers = {**self.headers, **(headers or {})}
        for key, value in all_headers.items():
            request.setRawHeader(key.encode(), str(value).encode())
        
        logger.debug(f"Request URL: {url.toString()}")
        logger.debug(f"Request headers: {list(all_headers.keys())}")
        logger.debug(f"Referer: {referer}")
        
        # Make request
        if method == 'GET':
            reply = self.nam.blockingGet(request)
        elif method == 'POST':
            body = json.dumps(parameters or {}).encode() if parameters else b''
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            reply = self.nam.blockingPost(request, body)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        # Check for errors
        error = reply.error()
        if error != QNetworkReply.NoError:
            error_msg = reply.errorString()
            status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            # QgsNetworkReplyContent doesn't have url() method - use original request URL
            final_url = request.url().toString()
            
            logger.error(f"Request failed to {final_url}")
            logger.error(f"Error: {error_msg} (status: {status_code}, error_code: {error})")
            
            # Provide more context for common errors
            if error == QNetworkReply.ProtocolUnknownError:
                raise Exception(f"Unknown protocol error. Original URL: {href}, Final URL: {final_url}")
            else:
                raise Exception(f"HTTP {status_code}: {error_msg}")
        
        # Get response content
        # QgsNetworkReplyContent.content() returns QByteArray that needs bytes() conversion
        content = reply.content()
        text = bytes(content).decode('utf-8')
        
        status_code = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        # QgsNetworkReplyContent doesn't have url() method - use original request URL
        final_url = request.url().toString()
        logger.debug(f"Response: status={status_code}, final_url={final_url}, length={len(text)}")
        
        return text
