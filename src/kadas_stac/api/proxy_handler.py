# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-



"""""""""

Proxy Detection and Configuration for KADAS STAC Plugin.

Proxy Detection and Configuration for KADAS STAC Plugin.Proxy Detection and Configuration for KADAS STAC Plugin.

Based on swisstopo/topo-rapidmapping proxy_handler.py

Uses QGIS QgsNetworkAccessManager proxy settings automatically.

No manual configuration needed - respects QGIS Settings → Network → Proxy.

Based on swisstopo/topo-rapidmapping proxy_handler.pyUses QGIS QgsNetworkAccessManager proxy settings automatically.

VPN SUPPORT: Automatically detects VPN connections and adapts SSL handling.

"""Uses QGIS QgsNetworkAccessManager proxy settings automatically.No manual configuration needed - respects QGIS Settings → Network → Proxy.



import loggingNo manual configuration needed - respects QGIS Settings → Network → Proxy.

from typing import Dict, Optional

VPN SUPPORT: Automatically detects VPN connections and adapts SSL handling.

from qgis.core import QgsNetworkAccessManager, QgsSettings

from qgis.PyQt.QtCore import QUrlVPN SUPPORT: Automatically detects VPN connections and adapts SSL handling."""

from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply

"""

# Setup logger

logger = logging.getLogger(__name__)import logging



import loggingfrom typing import Dict, Optional

# ============================================================================

# GLOBAL PROXY CONFIGURATIONfrom typing import Dict, Optionalfrom pathlib import Path

# ============================================================================

# This variable stores proxy settings after initialization

# and is reused by all modules

PROXY_CONFIG = {from qgis.core import QgsNetworkAccessManager, QgsSettingsfrom qgis.core import (

    'enabled': False,

    'proxy_url': None,    QgsNetworkAccessManager,

    'verify_ssl': True,

    'initialized': False,# Setup logger  )

    'is_vpn': False,

    'proxy_type': None,logger = logging.getLogger(__name__)

    'qgis_settings': {}

}# Setup logger



#logger = logging.getLogger(__name__)

def get_qgis_proxy_settings() -> Dict:

    """# ============================================================================

    Reads proxy configuration from QGIS Settings.

    # GLOBAL PROXY CONFIGURATION#

    Returns:

        Dict: Proxy configuration with keys:# ============================================================================# ============================================================================

            - enabled: Proxy enabled

            - type: Proxy type (0=None, 3=HttpProxy, 4=Socks5Proxy, etc.)# This variable stores proxy settings after initialization# GLOBAL PROXY CONFIGURATION

            - host: Proxy host

            - port: Proxy port# and is reused by all modules# ============================================================================

            - user: Username (if authentication)

            - password: Password (if authentication)PROXY_CONFIG = {# This variable stores proxy settings after initialization

    """

    settings = QgsSettings()    'enabled': False,# and is reused by all modules

    

    # Read proxy settings from QGIS    'proxy_url': None,PROXY_CONFIG = {

    proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)

    proxy_type = settings.value("proxy/proxyType", 0, type=int)    'verify_ssl': True,    'enabled': False,

    proxy_host = settings.value("proxy/proxyHost", "", type=str)

    proxy_port = settings.value("proxy/proxyPort", 8080, type=int)    'initialized': False,    'proxy_url': None,

    proxy_user = settings.value("proxy/proxyUser", "", type=str)

    proxy_password = settings.value("proxy/proxyPassword", "", type=str)    'is_vpn': False,    'verify_ssl': True,

    

    return {    'proxy_type': None,    'initialized': False,

        'enabled': proxy_enabled,

        'type': proxy_type,    'qgis_settings': {}    'is_vpn': False,

        'host': proxy_host,

        'port': proxy_port,}    'proxy_type': None,

        'user': proxy_user,

        'password': proxy_password    'qgis_settings': {}

    }

}



