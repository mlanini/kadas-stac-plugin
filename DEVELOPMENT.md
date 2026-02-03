# KADAS STAC Plugin - Development Guide# Development Guide



Technical documentation for developers contributing to the KADAS STAC Plugin.Technical documentation for KADAS STAC Plugin development.



------



## 🏗️ Architecture## 🏗️ Architecture



### High-Level Overview### Network Stack



```The plugin uses **QgsNetworkAccessManager** exclusively, matching KADAS Albireo 2 patterns:

┌─────────────────────────────────────────────────────────────┐

│                    KADAS Application                        │```python

└───────────────────────┬─────────────────────────────────────┘# Pattern used (identical to KADAS)

                        │from qgis.core import QgsNetworkAccessManager, QgsSettings

                        ▼from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply

┌─────────────────────────────────────────────────────────────┐

│                   Plugin Entry Point                         │nam = QgsNetworkAccessManager.instance()

│  main.py → KadasStac.initGui() → Auto-dock widget          │reply = nam.blockingGet(request)

└───────────────────────┬─────────────────────────────────────┘```

                        │

        ┌───────────────┴───────────────┐### Key Components

        │                               │

        ▼                               ▼#### 1. **QgisStacApiIO** (`api/qgis_stac_io.py`)

┌─────────────────┐           ┌─────────────────┐Custom StacApiIO implementation using Qt network stack:

│   GUI Layer     │           │   API Layer     │- **Purpose**: Avoid Python SSL module dependency

│  (gui/*.py)     │◄─────────►│  (api/*.py)     │- **Pattern**: Qt blocking HTTP requests

└─────────────────┘           └─────────────────┘- **Features**: URL normalization, redirect handling, Referer header

        │                               │

        │                               ▼```python

        │                   ┌─────────────────────┐class QgisStacApiIO(DefaultStacIO):

        │                   │  pystac_client      │    def request(self, href, method='GET', ...):

        └──────────────────►│  QgisStacApiIO      │        # Normalize URL (add https:// if missing)

                            └─────────────────────┘        # Create QNetworkRequest with redirect support

                                        │        # Add Referer header from QGIS Settings

                                        ▼        # Execute blocking request via QgsNetworkAccessManager

                            ┌─────────────────────┐        # Handle errors and return response

                            │ QgsNetworkAccess    │```

                            │ Manager (Qt Stack)  │

                            └─────────────────────┘#### 2. **Proxy Handler** (`api/proxy_handler.py`)

```Automatic proxy detection based on swisstopo/topo-rapidmapping:

- **Configuration**: QGIS Settings (no config file)

---- **Detection**: Automatic via `detect_proxy_requirement()`

- **VPN Support**: Heuristic detection

## 🔌 Network Stack- **SSL**: Always enabled (Qt handles certificates)



### KADAS Compatibility Pattern```python

# Global configuration cache

