# Changelog# Changelog# Changelog



All notable changes to the KADAS STAC Plugin.



---All notable changes to the KADAS STAC Plugin.All notable changes to the KADAS STAC Plugin.



## [1.1.2] - 2026-01-31



### Added------



- **Qt Network Stack**: Custom `QgisStacApiIO` using `QgsNetworkAccessManager` (100% KADAS compatible)

- **Proxy Handler**: Automatic proxy detection from QGIS Settings

- **Auto-docking**: Plugin docks to right panel on startup## [1.1.2] - 2026-01-31## [1.1.2] - 2026-01-31

- **URL Normalization**: Auto-prefix `https://` if missing

- **Referer Header**: KADAS-compatible referer support

- **Network Tests**: Comprehensive test suite (quick_network_test.py, test_network.py)

- **Logging System**: File-based logging with rotation (`~/.kadas/stac.log`)### KADAS Albireo 2 Optimization### KADAS Albireo 2 Optimization

- **22 STAC Catalogs**: Added 15 new verified catalogs (Copernicus, ESA, NASA, etc.)



### Changed

#### Added#### Added

- **Network Stack**: Switched from Python requests to Qt `QgsNetworkAccessManager`

- **SSL Handling**: Uses Qt SSL stack exclusively (no Python SSL module dependency)- **Auto-docking**: Plugin automatically docks to right panel on startup- **Auto-docking**: Plugin automatically docks to right panel on startup

- **Proxy Configuration**: Reads from QGIS Settings (Settings → Network → Proxy)

- **Documentation**: Consolidated to 4 files (README, DEVELOPMENT, TESTING, CHANGELOG)- **Clean unload**: Complete cleanup when plugin is deactivated (disconnect signals, deleteLater)- **Clean unload**: Complete cleanup when plugin is deactivated (disconnect signals, deleteLater)

- **UI Branding**: Renamed from QGIS STAC to KADAS STAC throughout interface

- **Qt Network Stack**: Custom `QgisStacApiIO` using `QgsNetworkAccessManager` instead of requests library- **Qt Network Stack**: Custom `QgisStacApiIO` using `QgsNetworkAccessManager` instead of requests library

### Fixed

- **Proxy Handler**: Automatic proxy detection based on QGIS Settings (swisstopo/topo-rapidmapping pattern)- **Proxy Handler**: Automatic proxy detection based on QGIS Settings (swisstopo/topo-rapidmapping pattern)

- **AttributeError**: `QgsNetworkReplyContent.url` → using `QNetworkRequest.url()`

- **AttributeError**: Added `conforms_to()` and `assert_conforms_to()` methods- **URL Normalization**: Auto-prefix `https://` if missing from URLs- **URL Normalization**: Auto-prefix `https://` if missing from URLs

- **AttributeError**: Added `get_pages()` iterator for STAC API pagination

- **SSL Errors**: No more "SSL module not available" errors- **Referer Header**: KADAS-compatible referer header support (from QGIS Settings)- **Referer Header**: KADAS-compatible referer header support (from QGIS Settings)

- **Protocol Errors**: Better handling with URL normalization

- **Proxy Detection**: Auto-detects VPN and corporate proxy- **Network Tests**: Comprehensive test suite (quick_network_test.py, test_network.py, unittest suite)- **Network Tests**: Comprehensive test suite (quick_network_test.py, test_network.py, unittest suite)

- **VPN Support**: Works with corporate VPNs and SSL inspection

- **Logging System**: File-based logging with rotation (`~/.kadas/stac.log`)

### Technical

  - Configurable log levels (STANDARD, DEBUG, ERRORS, WARNING, CRITICAL)#### Changed

- Network patterns 100% identical to KADAS Albireo 2 catalog providers

- No external runtime dependencies (pystac/pystac_client bundled)  - Automatic stacktrace capture for CRITICAL errors- **Network Stack**: Switched from Python requests to Qt `QgsNetworkAccessManager` (100% KADAS compatibility)

- Lazy proxy initialization with global caching

- Comprehensive logging for debugging  - Log file viewer in Settings tab- **SSL Handling**: Uses Qt SSL stack exclusively (no Python SSL module dependency)



