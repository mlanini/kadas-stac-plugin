# KADAS STAC Plugin

[![GitHub release](https://img.shields.io/github/v/release/mlanini/kadas-stac-plugin?include_prereleases)](https://github.com/mlanini/kadas-stac-plugin/releases)
[![License](https://img.shields.io/github/license/mlanini/kadas-stac-plugin)](LICENSE)

**STAC API Browser for KADAS Albireo 2**

Browse and load geospatial data from [STAC API](https://stacspec.org/) catalogs directly in KADAS Albireo 2.

**Origin**: Fork of [qgis-stac-plugin](https://github.com/stac-utils/qgis-stac-plugin) by Kartoza, optimized for KADAS.

---

## ✨ Features

- 🔍 **19 STAC API Catalogs**: Swiss Federal Geodata, Planetary Computer, Copernicus, NASA, USGS, and more
- 📂 **Static Catalogs**: Hierarchical navigation (Maxar Open Data, USGS Landsat)
- 🔍 **Advanced Search**: Date range, spatial extent, cloud cover, collections
- 🗺️ **Load Layers**: Add footprints or load assets (COG, GeoTIFF, GeoJSON)
- 📥 **Download Manager**: Auto-download with layer loading, S3 support via GDAL VSI
- 🔐 **Authentication**: Basic Auth, OAuth2, API Key (Planetary Computer SAS tokens)
- 🌐 **Enterprise Ready**: Automatic proxy/VPN support, SSL via Qt

---

## 📦 Installation

### From ZIP (Recommended)

1. Download latest release: [`kadas_stac.0.1.0.zip`](https://github.com/mlanini/kadas-stac-plugin/releases/latest)
2. KADAS → **Plugins** → **Manage and Install Plugins** → **Install from ZIP**
3. Select ZIP file → **Install Plugin**
4. Enable plugin if not auto-enabled

### From Source

```bash
git clone https://github.com/mlanini/kadas-stac-plugin.git
cd kadas-stac-plugin
python admin.py generate-zip
# Install dist/kadas_stac.0.1.0.zip in KADAS
```

---

## 🚀 Quick Start

1. KADAS → **STAC API Browser** → **New connection**
2. Select collection → Apply filters → **Search**
3. Select items → **Add footprints** or **View assets**

---

## 📚 Documentation

- [CHANGELOG.md](CHANGELOG.md) - Version history
- [GUIDE.md](GUIDE.md) - User guide with examples
- [DEVELOPMENT.md](DEVELOPMENT.md) - Technical guide
- [test/README.md](test/README.md) - Testing documentation

---

## 🌐 Available Catalogs

### STAC API Catalogs (19)

| Catalog | Provider | Region | Collections |
|---------|----------|--------|-------------|
| **Swiss Federal Geodata** | swisstopo | Switzerland | ~100 |
| **Microsoft Planetary Computer** | Microsoft | Global | 100+ |
| **Earth Search** | Element 84 | Global | Landsat, Sentinel |
| **Copernicus Data Space** | ESA | Global | 1000+ |
| **NASA CMR STAC** | NASA | Global | Earth Science |
| **USGS Landsat Collection 2** | USGS | Global | Landsat |
| **Digital Earth Africa** | AfriGEO | Africa | Regional |
| **Digital Earth Australia** | Geoscience AU | Australia | Regional |

### Static Catalogs (2)

- **Maxar Open Data**: Event imagery (disasters, conflicts)
- **USGS Landsat**: Static archive browser

---

## 🔧 Configuration

### Proxy Settings

Plugin uses **QGIS Network Settings** automatically:
- QGIS → **Settings** → **Options** → **Network** → **Proxy**
- Configure once, all QGIS plugins inherit

### Authentication

**Microsoft Planetary Computer** (S3 assets):
- Automatic SAS token retrieval (no config needed)

**Custom Catalogs**:
- **New Connection** → **Authentication** tab
- Select: Basic, OAuth2, API Header

### Static Catalog Type

If catalog has "Operation canceled" or "HTTP 404/405" errors:
1. **Edit Connection**
2. Change **Catalog Type** to **"Static Catalog (hierarchical)"**
3. Plugin uses recursive navigation instead of `/search`

---

## 🧪 Testing

Quick network test (copy/paste in KADAS Python Console):

```python
exec(open('test/quick_network_test.py').read())
```

Full test suite:

```bash
cd test
python test_network.py  # Network connectivity
python test_suite.py    # Full plugin tests
```

See [test/README.md](test/README.md) for details.

---

## 🐛 Troubleshooting

### "SSL module not available"
**Fixed in v0.1.0** - Uses Qt SSL stack instead of Python SSL

### "Operation canceled" on search
**Auto-fallback in v0.1.0** - Tries static catalog mode automatically
- Manually: Edit connection → Catalog Type → "Static Catalog"

### Download errors
- Check **View Log** in plugin menu
- Log location: `~/.kadas/stac.log`

### Proxy/VPN issues
- Ensure QGIS proxy settings are correct
- Test: `quick_network_test.py` (see Testing section)

---

## 🤝 Contributing

1. Fork repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Run tests: `cd test && python test_suite.py`
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature/my-feature`
6. Create Pull Request

See [DEVELOPMENT.md](DEVELOPMENT.md) for architecture details.

---

## 📜 License

**GNU General Public License v3.0** - See [LICENSE](LICENSE)

**Copyright** © 2026 Michael Lanini (KADAS fork)  
**Original** © 2024 Kartoza (qgis-stac-plugin)

---

## 🔗 Links

- **Repository**: https://github.com/mlanini/kadas-stac-plugin
- **Releases**: https://github.com/mlanini/kadas-stac-plugin/releases
- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues
- **STAC Specification**: https://stacspec.org/
- **KADAS**: https://github.com/kadas-albireo/kadas-albireo2

---

**Version**: 0.1.0 | **KADAS Compatibility**: Albireo 2.x | **Last Updated**: 2026-02-03