The plugin uses **QgsNetworkAccessManager** exclusively to match KADAS Albireo 2 patterns:PROXY_CONFIG = {

    'enabled': False,

```python    'proxy_url': None,

# Pattern used (identical to KADAS C++ code)    'verify_ssl': True,

from qgis.core import QgsNetworkAccessManager, QgsSettings    'is_vpn': False,

from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply    'qgis_settings': {}

}

nam = QgsNetworkAccessManager.instance()

reply = nam.blockingGet(request)# Lazy initialization

```def initialize_proxy():

    # Reads from QgsSettings

**Why?**    # Tests connection

- ✓ Respects QGIS proxy settings (corporate environments)    # Detects VPN

- ✓ Uses system SSL certificates (no Python SSL module)    # Caches result

- ✓ Handles authentication (QGIS auth manager)```

- ✓ 100% compatible with KADAS Albireo 2

#### 3. **Main Plugin** (`main.py`)

### QgisStacApiIO ImplementationPlugin lifecycle management:

- **Auto-docking**: Calls `self.run()` in `initGui()`

**File**: `src/kadas_stac/api/qgis_stac_io.py`- **Cleanup**: Complete disconnect/deleteLater in `unload()`

- **Dock Position**: `Qt.RightDockWidgetArea`

Custom `StacApiIO` that replaces `requests` library with Qt network stack:

### Network Patterns vs KADAS Albireo 2

```python

class QgisStacApiIO(DefaultStacIO):| Component | KADAS Albireo 2 (C++) | kadas-stac-plugin (Python) |

    """Custom StacApiIO using QGIS network stack."""|-----------|----------------------|---------------------------|

    | Network Manager | `QgsNetworkAccessManager::instance()` | `QgsNetworkAccessManager.instance()` |

    def request(self, href, method='GET', headers=None):| Requests | `blockingGet(request)` | `nam.blockingGet(request)` |

        # 1. Normalize URL (add https:// if missing)| Request Creation | `QNetworkRequest(QUrl(url))` | `QNetworkRequest(QUrl(href))` |

        href = self._normalize_url(href)| Referer Header | `req.setRawHeader("Referer", ...)` | `request.setRawHeader(b"Referer", ...)` |

        | Redirects | Qt automatic | `FollowRedirectsAttribute + max 5` |

        # 2. Create Qt request with redirects| Proxy | QGIS Settings | QGIS Settings |

        request = QNetworkRequest(QUrl(href))| SSL | Qt SSL stack | Qt SSL stack |

        request.setAttribute(

            QNetworkRequest.FollowRedirectsAttribute, **Result**: 100% pattern compatibility

            True

        )---

        

        # 3. Add Referer header from QGIS Settings## 🔧 Development Setup

        referer = QgsSettings().value("/qgis/networkAndProxy/networkReferer", "")

        if referer:### Prerequisites

            request.setRawHeader(b"Referer", referer.encode())

        - Python 3.8+

        # 4. Execute blocking request- QGIS 3.0+ or KADAS Albireo 2

        nam = QgsNetworkAccessManager.instance()- Poetry (https://python-poetry.org/)

        reply = nam.blockingGet(request)

        ### Installation

        # 5. Handle errors

        if reply.error() != QNetworkReply.NoError:```bash

            raise Exception(f"HTTP {reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)}: {reply.errorString()}")# Clone repository

        git clone https://github.com/mlanini/kadas-stac-plugin.git

        # 6. Return responsecd kadas-stac-plugin

        content = bytes(reply.content())

        return QgsNetworkReplyContent(reply, content)# Install dependencies

```poetry install --no-dev



**Key Features**:# Install plugin to QGIS

- URL normalization (adds `https://` if missing)poetry run python admin.py install

- Automatic redirect following (max 5 redirects)

- Referer header support# Or create symlink for development

- Error handling with HTTP status codespoetry run python admin.py symlink

- Compatible with both `QNetworkReply` and `QgsNetworkReplyContent````



---### Build Commands



## 📂 Project Structure```bash

# Build plugin (without tests)

```poetry run python admin.py build

src/kadas_stac/

├── __init__.py                      ← Plugin entry point# Build with tests

├── main.py                          ← KadasStac plugin classpoetry run python admin.py build --tests

├── conf.py                          ← Settings management

├── utils.py                         ← Utility functions# Generate ZIP for distribution

│poetry run python admin.py generate-zip

├── api/                             ← STAC API communication

│   ├── base.py                      ← BaseClient (pystac_client wrapper)# Output: dist/kadas_stac.1.1.2.zip

│   ├── client.py                    ← High-level API operations```

│   ├── models.py                    ← Data models (ItemSearch, CatalogType)

│   ├── network.py                   ← ContentFetcherTask (QgsTask)### Development Workflow

│   └── qgis_stac_io.py              ← Custom StacApiIO implementation

│1. **Edit source files** in `src/kadas_stac/`

├── gui/                             ← User interface2. **Build plugin**: `poetry run python admin.py build`

│   ├── qgis_stac_widget.py          ← Main widget (auto-docked)3. **Install to QGIS**: `poetry run python admin.py install`

│   ├── connection_dialog.py         ← Catalog connection dialog4. **Restart QGIS** to reload plugin

│   ├── collection_dialog.py         ← Collection selection dialog5. **Test changes** in QGIS/KADAS

│   ├── assets_dialog.py             ← Asset loading dialog

│   ├── asset_widget.py              ← Single asset display**Hot Reload**: Use symlink mode for faster development:

│   ├── result_item_widget.py        ← Search result item```bash

│   ├── result_item_model.py         ← Result list modelpoetry run python admin.py symlink

│   ├── queryable_property.py        ← Query builder widget# Now changes to src/ are reflected immediately (restart QGIS to reload)

│   └── json_highlighter.py          ← JSON syntax highlighter```

│

├── definitions/                     ← Constants and definitions---

│   ├── catalog.py                   ← Default catalog list

│   └── constants.py                 ← App constants## 🧪 Testing

│

├── jobs/                            ← Background tasks### Network Connectivity Tests

│   └── token_manager.py             ← Authentication token manager

│**Quick Test** (Python Console):

├── lib/                             ← Bundled dependencies```python

│   ├── pystac/                      ← STAC libraryexec(open('test/quick_network_test.py').read())

│   ├── pystac_client/               ← STAC API client```

│   ├── pydantic/                    ← Data validation

│   └── planetary_computer/          ← Microsoft Planetary Computer auth**Full Test Suite**:

│```bash

└── ui/                              ← Qt Designer UI filespython test_network.py

    ├── qgis_stac_main.ui```

    ├── connection_dialog.ui

    └── ...**Unit Tests**:

``````bash

python -m unittest test.test_network_connectivity -v

---```



## 🎯 Core ComponentsSee [TESTING.md](TESTING.md) for complete documentation.



### 1. Plugin Lifecycle### Test Coverage



**File**: `src/kadas_stac/main.py`Tests verify KADAS compatibility:

- ✅ QgsNetworkAccessManager availability

```python- ✅ QGIS Settings (proxy configuration)

class KadasStac:- ✅ HTTPS connection to data.geo.admin.ch

    def __init__(self, iface):- ✅ QgisStacApiIO implementation

        self.iface = iface- ✅ Proxy Handler functionality

        self.dock_widget = None- ✅ URL normalization

    - ✅ Redirect following

    def initGui(self):- ✅ Referer header setting

        """Plugin initialization (called by KADAS)."""

        # Auto-dock widget on startup---

        self.run()

    ## 📁 Project Structure

    def run(self):

        """Create and dock main widget."""```

        if not self.dock_widget:kadas-stac-plugin/

            self.dock_widget = QgisStacWidget(self.iface)├── src/

            self.iface.addDockWidget(│   └── kadas_stac/

                Qt.RightDockWidgetArea,│       ├── main.py                  # Plugin entry point

                self.dock_widget│       ├── api/

            )│       │   ├── qgis_stac_io.py     # Qt network integration ⭐

        else:│       │   ├── proxy_handler.py    # Proxy detection ⭐

            self.dock_widget.show()│       │   ├── network.py          # STAC API client

    │       │   ├── models.py           # Data models

    def unload(self):│       │   └── client.py           # API client wrapper

        """Cleanup (called by KADAS)."""│       ├── gui/

        if self.dock_widget:│       │   ├── kadas_stac_widget.py  # Main UI widget

            self.iface.removeDockWidget(self.dock_widget)│       │   ├── connection_dialog.py  # Connection settings

            self.dock_widget.deleteLater()│       │   └── ...

            self.dock_widget = None│       ├── lib/

```│       │   ├── pystac/             # Bundled pystac library

│       │   ├── pystac_client/      # Bundled pystac_client

### 2. Settings Management│       │   └── planetary_computer/ # Microsoft PC library

│       └── ui/                     # Qt Designer UI files

**File**: `src/kadas_stac/conf.py`├── test/

│   ├── quick_network_test.py       # Quick console test

```python│   └── test_network_connectivity.py # Full test suite

class ConnectionSettings:├── test_network.py                 # Standalone test runner

    """STAC catalog connection settings."""├── admin.py                        # Build & deployment script

    name: str├── pyproject.toml                  # Poetry dependencies

    url: str├── README.md                       # Main documentation

    catalog_type: str = "api"  # "api" or "static"├── DEVELOPMENT.md                  # This file

    auth_config: str = None├── TESTING.md                      # Testing guide

    headers: Dict[str, str] = {}└── CHANGELOG.md                    # Version history

    ```

    @classmethod

    def from_qgs_settings(cls, name):---

        """Load from QGIS settings."""

        settings = QgsSettings()## 🔌 Plugin Hooks

        settings.beginGroup(f"kadas_stac/connections/{name}")

        return cls(### Initialization (`initGui`)

            name=name,```python

            url=settings.value("url"),def initGui(self):

            catalog_type=settings.value("catalog_type", "api"),    # Create actions and menus

            auth_config=settings.value("auth_config"),    # Setup toolbar buttons

            headers=json.loads(settings.value("headers", "{}"))    # Initialize dock widget

        )    self.run()  # Auto-show dock (KADAS feature)

    ```

    def save(self):

        """Persist to QGIS settings."""### Cleanup (`unload`)

        settings = QgsSettings()```python

        settings.beginGroup(f"kadas_stac/connections/{self.name}")def unload(self):

        settings.setValue("url", self.url)    # Disconnect signals

        settings.setValue("catalog_type", self.catalog_type)    self.dock_widget.visibilityChanged.disconnect(...)

        settings.setValue("auth_config", self.auth_config)    

        settings.setValue("headers", json.dumps(self.headers))    # Close and delete widgets

```    self.dock_widget.close()

    self.dock_widget.deleteLater()

**Storage Location**: QGIS settings file    

- Windows: `C:\Users\<username>\.kadas\kadas.ini`    # Clear menus

- Linux: `~/.kadas/kadas.ini`    self.menu.clear()

- Mac: `~/Library/Preferences/org.kadas.ini`    self.menu.deleteLater()

```

### 3. STAC API Client

### Run (`run`)

**File**: `src/kadas_stac/api/base.py````python

def run(self):

```python    # Create or show dock widget

class BaseClient:    if self.dock_widget is None:

    """Wrapper around pystac_client.Client."""        self.dock_widget = KadasStacDockWidget(...)

            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)

    def __init__(self, url, catalog_type="api", headers=None):    

        self.url = url    self.dock_widget.show()

        self.catalog_type = catalog_type    self.dock_widget.raise_()

        self.headers = headers or {}```

        self.client = None

    ---

    def open(self):

        """Open STAC catalog with custom StacApiIO."""## 🐛 Debugging

        stac_io = QgisStacApiIO(headers=self.headers)

        self.client = Client.open(### Enable Debug Logging

            self.url,

            stac_io=stac_io```python

        )# In QGIS Python Console:

        return self.clientimport logging

    logging.basicConfig(level=logging.DEBUG)

    def search(self, **kwargs):

        """Execute STAC search."""# Re-import plugin module

        if self.catalog_type == "static":from kadas_stac.api import qgis_stac_io

            # Use recursive navigation```

            return self._search_static(**kwargs)

        else:### Common Issues

            # Use API search

            return self.client.search(**kwargs)**SSL Module Not Available**:

```- ✅ **Solution**: Plugin uses Qt SSL stack (no Python SSL module needed)



### 4. Background Task Execution**Protocol Unknown Error**:

- ✅ **Solution**: URL normalization auto-adds `https://` prefix

**File**: `src/kadas_stac/api/network.py`

**Proxy Not Working**:

```python- Check QGIS Settings → Options → Network

class ContentFetcherTask(QgsTask):- Verify proxy enabled and correct host/port

    """Background task for STAC API operations."""- Restart QGIS after changing proxy settings

    

    def __init__(self, url, search_params, catalog_type="api"):**VPN Issues**:

        super().__init__("STAC Search", QgsTask.CanCancel)- Connect VPN before starting QGIS/KADAS

        self.url = url- Qt SSL stack handles VPN certificates automatically

        self.search_params = search_params

        self.catalog_type = catalog_type---

        self.response = None

        self.error_message = None## 📦 Dependencies

    

    def run(self):### Runtime (Bundled in plugin)

        """Execute task (runs in background thread)."""- pystac

        try:- pystac_client

            # 1. Open client- planetary_computer (Microsoft)

            client = Client.open(

                self.url,### Build-time (Poetry)

                stac_io=QgisStacApiIO()- httpx (for admin.py)

            )- toml (for admin.py)

            - typer (for admin.py)

            # 2. Attempt API search- mkdocs (for documentation)

            if self.catalog_type == "api":

                try:### No External Runtime Dependencies

                    search = client.search(**self.search_params)The plugin bundles all Python dependencies and uses Qt/QGIS libraries exclusively at runtime.

                    items = list(search.items())

                except (NotImplementedError, Exception) as e:---

                    # Automatic fallback to static mode

                    if self._should_fallback(e):## 🚀 Release Process

                        return self._try_static_fallback()

                    raise1. Update version in `pyproject.toml`

            2. Update `CHANGELOG.md`

            # 3. Static catalog navigation3. Build distribution: `poetry run python admin.py generate-zip`

            else:4. Test ZIP installation in clean QGIS/KADAS

                return self._try_static_fallback()5. Create GitHub release

            6. Upload ZIP to release assets

            self.response = self._prepare_items(items)

            return True---

            

        except Exception as e:## 🤝 Contributing

            self.error_message = str(e)

            return False1. Fork repository

    2. Create feature branch

    def finished(self, result):3. Make changes

        """Called when task completes (runs in main thread)."""4. Run tests: `python test_network.py`

        if result:5. Build and test: `poetry run python admin.py generate-zip`

            # Emit success signal with results6. Create pull request

            self.taskCompleted.emit(self.response)

        else:---

            # Emit error signal

            self.taskFailed.emit(self.error_message)## 📞 Support

```

- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues

---- **Original Plugin**: https://github.com/stac-utils/qgis-stac-plugin


## 🔀 Static Catalog Support

### Architecture

STAC catalogs come in two flavors:

1. **STAC API** (Dynamic):
   - HTTP service with `/search` endpoint
   - Supports dynamic queries (bbox, datetime, collections, CQL2)
   - Example: `https://planetarycomputer.microsoft.com/api/stac/v1`

2. **Static Catalog** (Hierarchical):
   - JSON files with hierarchical structure
   - Browse via `rel: "child"` and `rel: "item"` links
   - Example: `https://maxar-opendata.s3.amazonaws.com/events/catalog.json`

### Automatic Fallback Mechanism

**Problem**: Many catalogs are configured as "API" but are actually static.

**Solution**: Automatic detection and fallback.

**File**: `src/kadas_stac/api/network.py`

```python
def _should_fallback(self, exception):
    """Detect if error suggests static catalog."""
    error_str = str(exception).lower()
    
    # Pattern matching
    is_search_error = (
        '/search' in error_str or
        'operation canceled' in error_str or
        'http 400' in error_str or
        'http 404' in error_str or
        'http 405' in error_str or
        'http 501' in error_str or
        'method not allowed' in error_str or
        'not found' in error_str
    )
    
    return (
        isinstance(exception, NotImplementedError) or
        is_search_error
    )

def _try_static_fallback(self):
    """Switch to static catalog mode."""
    try:
        # Recursive navigation
        items = get_all_items_recursive(
            self.client,
            max_items=100,
            max_depth=3,
            collection_filter=self.selected_collections
        )
        
        self.response = [
            self._prepare_single_item(item)
            for item in items
        ]
        
        # Warn user
        QgsMessageLog.logMessage(
            "⚠️ This catalog should be configured as 'Static Catalog' type",
            "STAC",
            Qgis.Warning
        )
        
        return True
    except Exception as e:
        self.error_message = f"Static fallback failed: {str(e)}"
        return False
```

**Trigger Patterns**:
- `NotImplementedError` from pystac_client
- `Operation canceled` (Qt timeout)
- HTTP 400 Bad Request
- HTTP 404 Not Found
- HTTP 405 Method Not Allowed
- HTTP 501 Not Implemented
- Error message contains `/search` or `not found`

**Examples**:
- ✓ Digital Earth Africa: Timeout → Auto-fallback
- ✓ Maxar Open Data: 404 on /search → Auto-fallback
- ✗ ESA Catalog: HTTP 405 (OpenSearch, not STAC)

### Recursive Navigation

**File**: `src/kadas_stac/api/client.py`

```python
def get_all_items_recursive(
    catalog,
    max_items=100,
    max_depth=3,
    collection_filter=None
):
    """Recursively navigate static catalog."""
    items = []
    visited = set()
    
    def traverse(node, depth=0):
        # Stop conditions
        if depth > max_depth:
            return
        if len(items) >= max_items:
            return
        if id(node) in visited:
            return
        
        visited.add(id(node))
        
        # Collect items
        for item in node.get_items():
            if collection_filter:
                if item.collection_id not in collection_filter:
                    continue
            items.append(item)
            if len(items) >= max_items:
                return
        
        # Traverse children
        for child in node.get_children():
            traverse(child, depth + 1)
    
    traverse(catalog)
    return items
```

**Performance**:
- Max depth: 3 levels (configurable)
- Max items: 100 (safety limit)
- Visited tracking: Avoids infinite loops
- Collection filter: Scopes search to selected collections

---

## 🛠️ Development Workflow

### Setup

```powershell
# Clone repository
git clone https://github.com/mlanini/kadas-stac-plugin.git
cd kadas-stac-plugin

# Create virtual environment (optional, for IDE support)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies (for development)
pip install poetry
poetry install

# Install pre-commit hooks
pre-commit install
```

### Building

```powershell
# Generate plugin ZIP
python admin.py generate-zip

# Output: dist/kadas_stac.0.1.0.zip
```

### Installing for Development

```powershell
# Option 1: Symlink (recommended for development)
cd "C:\Users\<username>\.kadas\python\plugins"
New-Item -ItemType SymbolicLink -Name "kadas_stac" -Target "C:\path\to\kadas-stac-plugin\src\kadas_stac"

# Option 2: Copy
Copy-Item -Recurse "C:\path\to\kadas-stac-plugin\src\kadas_stac" "C:\Users\<username>\.kadas\python\plugins\kadas_stac"
```

### Testing

See [test/README.md](test/README.md) for comprehensive testing guide.

**Quick Test**:
```python
# In KADAS Python Console
exec(open('test/quick_network_test.py').read())
```

**Full Test Suite**:
```powershell
cd test
python test_suite.py
```

### Debugging

#### Enable Debug Logging

```python
# In KADAS Python Console
from kadas_stac.logger import get_logger
logger = get_logger(level="DEBUG")
```

**Log Location**: `~/.kadas/stac.log`

#### Debug Specific Component

```python
# Example: Debug network requests
from kadas_stac.api.qgis_stac_io import QgisStacApiIO

io = QgisStacApiIO()
response = io.request("https://data.geo.admin.ch/api/stac/v1/")
print(response.content)
```

#### PyCharm Remote Debugging

```python
# 1. Install pydevd-pycharm in QGIS Python
import subprocess
subprocess.call([
    "C:\\Program Files\\QGIS 3.40.7\\apps\\Python312\\python.exe",
    "-m", "pip", "install", "pydevd-pycharm"
])

# 2. Add to plugin code
import pydevd_pycharm
pydevd_pycharm.settrace(
    'localhost',
    port=12345,
    stdoutToServer=True,
    stderrToServer=True
)

# 3. Start PyCharm debug server (port 12345)
```

---

## 📝 Code Style

### Python Style Guide

Follow PEP 8 with these exceptions:
- Line length: 100 characters (not 79)
- String quotes: Double quotes preferred
- Imports: Group by stdlib, third-party, local

```python
# Standard library
import os
import sys
from typing import Optional, Dict

# Third-party
from qgis.core import QgsSettings, QgsMessageLog
from qgis.PyQt.QtCore import Qt

# Local
from kadas_stac.conf import ConnectionSettings
from kadas_stac.api.base import BaseClient
```

### Type Hints

Use type hints for all public functions:

```python
def search_items(
    catalog_url: str,
    bbox: Optional[List[float]] = None,
    collections: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """Search STAC items.
    
    Args:
        catalog_url: STAC catalog URL
        bbox: Bounding box [west, south, east, north]
        collections: Collection IDs to search
    
    Returns:
        List of STAC items as dictionaries
    """
    ...
```

### Documentation

Use Google-style docstrings:

```python
def complex_function(param1, param2):
    """Short description.
    
    Longer description with more details about what
    the function does and how it works.
    
    Args:
        param1 (str): Description of param1.
        param2 (int): Description of param2.
    
    Returns:
        bool: Description of return value.
    
    Raises:
        ValueError: When param1 is invalid.
        ConnectionError: When network fails.
    
    Example:
        >>> result = complex_function("test", 42)
        >>> print(result)
        True
    """
    ...
```

---

## 🧪 Testing Strategy

### Test Pyramid

```
        /\
       /  \  E2E Tests (manual, full workflows)
      /____\
     /      \  Integration Tests (API + GUI)
    /________\
   /          \  Unit Tests (individual functions)
  /__________  \
```

### Unit Tests

**Target**: Individual functions, no external dependencies

```python
# test/test_url_normalization.py
def test_url_normalization():
    from kadas_stac.api.qgis_stac_io import QgisStacApiIO
    
    io = QgisStacApiIO()
    
    assert io._normalize_url("example.com") == "https://example.com"
    assert io._normalize_url("http://example.com") == "http://example.com"
    assert io._normalize_url("https://example.com") == "https://example.com"
```

### Integration Tests

**Target**: Component interactions, mock external services

```python
# test/test_stac_api_client_functions.py
def test_search_with_bbox():
    from kadas_stac.api.base import BaseClient
    
    client = BaseClient("https://data.geo.admin.ch/api/stac/v1/")
    client.open()
    
    items = client.search(bbox=[5.96, 45.82, 10.49, 47.81])
    assert len(items) > 0
    assert all(item.bbox for item in items)
```

### E2E Tests

**Target**: Full workflows, real catalogs

```python
# Manual test checklist:
# 1. Connect to catalog
# 2. Search with filters
# 3. Load footprints
# 4. Load raster asset
# 5. Download asset
# 6. Verify layers in map
```

---

## 🐛 Debugging Common Issues

### SSL Certificate Errors

**Symptoms**:
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**Causes**:
- Corporate SSL inspection
- Self-signed certificates
- Outdated certificate store

**Solutions**:

1. **Configure QGIS proxy** (Settings → Network):
   ```
   Proxy Type: HttpProxy
   Host: proxy.company.com
   Port: 8080
   ```

2. **Add CA certificate**:
   ```powershell
   # Windows
   $env:REQUESTS_CA_BUNDLE = "C:\certs\company-ca-bundle.crt"
   ```

3. **Disable SSL verification** (NOT RECOMMENDED):
   ```python
   # In QgisStacApiIO
   request.setSslConfiguration(...)
   ```

### "Operation canceled" Errors

**Symptoms**:
```
Error in getting items from catalog: HTTP None: Operation canceled
```

**Causes**:
- Catalog is static, not API
- `/search` endpoint timeout
- Network connectivity issues

**Solutions**:

1. **Configure as Static Catalog**:
   - Edit connection → Catalog Type → "Static Catalog"
   - Plugin will use recursive navigation

2. **Check automatic fallback**:
   - Look for warning: "This catalog should be configured as 'Static Catalog' type"
   - If warning appears, fallback worked but connection should be reconfigured

3. **Increase timeout** (if truly slow network):
   ```python
   # In QgisStacApiIO
   request.setTransferTimeout(30000)  # 30 seconds
   ```

### HTTP 405 Method Not Allowed

**Symptoms**:
```
HTTP 405: Method Not Allowed
```

**Causes**:
- Catalog is OpenSearch, not STAC
- Wrong endpoint URL

**Solutions**:

1. **Verify STAC conformance**:
   ```python
   import requests
   response = requests.get(f"{catalog_url}/conformance")
   print(response.json())
   
   # Should contain "https://api.stacspec.org/..."
   ```

2. **Remove incompatible catalog**:
   - OpenSearch catalogs (ESA, FedEO) are NOT STAC
   - Use STAC-specific catalogs only

### Download Errors

**Symptoms**:
```
'QNetworkReply' object has no attribute 'content'
```

**Cause**: Wrong network reply type

**Solution**: Use `readAll()` instead of `content()`:

```python
# WRONG
content = reply.content()

# CORRECT
content = reply.readAll()  # Returns QByteArray
data = content.data()       # Convert to bytes
```

---

## 🔐 Authentication

### Planetary Computer

**File**: `src/kadas_stac/lib/planetary_computer/sas.py`

```python
from planetary_computer import sign_url

# Automatically signs URLs with SAS tokens
signed_url = sign_url(asset_href)
```

**How it works**:
1. Detects `planetarycomputer.microsoft.com` URLs
2. Requests temporary SAS token from API
3. Appends token to asset URL
4. Token valid for 1 hour

### Custom Headers

```python
# In connection settings
headers = {
    "Authorization": "Bearer <token>",
    "X-API-Key": "<api-key>"
}

connection = ConnectionSettings(
    name="Custom Catalog",
    url="https://api.custom.com/stac",
    headers=headers
)
connection.save()
```

### QGIS Auth Manager

```python
# In connection dialog
auth_config_id = "my_auth_config"

connection = ConnectionSettings(
    name="Authenticated Catalog",
    url="https://api.secure.com/stac",
    auth_config=auth_config_id
)
```

---

## 📦 Dependencies

### Bundled Libraries

Located in `src/kadas_stac/lib/`:

- **pystac** 1.10.1: STAC core library
- **pystac_client** 0.8.5: STAC API client
- **pydantic** 1.10.18: Data validation
- **planetary_computer** 1.0.0: Microsoft Planetary Computer auth

**Why bundled?**
- Avoid dependency conflicts
- Ensure specific versions
- Simplify installation (no pip required)

### External Dependencies

Provided by QGIS/KADAS:

- Qt 5.15+
- PyQt5
- QGIS Core libraries
- QGIS Network libraries

---

## 🚀 Release Process

### Version Bumping

1. Update version in `pyproject.toml`:
   ```ini
   version = "0.2.0"
   ```

2. Update `CHANGELOG.md`:
   ```markdown
   ## [0.2.0] - 2026-03-01
   
   ### Fixed
   - Fixed download error with certain catalogs
   ```

3. Commit:
   ```powershell
   git add pyproject.toml CHANGELOG.md
   git commit -m "Bump version to 0.2.0"
   git tag v0.2.0
   git push origin main --tags
   ```

### Building Release

```powershell
# Generate plugin ZIP
python admin.py generate-zip

# Output: dist/kadas_stac.0.2.0.zip
```

### Publishing

1. **GitHub Release**:
   - Create release from tag
   - Attach `kadas_stac.0.2.0.zip`
   - Copy CHANGELOG entry to release notes

2. **QGIS Plugin Repository** (future):
   - Upload ZIP to https://plugins.qgis.org/
   - Fill metadata form
   - Submit for review

---

## 🤝 Contributing

### Workflow

1. **Fork** repository
2. **Create branch**: `git checkout -b feature/my-feature`
3. **Make changes** with tests
4. **Run tests**: `python test/test_suite.py`
5. **Commit**: `git commit -m "Add my feature"`
6. **Push**: `git push origin feature/my-feature`
7. **Open Pull Request**

### Pull Request Checklist

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts
- [ ] Commit messages are clear

### Code Review Process

1. Automated checks (future: GitHub Actions)
2. Manual code review by maintainer
3. Testing on Windows/Linux/Mac
4. Merge to main
5. Tag release

---

## 📚 Resources

### STAC Specification
- **STAC Spec**: https://stacspec.org/
- **STAC API**: https://github.com/radiantearth/stac-api-spec
- **pystac**: https://pystac.readthedocs.io/
- **pystac-client**: https://pystac-client.readthedocs.io/

### QGIS Development
- **PyQGIS Cookbook**: https://docs.qgis.org/latest/en/docs/pyqgis_developer_cookbook/
- **QGIS API**: https://qgis.org/pyqgis/latest/
- **Qt Documentation**: https://doc.qt.io/qt-5/

### Project Links
- **Repository**: https://github.com/mlanini/kadas-stac-plugin
- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **User Guide**: [GUIDE.md](GUIDE.md)
- **Testing**: [test/README.md](test/README.md)

---

**Last Updated**: 2026-02-03 | **Version**: 0.1.0