---- **Dock Widget Restrictions**: Limited to left/right docking areas only- **Proxy Configuration**: Reads from QGIS Settings GUI (Settings → Network → Proxy)



## [1.1.0] - 2022-07-18  - Prevents accidental docking to top/bottom panels- **Documentation**: Consolidated to 4 files (README, DEVELOPMENT, TESTING, CHANGELOG)



### Features  - Auto-docks to right on startup



- Data-driven filtering using STAC Queryables#### Fixed

- Multiple assets and footprints loading/downloading

- Minimizable plugin main window#### Changed- **AttributeError**: `QgsNetworkReplyContent` object has no attribute 'url' in qgis_stac_io.py

- Subscription key usage for SAS-based connections

- Support for COPC and netCDF layers- **Network Stack**: Switched from Python requests to Qt `QgsNetworkAccessManager` (100% KADAS compatibility)  - Now using `request.url().toString()` instead of `reply.url().toString()`

- New collection information dialog

- Auto-load assets after downloading- **SSL Handling**: Uses Qt SSL stack exclusively (no Python SSL module dependency)  - Pattern matches KADAS Albireo 2 catalog providers

- Support for CQL2-JSON filter language

- Moved sort/order controls to search tab- **Proxy Configuration**: Reads from QGIS Settings GUI (Settings → Network → Proxy)  - Fixed in both error handling and success logging paths



### Fixes- **Documentation**: Consolidated to 4 files (README, DEVELOPMENT, TESTING, CHANGELOG)- **AttributeError**: `QgisStacApiIO` object has no attribute 'conforms_to'



- Footprints layer loading workflow- **UI Branding**: Renamed from QGIS STAC to KADAS STAC throughout interface  - Added `conforms_to()` and `assert_conforms_to()` methods to QgisStacApiIO

- Connection dialog window title in edit mode

- Fallback to overview when thumbnail not available  - Methods check API conformance classes (COLLECTIONS, ITEM_SEARCH, FILTER, SORT, FIELDS)

- Display selected collections correctly

- Upgraded pystac-client library to 0.3.2#### Fixed  - Pattern matches pystac_client StacApiIO implementation



---- **AttributeError**: `QgsNetworkReplyContent` object has no attribute 'url'- **AttributeError**: `QgisStacApiIO` object has no attribute 'get_pages'



## [1.0.0] - 2022-01-13  - Changed `reply.url().toString()` to `request.url().toString()` in qgis_stac_io.py  - Added `get_pages()` iterator method for STAC API pagination



### Fixes  - Pattern matches KADAS Albireo 2 catalog providers  - Automatically follows 'next' links in responses



- Plugin UI lagging bug  - Fixed in both error handling and success logging paths (lines ~196 and ~212)  - Supports /collections and /search endpoints with pagination

- Assets loading and downloading workflow

- Support for vector-based assets (GeoJSON, GeoPackage)- **AttributeError**: `QgisStacApiIO` object has no attribute 'conforms_to'- **SSL Errors**: No more SSL module errors in restricted environments

- API page size (default: 10 items)

- Include file extension in downloaded files  - Added `conforms_to()` method to check API conformance classes- **Protocol Errors**: Better error handling for unknown protocols

- Updated UI tooltips

  - Added `assert_conforms_to()` method raising NotImplementedError if not conformant- **Proxy Detection**: Auto-detects VPN and corporate proxy settings

---

  - Supports COLLECTIONS, ITEM_SEARCH, FILTER, SORT, FIELDS conformance classes- **VPN Support**: Works with Swiss federal VPN (forti-vpn pattern)

## [1.0.0-pre] - 2022-01-11

  - Pattern matches pystac_client StacApiIO implementation

### Features

- **AttributeError**: `QgisStacApiIO` object has no attribute 'get_pages'  - Creazione oggetto `QMenu` invece di stringa

- Connection testing functionality

- Reworked filter and sort features  - Added `get_pages()` iterator method for STAC API pagination

- STAC API conformance classes support

- SAS token signing  - Automatically follows 'next' rel links in responses#### Fixed  - Gestione differenziata Kadas vs QGIS in `initGui()`

- Asset downloading and footprint loading

- Add STAC item assets as QGIS layers  - Returns Iterator[Dict] for memory-efficient pagination

