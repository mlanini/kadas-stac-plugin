# Development Guide

Technical documentation for KADAS STAC Plugin development.

---

## 🏗️ Architecture

### Network Stack

The plugin uses **QgsNetworkAccessManager** exclusively, matching KADAS Albireo 2 patterns:

```python
# Pattern used (identical to KADAS)
from qgis.core import QgsNetworkAccessManager, QgsSettings
from qgis.PyQt.QtNetwork import QNetworkRequest, QNetworkReply

nam = QgsNetworkAccessManager.instance()
reply = nam.blockingGet(request)
```

### Key Components

#### 1. **QgisStacApiIO** (`api/qgis_stac_io.py`)
Custom StacApiIO implementation using Qt network stack:
- **Purpose**: Avoid Python SSL module dependency
- **Pattern**: Qt blocking HTTP requests
- **Features**: URL normalization, redirect handling, Referer header

```python
class QgisStacApiIO(DefaultStacIO):
    def request(self, href, method='GET', ...):
        # Normalize URL (add https:// if missing)
        # Create QNetworkRequest with redirect support
        # Add Referer header from QGIS Settings
        # Execute blocking request via QgsNetworkAccessManager
        # Handle errors and return response
```

#### 2. **Proxy Handler** (`api/proxy_handler.py`)
Automatic proxy detection based on swisstopo/topo-rapidmapping:
- **Configuration**: QGIS Settings (no config file)
- **Detection**: Automatic via `detect_proxy_requirement()`
- **VPN Support**: Heuristic detection
- **SSL**: Always enabled (Qt handles certificates)

```python
# Global configuration cache
PROXY_CONFIG = {
    'enabled': False,
    'proxy_url': None,
    'verify_ssl': True,
    'is_vpn': False,
    'qgis_settings': {}
}

# Lazy initialization
def initialize_proxy():
    # Reads from QgsSettings
    # Tests connection
    # Detects VPN
    # Caches result
```

#### 3. **Main Plugin** (`main.py`)
Plugin lifecycle management:
- **Auto-docking**: Calls `self.run()` in `initGui()`
- **Cleanup**: Complete disconnect/deleteLater in `unload()`
- **Dock Position**: `Qt.RightDockWidgetArea`

### Network Patterns vs KADAS Albireo 2

| Component | KADAS Albireo 2 (C++) | kadas-stac-plugin (Python) |
|-----------|----------------------|---------------------------|
| Network Manager | `QgsNetworkAccessManager::instance()` | `QgsNetworkAccessManager.instance()` |
| Requests | `blockingGet(request)` | `nam.blockingGet(request)` |
| Request Creation | `QNetworkRequest(QUrl(url))` | `QNetworkRequest(QUrl(href))` |
| Referer Header | `req.setRawHeader("Referer", ...)` | `request.setRawHeader(b"Referer", ...)` |
| Redirects | Qt automatic | `FollowRedirectsAttribute + max 5` |
| Proxy | QGIS Settings | QGIS Settings |
| SSL | Qt SSL stack | Qt SSL stack |

**Result**: 100% pattern compatibility

---

## 🔧 Development Setup

### Prerequisites

