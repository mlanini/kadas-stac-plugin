# KADAS STAC Plugin# KADAS STAC Plugin



[![GitHub release](https://img.shields.io/github/v/release/mlanini/kadas-stac-plugin?include_prereleases)](https://github.com/mlanini/kadas-stac-plugin/releases)[![GitHub release](https://img.shields.io/github/v/release/mlanini/kadas-stac-plugin?include_prereleases)](https://github.com/mlanini/kadas-stac-plugin/releases)

[![License](https://img.shields.io/github/license/mlanini/kadas-stac-plugin)](LICENSE)[![License](https://img.shields.io/github/license/mlanini/kadas-stac-plugin)](LICENSE)



**STAC API Browser for KADAS Albireo 2****STAC API Browser for KADAS Albireo 2** - Browse and load STAC API catalogs directly in KADAS.



------



## 📖 About## 📖 About



KADAS STAC Plugin allows you to explore and load geospatial data from [STAC API](https://stacspec.org/) catalogs directly in KADAS Albireo 2.KADAS STAC Plugin allows you to explore and load geospatial data from [STAC API](https://stacspec.org/) catalogs directly in KADAS Albireo 2.



**Origin**: This plugin is an adapted fork of [qgis-stac-plugin](https://github.com/stac-utils/qgis-stac-plugin) developed by **Kartoza**, optimized for KADAS Albireo 2 compatibility.**Origin**: This plugin is an adapted fork of [qgis-stac-plugin](https://github.com/stac-utils/qgis-stac-plugin) developed by **Kartoza**, optimized for KADAS Albireo 2 compatibility.



**Credits**: Original project by [Kartoza](https://kartoza.com) under GNU GPL 3.0 License.**Credits**: Original project by [Kartoza](https://kartoza.com) under GNU GPL 3.0 License.



------



## ✨ Features## ✨ Features



- 🔍 Browse 22+ STAC API catalogs (Planetary Computer, Earth Search, Copernicus, ESA, NASA, etc.)- 🔍 Browse 22+ STAC API catalogs (Planetary Computer, Earth Search, Copernicus, ESA, etc.)

- 📊 Advanced filters: date, extent, collection, custom properties- 📊 Advanced filters (date, extent, collection, custom properties)

- 🗺️ Load footprints and assets as KADAS layers- 🗺️ Load footprints and assets as KADAS layers

- 📥 Download assets with optional auto-loading- 📥 Download assets with optional auto-loading

- 🔐 Authentication support (Basic, OAuth2, API Key)- 🔐 Authentication support (Basic, OAuth2, API Key)

- 🌐 Automatic proxy/VPN support via QGIS settings- 🌐 Automatic proxy/VPN support via QGIS settings



------



## 📦 Installation## 📦 Installation



1. Download: [`kadas_stac.1.1.2.zip`](https://github.com/mlanini/kadas-stac-plugin/releases/download/v1.1.2/kadas_stac.1.1.2.zip)### Install from ZIP

2. KADAS/QGIS → **Plugins** → **Manage and Install Plugins** → **Install from ZIP**

3. Browse to downloaded ZIP → **Install Plugin**1. Download: [`kadas_stac.1.1.2.zip`](https://github.com/mlanini/kadas-stac-plugin/releases)

2. KADAS/QGIS → **Plugins** → **Manage and Install Plugins**

---3. Select **Install from ZIP**

4. Browse to downloaded ZIP → **Install Plugin**

## 🚀 Quick Start

---

1. **Connect**: KADAS → **STAC API Browser** → **New connection**

2. **Search**: Select collection → Apply filters → Click **Search**## 🚀 Quick Start

3. **Load**: Select items → **Add footprints** or **View assets** → **Add to map**

### 1️⃣ Connect to STAC API

---

Site https://stac-utils.github.io/qgis-stac-plugin

## 📚 Documentation

1. Open the plugin: **KADAS** → **STAC API Browser**

- [CHANGELOG.md](CHANGELOG.md) - Version history

- [DEVELOPMENT.md](DEVELOPMENT.md) - Technical guide2. In the **Search** tab, click **New** to create a new connection## ✨ Features

- [TESTING.md](TESTING.md) - Network testing

3. Configure parameters:

---

   - **Name**: Descriptive name (e.g., "Planetary Computer")Questo plugin è un **fork adattato** del progetto open source [qgis-stac-plugin](https://github.com/stac-utils/qgis-stac-plugin) sviluppato da **Kartoza**, rielaborato per garantire piena compatibilità con l'ambiente KADAS Albireo 2.

## 📝 License

   - **URL**: STAC API endpoint (e.g., `https://planetarycomputer.microsoft.com/api/stac/v1`)

GNU General Public License v2.0 - See [LICENSE](LICENSE)

   - **Authentication** (optional): Configure credentials if required- 🔍 **STAC API Search**: Browse STAC catalogs (Planetary Computer, Earth Search, data.geo.admin.ch, etc.)

**Version**: 1.1.2 | **Compatibility**: KADAS Albireo 2.x / QGIS 3.28+

   - **Page Size**: Number of results per page (default: 10)

4. Click **Test Connection** to verify- 📊 **Advanced Filters**: Filter by date, geographic extent, collection, custom properties---

5. Click **OK** to save

- 🗺️ **Layer Loading**: Add footprints and assets directly as QGIS/KADAS layers

**Included default catalogs:**

- Microsoft Planetary Computer- 📥 **Asset Download**: Download assets locally with optional automatic loading**Differenze principali rispetto al plugin QGIS originale:**

- Earth Search (AWS)

- Swiss Federal Geoportal (data.geo.admin.ch)- 🔐 **Authentication**: QGIS authentication support (Basic, OAuth2, API Key)



### 2️⃣ Search Items- 🌐 **Multi-catalog**: Manage multiple connections to different STAC endpoints**The QGIS STAC API Browser currently lacks funding for maintenance,



1. Select a **Collection** from the list (click **Fetch collections** if empty)- 📄 **Metadata Viewer**: View complete collection and item metadata

2. (Optional) Apply filters:

   - **Filter by date**: Time range- ✅ **Network Stack Qt**: Utilizza esclusivamente `QgsNetworkAccessManager` (identico ai catalog providers di KADAS)

   - **Extent**: Geographic area (use current map or draw bbox)

   - **Advanced filter**: CQL2-JSON or other supported languages---

   - **Data-driven queryables**: Custom catalog properties

3. Click **Search** to start the search- ✅ **Proxy QGIS automatico**: Rispetta le impostazioni proxy di QGIS/KADAS senza configurazioni aggiuntive## 📦 Installationbug fixes and new features; therefore development will be slow for now.

4. Results will appear in the **Results** tab

## 📦 Installation

### 3️⃣ Load Data

- ✅ **Logger dedicato**: Sistema di logging file-based con rotazione automatica (`~/.kadas/stac.log`)

**Option A: Footprint (geometry)**

- Select **Select footprint** checkbox on desired items### Method 1: Install from ZIP (Recommended)

- Click **Add the selected footprints** or **Add all footprints**

- Footprints will be added as a vector layer- ✅ **UI KADAS-optimized**: Dock widget con aree di ancoraggio limitate (solo sinistra/destra)However we’re dedicated to maintaining the project. 



**Option B: Asset (raster/vector data)**1. Download the latest release: [`kadas_stac.1.1.2.zip`](https://github.com/mlanini/kadas-stac-plugin/releases)

- Click **View assets** on an item

- Select assets to load2. Open KADAS/QGIS → **Plugins** → **Manage and Install Plugins**- ✅ **Branding KADAS**: Interfaccia rinominata e personalizzata per l'ecosistema KADAS

- Click **Add assets as layers** (direct loading) or **Download the assets** (download first)

3. Select **Install from ZIP**

---

4. Browse to the downloaded ZIP file- ✅ **Conformance validation**: Supporto completo STAC API conformance classes### Method 1: Install from ZIP (Recommended)For assistance or if you have funding to contribute 

## 🛠️ Configuration

5. Click **Install Plugin**

### Settings (Settings Tab)

- ✅ **Pagination support**: Iterator efficiente per cataloghi di grandi dimensioni

- **Download folder**: Destination folder for asset downloads

- **Enable loading assets after download**: Automatically load assets after download### Method 2: Plugin Repository



### Advanced Connection Settingsplease reach out to Kartoza ([info@kartoza.com](mailto:info@kartoza.com))**



- **SAS subscription key**: Key for SAS signing (e.g., Azure Blob Storage)Not yet available in the official QGIS plugin repository.

- **API Conformance classes**: Display STAC API endpoint conformance

- **API Capabilities**: Select supported features (Collections, Filter, Sort, Fields)**Credits**: Progetto originale sviluppato da [Kartoza](https://kartoza.com) per QGIS. Ringraziamenti alla community STAC e agli sviluppatori del plugin QGIS originale.



------



## 🐛 Troubleshooting1. Download the latest release: [`kadas_stac.1.1.2.zip`](https://github.com/mlanini/kadas-stac-plugin/releases)



### Plugin does not load## 🚀 Usage



**Solution**: Verify QGIS/KADAS version---



```### 1️⃣ Connect to STAC API

Requirements: QGIS >= 3.28 / KADAS Albireo 2

```2. Open KADAS/QGIS → **Plugins** → **Manage and Install Plugins**### Installation



### STAC API connection error1. Open the plugin: **KADAS** → **STAC API Browser**



**Symptoms**: "Connection failed" during test connection2. In the **Search** tab, click **New** to create a new connection## ✨ Funzionalità



**Solutions**:3. Configure parameters:

1. Verify endpoint URL (must end with `/` if required by the API)

2. Check proxy settings: **QGIS** → **Settings** → **Options** → **Network**   - **Name**: Descriptive name (e.g., "Planetary Computer")3. Select **Install from ZIP**

3. Test connectivity manually:

   ```bash   - **URL**: STAC API endpoint (e.g., `https://planetarycomputer.microsoft.com/api/stac/v1`)

   curl https://planetarycomputer.microsoft.com/api/stac/v1/

   ```   - **Authentication** (optional): Configure credentials if required- 🔍 **Ricerca STAC API**: Naviga cataloghi STAC (Planetary Computer, Earth Search, data.geo.admin.ch, etc.)

4. Check logs: `~/.kadas/stac.log` (or environment variable `KADAS_STAC_LOG`)

   - **Page Size**: Number of results per page (default: 10)

### Assets cannot be loaded

4. Click **Test Connection** to verify- 📊 **Filtri avanzati**: Filtra per data, estensione geografica, collection, proprietà custom4. Browse to the downloaded ZIP fileDuring the development phase the plugin is available to install via 

**Symptoms**: "Failed to load asset as layer"

5. Click **OK** to save

**Solutions**:

1. Verify format supported by QGIS (GeoTIFF, COG, GeoJSON, etc.)- 🗺️ **Caricamento layer**: Aggiungi footprint e asset direttamente come layer QGIS/KADAS

2. For remote assets (HTTP), verify connectivity

3. For authenticated assets, configure authentication in connection settings**Included default catalogs:**

4. Try manual download before loading

- Microsoft Planetary Computer- 📥 **Download asset**: Scarica asset localmente con caricamento automatico opzionale5. Click **Install Plugin**a dedicated plugin repository 

### Logging

- Earth Search (AWS)

Enable detailed logging by modifying `src/kadas_stac/main.py`:

- Swiss Federal Geoportal (data.geo.admin.ch)- 🔐 **Autenticazione**: Supporto autenticazione QGIS (Basic, OAuth2, API Key)

```python

# Change from "STANDARD" to "DEBUG"

self.log = get_logger(level="DEBUG")

```### 2️⃣ Search Items- 🌐 **Multi-catalog**: Gestisci connessioni multiple a diversi endpoint STAChttps://stac-utils.github.io/qgis-stac-plugin/repository/plugins.xml



Log file location:

- Default: `~/.kadas/stac.log`

- Custom: set environment variable `KADAS_STAC_LOG=/path/to/log.log`1. Select a **Collection** from the list (click **Fetch collections** if empty)- 📄 **Metadata viewer**: Visualizza metadati completi di collection e item



Open log: **Plugin** → **STAC API Browser** → **Settings** → **Open Log File**2. (Optional) Apply filters:



---   - **Filter by date**: Time range### Method 2: Plugin Repository



## 🌐 Network & Proxy Support   - **Extent**: Geographic area (use current map or draw bbox)



The plugin **automatically supports** enterprise network configurations:   - **Advanced filter**: CQL2-JSON or other supported languages---



### ✅ Automatic Proxy Detection   - **Data-driven queryables**: Custom catalog properties



- Reads proxy settings from **QGIS Settings** → **Options** → **Network**3. Click **Search** to start the searchOpen the QGIS plugin manager, then select the **Settings** page, click **Add** 

- Supports HTTP/HTTPS proxy with or without authentication

- No manual configuration needed4. Results will appear in the **Results** tab



### ✅ VPN Compatibility## 📦 Installazione



- Works seamlessly with corporate VPN connections### 3️⃣ Load Data

- Qt SSL stack handles VPN certificates automatically

- Connect VPN before starting KADAS/QGISNot yet available in official QGIS plugin repository.button on the **Plugin Repositories** group box and use the above url to create



### ✅ SSL/HTTPS**Option A: Footprint (geometry)**



- Uses Qt SSL stack (always available in KADAS)- Select **Select footprint** checkbox on desired items### Metodo 1: Installazione da ZIP (Consigliato)

- No dependency on Python SSL module

- Handles corporate SSL certificates- Click **Add the selected footprints** or **Add all footprints**



### 🔧 Network Configuration- Footprints will be added as a vector layerthe new plugin repository.



Configure proxy in QGIS:



1. **Settings** → **Options** → **Network****Option B: Asset (raster/vector data)**1. Scarica l'ultima release: [`kadas_stac.1.1.2.zip`](https://github.com/mlanini/kadas-stac-plugin/releases)

2. Enable **"Use proxy for web access"**

3. Enter proxy details:- Click **View assets** on an item

   - **Host**: `proxy.example.com`

   - **Port**: `8080`- Select assets to load2. Apri KADAS/QGIS → **Plugin** → **Gestisci e Installa Plugin**---![Add plugin repository](docs/images/plugin_settings.png)

   - **User/Password**: (if required)

4. Restart QGIS/KADAS- Click **Add assets as layers** (direct loading) or **Download the assets** (download first)



**Technical Details**: The plugin uses identical network patterns to KADAS Albireo 2 (`QgsNetworkAccessManager`). See [DEVELOPMENT.md](DEVELOPMENT.md) for details.3. Seleziona **Installa da ZIP**



------



## 🧪 Testing4. Naviga verso il file ZIP scaricato



### Quick Network Test## 🛠️ Configuration



Verify network connectivity using KADAS Python Console:5. Clicca **Installa Plugin**



```python### Settings (Settings Tab)

# Copy and paste into KADAS Python Console:

exec(open('path/to/kadas-stac-plugin/test/quick_network_test.py').read())## 🚀 Quick StartAfter adding the new repository, the plugin should be available from the list

```

- **Download folder**: Destination folder for asset downloads

### Full Test Suite

- **Enable loading assets after download**: Automatically load assets after download### Metodo 2: Repository Plugin

Run comprehensive tests:



```bash

# Windows (PowerShell)### Advanced Connection Settingsof all plugins that can be installed.

.\run-network-tests.ps1



# Linux/Mac

./run-network-tests.sh- **SAS subscription key**: Key for SAS signing (e.g., Azure Blob Storage)Non ancora disponibile nel repository ufficiale QGIS.

```

- **API Conformance classes**: Display STAC API endpoint conformance

See [TESTING.md](TESTING.md) for detailed testing instructions.

- **API Capabilities**: Select supported features (Collections, Filter, Sort, Fields)1. Open KADAS Albireo 2

---



## 📚 Resources

------

- **STAC Specification**: https://stacspec.org/

- **STAC API Specification**: https://github.com/radiantearth/stac-api-spec

- **Original QGIS Plugin**: https://github.com/stac-utils/qgis-stac-plugin

- **KADAS Albireo**: https://github.com/kadas-albireo/kadas-albireo2## 🐛 Troubleshooting2. Go to **Plugins** → **KADAS STAC API Browser****NOTE:** While the development phase is on going the plugin will be flagged as experimental, make

- **Issue Tracker**: https://github.com/mlanini/kadas-stac-plugin/issues



---

### Plugin does not load## 🚀 Utilizzo

## 🤝 Contributing



Contributions welcome! Please:

**Solution**: Verify QGIS/KADAS version3. Plugin dock automatically appears on the right panelsure to enable the QGIS plugin manager in the **Settings** page to show the experimental plugins

1. Fork the repository

2. Create a feature branch (`git checkout -b feature/amazing-feature`)```

3. Commit your changes (`git commit -m 'Add amazing feature'`)

4. Push to the branch (`git push origin feature/amazing-feature`)Requirements: QGIS >= 3.28 / KADAS Albireo 2### 1️⃣ Connessione a STAC API

5. Open a Pull Request

```

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed instructions.

4. Add a STAC API connection (e.g., `https://data.geo.admin.ch/api/stac/v1/`)in order to be able to install it.

---

### STAC API connection error

## 📝 License

1. Apri il plugin: **KADAS** → **STAC API Browser**

This project is released under the **GNU General Public License v2.0** - see [LICENSE](LICENSE) file for details.

**Symptoms**: "Connection failed" during test connection

**Original Plugin**: Copyright (c) 2021-2024 Kartoza  

**KADAS Fork**: Copyright (c) 2026 Michele Lanini2. Nella tab **Search**, clicca **New** per creare una nuova connessione5. Browse collections and search for items



---**Solutions**:



## 🙏 Credits1. Verify endpoint URL (must end with `/` if required by the API)3. Configura i parametri:



- **Kartoza** - Original QGIS plugin development2. Check proxy settings: **QGIS** → **Settings** → **Options** → **Network**

- **STAC Community** - Specifications and support

- **KADAS Albireo Team** - KADAS framework3. Test connectivity manually:   - **Name**: Nome descrittivo (es. "Planetary Computer")6. Add items to map with one clickAlternatively the plugin can be installed using **Install from ZIP** option on the 

- **Contributors** - All project contributors

   ```bash

---

   curl https://planetarycomputer.microsoft.com/api/stac/v1/   - **URL**: Endpoint STAC API (es. `https://planetarycomputer.microsoft.com/api/stac/v1`)

**Version**: 1.1.2 (February 2, 2026)  

**Compatibility**: KADAS Albireo 2.x / QGIS 3.28+     ```

**Maintainer**: Michele Lanini

4. Check logs: `~/.kadas/stac.log` (or environment variable `KADAS_STAC_LOG`)   - **Authentication** (opzionale): Configura credenziali se necessarioQGIS plugin manager. Download zip file from the required plugin released version



### Assets cannot be loaded   - **Page Size**: Numero di risultati per pagina (default: 10)



**Symptoms**: "Failed to load asset as layer"4. Clicca **Test Connection** per verificare---https://github.com/stac-utils/qgis-stac-plugin/releases/download/{tagname}/qgis_stac.{version}.zip.



**Solutions**:5. Clicca **OK** per salvare

1. Verify format supported by QGIS (GeoTIFF, COG, GeoJSON, etc.)

2. For remote assets (HTTP), verify connectivity

3. For authenticated assets, configure authentication in connection settings

4. Try manual download before loading**Cataloghi predefiniti inclusi:**



### Logging- Microsoft Planetary Computer## 🌐 Network & Proxy SupportFrom the **Install from ZIP** page, select the zip file and click the **Install** button to install



Enable detailed logging by modifying `src/kadas_stac/main.py`:- Earth Search (AWS)



```python- Swiss Federal Geoportal (data.geo.admin.ch)plugin

# Change from "STANDARD" to "DEBUG"

self.log = get_logger(level="DEBUG")

```

### 2️⃣ Ricerca ItemThe plugin **automatically supports** enterprise network configurations:![Screenshot for install from zip option](docs/images/install_from_zip.png)

Log file location:

- Default: `~/.kadas/stac.log`

- Custom: set environment variable `KADAS_STAC_LOG=/path/to/log.log`

1. Seleziona una **Collection** dalla lista (clicca **Fetch collections** se vuoto)

Open log: **Plugin** → **STAC API Browser** → **Settings** → **Open Log File**

2. (Opzionale) Applica filtri:

---

   - **Filter by date**: Range temporale### ✅ Automatic Proxy DetectionWhen the development work is complete the plugin will be available on the QGIS

## 🌐 Network & Proxy Support

   - **Extent**: Area geografica (usa mappa corrente o disegna bbox)

The plugin **automatically supports** enterprise network configurations:

   - **Advanced filter**: CQL2-JSON o altri linguaggi supportati- Reads proxy settings from **QGIS Settings** → **Options** → **Network**official plugin repository.

### ✅ Automatic Proxy Detection

   - **Data-driven queryables**: Proprietà custom del catalogo

- Reads proxy settings from **QGIS Settings** → **Options** → **Network**

- Supports HTTP/HTTPS proxy with or without authentication3. Clicca **Search** per avviare la ricerca- Supports HTTP/HTTPS proxy with or without authentication

- No manual configuration needed

4. I risultati appariranno nella tab **Results**

### ✅ VPN Compatibility

- No manual configuration needed

- Works seamlessly with corporate VPN connections

- Qt SSL stack handles VPN certificates automatically### 3️⃣ Caricamento Dati

- Connect VPN before starting KADAS/QGIS

### Network & Proxy Support

### ✅ SSL/HTTPS

**Opzione A: Footprint (geometria)**

- Uses Qt SSL stack (always available in KADAS)

- No dependency on Python SSL module- Seleziona checkbox **Select footprint** sugli item desiderati### ✅ VPN Compatibility

- Handles corporate SSL certificates

- Clicca **Add the selected footprints** o **Add all footprints**

### 🔧 Network Configuration

- I footprint verranno aggiunti come layer vettoriale- Works seamlessly with corporate VPN connectionsThe plugin **automatically supports** proxy and VPN configurations:

Configure proxy in QGIS:



1. **Settings** → **Options** → **Network**

2. Enable **"Use proxy for web access"****Opzione B: Asset (dati raster/vettoriali)**- Qt SSL stack handles VPN certificates automatically

3. Enter proxy details:

   - **Host**: `proxy.example.com`- Clicca **View assets** su un item

   - **Port**: `8080`

   - **User/Password**: (if required)- Seleziona gli asset da caricare- Connect VPN before starting KADAS/QGIS- **Proxy Configuration**: Uses QGIS/Kadas network settings automatically

4. Restart QGIS/KADAS

- Clicca **Add assets as layers** (caricamento diretto) o **Download the assets** (scarica prima)

**Technical Details**: The plugin uses identical network patterns to KADAS Albireo 2 (`QgsNetworkAccessManager`). See [DEVELOPMENT.md](DEVELOPMENT.md) for details.

  - Configure in: Settings → Options → Network

---

---

## 🧪 Testing

### ✅ SSL/HTTPS  - Supports: HTTP/HTTPS proxy with or without authentication

### Quick Network Test

## 🛠️ Configurazione

Verify network connectivity using KADAS Python Console:

- Uses Qt SSL stack (always available in KADAS)  

```python

# Copy and paste into KADAS Python Console:### Settings (Tab Settings)

exec(open('path/to/kadas-stac-plugin/test/quick_network_test.py').read())

```- No dependency on Python SSL module- **VPN Support**: Works seamlessly with VPN connections



### Full Test Suite- **Download folder**: Cartella di destinazione per download asset



Run comprehensive tests:- **Enable loading assets after download**: Carica automaticamente asset dopo download- Handles corporate SSL certificates  - Connect VPN before opening QGIS/Kadas



```bash

# Windows (PowerShell)

.\run-network-tests.ps1### Advanced Connection Settings  - Plugin automatically routes through VPN



# Linux/Mac

./run-network-tests.sh

```- **SAS subscription key**: Chiave per firma SAS (es. Azure Blob Storage)### 🔧 Network Configuration



See [TESTING.md](TESTING.md) for detailed testing instructions.- **API Conformance classes**: Visualizza conformità STAC API dell'endpoint



---- **API Capabilities**: Seleziona funzionalità supportate (Collections, Filter, Sort, Fields)- **STAC API Authentication**: Supports multiple auth methods via QGIS Auth Manager



## 📚 Resources



- **STAC Specification**: https://stacspec.org/---Configure proxy in QGIS:  - OAuth2, API Keys, Basic Authentication

- **STAC API Specification**: https://github.com/radiantearth/stac-api-spec

- **Original QGIS Plugin**: https://github.com/stac-utils/qgis-stac-plugin

- **KADAS Albireo**: https://github.com/kadas-albireo/kadas-albireo2

- **Issue Tracker**: https://github.com/mlanini/kadas-stac-plugin/issues## 🐛 Risoluzione Problemi1. **Settings** → **Options** → **Network**  - Configure in QGIS Auth Manager and assign to STAC connections



---



## 🤝 Contributing### Plugin non si carica2. Enable **"Use proxy for web access"**



Contributions welcome! Please:



1. Fork the repository**Soluzione**: Verifica versione QGIS/KADAS3. Enter proxy details:For detailed technical analysis, see [PROXY_VPN_ANALYSIS.md](PROXY_VPN_ANALYSIS.md)

2. Create a feature branch (`git checkout -b feature/amazing-feature`)

3. Commit your changes (`git commit -m 'Add amazing feature'`)```

4. Push to the branch (`git push origin feature/amazing-feature`)

5. Open a Pull RequestRequisiti: QGIS >= 3.28 / KADAS Albireo 2   - **Host**: `prp01.adb.intra.admin.ch` (example)



See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed instructions.```



---   - **Port**: `8080`#### Testing Network Connectivity



## 📝 License### Errore connessione STAC API



This project is released under the **GNU General Public License v2.0** - see [LICENSE](LICENSE) file for details.   - **User/Password**: (if required)



**Original Plugin**: Copyright (c) 2021-2024 Kartoza  **Sintomi**: "Connection failed" durante test connection

**KADAS Fork**: Copyright (c) 2026 Michele Lanini

4. Restart QGIS/KADASTo verify that network connectivity is working correctly:

---

**Soluzioni**:

## 🙏 Credits

1. Verifica URL endpoint (deve terminare con `/` se richiesto dall'API)

- **Kartoza** - Original QGIS plugin development

- **STAC Community** - Specifications and support2. Controlla impostazioni proxy: **QGIS** → **Impostazioni** → **Opzioni** → **Rete**

- **KADAS Albireo Team** - KADAS framework

- **Contributors** - All project contributors3. Testa connettività manuale:**Technical Details**: The plugin uses identical network patterns to KADAS Albireo 2 (QgsNetworkAccessManager). See [DEVELOPMENT.md](DEVELOPMENT.md) for details.**Quick Test (KADAS Python Console):**



---   ```bash



**Version**: 1.1.2 (February 2, 2026)     curl https://planetarycomputer.microsoft.com/api/stac/v1/```python

**Compatibility**: KADAS Albireo 2.x / QGIS 3.28+  

**Maintainer**: Michele Lanini   ```


4. Controlla log: `~/.kadas/stac.log` (o variabile ambiente `KADAS_STAC_LOG`)---# Copy and paste into KADAS Python Console:



### Asset non caricabiliexec(open('path/to/kadas-stac-plugin/test/quick_network_test.py').read())



**Sintomi**: "Failed to load asset as layer"## 🧪 Testing```



**Soluzioni**:

1. Verifica formato supportato da QGIS (GeoTIFF, COG, GeoJSON, etc.)

2. Per asset remoti (HTTP), verifica connettivitàVerify network connectivity:**Full Test Suite:**

3. Per asset autenticati, configura autenticazione in connection settings

4. Prova download manuale prima del caricamento```bash



### Logging```python# From terminal with QGIS/KADAS Python:



Abilita logging dettagliato modificando `src/kadas_stac/main.py`:# Quick test - Copy/paste in KADAS Python Console:python test_network.py



```pythonexec(open('test/quick_network_test.py').read())```

# Cambia da "STANDARD" a "DEBUG"

self.log = get_logger(level="DEBUG")```

```

See [test/NETWORK_TESTS.md](test/NETWORK_TESTS.md) for detailed testing documentation.

Log file location:

- Default: `~/.kadas/stac.log`Or run full test suite:

- Custom: imposta variabile ambiente `KADAS_STAC_LOG=/path/to/log.log`

```bash**Expected Results:**

Apri log: **Plugin** → **STAC API Browser** → **Settings** → **Open Log File**

python test_network.py- ✓ QgsNetworkAccessManager available

---

```- ✓ QGIS Settings accessible (proxy configuration)

## 📚 Risorse

- ✓ Connection to data.geo.admin.ch successful

- **STAC Specification**: https://stacspec.org/

- **STAC API Specification**: https://github.com/radiantearth/stac-api-specSee [TESTING.md](TESTING.md) for complete testing documentation.- ✓ QgisStacApiIO working correctly

- **Plugin originale QGIS**: https://github.com/stac-utils/qgis-stac-plugin

- **KADAS Albireo**: https://github.com/kadas-albireo/kadas-albireo2- ✓ Proxy Handler functional

- **Issue Tracker**: https://github.com/mlanini/kadas-stac-plugin/issues

---- ✓ URL Normalization working

---



## 🤝 Contributi

## 📚 Documentation**Compatibility**: The plugin uses **identical network patterns** to KADAS Albireo 2.

Contributi benvenuti! Per favore:



1. Fork del repository

2. Crea un branch per la feature (`git checkout -b feature/amazing-feature`)- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

3. Commit delle modifiche (`git commit -m 'Add amazing feature'`)

4. Push al branch (`git push origin feature/amazing-feature`)- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide and technical details#### Development 

5. Apri una Pull Request

- **[TESTING.md](TESTING.md)** - Network testing and troubleshooting

Vedi [DEVELOPMENT.md](DEVELOPMENT.md) per istruzioni dettagliate.

To use the plugin for development purposes, clone the repository locally,

---

---install poetry, a python dependencies management tool see https://python-poetry.org/docs/#installation

## 📝 Licenza

then using the poetry tool, update the poetry lock file and install plugin dependencies by running 

Questo progetto è rilasciato sotto licenza **GNU General Public License v2.0** - vedi file [LICENSE](LICENSE) per dettagli.

## 🛠️ Development``` 

**Plugin originale**: Copyright (c) 2021-2024 Kartoza  

**Fork KADAS**: Copyright (c) 2026 Michele Laninipoetry update --lock



---### Setuppoetry install --no-dev



## 🙏 Credits```



- **Kartoza** - Sviluppo plugin QGIS originale```bash

- **STAC Community** - Specifiche e supporto

- **KADAS Albireo Team** - Framework KADAS# Clone repositoryTo install the plugin into the QGIS application use the below command

- **Contributors** - Tutti i contributori del progetto

git clone https://github.com/mlanini/kadas-stac-plugin.git```

---

cd kadas-stac-pluginpoetry run python admin.py install

**Versione**: 1.1.2 (2 febbraio 2026)  

**Compatibilità**: KADAS Albireo 2.x / QGIS 3.28+  ```

**Maintainer**: Michele Lanini

# Install Poetry (if not installed)

# See: https://python-poetry.org/docs/#installation


# Install dependencies
poetry install --no-dev

# Install plugin to QGIS
poetry run python admin.py install
```

### Build Distribution Package

```bash
# Generate plugin ZIP
poetry run python admin.py generate-zip

# Output: dist/kadas_stac.1.1.2.zip
```

### Key Files

- `src/kadas_stac/main.py` - Plugin entry point
- `src/kadas_stac/api/qgis_stac_io.py` - QGIS network integration
- `src/kadas_stac/api/proxy_handler.py` - Proxy detection
- `src/kadas_stac/gui/kadas_stac_widget.py` - Main UI

---

## 🏢 Enterprise Features

### KADAS Albireo 2 Compatibility

✅ **Auto-docking**: Plugin automatically docks to right panel on startup  
✅ **Clean unload**: Complete cleanup when plugin is deactivated  
✅ **Network stack**: Identical to KADAS native network handling  
✅ **Proxy support**: Corporate proxy with authentication  
✅ **VPN support**: Works with corporate VPN and SSL inspection  

### Network Architecture

The plugin uses **QgsNetworkAccessManager** exclusively:
- No Python `requests` library dependency
- No Python SSL module dependency
- Qt SSL stack for all HTTPS connections
- Automatic redirect handling (HTTP → HTTPS)
- Referer header support (KADAS pattern)

**Pattern Identity**: 100% identical to KADAS Albireo 2 catalog providers.

---

## 📄 License

GPL v3.0 - See [LICENSE](LICENSE) file

---

## 🤝 Credits

- **Original Plugin**: [QGIS STAC Plugin](https://github.com/stac-utils/qgis-stac-plugin) by Kartoza
- **KADAS Adaptation**: mlanini
- **Proxy Handler**: Based on [swisstopo/topo-rapidmapping](https://github.com/swisstopo/topo-rapidmapping)
- **Sponsored by**: Microsoft (original), Swiss Federal Office of Topography (adaptations)

---

## 📞 Support

- **Issues**: https://github.com/mlanini/kadas-stac-plugin/issues
- **Discussions**: https://github.com/mlanini/kadas-stac-plugin/discussions
- **Original Plugin**: info@kartoza.com

---

## 🔄 Version

**Current Version**: 1.1.2  
**Release Date**: January 31, 2026  
**KADAS Compatibility**: KADAS Albireo 2  
**QGIS Compatibility**: QGIS 3.0 - 3.99