- Plugin documentation

  - Supports /collections and /search endpoints with large result sets- **SSL Module Error**: `SSLError: Can't connect to HTTPS URL because the SSL module is not available`  - Cleanup migliorato in `unload()` con rimozione custom ribbon tab

---

- **SSL Errors**: No more "SSL module not available" errors in restricted environments

## [beta] - 2021-12-11

- **Protocol Errors**: Better error handling for unknown protocols with URL normalization- **Protocol Unknown Error**: HTTP → HTTPS redirect handling with URL normalization- **TECHNICAL**: Verifica proxy e VPN handling

### Initial Release

- **Proxy Detection**: Auto-detects VPN and corporate proxy settings from QGIS

- Browse and search STAC API catalogs

- Load STAC items as layers- **VPN Support**: Works with corporate VPNs (SSL inspection, certificates, routing)- **Proxy Detection**: Corporate proxy support with authentication  - Plugin compatibile con proxy HTTP/HTTPS (via QGIS settings)

- Connection management

- Asset preview and download

- Basic authentication support

- OAuth2 support via QGIS Auth Manager#### Technical Details- **VPN Support**: Works with VPN SSL inspection and corporate certificates  - Supporto VPN automatico (routing sistema operativo)

- Search result pagination

- Filter and sort support- Network patterns **100% identical** to KADAS Albireo 2 catalog providers

- Default STAC API catalogs

- No external runtime dependencies (pystac/pystac_client bundled in plugin)  - Auth STAC API via QGIS Auth Manager (OAuth2, API Key, Basic)

---

- Lazy proxy initialization with global configuration caching

## Version Comparison

- VPN heuristic detection (proxy enabled + successful connection = VPN active)#### Technical  - Usa `pystac_client` che rispetta proxy di sistema

| Version | KADAS Support | Network Stack | Proxy | SSL |

|---------|---------------|---------------|-------|-----|- Comprehensive logging for debugging and troubleshooting

| 1.1.2 | ✅ Albireo 2 | Qt (QgsNetworkAccessManager) | Auto | Qt SSL |

| 1.1.0 | ⚠️ Partial | Python requests | Manual | Python SSL |- Network patterns **100% identical** to KADAS Albireo 2 catalog providers- **DOCS**: Aggiunto `KADAS_INTEGRATION.md` con dettagli implementazione

| 1.0.0 | ❌ No | Python requests | Manual | Python SSL |

#### Documentation

---

- **DEVELOPMENT.md**: Technical documentation for developers- No external runtime dependencies (pystac/pystac_client bundled)- **DOCS**: Aggiunto `PROXY_VPN_ANALYSIS.md` con analisi tecnica network

## Upgrade Notes

- **TESTING.md**: Network connectivity testing guide

### From 1.1.0 to 1.1.2

- **README.md**: Updated with detailed Network & Proxy Support section- Lazy proxy initialization with global caching- **DOCS**: Aggiornato README con sezione Network & Proxy Support

**Breaking Changes**: None

- **CHANGELOG.md**: Complete version history with upgrade notes

**New Features**:

- Auto-docking to right panel- VPN heuristic detection (proxy + connection = VPN)

- Automatic proxy detection

- Full VPN support---

- KADAS Albireo 2 optimizations

- 15 new STAC catalogs- Comprehensive logging for debugging### 1.1.0 2022-07-18



**Configuration Changes**:## [1.1.0] - 2022-07-18

- Proxy: Configure in QGIS Settings (Settings → Options → Network → Proxy)

- No plugin-specific proxy configuration needed- Fix for footprints layer loading workflow

- SSL certificates handled automatically by Qt

### Features

**Testing**:

```python- Data-driven filtering using STAC Queryables---- Data driven filtering using STAC Queryables

# In KADAS Python Console:

exec(open('test/quick_network_test.py').read())- Multiple assets and footprints loading/downloading

```

- Minimizable plugin main window- Multiple assets and footprints loading and downloading

---

- Subscription key usage for SAS-based connections (Azure Blob Storage)

## Credits

- Support for COPC (Cloud Optimized Point Cloud) layers## [1.1.0] - 2022-07-18- Minimizeable plugin main window

