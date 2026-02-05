---
hide:
  - navigation
---

# User Guide
The plugin supports searching for STAC resources, loading and downloading STAC items,
retrieving information about the STAC API services.

STAC API services that adhere and conform to the standard STAC specification and practices are recommended
to be used in order to fully utilize the usage of the available plugin features.

## Features
The plugin features can be categorized in two parts, search of STAC resources and access of STAC assets.

### Search of STAC resources 
The STAC API specification allows search for core catalog API capabilities and search for STAC item object.
The plugin support item search and provides filters that can be used along with the search. 

The corresponding STAC API service used when searching needs to ensure that it has implemented the `/search` 
API endpoint accordingly to the specification,
see [https://github.com/radiantearth/stac-api-spec/tree/master/item-search](https://github.com/radiantearth/stac-api-spec/tree/master/item-search).

The plugin contains the following filters that can be used when searching for STAC items objects.

- **Date filter** - users can search for single instant temporal resources or resources with a temporal range.
- **Spatial extent filter** - users can provide a bounding box from which the results should be filtered against
- **Advanced Filter** - this enables usage of STAC API filter languages to provide advanced queries for the search
 for more information 
see [https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter).

### Accessing STAC assets 
Each STAC Item object contains a number of assets and a footprint which a GeoJSON geometry that defines the full
footprint of the assets represented by an item.

The plugin search results items contain a dedicated dialog for viewing, loading and downloading item assets into
QGIS, see [adding assets section](./user-guide#adding-assets) for more details.


## How to use
After installing the plugin in QGIS, the following sections provides a guide on how to use the plugin.
For the installation procedure see [installation page](./installation).

### Launching the STAC API Browser plugin

Three plugin menus can be used to launch the plugin in QGIS.

#### QGIS toolbar

In QGIS toolbar, there will be a plugin entry with the STAC APIs Browser icon.
Click on the icon to open the plugin main dialog.

![image](images/toolbar.png)

_QGIS toolbar_

#### QGIS Plugins Menu
In the QGIS main plugins menu, Go to **STAC API Browser Plugin** > **Open STAC API Browser** 

![image](images/plugin_menu.gif)
_Screenshot showing how to use plugins menu to open the plugin_


#### QGIS Web Menu
In the QGIS web menu which is located in the toolbar,
Go to **STAC API Browser Plugin** > **Open STAC API Browser** 

![image](images/web_menu.gif)
_Screenshot showing how to use QGIS web menu to open the plugin_

### Adding a STAC API connection

The STAC API Browser provides by default some predefined STAC API service connections when installed for the first time.

To add a new STAC API service connection, click the **New** connection button, add the required details 
and click ok to save the connection.

![image](images/add_stac_connectin.png)

_Connection dialog with a Microsoft Planetary Computer STAC API details_

The connection dialog contains a **API Capabilities** field which can be used to set the connection to use
a `SAS Token` [signing mechanism](https://planetarycomputer.microsoft.com/docs/concepts/sas/).
The signing mechanism includes a token that have expiry period, Users should research the API after the period passes in order to resign the items.

The **Advanced** group contain a list of the conformances type that the STAC API adhere to, when creating
new connections the list is empty, users can click the **Get conformance classes** button to fetch the conformance
classes. The above image shows the [Planetary Computer STAC API](https://planetarycomputer.microsoft.com/api/stac/v1)
with a list of conformances classes that have already been fetched.

### Configuring OAuth2 for Copernicus Data Space Ecosystem

The [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu) provides access to Sentinel satellite data through their STAC API. To access S3 assets from Copernicus, you need to configure OAuth2 authentication.

#### Step 1: Register for Copernicus Account

1. Visit [https://dataspace.copernicus.eu](https://dataspace.copernicus.eu)
2. Register for a free account
3. Log in to the [Copernicus Dashboard](https://shapps.dataspace.copernicus.eu/dashboard)

#### Step 2: Create OAuth2 Client Credentials

1. In the Copernicus Dashboard, go to **User Settings** → **OAuth clients**
2. Click **Create** to create a new OAuth client
3. Provide a name for your client (e.g., "KADAS STAC Plugin")
4. Select expiry date or choose "Never expire"
5. **Important**: Do NOT select "Single-page application (SPA)" option
6. Click **Create**
7. **Copy both Client ID and Client Secret** immediately (the secret won't be shown again!)

#### Step 3: Configure OAuth2 in QGIS Auth Manager

1. In QGIS, go to **Settings** → **Options** → **Authentication**
2. Click the green **+** button to add a new authentication configuration
3. Select **Type**: `OAuth2`
4. Configure the OAuth2 settings:
   - **Name**: `Copernicus STAC` (or any descriptive name)
   - **Grant Flow**: `Client Credentials`
   - **Token URL**: `https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token`
   - **Client ID**: Paste the Client ID from Step 2
   - **Client Secret**: Paste the Client Secret from Step 2
5. Click **OK** to save

#### Step 4: Create Copernicus STAC Connection

1. In the STAC API Browser plugin, click **New** connection
2. Configure the connection:
   - **Name**: `Copernicus Data Space`
   - **URL**: `https://stac.dataspace.copernicus.eu/v1`
   - **Authentication**: Select the OAuth2 configuration you created in Step 3
3. Click **OK** to save

#### Step 5: Using Copernicus S3 Assets

Once configured, the plugin will automatically:

1. Use OAuth2 to authenticate STAC API requests
2. When loading or downloading S3 assets, exchange your OAuth2 token for temporary S3 credentials
3. Configure GDAL to access the Copernicus `eodata` S3 bucket seamlessly

**Note**: Temporary S3 credentials are requested automatically when needed and are valid for a limited time. If credentials expire during long sessions, the plugin will request new ones automatically.

**Example S3 assets from Copernicus**:
- `s3://eodata/Sentinel-2/MSI/L2A/2024/01/15/S2A_MSIL2A_*.SAFE/...`
- `s3://eodata/Sentinel-1/SAR/SLC/2019/10/13/S1B_IW_SLC__*.SAFE/...`

### STAC API Items search

#### Using the search filters
All the search filters can be used only when their corresponding group boxes have been checked.

For the **Advanced filter** group, the available filter languages are based on the supported STAC API filter
languages, when **STAC_QUERY** is used then filter input will be treated as a [STAC QUERY](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/query).
If **CQL_JSON** is selected then filter will used as a [CQL_FILTER](https://github.com/radiantearth/stac-api-spec/tree/master/fragments/filter).


![image](images/available_filters_planetary.png)

_Available filters_



![image](images/search_results_planetary.png)

_Example search result items_

### Items footprint and assets

The plugin enables to loading STAC Item assets and footprints in QGIS as map layers.
After searching is complete and items footprint and assets can be viewed and added inside QGIS.


#### Adding and downloading item assets

The plugin currently support loading assets as [COGs](https://github.com/cogeotiff/cog-spec/blob/master/spec.md) layers in QGIS.
To add the assets into QGIS canvas, click the **View assets** button from the required result item.


![image](images/view_assets_planetary.png)

_Image showing the button used for viewing the STAC item assets_

Assets dialog will be opened, from the assets list click **Add assets as layers** button to add the item into QGIS
as a COG layer, to download the asset click the **Download asset** button.

![image](images/assets_dialog.png)

_Assets dialog_



![image](images/added_asset_planetary.png)
_One of the added asset as a QGIS map layer_

#### Adding item footprint

Click the **Add footprint** button to add the footprint of an item into QGIS canvas.
The footprint map layer will be loaded into QGIS, if the STAC item had properties then will be added in the
resulting map layer attribute table as layer data.

![image](images/add_footprint_planetary.png)

_Image showing the button used for adding the STAC item footprint_