def build_proxy_url(settings: Dict) -> Optional[str]:def get_qgis_proxy_settings() -> Dict:

    """

    Builds proxy URL from QGIS settings.    """

    

    Args:    Reads proxy configuration from QGIS QgsNetworkAccessManager.def get_qgis_proxy_settings() -> Dict:

        settings: QGIS proxy settings dict

                """

    Returns:

        Proxy URL string or None    Returns:    Reads proxy configuration from QGIS QgsNetworkAccessManager.

    """

    if not settings.get('enabled') or not settings.get('host'):        Dict: Proxy configuration with keys:    

        return None

                - enabled: Proxy enabled    Returns:

    host = settings['host']

    port = settings['port']            - type: Proxy type (0=None, 3=HttpProxy, 4=Socks5Proxy, etc.)        Dict: Proxy configuration with keys:

    user = settings.get('user', '')

    password = settings.get('password', '')            - host: Proxy host            - type: Proxy type (0=None, 3=HttpProxy, 4=Socks5Proxy, etc.)

    

    # Build URL with or without authentication            - port: Proxy port            - host: Proxy host

    if user and password:

        return f"http://{user}:{password}@{host}:{port}"            - user: Username (if authentication)            - port: Proxy port

    else:

        return f"http://{host}:{port}"            - password: Password (if authentication)            - user: Username (if authentication)



    """            - password: Password (if authentication)

def test_connection_qgis(test_url: str = "https://data.geo.admin.ch/api/stac/v1/") -> bool:

    """    settings = QgsSettings()    """

    Tests connection using QGIS QgsNetworkAccessManager.

            from qgis.core import QgsSettings

    Args:

        test_url: URL to test    # Read proxy settings from QGIS    

        

    Returns:    proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)    settings = QgsSettings()

        bool: True if connection successful

    """    proxy_type = settings.value("proxy/proxyType", 0, type=int)    

    try:

        nam = QgsNetworkAccessManager.instance()    proxy_host = settings.value("proxy/proxyHost", "", type=str)    # Read proxy settings from QGIS

        

        url = QUrl(test_url)    proxy_port = settings.value("proxy/proxyPort", 8080, type=int)    proxy_enabled = settings.value("proxy/proxyEnabled", False, type=bool)

        request = QNetworkRequest(url)

        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)    proxy_user = settings.value("proxy/proxyUser", "", type=str)    proxy_type = settings.value("proxy/proxyType", 0, type=int)

        

        reply = nam.blockingGet(request)    proxy_password = settings.value("proxy/proxyPassword", "", type=str)    proxy_host = settings.value("proxy/proxyHost", "", type=str)

        

        error = reply.error()        proxy_port = settings.value("proxy/proxyPort", 8080, type=int)

        if error == QNetworkReply.NoError:

            status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)    return {    proxy_user = settings.value("proxy/proxyUser", "", type=str)

            return status == 200

                'enabled': proxy_enabled,    proxy_password = settings.value("proxy/proxyPassword", "", type=str)

        return False

            'type': proxy_type,    

    except Exception as e:

        logger.debug(f"Connection test failed: {e}")        'host': proxy_host,    return {

        return False

        'port': proxy_port,        'enabled': proxy_enabled,



def detect_vpn_connection() -> bool:        'user': proxy_user,        'type': proxy_type,

    """

    Attempts to detect if a VPN connection is active.        'password': proxy_password        'host': proxy_host,

    

    Heuristic: If connection works but SSL verification needs to be disabled,    }        'port': proxy_port,

    VPN with SSL-Inspection is probably active.

            'user': proxy_user,

    Returns:

        bool: True if VPN suspected        'password': proxy_password

    """

    # For QGIS, we rely on QgsNetworkAccessManager which handles SSL automaticallydef build_proxy_url(settings: Dict) -> Optional[str]:    }

    # VPN detection is less critical since Qt SSL stack handles corporate proxies well

        """

    # Simple heuristic: if proxy is configured and connection works, assume corporate network

    settings = get_qgis_proxy_settings()    Builds proxy URL from QGIS settings.

    

    if settings.get('enabled') and settings.get('host'):    def build_proxy_url(settings: Dict) -> Optional[str]:

        # Test if connection works

        if test_connection_qgis():    Args:    """

            logger.info("  ℹ Corporate proxy detected - assuming VPN may be active")

            return True        settings: QGIS proxy settings dict    Builds proxy URL from QGIS settings.

    

    return False            



    Returns:    Args:

def detect_proxy_requirement() -> Dict:

    """        Proxy URL string or None        settings: QGIS proxy settings dict

    Detects automatically if a proxy is required.

        """        

    Uses QGIS proxy settings from Settings → Network → Proxy.

        if not settings.get('enabled') or not settings.get('host'):    Returns:

    Returns:

        Dict: Proxy configuration with keys:        return None        Proxy URL string or None

            - enabled (bool): Proxy enabled

            - proxy_url (str): Proxy URL        """

            - verify_ssl (bool): SSL verification active

            - initialized (bool): True (marked as initialized)    host = settings['host']    if not settings.get('enabled') or not settings.get('host'):

            - is_vpn (bool): True if VPN detected

            - proxy_type (int): QGIS proxy type    port = settings['port']        return None

            - qgis_settings (dict): Full QGIS proxy settings

    """    user = settings.get('user', '')    

    logger.info("Detecting internet connectivity...")

        password = settings.get('password', '')    host = settings['host']

    # Read QGIS proxy settings

    qgis_settings = get_qgis_proxy_settings()        port = settings['port']

    

    logger.info(f"  QGIS Proxy Settings:")    # Build URL with or without authentication    user = settings.get('user', '')

    logger.info(f"    Enabled: {qgis_settings.get('enabled')}")

    logger.info(f"    Type: {qgis_settings.get('type')}")    if user and password:    password = settings.get('password', '')

    logger.info(f"    Host: {qgis_settings.get('host')}")

    logger.info(f"    Port: {qgis_settings.get('port')}")        return f"http://{user}:{password}@{host}:{port}"    

    

    # Test connection    else:    # Build URL with or without authentication

    test_url = "https://data.geo.admin.ch/api/stac/v1/"

    logger.info(f"  Testing connection to {test_url}...")        return f"http://{host}:{port}"    if user and password:

    

    connection_ok = test_connection_qgis(test_url)        return f"http://{user}:{password}@{host}:{port}"

    

    if connection_ok:    else:

        logger.info("  ✓ Connection successful")

    else:def test_connection_qgis(test_url: str = "https://data.geo.admin.ch/api/stac/v1/") -> bool:        return f"http://{host}:{port}"

        logger.warning("  ✗ Connection test failed")

        """

    # Build proxy URL if configured

    proxy_url = None    Tests connection using QGIS QgsNetworkAccessManager.

    if qgis_settings.get('enabled'):

        proxy_url = build_proxy_url(qgis_settings)    def test_connection_qgis(test_url: str = "https://data.geo.admin.ch/api/stac/v1/") -> bool:

        logger.info(f"  Proxy URL: {proxy_url.replace(qgis_settings.get('password', ''), '***') if proxy_url and qgis_settings.get('password') else proxy_url}")

        Args:    """

    # Detect VPN

    is_vpn = detect_vpn_connection()        test_url: URL to test    Tests connection using QGIS QgsNetworkAccessManager.

    

    # QGIS handles SSL automatically via Qt - we always use SSL verification            

    # Qt's SSL stack is more robust than Python's and handles corporate proxies better

    verify_ssl = True    Returns:    Args:

    

    return {        bool: True if connection successful        test_url: URL to test

        'enabled': qgis_settings.get('enabled', False),

        'proxy_url': proxy_url,    """        

        'verify_ssl': verify_ssl,

        'initialized': True,    try:    Returns:

        'is_vpn': is_vpn,

        'proxy_type': qgis_settings.get('type'),        from qgis.PyQt.QtCore import QUrl        bool: True if connection successful

        'qgis_settings': qgis_settings

    }        from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply    """



            try:

def initialize_proxy():

    """        nam = QgsNetworkAccessManager.instance()        from qgis.PyQt.QtCore import QUrl

    Initializes proxy configuration and stores in PROXY_CONFIG.

                    from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply

    This function:

    1. Checks if already initialized (if yes, skips tests)        url = QUrl(test_url)        

    2. Reads QGIS proxy settings

    3. Stores results in global PROXY_CONFIG        request = QNetworkRequest(url)        nam = QgsNetworkAccessManager.instance()

    

    Should be called at program startup.        request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)        

    """

    global PROXY_CONFIG                url = QUrl(test_url)

    

    # ========================================================================        reply = nam.blockingGet(request)        request = QNetworkRequest(url)

    # CHECK IF ALREADY INITIALIZED

    # ========================================================================                request.setAttribute(QNetworkRequest.FollowRedirectsAttribute, True)

    if PROXY_CONFIG.get('initialized', False):

        logger.info("ℹ️  Proxy already initialized, using saved settings")        error = reply.error()        

        logger.info("=" * 70)

        if PROXY_CONFIG['enabled']:        if error == QNetworkReply.NoError:        reply = nam.blockingGet(request)

            logger.info("Proxy Configuration:")

            logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")            status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)        

            logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")

            if PROXY_CONFIG.get('is_vpn'):            return status == 200        error = reply.error()

                logger.info(f"  VPN Connection: Detected")

        else:                if error == QNetworkReply.NoError:

            logger.info("No proxy configuration required")

        logger.info("=" * 70)        return False            status = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)

        return

                        return status == 200

    # ========================================================================

    # RUN PROXY TESTS (only on first call)    except Exception as e:        

    # ========================================================================

    logger.info("=" * 70)        logger.debug(f"Connection test failed: {e}")        return False

    logger.info("INITIALIZING PROXY AND SSL CONFIGURATION")

    logger.info("=" * 70)        return False        

    

    config = detect_proxy_requirement()    except Exception as e:

    PROXY_CONFIG.update(config)

            logger.debug(f"Connection test failed: {e}")

    logger.info("=" * 70)

    if PROXY_CONFIG['enabled']:def detect_vpn_connection() -> bool:        return False

        logger.info("Proxy Configuration:")

        logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")    """

        logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")

        if PROXY_CONFIG.get('is_vpn'):    Attempts to detect if a VPN connection is active.

            logger.info(f"  VPN Connection: Detected (SSL handling adapted)")

    else:    def detect_vpn_connection() -> bool:

        logger.info("No proxy configuration required")

    logger.info("=" * 70)    Heuristic: If connection works but SSL verification needs to be disabled,    """



    VPN with SSL-Inspection is probably active.    Attempts to detect if a VPN connection is active.

def get_proxy_config() -> Dict:

    """        

    Returns the current proxy configuration.

        Returns:    Heuristic: If connection works but SSL verification needs to be disabled,

    If proxy not yet initialized, initialize_proxy() will be called.

            bool: True if VPN suspected    VPN with SSL-Inspection is probably active.

    Returns:

        Dict: Proxy configuration with keys:    """    

            - enabled (bool): Proxy enabled

            - proxy_url (str): Proxy URL    # For QGIS, we rely on QgsNetworkAccessManager which handles SSL automatically    Returns:

            - verify_ssl (bool): SSL verification active

            - initialized (bool): Initialization status    # VPN detection is less critical since Qt SSL stack handles corporate proxies well        bool: True if VPN suspected

            - is_vpn (bool): VPN detected

            - proxy_type (int): QGIS proxy type        """

            - qgis_settings (dict): Full QGIS settings

    """    # Simple heuristic: if proxy is configured and connection works, assume corporate network    # For QGIS, we rely on QgsNetworkAccessManager which handles SSL automatically

    global PROXY_CONFIG

        settings = get_qgis_proxy_settings()    # VPN detection is less critical since Qt SSL stack handles corporate proxies well

    # If not yet initialized, initialize now

    if not PROXY_CONFIG.get('initialized', False):        

        logger.warning("⚠️  Proxy not yet initialized - initializing now...")

        initialize_proxy()    if settings.get('enabled') and settings.get('host'):    # Simple heuristic: if proxy is configured and connection works, assume corporate network

    

    return PROXY_CONFIG.copy()        # Test if connection works    settings = get_qgis_proxy_settings()



        if test_connection_qgis():    

def is_proxy_enabled() -> bool:

    """            logger.info("  ℹ Corporate proxy detected - assuming VPN may be active")    if settings.get('enabled') and settings.get('host'):

    Checks if proxy is enabled.

                return True        # Test if connection works

    If proxy not yet initialized, initialize_proxy() will be called.

                if test_connection_qgis():

    Returns:

        bool: True if proxy enabled, False otherwise    return False            logger.info("  ℹ Corporate proxy detected - assuming VPN may be active")

    """

    global PROXY_CONFIG            return True

    

    # If not yet initialized, initialize now    

    if not PROXY_CONFIG.get('initialized', False):

        logger.warning("⚠️  Proxy not yet initialized - initializing now...")def detect_proxy_requirement() -> Dict:    return False

        initialize_proxy()

        """

    return PROXY_CONFIG['enabled']

    Detects automatically if a proxy is required.



def is_vpn_detected() -> bool:    def detect_proxy_requirement() -> Dict:

    """

    Checks if a VPN connection was detected.    Uses QGIS proxy settings from Settings → Network → Proxy.    """

    

    Returns:        Detects automatically if a proxy is required.

        bool: True if VPN detected

    """    Returns:    

    config = get_proxy_config()

    return config.get('is_vpn', False)        Dict: Proxy configuration with keys:    Uses QGIS proxy settings from Settings → Network → Proxy.



            - enabled (bool): Proxy enabled    

def get_verify_ssl() -> bool:

    """            - proxy_url (str): Proxy URL    Returns:

    Returns whether SSL verification is enabled.

                - verify_ssl (bool): SSL verification active        Dict: Proxy configuration with keys:

    Returns:

        bool: True if SSL verification active, False otherwise            - initialized (bool): True (marked as initialized)            - enabled (bool): Proxy enabled

    """

    config = get_proxy_config()            - is_vpn (bool): True if VPN detected            - proxy_url (str): Proxy URL

    return config.get('verify_ssl', True)

            - proxy_type (int): QGIS proxy type            - verify_ssl (bool): SSL verification active

            - qgis_settings (dict): Full QGIS proxy settings            - initialized (bool): True (marked as initialized)

    """            - is_vpn (bool): True if VPN detected

    logger.info("Detecting internet connectivity...")            - proxy_type (int): QGIS proxy type

                - qgis_settings (dict): Full QGIS proxy settings

    # Read QGIS proxy settings    """

    qgis_settings = get_qgis_proxy_settings()    logger.info("Detecting internet connectivity...")

        

    logger.info(f"  QGIS Proxy Settings:")    # Read QGIS proxy settings

    logger.info(f"    Enabled: {qgis_settings.get('enabled')}")    qgis_settings = get_qgis_proxy_settings()

    logger.info(f"    Type: {qgis_settings.get('type')}")    

    logger.info(f"    Host: {qgis_settings.get('host')}")    logger.info(f"  QGIS Proxy Settings:")

    logger.info(f"    Port: {qgis_settings.get('port')}")    logger.info(f"    Enabled: {qgis_settings.get('enabled')}")

        logger.info(f"    Type: {qgis_settings.get('type')}")

    # Test connection    logger.info(f"    Host: {qgis_settings.get('host')}")

    test_url = "https://data.geo.admin.ch/api/stac/v1/"    logger.info(f"    Port: {qgis_settings.get('port')}")

    logger.info(f"  Testing connection to {test_url}...")    

        # Test connection

    connection_ok = test_connection_qgis(test_url)    test_url = "https://data.geo.admin.ch/api/stac/v1/"

        logger.info(f"  Testing connection to {test_url}...")

    if connection_ok:    

        logger.info("  ✓ Connection successful")    connection_ok = test_connection_qgis(test_url)

    else:    

        logger.warning("  ✗ Connection test failed")    if connection_ok:

            logger.info("  ✓ Connection successful")

    # Build proxy URL if configured    else:

    proxy_url = None        logger.warning("  ✗ Connection test failed")

    if qgis_settings.get('enabled'):    

        proxy_url = build_proxy_url(qgis_settings)    # Build proxy URL if configured

        # Hide password in logs    proxy_url = None

        display_url = proxy_url    if qgis_settings.get('enabled'):

        if proxy_url and qgis_settings.get('password'):        proxy_url = build_proxy_url(qgis_settings)

            display_url = proxy_url.replace(qgis_settings.get('password'), '***')        logger.info(f"  Proxy URL: {proxy_url.replace(qgis_settings.get('password', ''), '***') if proxy_url and qgis_settings.get('password') else proxy_url}")

        logger.info(f"  Proxy URL: {display_url}")    

        # Detect VPN

    # Detect VPN    is_vpn = detect_vpn_connection()

    is_vpn = detect_vpn_connection()    

        # QGIS handles SSL automatically via Qt - we always use SSL verification

    # QGIS handles SSL automatically via Qt - we always use SSL verification    # Qt's SSL stack is more robust than Python's and handles corporate proxies better

    # Qt's SSL stack is more robust than Python's and handles corporate proxies better    verify_ssl = True

    verify_ssl = True    

        return {

    return {        'enabled': qgis_settings.get('enabled', False),

        'enabled': qgis_settings.get('enabled', False),        'proxy_url': proxy_url,

        'proxy_url': proxy_url,        'verify_ssl': verify_ssl,

        'verify_ssl': verify_ssl,        'initialized': True,

        'initialized': True,        'is_vpn': is_vpn,

        'is_vpn': is_vpn,        'proxy_type': qgis_settings.get('type'),

        'proxy_type': qgis_settings.get('type'),        'qgis_settings': qgis_settings

        'qgis_settings': qgis_settings    }

    }



def initialize_proxy():

def initialize_proxy():    """

    """    Initializes proxy configuration and stores in PROXY_CONFIG.

    Initializes proxy configuration and stores in PROXY_CONFIG.    

        This function:

    This function:    1. Checks if already initialized (if yes, skips tests)

    1. Checks if already initialized (if yes, skips tests)    2. Reads QGIS proxy settings

    2. Reads QGIS proxy settings    3. Stores results in global PROXY_CONFIG

    3. Stores results in global PROXY_CONFIG    

        Should be called at program startup.

    Should be called at program startup (optional - called automatically if needed).    """

    """    global PROXY_CONFIG

    global PROXY_CONFIG    

        # ========================================================================

    # ========================================================================    # CHECK IF ALREADY INITIALIZED

    # CHECK IF ALREADY INITIALIZED    # ========================================================================

    # ========================================================================    if PROXY_CONFIG.get('initialized', False):

    if PROXY_CONFIG.get('initialized', False):        logger.info("ℹ️  Proxy already initialized, using saved settings")

        logger.info("ℹ️  Proxy already initialized, using saved settings")        logger.info("=" * 70)

        logger.info("=" * 70)        if PROXY_CONFIG['enabled']:

        if PROXY_CONFIG['enabled']:            logger.info("Proxy Configuration:")

            logger.info("Proxy Configuration:")            logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")

            logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")            logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")

            logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")            if PROXY_CONFIG.get('is_vpn'):

            if PROXY_CONFIG.get('is_vpn'):                logger.info(f"  VPN Connection: Detected")

                logger.info(f"  VPN Connection: Detected")        else:

        else:            logger.info("No proxy configuration required")

            logger.info("No proxy configuration required")        logger.info("=" * 70)

        logger.info("=" * 70)        return

        return    

        # ========================================================================

    # ========================================================================    # RUN PROXY TESTS (only on first call)

    # RUN PROXY DETECTION (only on first call)    # ========================================================================

    # ========================================================================    logger.info("=" * 70)

    logger.info("=" * 70)    logger.info("INITIALIZING PROXY AND SSL CONFIGURATION")

    logger.info("INITIALIZING PROXY AND SSL CONFIGURATION")    logger.info("=" * 70)

    logger.info("=" * 70)    

        config = detect_proxy_requirement()

    config = detect_proxy_requirement()    PROXY_CONFIG.update(config)

    PROXY_CONFIG.update(config)    

        logger.info("=" * 70)

    logger.info("=" * 70)    if PROXY_CONFIG['enabled']:

    if PROXY_CONFIG['enabled']:        logger.info("Proxy Configuration:")

        logger.info("Proxy Configuration:")        logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")

        logger.info(f"  Proxy URL: {PROXY_CONFIG['proxy_url']}")        logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")

        logger.info(f"  SSL Verification: {'Disabled' if not PROXY_CONFIG['verify_ssl'] else 'Enabled'}")        if PROXY_CONFIG.get('is_vpn'):

        if PROXY_CONFIG.get('is_vpn'):            logger.info(f"  VPN Connection: Detected (SSL handling adapted)")

            logger.info(f"  VPN Connection: Detected (SSL handling adapted)")    else:

    else:        logger.info("No proxy configuration required")

        logger.info("No proxy configuration required")    logger.info("=" * 70)

    logger.info("=" * 70)



def get_proxy_config() -> Dict:

def get_proxy_config() -> Dict:    """

    """    Returns the current proxy configuration.

    Returns the current proxy configuration.    

        If proxy not yet initialized, initialize_proxy() will be called.

    If proxy not yet initialized, initialize_proxy() will be called automatically.    

        Returns:

    Returns:        Dict: Proxy configuration with keys:

        Dict: Proxy configuration with keys:            - enabled (bool): Proxy enabled

            - enabled (bool): Proxy enabled            - proxy_url (str): Proxy URL

            - proxy_url (str): Proxy URL            - verify_ssl (bool): SSL verification active

            - verify_ssl (bool): SSL verification active            - initialized (bool): Initialization status

            - initialized (bool): Initialization status            - is_vpn (bool): VPN detected

            - is_vpn (bool): VPN detected            - proxy_type (int): QGIS proxy type

            - proxy_type (int): QGIS proxy type            - qgis_settings (dict): Full QGIS settings

            - qgis_settings (dict): Full QGIS settings    """

    """    global PROXY_CONFIG

    global PROXY_CONFIG    

        # If not yet initialized, initialize now

    # If not yet initialized, initialize now    if not PROXY_CONFIG.get('initialized', False):

    if not PROXY_CONFIG.get('initialized', False):        logger.warning("⚠️  Proxy not yet initialized - initializing now...")

        logger.warning("⚠️  Proxy not yet initialized - initializing now...")        initialize_proxy()

        initialize_proxy()    

        return PROXY_CONFIG.copy()

    return PROXY_CONFIG.copy()



def is_proxy_enabled() -> bool:

def is_proxy_enabled() -> bool:    """

    """    Checks if proxy is enabled.

    Checks if proxy is enabled.    

        If proxy not yet initialized, initialize_proxy() will be called.

    If proxy not yet initialized, initialize_proxy() will be called.    

        Returns:

    Returns:        bool: True if proxy enabled, False otherwise

        bool: True if proxy enabled, False otherwise    """

    """    global PROXY_CONFIG

    config = get_proxy_config()    

    return config['enabled']    # If not yet initialized, initialize now

    if not PROXY_CONFIG.get('initialized', False):

        logger.warning("⚠️  Proxy not yet initialized - initializing now...")

def is_vpn_detected() -> bool:        initialize_proxy()

    """    

    Checks if a VPN connection was detected.    return PROXY_CONFIG['enabled']

    

    Returns:

        bool: True if VPN detecteddef is_vpn_detected() -> bool:

    """    """

    config = get_proxy_config()    Checks if a VPN connection was detected.

    return config.get('is_vpn', False)    

    Returns:

        bool: True if VPN detected

def get_verify_ssl() -> bool:    """

    """    config = get_proxy_config()

    Returns whether SSL verification is enabled.    return config.get('is_vpn', False)

    

    For QGIS/Qt, this is always True as Qt handles SSL robustly.

    def get_verify_ssl() -> bool:

    Returns:    """

        bool: True (SSL verification via Qt is always enabled)    Returns whether SSL verification is enabled.

    """    

    config = get_proxy_config()    Returns:

    return config.get('verify_ssl', True)        bool: True if SSL verification active, False otherwise

    """
    config = get_proxy_config()
    return config.get('verify_ssl', True)

"""
Proxy and SSL Handler for KADAS STAC Plugin

Handles proxy detection and SSL certificate verification issues
commonly encountered in corporate networks and VPN connections.

Inspired by swisstopo/topo-rapidmapping proxy handler.
"""

import os
from typing import Optional, Dict

# Defer urllib3 import to avoid SSL issues at module load time
try:
    import certifi
    CERTIFI_AVAILABLE = True
except ImportError:
    CERTIFI_AVAILABLE = False

from qgis.core import QgsNetworkAccessManager
from qgis.PyQt.QtNetwork import QNetworkProxy

from ..utils import log
from ..logger import get_logger

# Initialize logger
logger = get_logger(level="DEBUG")


# Global proxy configuration
PROXY_CONFIG = {
    'enabled': False,
    'proxies': None,
    'verify_ssl': True,
    'initialized': False,
}


def get_qgis_proxy() -> Optional[Dict]:
    """
    Retrieves proxy settings from QGIS Network Access Manager.
    
    Returns:
        Optional[Dict]: Proxy dictionary for requests or None
    """
    logger.debug("Retrieving QGIS proxy settings")
    nam = QgsNetworkAccessManager.instance()
    proxy = nam.proxy()
    
    logger.debug(f"QGIS proxy type: {proxy.type()}")
    
    if proxy.type() == QNetworkProxy.NoProxy:
        logger.info("No proxy configured in QGIS")
        return None
    
    if proxy.type() in (QNetworkProxy.HttpProxy, QNetworkProxy.Socks5Proxy):
        proxy_url = f"{proxy.hostName()}:{proxy.port()}"
        
        # Add authentication if available
        if proxy.user():
            proxy_url = f"{proxy.user()}:***@{proxy_url}"  # Hide password in logs
            logger.debug(f"Proxy has authentication configured")
        
        # Determine scheme
        scheme = "http" if proxy.type() == QNetworkProxy.HttpProxy else "socks5"
        full_url = f"{scheme}://{proxy_url}"
        
        # Create actual URL with password (not logged)
        actual_url = f"{scheme}://"
        if proxy.user():
            actual_url += f"{proxy.user()}:{proxy.password()}@"
        actual_url += f"{proxy.hostName()}:{proxy.port()}"
        
        logger.info(f"QGIS proxy detected: {scheme}://{proxy.hostName()}:{proxy.port()}")
        
        return {
            "http": actual_url,
            "https": actual_url
        }
    
    logger.warning(f"Unknown proxy type: {proxy.type()}")
    return None


def setup_ssl_context():
    """
    Configures SSL context to use certifi certificates and handle SSL issues.
    
    This helps resolve SSL errors in Python environments where SSL module
    is not properly configured or certificates are missing.
    """
    logger.debug("Setting up SSL context")
    try:
        # Use certifi's certificate bundle if available
        if CERTIFI_AVAILABLE:
            cert_path = certifi.where()
            os.environ['REQUESTS_CA_BUNDLE'] = cert_path
            os.environ['SSL_CERT_FILE'] = cert_path
            logger.info(f"SSL context configured with certifi certificates: {cert_path}")
            log("SSL context configured with certifi certificates", info=True, notify=False)
        else:
            logger.warning("certifi not available, SSL certificates may not be properly configured")
        
        # Disable SSL warnings for known issues (import urllib3 only when needed)
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.debug("SSL warnings disabled")
        except (ImportError, Exception) as e:
            logger.debug(f"Could not disable SSL warnings: {e}")
            pass  # urllib3 not available or SSL warnings can't be disabled
        
    except Exception as e:
        logger.error(f"Could not configure SSL context: {e}", exc_info=True)
        log(f"Warning: Could not configure SSL context: {e}", info=False, notify=False)


def test_connection(url: str, proxies: Optional[Dict] = None, verify_ssl: bool = True) -> bool:
    """
    Tests a connection to check if it works.
    
    Args:
        url: URL to test
        proxies: Proxy dictionary for requests
        verify_ssl: Whether to verify SSL certificates
    
    Returns:
        bool: True if connection successful
    """
    try:
        import requests
        logger.debug(f"Testing connection to {url} (proxies={bool(proxies)}, verify_ssl={verify_ssl})")
        response = requests.get(
            url,
            proxies=proxies,
            verify=verify_ssl,
            timeout=5
        )
        success = response.status_code == 200
        logger.debug(f"Connection test result: {response.status_code} - {'SUCCESS' if success else 'FAILED'}")
        return success
    except Exception as e:
        logger.debug(f"Connection test failed: {type(e).__name__}: {e}")
        return False


def detect_proxy_and_ssl():
    """
    Detects proxy settings and determines if SSL verification should be enabled.
    
    Tests in the following order:
    1. Direct connection with SSL verification
    2. Direct connection without SSL verification
    3. QGIS proxy with SSL verification
    4. QGIS proxy without SSL verification
    
    Returns:
        Dict: Configuration with 'proxies' and 'verify_ssl' keys
    """
    test_url = "https://data.geo.admin.ch/api/stac/v1/"
    logger.info("=" * 60)
    logger.info("Detecting proxy and SSL configuration")
    logger.info(f"Test URL: {test_url}")
    logger.info("=" * 60)
    
    # Configure SSL first
    setup_ssl_context()
    
    # Test 1: Direct connection with SSL
    logger.info("Test 1/4: Direct connection with SSL verification")
    log("Testing direct connection with SSL verification...", info=True, notify=False)
    if test_connection(test_url, proxies=None, verify_ssl=True):
        logger.info("✓ SUCCESS: Direct connection works with SSL verification")
        log("✓ Direct connection works with SSL verification", info=True, notify=False)
        return {
            'enabled': False,
            'proxies': None,
            'verify_ssl': True
        }
    
    # Test 2: Direct connection without SSL (for VPN with SSL inspection)
    logger.info("Test 2/4: Direct connection without SSL verification")
    log("Testing direct connection without SSL verification...", info=True, notify=False)
    if test_connection(test_url, proxies=None, verify_ssl=False):
        logger.warning("⚠ Direct connection works only without SSL verification (VPN detected)")
        log("⚠ Direct connection works only without SSL verification (VPN detected)", info=False, notify=False)
        return {
            'enabled': False,
            'proxies': None,
            'verify_ssl': False
        }
    
    # Test 3: Try QGIS proxy settings
    logger.info("Test 3/4: QGIS proxy with SSL verification")
    qgis_proxy = get_qgis_proxy()
    if qgis_proxy:
        logger.info(f"QGIS proxy found: {list(qgis_proxy.keys())}")
        log(f"Testing QGIS proxy...", info=True, notify=False)
        
        # Test with SSL
        logger.debug("Testing proxy with SSL verification")
        if test_connection(test_url, proxies=qgis_proxy, verify_ssl=True):
            logger.info("✓ SUCCESS: QGIS proxy works with SSL verification")
            log("✓ QGIS proxy works with SSL verification", info=True, notify=False)
            return {
                'enabled': True,
                'proxies': qgis_proxy,
                'verify_ssl': True
            }
        
        # Test without SSL
        logger.info("Test 4/4: QGIS proxy without SSL verification")
        logger.debug("Testing proxy without SSL verification")
        if test_connection(test_url, proxies=qgis_proxy, verify_ssl=False):
            logger.warning("⚠ QGIS proxy works only without SSL verification")
            log("⚠ QGIS proxy works only without SSL verification", info=False, notify=False)
            return {
                'enabled': True,
                'proxies': qgis_proxy,
                'verify_ssl': False
            }
        
        logger.error("QGIS proxy configured but all connection tests failed")
    else:
        logger.info("No QGIS proxy configured, skipping proxy tests")
    
    # All tests failed - return default with SSL disabled as fallback
    logger.error("All connection tests FAILED - using fallback configuration")
    log("⚠ Could not establish connection. Trying with SSL verification disabled as fallback.", info=False, notify=True)
    return {
        'enabled': False,
        'proxies': None,
        'verify_ssl': False  # Last resort
    }


def initialize_proxy():
    """
    Initializes proxy configuration and stores it globally.
    Should be called once at plugin startup.
    
    For pystac_client 0.3.2 compatibility, also sets environment variables
    that the requests library will use automatically.
    """
    global PROXY_CONFIG
    
    if PROXY_CONFIG.get('initialized', False):
        logger.info("Proxy already initialized, skipping")
        log("Proxy already initialized", info=True, notify=False)
        return
    
    logger.info("=" * 60)
    logger.info("INITIALIZING PROXY AND SSL CONFIGURATION")
    logger.info("=" * 60)
    log("Initializing proxy and SSL configuration...", info=True, notify=False)
    
    config = detect_proxy_and_ssl()
    PROXY_CONFIG.update(config)
    PROXY_CONFIG['initialized'] = True
    
    # Configure environment variables for requests library (pystac_client 0.3.2 compatibility)
    import os
    if PROXY_CONFIG['enabled'] and PROXY_CONFIG.get('proxies'):
        http_proxy = PROXY_CONFIG['proxies'].get('http', '')
        https_proxy = PROXY_CONFIG['proxies'].get('https', http_proxy)
        
        if http_proxy:
            os.environ['HTTP_PROXY'] = http_proxy
            logger.info(f"Set HTTP_PROXY environment variable: {http_proxy}")
        if https_proxy:
            os.environ['HTTPS_PROXY'] = https_proxy
            logger.info(f"Set HTTPS_PROXY environment variable: {https_proxy}")
    
    # Configure SSL verification via environment variable
    if not PROXY_CONFIG.get('verify_ssl', True):
        # Disable SSL warnings if verification is disabled
        try:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            logger.info("urllib3 SSL warnings disabled")
        except:
            pass
        
        # Note: requests library doesn't support REQUESTS_CA_BUNDLE=False
        # We'll need to handle SSL verification differently in the client code
        os.environ['CURL_CA_BUNDLE'] = ''
        logger.warning("SSL verification disabled via environment (CURL_CA_BUNDLE cleared)")
    
    # Log final configuration
    logger.info("=" * 60)
    logger.info("FINAL PROXY CONFIGURATION:")
    logger.info(f"  Proxy enabled: {PROXY_CONFIG['enabled']}")
    if PROXY_CONFIG['enabled'] and PROXY_CONFIG.get('proxies'):
        logger.info(f"  Proxy URL: {PROXY_CONFIG['proxies'].get('http', 'N/A')}")
        log(f"Proxy enabled", info=True, notify=False)
    else:
        logger.info("  No proxy required")
        log("No proxy required", info=True, notify=False)
    
    logger.info(f"  SSL verification: {PROXY_CONFIG.get('verify_ssl', True)}")
    if not PROXY_CONFIG['verify_ssl']:
        logger.warning("  ⚠ SSL verification DISABLED")
        log("⚠ SSL verification disabled (VPN or corporate network detected)", info=False, notify=False)
    
    logger.info("=" * 60)


def get_proxy_config() -> Dict:
    """
    Returns the current proxy configuration.
    Initializes if not already done.
    
    Returns:
        Dict: Proxy configuration with 'proxies' and 'verify_ssl' keys
    """
    global PROXY_CONFIG
    
    if not PROXY_CONFIG.get('initialized', False):
        initialize_proxy()
    
    return {
        'proxies': PROXY_CONFIG.get('proxies'),
        'verify': PROXY_CONFIG.get('verify_ssl', True)
    }


def get_pystac_kwargs() -> Dict:
    """
    Returns kwargs suitable for pystac_client.Client.open()
    
    IMPORTANT: pystac_client 0.3.2 does NOT support 'request_kwargs' parameter.
    For compatibility, we pass parameters directly.
    
    Returns:
        Dict: Dictionary with parameters for pystac client
    """
    config = get_proxy_config()
    
    # For pystac_client 0.3.2, we cannot pass proxy/verify directly to Client.open()
    # These must be configured at the requests Session level or via environment variables
    # For now, return empty dict and rely on environment variables set by initialize_proxy()
    
    logger.debug("pystac_client 0.3.2 detected - using environment-based proxy configuration")
    
    # pystac_client 0.3.2 doesn't accept any http configuration parameters
    # It uses the requests library defaults which respect environment variables
    return {}