- Python 3.8+
- QGIS 3.0+ or KADAS Albireo 2
- Poetry (https://python-poetry.org/)

### Installation

```bash
# Clone repository
git clone https://github.com/mlanini/kadas-stac-plugin.git
cd kadas-stac-plugin

# Install dependencies
poetry install --no-dev

# Install plugin to QGIS
poetry run python admin.py install

# Or create symlink for development
poetry run python admin.py symlink
```

### Build Commands

```bash
# Build plugin (without tests)
poetry run python admin.py build

# Build with tests
poetry run python admin.py build --tests

# Generate ZIP for distribution
poetry run python admin.py generate-zip

# Output: dist/kadas_stac.1.1.2.zip
```

### Development Workflow

1. **Edit source files** in `src/kadas_stac/`
2. **Build plugin**: `poetry run python admin.py build`
3. **Install to QGIS**: `poetry run python admin.py install`
4. **Restart QGIS** to reload plugin
5. **Test changes** in QGIS/KADAS

**Hot Reload**: Use symlink mode for faster development:
```bash
poetry run python admin.py symlink
# Now changes to src/ are reflected immediately (restart QGIS to reload)
```

---

## 🧪 Testing

### Network Connectivity Tests

**Quick Test** (Python Console):
```python
exec(open('test/quick_network_test.py').read())
```

**Full Test Suite**:
```bash
python test_network.py
```

**Unit Tests**:
```bash
python -m unittest test.test_network_connectivity -v
```

See [TESTING.md](TESTING.md) for complete documentation.

### Test Coverage

Tests verify KADAS compatibility:
- ✅ QgsNetworkAccessManager availability
- ✅ QGIS Settings (proxy configuration)
- ✅ HTTPS connection to data.geo.admin.ch
- ✅ QgisStacApiIO implementation
- ✅ Proxy Handler functionality
- ✅ URL normalization
- ✅ Redirect following
- ✅ Referer header setting

---

## 📁 Project Structure

```
kadas-stac-plugin/
├── src/
│   └── kadas_stac/
│       ├── main.py                  # Plugin entry point
│       ├── api/
│       │   ├── qgis_stac_io.py     # Qt network integration ⭐
│       │   ├── proxy_handler.py    # Proxy detection ⭐
│       │   ├── network.py          # STAC API client
│       │   ├── models.py           # Data models
│       │   └── client.py           # API client wrapper
│       ├── gui/
│       │   ├── kadas_stac_widget.py  # Main UI widget
│       │   ├── connection_dialog.py  # Connection settings
│       │   └── ...
│       ├── lib/
│       │   ├── pystac/             # Bundled pystac library
│       │   ├── pystac_client/      # Bundled pystac_client
│       │   └── planetary_computer/ # Microsoft PC library
│       └── ui/                     # Qt Designer UI files
├── test/
│   ├── quick_network_test.py       # Quick console test
│   └── test_network_connectivity.py # Full test suite
├── test_network.py                 # Standalone test runner
├── admin.py                        # Build & deployment script
├── pyproject.toml                  # Poetry dependencies
├── README.md                       # Main documentation
├── DEVELOPMENT.md                  # This file
├── TESTING.md                      # Testing guide
└── CHANGELOG.md                    # Version history
```

---

## 🔌 Plugin Hooks

### Initialization (`initGui`)
```python
def initGui(self):
    # Create actions and menus
    # Setup toolbar buttons
    # Initialize dock widget
    self.run()  # Auto-show dock (KADAS feature)
```

### Cleanup (`unload`)
```python
def unload(self):
    # Disconnect signals
    self.dock_widget.visibilityChanged.disconnect(...)
    
    # Close and delete widgets
    self.dock_widget.close()
    self.dock_widget.deleteLater()
    
    # Clear menus
    self.menu.clear()
    self.menu.deleteLater()
```

### Run (`run`)
```python
def run(self):
    # Create or show dock widget
    if self.dock_widget is None:
        self.dock_widget = KadasStacDockWidget(...)
        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dock_widget)
    
    self.dock_widget.show()
    self.dock_widget.raise_()
```

---

## 🐛 Debugging

### Enable Debug Logging

```python
# In QGIS Python Console:
import logging
logging.basicConfig(level=logging.DEBUG)

# Re-import plugin module
from kadas_stac.api import qgis_stac_io
```

### Common Issues

**SSL Module Not Available**:
- ✅ **Solution**: Plugin uses Qt SSL stack (no Python SSL module needed)

**Protocol Unknown Error**:
- ✅ **Solution**: URL normalization auto-adds `https://` prefix

**Proxy Not Working**:
- Check QGIS Settings → Options → Network
- Verify proxy enabled and correct host/port
- Restart QGIS after changing proxy settings

**VPN Issues**:
- Connect VPN before starting QGIS/KADAS
- Qt SSL stack handles VPN certificates automatically

---

## 📦 Dependencies

### Runtime (Bundled in plugin)
- pystac
- pystac_client
- planetary_computer (Microsoft)

### Build-time (Poetry)
- httpx (for admin.py)
- toml (for admin.py)
- typer (for admin.py)
- mkdocs (for documentation)

### No External Runtime Dependencies
The plugin bundles all Python dependencies and uses Qt/QGIS libraries exclusively at runtime.

---

## 🚀 Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Build distribution: `poetry run python admin.py generate-zip`
4. Test ZIP installation in clean QGIS/KADAS
5. Create GitHub release
6. Upload ZIP to release assets

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests: `python test_network.py`
5. Build and test: `poetry run python admin.py generate-zip`
6. Create pull request

---

## 📞 Support

- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues
- **Original Plugin**: https://github.com/stac-utils/qgis-stac-plugin
