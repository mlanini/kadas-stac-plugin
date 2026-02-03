# KADAS STAC Plugin - User Guide

Complete guide with examples and screenshots for using the KADAS STAC Plugin.

---

## Table of Contents

1. [Installation](#installation)
2. [First Steps](#first-steps)
3. [Connecting to Catalogs](#connecting-to-catalogs)
4. [Searching for Data](#searching-for-data)
5. [Loading Data](#loading-data)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites

- **KADAS Albireo 2.x** (tested with 2.x+)
- **Internet connection** (for catalog access)
- **Optional**: Corporate proxy/VPN configured in QGIS Settings

### Install from ZIP

1. **Download Plugin**:
   - Go to [Releases](https://github.com/mlanini/kadas-stac-plugin/releases)
   - Download `kadas_stac.0.1.0.zip`

2. **Install in KADAS**:
   - KADAS → **Plugins** → **Manage and Install Plugins**
   - Click **Install from ZIP**
   - Browse to downloaded ZIP
   - Click **Install Plugin**

3. **Verify Installation**:
   - Check **STAC** tab appears in KADAS ribbon
   - Or: Check **Plugins** menu has **STAC API Browser**

---

## First Steps

### Open the Plugin

**Method 1 - Ribbon Tab**:
- Click **STAC** tab in KADAS ribbon
- Click **STAC API Browser** icon

**Method 2 - Menu**:
- **Plugins** → **STAC API Browser**

**Result**: Dock panel opens on right side

### Interface Overview

```
┌─────────────────────────────┐
│ [Connections ▼] [New] [Edit]│  ← Connection toolbar
├─────────────────────────────┤
│ Collections                 │  ← Collection list
│ ☑ Sentinel-2 Level-2A      │
│ ☐ Landsat Collection 2     │
├─────────────────────────────┤
│ Filters                     │  ← Search filters
│  Date Range: [___] - [___] │
│  Extent: [Draw] [Paste]    │
│  Cloud Cover: [____] %     │
│  [Search]                  │
├─────────────────────────────┤
│ Results (42 items)         │  ← Search results
│ ├─ S2A_20240115_...       │
│ ├─ S2A_20240120_...       │
│ └─ ...                    │
└─────────────────────────────┘
```

---

## Connecting to Catalogs

### Use Pre-configured Catalog

The plugin comes with 19 verified STAC API catalogs:

1. **Select Connection**:
   - Open **Connections** dropdown
   - Choose: e.g., "Swiss Federal Geodata"

2. **Load Collections**:
   - Click **Load Collections** button
   - Wait for collection list to populate

3. **Ready to Search**!

### Add Custom Catalog

**Example: Add Private STAC API**

1. **Click** "New Connection" button

2. **Fill Dialog**:
   ```
   Name: My Custom Catalog
   URL: https://stac.example.com/api/v1
   Catalog Type: API Catalog (dynamic)
   ```

3. **Optional - Authentication**:
   - Click **Authentication** tab
   - Select method: API Header
   - Enter: `X-API-Key` → `your-key-here`

4. **Save** → **Load Collections**

### Catalog Types

**API Catalog** (Dynamic):
- Has `/search` endpoint
- Supports filters (date, extent, etc.)
- Examples: Planetary Computer, Copernicus

**Static Catalog** (Hierarchical):
- JSON files with links
- Recursive navigation
- Examples: Maxar Open Data, USGS Landsat Static

**How to Choose**:
- Try **API** first
- If "Operation canceled" or "HTTP 404" → Switch to **Static**

---

## Searching for Data

### Basic Search

**Example: Find Sentinel-2 images of Switzerland**

1. **Select Collection**:
   - ☑ Check "Sentinel-2 Level-2A"

2. **Set Date Range**:
   - Start: `2024-01-01`
   - End: `2024-01-31`

3. **Set Spatial Extent**:
   - **Option A**: Click **Draw** → Draw rectangle on map
   - **Option B**: Click **Paste** → Paste GeoJSON:
     ```json
     {
       "type": "Polygon",
       "coordinates": [[
         [6.0, 45.8],
         [10.5, 45.8],
         [10.5, 47.8],
         [6.0, 47.8],
         [6.0, 45.8]
       ]]
     }
     ```

4. **Click** "Search"

5. **Results**: Items appear in list (max 100)

### Advanced Filters

**Cloud Cover Filter**:
```
Cloud Cover Max: 20
```
→ Only items with ≤20% cloud cover

**Multiple Collections**:
```
☑ Sentinel-2 Level-2A
☑ Landsat Collection 2
```
→ Results from both collections

**CQL2 Filter** (Advanced):
```
Filter: eo:cloud_cover < 10 AND view:off_nadir < 5
```
→ Custom query language

---

## Loading Data

### Quick Footprints

**Use Case**: Visualize item coverage quickly

1. **Search** for items (see above)

2. **Select Items**:
   - Click single item
   - OR: Ctrl+Click multiple items

3. **Click** "Add Footprints" button

4. **Result**: Polygon layer added to map
   - Layer name: "STAC Footprints"
   - Attributes: Item ID, Date, Cloud Cover

### Load Raster Assets

**Example: Load Sentinel-2 True Color Image**

1. **Select Item** from results

2. **Click** "View Assets" button

3. **Asset Dialog Opens**:
   ```
   ┌─────────────────────────────┐
   │ Assets for S2A_20240115_... │
   ├─────────────────────────────┤
   │ ☑ visual (COG)             │  ← True color
   │ ☐ B02 (GeoTIFF)            │
   │ ☐ B03 (GeoTIFF)            │
   │ ☐ thumbnail (PNG)          │
   ├─────────────────────────────┤
   │ [Load] [Download]          │
   └─────────────────────────────┘
   ```

4. **Check** "visual (COG)"

5. **Click** "Load"

6. **Result**: Raster layer added to map
   - Uses GDAL VSI (virtual file system)
   - No download needed for COG
   - Direct cloud access

### Download and Load

**Use Case**: Work offline or edit locally

1. **Select Asset** (as above)

2. **Click** "Download"

3. **Choose Location**:
   ```
   Save As: C:\Data\sentinel2_20240115.tif
   ```

4. **Options**:
   - ☑ Load layer after download
   - ☐ Keep in original format

5. **Result**: 
   - File downloaded
   - Layer auto-loaded (if checked)

### Load Vector Assets

**Example: GeoJSON Footprint**

1. **Select Item** → **View Assets**

2. **Check** "footprint (GeoJSON)"

3. **Load** → Vector layer added

---

## Advanced Features

### S3 Asset Loading

**Microsoft Planetary Computer**:

Assets use S3 URLs like:
```
s3://sentinel-s2-l2a/tiles/32/T/MR/2024/1/15/0/TCI.tif
```

Plugin automatically:
1. Gets SAS token from Planetary Computer API
2. Converts to GDAL VSI format: `/vsis3/...`
3. Loads directly (no download)

**Troubleshooting S3**:
- Error: "S3 access denied" → Token expired, retry
- Slow loading → S3 bucket far from your location

### Authentication

**Basic Auth Example**:
```
Connection → Authentication
Type: Basic Authentication
Username: myuser
Password: mypassword
```

**OAuth2 Example**:
```
Type: OAuth2
Token URL: https://auth.example.com/token
Client ID: my-client-id
Client Secret: my-client-secret
```

**API Key Example**:
```
Type: API Header
Header Name: X-API-Key
Header Value: abc123def456
```

### Proxy Configuration

Plugin uses **QGIS Proxy Settings**:

1. QGIS → **Settings** → **Options**
2. **Network** tab → **Proxy** section
3. Configure:
   ```
   Type: HTTP
   Host: proxy.company.com
   Port: 8080
   Authentication: [Username/Password]
   ```

4. **Test**: Run `test/quick_network_test.py` in Python Console

### Static Catalog Navigation

**Example: Maxar Open Data (3-level hierarchy)**

Structure:
```
Root Catalog
├─ Emilia-Romagna-Italy-flooding-may23
│  ├─ Collection 10300100BF164000
│  │  ├─ Item 001
│  │  └─ Item 002
│  └─ Collection 10300100C0C4D700
│     └─ Item 003
└─ Turkey-Syria-earthquake-23
   └─ ...
```

Plugin automatically:
1. Opens root catalog
2. Descends into selected collection
3. Recursively finds all items (max depth 3)
4. Returns up to 100 items

**Performance**: Static catalogs slower than API search

---

## Troubleshooting

### Connection Issues

**"SSL module not available"**
- **Solution**: Fixed in v1.1.2
- Plugin uses Qt SSL instead of Python SSL
- No action needed

**"Operation canceled"**
- **Cause**: Timeout or static catalog detected as API
- **Solution**: Edit connection → Catalog Type → "Static Catalog"

**"HTTP 404: /search not found"**
- **Cause**: Static catalog, not API
- **Solution**: Same as above

**"HTTP 405: Method Not Allowed"**
- **Cause**: Catalog is OpenSearch, not STAC
- **Solution**: Remove catalog (not supported)
- **Example**: ESA eocat (removed in v0.1.0)

### Search Issues

**No results found**
- Check filters are not too restrictive
- Try wider date range
- Remove cloud cover filter
- Check spatial extent covers data area

**Results incomplete (max 100)**
- API/static limit for safety
- Use more specific filters
- Search smaller time periods

### Loading Issues

**"Download failed: QNetworkReply content"**
- **Solution**: Fixed in v1.1.2
- Uses `readAll()` instead of `content()`

**"GDAL Error: Cannot open file"**
- Check asset URL is accessible
- For S3: Check token is valid
- Try download instead of direct load

**Slow loading**
- COG files load on-the-fly (slower)
- Try download for faster performance
- Check network speed

### View Logs

**Open Log File**:
- Plugin menu → **Open Log File**
- OR: Navigate to `~/.kadas/stac.log`

**Log Levels**:
- **[INFO]**: Normal operations
- **[WARNING]**: Non-critical issues
- **[ERROR]**: Failed operations
- **[CRITICAL]**: Plugin crashes

**Example Log**:
```
2026-02-03 10:15:32 [INFO] Opening STAC client: https://...
2026-02-03 10:15:33 [WARNING] Static catalog fallback activated
2026-02-03 10:15:35 [INFO] ✅ Found 42 items
```

---

## Tips & Best Practices

### Performance

- **Use API catalogs** when possible (faster than static)
- **Apply filters** to reduce result count
- **Download frequently used** assets for offline work
- **Check collection metadata** before searching

### Data Organization

- **Create Projects**: Save KADAS projects with loaded STAC layers
- **Export Footprints**: Save footprint layers for reference
- **Organize Downloads**: Use consistent folder structure:
  ```
  C:\STAC_Data\
  ├─ Sentinel2\
  ├─ Landsat\
  └─ Maxar\
  ```

### Catalog Selection

| Use Case | Recommended Catalog |
|----------|---------------------|
| **Swiss Data** | Swiss Federal Geodata |
| **Global Satellite** | Microsoft Planetary Computer |
| **Landsat/Sentinel** | Earth Search, USGS Landsat |
| **Copernicus** | Copernicus Data Space |
| **Event Imagery** | Maxar Open Data (static) |
| **Regional (Africa)** | Digital Earth Africa |
| **Regional (Australia)** | Digital Earth Australia |

---

## Example Workflows

### Workflow 1: Disaster Response

**Goal**: Find recent satellite imagery of flood-affected area

1. **Catalog**: Maxar Open Data
2. **Collection**: "Emilia-Romagna-Italy-flooding-may23"
3. **Load**: Footprints → Identify affected tiles
4. **Download**: High-res visual assets
5. **Analysis**: Compare pre/post event imagery

### Workflow 2: Time Series Analysis

**Goal**: Analyze vegetation changes over time

1. **Catalog**: Microsoft Planetary Computer
2. **Collection**: "Sentinel-2 Level-2A"
3. **Filters**:
   - Date: Last 12 months
   - Extent: Study area
   - Cloud Cover: <10%
4. **Load**: All matching items as footprints
5. **Filter**: Select monthly images
6. **Download**: NDVI bands (B04, B08)
7. **Analysis**: Time series in QGIS/R

### Workflow 3: Large Area Mapping

**Goal**: Create basemap from Landsat

1. **Catalog**: USGS Landsat Collection 2
2. **Collection**: "Landsat 8-9 OLI/TIRS"
3. **Filters**:
   - Date: Recent cloud-free season
   - Cloud Cover: <5%
4. **Search**: Tiles covering region
5. **Load**: True color assets (COG)
6. **Mosaic**: Use QGIS Virtual Raster

---

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| **Open Plugin** | None (customize in KADAS) |
| **Search** | Enter (in filter fields) |
| **Select Multiple** | Ctrl + Click |
| **Select Range** | Shift + Click |
| **Refresh** | F5 (in collections) |

---

## Further Resources

- **STAC Specification**: https://stacspec.org/
- **STAC Browser**: https://radiantearth.github.io/stac-browser/
- **Catalog List**: https://stacindex.org/
- **KADAS Documentation**: https://github.com/kadas-albireo/kadas-albireo2

---

**Last Updated**: 2026-02-03 | **Version**: 0.1.0