- **Original Plugin**: QGIS STAC Plugin by Kartoza (sponsored by Microsoft)

- **KADAS Adaptation**: Michael Lanini (2026)- Support for netCDF layers

- **Proxy Handler**: Based on swisstopo/topo-rapidmapping

- **Network Patterns**: KADAS Albireo 2 catalog providers- New collection information dialog- Subscription key usage for SAS based connections



---- Auto-load assets after downloading



## Links- Support for CQL2-JSON filter language### Features- Support for COPC layers



- **Repository**: https://github.com/mlanini/kadas-stac-plugin- Moved sort and order controls to search tab

- **Original Plugin**: https://github.com/stac-utils/qgis-stac-plugin

- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues- Data-driven filtering using STAC Queryables- Support for netCDF layers

- **Releases**: https://github.com/mlanini/kadas-stac-plugin/releases

### Fixes

- Footprints layer loading workflow improvements- Multiple assets and footprints loading/downloading- New collection dialog

- Fixed connection dialog window title when in edit mode

- Fallback to overview image when item thumbnail asset is not available- Subscription key usage for SAS-based connections- Auto assets loading after downloading assets

- Display selected collections correctly in UI

- Upgraded pystac-client library to 0.3.2- Support for COPC layers- Fixed connection dialog window title when in edit mode



---- Support for netCDF layers- Fallback to overview when item thumbnail asset is not available



## [1.0.0] - 2022-01-13- New collection dialog- Display selected collections



### Fixes- Auto assets loading after downloading- Upgraded pystac-client library to 0.3.2

- Fixed plugin UI lagging bug

- Updates to loading and downloading assets workflow- Support for CQL2-JSON filter language

- Support for adding vector-based assets (GeoJSON, GeoPackage)

- Fixed API page size (default is now 10 items)### Fixes- Moved sort and order buttons to search tab

- Include file extension in downloaded files

- Updated UI with more descriptive tooltips- Footprints layer loading workflow



---- Connection dialog window title in edit mode### 1.0.0 2022-01-13



## [1.0.0-pre] - 2022-01-11- Fallback to overview when item thumbnail not available- Fix for plugin UI lagging bug.



### Features- Display selected collections correctly- Updates to loading and downloading assets workflow.

- Changed loading and downloading assets workflow

- Implemented connection testing functionality- Support for adding vector based assets eg. GeoJSON, GeoPackage

- Reworked filter and sort features on search item results

- Fetch STAC API conformance classes---- Fix API page size now default is 10 items.

- Added STAC API signing using SAS token

- Support for downloading assets and loading item footprints- Include extension in the downloaded files.

- Enabled adding STAC item assets as map layers in QGIS

- Added plugin documentation in GitHub pages## [1.0.0] - 2021-12-15- Update UI with more descriptive tooltips.



---



## [beta] - 2021-12-11### Initial Release## [Unreleased] 



### Features- Browse and search STAC API catalogs

- Fixed slow item search performance

- Updated plugin search results to include pagination- Load STAC items as layers### 1.0.0-pre 2022-01-11

- Support for search result filtering and sorting

