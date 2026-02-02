# -*- coding: utf-8 -*-
"""
    Definitions for all pre-installed STAC API catalog connections
"""

from ..api.models import ApiCapability

CATALOGS = [
    {
        "id": "07e3e9dd-cbad-4cf6-8336-424b88abf8f3",
        "name": "Microsoft Planetary Computer STAC API",
        "url": "https://planetarycomputer.microsoft.com/api/stac/v1",
        "selected": True,
        "capability": ApiCapability.SUPPORT_SAS_TOKEN.value
    },
    {
        "id": "d74817bf-da1f-44d7-a464-b87d4009c8a3",
        "name": "Earth Search",
        "url": "https://earth-search.aws.element84.com/v1",
        "selected": False,
        "capability": None,
    },
    {
        "id": "aff201e0-58aa-483d-9e87-090c8baecd3c",
        "name": "Digital Earth Africa",
        "url": "https://explorer.digitalearth.africa/stac/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "98c95473-9f32-4947-83b2-acc8bbf71f36",
        "name": "Radiant MLHub",
        "url": "https://api.radiant.earth/mlhub/v1/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "17a79ce2-9a61-457d-926f-03d37c0606b6",
        "name": "NASA CMR STAC",
        "url": "https://cmr.earthdata.nasa.gov/stac",
        "selected": False,
        "capability": None,
    },
    {
        "id": "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d",
        "name": "Swiss Federal Geodata",
        "url": "https://data.geo.admin.ch/api/stac/v1/",
        "selected": False,
        "capability": None,
    },
    # Additional verified STAC API 1.0 catalogs
    {
        "id": "b1c2d3e4-f5a6-4b7c-8d9e-0f1a2b3c4d5e",
        "name": "Digital Earth Australia",
        "url": "https://explorer.sandbox.dea.ga.gov.au/stac/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "c2d3e4f5-a6b7-4c8d-9e0f-1a2b3c4d5e6f",
        "name": "Copernicus Data Space Ecosystem",
        "url": "https://stac.dataspace.copernicus.eu/v1",
        "selected": False,
        "capability": None,
    },
    {
        "id": "d3e4f5a6-b7c8-4d9e-0f1a-2b3c4d5e6f7a",
        "name": "ESA Catalog",
        "url": "https://eocat.esa.int/eo-catalogue/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "e4f5a6b7-c8d9-4e0f-1a2b-3c4d5e6f7a8b",
        "name": "FedEO Clearinghouse (CEOS)",
        "url": "https://fedeo.ceos.org/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "f5a6b7c8-d9e0-4f1a-2b3c-4d5e6f7a8b9c",
        "name": "Canadian Geospatial Data Collections",
        "url": "https://datacube.services.geo.ca/stac/api/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "a6b7c8d9-e0f1-4a2b-3c4d-5e6f7a8b9c0d",
        "name": "USGS Landsat Collection 2",
        "url": "https://landsatlook.usgs.gov/stac-server/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "b7c8d9e0-f1a2-4b3c-4d5e-6f7a8b9c0d1e",
        "name": "NASA CMR CLOUDSTAC",
        "url": "https://cmr.earthdata.nasa.gov/cloudstac/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "c8d9e0f1-a2b3-4c4d-5e6f-7a8b9c0d1e2f",
        "name": "Digitale Orthophotos Niedersachsen (Germany)",
        "url": "https://dop.stac.lgln.niedersachsen.de",
        "selected": False,
        "capability": None,
    },
    {
        "id": "d9e0f1a2-b3c4-4d5e-6f7a-8b9c0d1e2f3a",
        "name": "Paituli STAC (Finland)",
        "url": "https://paituli.csc.fi/geoserver/ogc/stac/v1",
        "selected": False,
        "capability": None,
    },
    {
        "id": "e0f1a2b3-c4d5-4e6f-7a8b-9c0d1e2f3a4b",
        "name": "KAGIS Katalog (Carinthia, Austria)",
        "url": "https://gis.ktn.gv.at/api/stac/v1/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "f1a2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c",
        "name": "EOC EO Products Service (DLR)",
        "url": "https://geoservice.dlr.de/eoc/ogc/stac/v1/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "a2b3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d",
        "name": "Thünen Earth Observation (Germany)",
        "url": "https://eodata.thuenen.de/stac/api/v1/",
        "selected": False,
        "capability": None,
    },
    {
        "id": "b3c4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e",
        "name": "WorldPop STAC API",
        "url": "https://api.stac.worldpop.org",
        "selected": False,
        "capability": None,
    },
    {
        "id": "c4d5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f",
        "name": "Hub Ocean Data Platform",
        "url": "https://api.hubocean.earth/api/stac",
        "selected": False,
        "capability": None,
    },
    {
        "id": "d5e6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a",
        "name": "DestinE Data Lake API",
        "url": "https://hda.data.destination-earth.eu/stac/v2",
        "selected": False,
        "capability": None,
    },
]

SITE = "https://github.com/mlanini/kadas-stac-plugin"