- Implemented STAC catalog search- Connection management- Changed loading and downloading assets workflow [#93](https://github.com/stac-utils/qgis-stac-plugin/pull/93).

- Added default configured STAC API catalogs

- Basic STAC API support- Asset preview and download- Implemented testing connection functionality.



---- Basic authentication support- Reworked filter and sort features on the search item results.



## Version Comparison- OAuth2 support via QGIS Auth Manager- Fetch for STAC API conformance classes [#82](https://github.com/stac-utils/qgis-stac-plugin/pull/82).



| Version | KADAS Support | Network Stack | Proxy | SSL |- Added STAC API signing using SAS token [#79](https://github.com/stac-utils/qgis-stac-plugin/pull/79).

|---------|---------------|---------------|-------|-----|

| 1.1.2 | ✅ Albireo 2 | Qt (QgsNetworkAccessManager) | Auto | Qt SSL |---- Support for downloading assets and loading item footprints in QGIS, [#70](https://github.com/stac-utils/qgis-stac-plugin/pull/70).

| 1.1.0 | ⚠️ Partial | Python requests | Manual | Python SSL |

| 1.0.0 | ❌ No | Python requests | Manual | Python SSL |- Enabled adding STAC item assets as map layers in QGIS [#58](https://github.com/stac-utils/qgis-stac-plugin/pull/58).



---## Version Comparison- Added plugin documentation in GitHub pages.



## Upgrade Notes



### From 1.1.0 to 1.1.2| Version | KADAS Support | Network Stack | Proxy | SSL |## [beta]



**Breaking Changes**: None|---------|---------------|---------------|-------|-----|



**New Features**:| 1.1.2 | ✅ Albireo 2 | Qt (QgsNetworkAccessManager) | Auto | Qt SSL |### 1.0.0-beta 2021-12-11

- Auto-docking to right panel on startup

- Automatic proxy detection from QGIS Settings| 1.1.0 | ⚠️ Partial | Python requests | Manual | Python SSL |- Fixed slow item search.

- Full VPN support (corporate SSL certificates, VPN routing)

- KADAS Albireo 2 UI optimizations| 1.0.0 | ❌ No | Python requests | Manual | Python SSL |- Updated plugin search result to include pagination [#51](https://github.com/stac-utils/qgis-stac-plugin/pull/51).

- Comprehensive logging system

- Support for search result filtering and sorting [#47](https://github.com/stac-utils/qgis-stac-plugin/pull/47).

**Configuration Changes**:

- **Proxy**: Now configured in QGIS Settings (Settings → Options → Network → Proxy)---- Implemented search [#40](https://github.com/stac-utils/qgis-stac-plugin/pull/40).

- No plugin-specific proxy configuration needed

- SSL certificates handled automatically by Qt SSL stack- Added default configured STAC API catalogs [#26](https://github.com/stac-utils/qgis-stac-plugin/pull/26).



**Testing**:## Upgrade Notes- Basic STAC API support [#17](https://github.com/stac-utils/qgis-stac-plugin/pull/17).

- Run network tests after upgrade:

  ```python

  # In KADAS Python Console:### From 1.1.0 to 1.1.2

  exec(open('test/quick_network_test.py').read())

  ```**Breaking Changes**: None

- Verify auto-docking: Plugin should appear on right panel automatically

- Test proxy: Should work without manual configuration if set in QGIS Settings**New Features**:

- Auto-docking to right panel

### From 1.0.0 to 1.1.0- Automatic proxy detection

- VPN support

**Breaking Changes**: None- KADAS Albireo 2 optimizations



**New Features**:**Configuration Changes**:

- STAC Queryables support for advanced filtering- Proxy: Now configured in QGIS Settings (Settings → Network → Proxy)

- Multiple asset/footprint operations- No plugin-specific proxy configuration needed

- SAS token authentication- SSL certificates handled automatically by Qt

- COPC and netCDF layer support

**Testing**:

---- Run network tests after upgrade: `exec(open('test/quick_network_test.py').read())`

- Verify auto-docking: Plugin should appear on right panel automatically

## Credits- Test proxy: Should work without manual configuration if set in QGIS



- **Original Plugin**: QGIS STAC Plugin by Kartoza (sponsored by Microsoft)---

- **KADAS Adaptation**: Michael Lanini (2026)

- **Proxy Handler**: Based on swisstopo/topo-rapidmapping network patterns## Credits

- **Network Stack**: KADAS Albireo 2 catalog provider patterns

- **Original Plugin**: QGIS STAC Plugin by Kartoza (sponsored by Microsoft)

---- **KADAS Adaptation**: Michael Lanini (2026)

- **Proxy Handler**: Based on swisstopo/topo-rapidmapping

## Links- **Network Patterns**: KADAS Albireo 2 catalog providers



- **Repository**: https://github.com/mlanini/kadas-stac-plugin---

- **Original Plugin**: https://github.com/stac-utils/qgis-stac-plugin

- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues## Links

- **Releases**: https://github.com/mlanini/kadas-stac-plugin/releases

- **Documentation**: https://github.com/mlanini/kadas-stac-plugin#readme- **Repository**: https://github.com/mlanini/kadas-stac-plugin

- **Original Plugin**: https://github.com/stac-utils/qgis-stac-plugin
- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues
- **Releases**: https://github.com/mlanini/kadas-stac-plugin/releases
