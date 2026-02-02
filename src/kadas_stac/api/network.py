import os
import typing
import uuid
import json

from dateutil import parser
from functools import partial

from json.decoder import JSONDecodeError

from qgis.core import (
    QgsApplication,
    QgsAuthMethodConfig,
    QgsNetworkContentFetcherTask,
    QgsTask,
)

from qgis.PyQt import (
    QtGui,
    QtCore,
    QtWidgets,
    QtNetwork
)

from .models import (
    ApiCapability,
    CatalogType,
    Conformance,
    Collection,
    Constants,
    Item,
    ItemSearch,
    ResourceAsset,
    ResourceExtent,
    ResourceLink,
    ResourcePagination,
    ResourceProperties,
    ResourceProvider,
    ResourceType,
    SpatialExtent,
    TemporalExtent,
    QgsAuthMethods,
    Queryable,
    QueryableProperty,
    QueryableFetchType
)

from ..lib import planetary_computer as pc

from pystac_client import Client
from pystac_client.exceptions import APIError

from pystac.errors import STACTypeError

from ..utils import log, tr

from ..conf import settings_manager
from ..definitions.constants import SAS_SUBSCRIPTION_VARIABLE
from ..logger import get_logger

# Initialize logger
logger = get_logger(level="DEBUG")

# Import proxy handler only when needed (lazy import to avoid SSL issues)
# from .proxy_handler import get_pystac_kwargs


def get_all_items_recursive(client, max_items=100, max_depth=3, collection_filter=None):
    """
    Recursively navigate a static STAC catalog to collect all items.
    
    For hierarchical static catalogs (like Maxar Open Data), items may be nested
    in sub-collections. This function:
    1. Gets items from the current catalog/collection
    2. Recursively gets items from all child collections
    
    Args:
        client: pystac_client.Client instance
        max_items: Maximum total items to return (safety limit)
        max_depth: Maximum recursion depth (safety limit)
        collection_filter: Optional list of collection IDs to filter (only items from these collections)
    
    Returns:
        List of pystac.Item objects
    """
    all_items = []
    
    def _collect_items_recursive(catalog_or_collection, current_depth=0):
        """Internal recursive function to collect items."""
        if current_depth > max_depth:
            logger.warning(f"Max recursion depth ({max_depth}) reached, stopping")
            return
        
        if len(all_items) >= max_items:
            logger.info(f"Max items ({max_items}) reached, stopping")
            return
        
        # Check if we should skip this collection based on filter
        if collection_filter and hasattr(catalog_or_collection, 'id'):
            collection_id = catalog_or_collection.id
            if collection_id not in collection_filter:
                logger.debug(f"Skipping collection '{collection_id}' (not in filter: {collection_filter})")
                # Still check child collections (might match deeper in hierarchy)
            else:
                logger.info(f"✓ Collection '{collection_id}' matches filter")
        
        # Get direct items from this catalog/collection
        try:
            items_iterator = catalog_or_collection.get_items()
            for item in items_iterator:
                if len(all_items) >= max_items:
                    break
                    
                # Apply collection filter to items
                if collection_filter:
                    item_collection = getattr(item, 'collection_id', None)
                    logger.debug(f"Item {item.id} has collection_id: '{item_collection}'")
                    if item_collection and item_collection not in collection_filter:
                        logger.debug(f"Skipping item from collection '{item_collection}' (not in filter: {collection_filter})")
                        continue
                    elif not item_collection:
                        logger.warning(f"Item {item.id} has no collection_id attribute, including it")
                
                all_items.append(item)
                logger.debug(f"Found item: {item.id} (total: {len(all_items)})")
        except Exception as e:
            logger.debug(f"No items at this level: {e}")
        
        # Recursively get items from child collections
        try:
            collections_iterator = catalog_or_collection.get_collections()
            for collection in collections_iterator:
                if len(all_items) >= max_items:
                    break
                logger.debug(f"Descending into collection: {collection.id}")
                _collect_items_recursive(collection, current_depth + 1)
        except Exception as e:
            logger.debug(f"No child collections: {e}")
    
    # Start recursive collection from the client (root catalog)
    if collection_filter:
        logger.info(f"Starting recursive item collection with collection filter: {collection_filter}")
    else:
        logger.info("Starting recursive item collection from static catalog")
    _collect_items_recursive(client)
    logger.info(f"Recursive collection complete: {len(all_items)} items found")
    
    return all_items


class ContentFetcherTask(QgsTask):
    """
    Task to manage the STAC API content search using the pystac_client library,
    passes the found content to a provided response handler
    once fetching has finished.
    """

    url: str
    search_params: ItemSearch
    resource_type: ResourceType
    api_capability: ApiCapability
    response_handler: typing.Callable
    error_handler: typing.Callable

    response = None
    error = None
    client = None
    pagination = None

    def __init__(
            self,
            url: str,
            search_params: ItemSearch,
            resource_type: ResourceType,
            api_capability: ApiCapability = None,
            catalog_type: str = "api",  # 'api' or 'static'
            response_handler: typing.Callable = None,
            error_handler: typing.Callable = None,
            auth_config = None,
    ):
        super().__init__()
        self.url = url
        self.search_params = search_params
        self.resource_type = resource_type
        self.api_capability = api_capability
        self.catalog_type = catalog_type
        self.response_handler = response_handler
        self.error_handler = error_handler
        self.auth_config = auth_config

    def _try_static_fallback(self):
        """
        Try to fetch items using static catalog navigation as fallback.
        
        :returns: True if fallback succeeded, False otherwise
        :rtype: bool
        """
        logger.warning(f"Attempting static catalog fallback for {self.url}")
        logger.info("Auto-switching to static catalog navigation (recursive get_items)")
        
        try:
            # Get collection filter from search params if available
            collection_filter = None
            if self.search_params and hasattr(self.search_params, 'collections') and self.search_params.collections:
                collection_filter = self.search_params.collections
                logger.info(f"Applying collection filter in fallback mode: {collection_filter}")
            
            # Use recursive navigation for hierarchical static catalogs
            items = get_all_items_recursive(
                self.client, 
                max_items=100, 
                max_depth=3,
                collection_filter=collection_filter
            )
            
            # Convert pystac.Item objects to models.Item objects
            self.response = [self._prepare_single_item(item) for item in items if item]
            # Filter out None results
            self.response = [r for r in self.response if r is not None]
            
            # Create pagination object for fallback mode
            self.pagination = ResourcePagination(
                total_items=len(self.response),
                total_pages=1,
                current_page=1,
                page_size=len(self.response)
            )
            logger.info(f"✅ Static catalog fallback successful: {len(self.response)} items")
            logger.warning(f"⚠️ This catalog should be configured as 'Static Catalog' type in connection settings")
            return True
            
        except Exception as fallback_error:
            logger.error(f"❌ Static catalog fallback failed: {str(fallback_error)}", exc_info=True)
            return False
    
    def run(self):
        """
        Runs the main task operation in the background.

        :returns: Whether the task completed successfully
        :rtype: bool
        """
        logger.debug(f"ContentFetcherTask starting: url={self.url}, resource_type={self.resource_type}")
        
        pystac_auth = {}
        if self.auth_config:
            logger.debug("Preparing auth properties")
            pystac_auth = self.prepare_auth_properties(
                self.auth_config
            )
        
        # Get proxy and SSL configuration
        stac_io = None
        try:
            logger.debug("Creating QGIS-based StacApiIO (avoids Python SSL module)")
            from .qgis_stac_io import QgisStacApiIO
            
            # QgisStacApiIO uses QGIS QgsNetworkAccessManager which handles proxy/SSL automatically
            # No need to configure proxy manually - QGIS settings are respected
            stac_io = QgisStacApiIO(headers=pystac_auth.get('headers', {}))
            
            logger.info("QgisStacApiIO created - using QGIS network stack (SSL via Qt)")
            
        except Exception as e:
            # If QGIS StacIO fails, log error
            logger.error(f"Failed to create QgisStacApiIO: {e}", exc_info=True)
            log(f"Error: QGIS network not available: {e}", info=False, notify=True)
        
        try:
            logger.info(f"Opening STAC client: {self.url}")
            
            # Open client with QGIS StacIO
            if stac_io:
                from ..lib.pystac_client import Client
                self.client = Client.from_file(self.url, stac_io=stac_io, headers=pystac_auth.get('headers', {}))
                logger.info("STAC client opened with QgisStacApiIO")
            else:
                # This will fail if SSL module is not available, but try anyway as fallback
                logger.warning("Falling back to default Client.open() - may fail without SSL module")
                self.client = Client.open(self.url, headers=pystac_auth.get('headers', {}))
                logger.info("STAC client opened with default configuration")
            
            logger.info(f"STAC client opened successfully")
            
            if self.resource_type == \
                    ResourceType.FEATURE:
                logger.debug("Fetching FEATURE resources")
                
                # Static catalogs: use get_items() instead of search()
                if self.catalog_type == CatalogType.STATIC.value:
                    logger.info("Using static catalog navigation (recursive get_items)")
                    
                    # For static catalogs with collection selected: use collection URL directly
                    catalog_url = self.url
                    if self.search_params and hasattr(self.search_params, 'collection_url') and self.search_params.collection_url:
                        catalog_url = self.search_params.collection_url
                        logger.info(f"🎯 Using collection-specific URL: {catalog_url}")
                    else:
                        logger.info(f"🌐 Using root catalog URL: {catalog_url}")
                    
                    try:
                        # Re-open client with the appropriate URL (root or collection)
                        if catalog_url != self.url:
                            logger.info(f"Opening new client for collection URL...")
                            if stac_io:
                                from ..lib.pystac_client import Client
                                collection_client = Client.from_file(catalog_url, stac_io=stac_io, headers=pystac_auth.get('headers', {}))
                            else:
                                collection_client = Client.open(catalog_url, headers=pystac_auth.get('headers', {}))
                            logger.info(f"Client opened for collection")
                        else:
                            collection_client = self.client
                        
                        # Get collection filter from search params if available
                        collection_filter = None
                        if self.search_params and hasattr(self.search_params, 'collections') and self.search_params.collections:
                            collection_filter = self.search_params.collections
                            logger.info(f"📋 Collection filter provided: {collection_filter}")
                            logger.info(f"📋 Filter type: {type(collection_filter)}, Length: {len(collection_filter)}")
                        else:
                            logger.info("📋 No collection filter - will search all collections")
                        
                        # Use recursive navigation for hierarchical static catalogs
                        items = get_all_items_recursive(
                            collection_client,  # Use collection-specific client if available 
                            max_items=100, 
                            max_depth=3,
                            collection_filter=collection_filter
                        )
                        
                        # Convert pystac.Item objects to models.Item objects
                        self.response = [self._prepare_single_item(item) for item in items if item]
                        # Filter out None results
                        self.response = [r for r in self.response if r is not None]
                        
                        # Create pagination object for static catalogs
                        self.pagination = ResourcePagination(
                            total_items=len(self.response),
                            total_pages=1,
                            current_page=1,
                            page_size=len(self.response)
                        )
                        logger.info(f"Static catalog fetch completed: {len(self.response)} items")
                    except Exception as e:
                        error_msg = (
                            f"Failed to retrieve items from static catalog.\n\n"
                            f"Error: {str(e)}\n\n"
                            f"Static catalogs use hierarchical navigation (rel='child' and rel='item' links). "
                            f"Please verify the catalog URL is correct and accessible."
                        )
                        logger.error(f"Static catalog error: {str(e)}")
                        raise Exception(error_msg) from e
                else:
                    # API catalogs: use search()
                    logger.info("Using STAC API search")
                    try:
                        if self.search_params:
                            response = self.client.search(
                                **self.search_params.params()
                            )
                        else:
                            response = self.client.search()
                        self.response = self.prepare_items_results(
                            response
                        )
                        logger.info(f"Feature search completed: {len(self.response) if isinstance(self.response, list) else 'unknown'} results")
                    except NotImplementedError as e:
                        # Automatic fallback: try static catalog mode
                        logger.warning(f"API search not implemented (NotImplementedError): {str(e)}")
                        if not self._try_static_fallback():
                            error_msg = (
                                f"This catalog does not support search operations.\n\n"
                                f"The URL '{self.url}' appears to be a static STAC catalog (JSON file), "
                                f"not a STAC API endpoint.\n\n"
                                f"Please edit this connection and change 'Catalog Type' to 'Static Catalog (hierarchical)'."
                            )
                            logger.error(f"NotImplementedError: {str(e)}")
                            logger.error(f"URL: {self.url}")
                            logger.error(error_msg)
                            raise Exception(error_msg) from e

            elif self.resource_type == \
                    ResourceType.COLLECTION:
                logger.debug("Fetching COLLECTION resources")
                if self.search_params and self.search_params.get('collection_id'):
                    response = self.client.get_collection(
                        self.search_params.get('collection_id')
                    )
                    self.response = self.prepare_collection_result(
                        response
                    )
                else:
                    response = self.client.get_collections()
                    self.response = self.prepare_collections_results(
                        response
                    )
                logger.info(f"Collection fetch completed")

            elif self.resource_type == ResourceType.CONFORMANCE:
                logger.debug("Fetching CONFORMANCE information")
                if self.client._stac_io and \
                        self.client._stac_io._conformance:
                    self.response = self.prepare_conformance_results(
                        self.client._stac_io._conformance
                    )
                else:
                    self.error = tr("No conformance available")
                    logger.warning("No conformance available")
                self.pagination = ResourcePagination()
            else:
                raise NotImplementedError
        except (
                APIError,
                NotImplementedError,
                JSONDecodeError,
                STACTypeError
        ) as err:
            logger.error(f"STAC API Error ({type(err).__name__}): {str(err)}", exc_info=True)
            log(str(err))
            self.error = str(err)
        except Exception as err:
            error_str = str(err)
            logger.critical(f"Unexpected error in ContentFetcherTask: {type(err).__name__}: {error_str}", exc_info=True)
            
            # Check if error is related to /search endpoint (likely static catalog)
            # Common patterns: "Operation canceled", "HTTP 4xx/5xx", "/search" in error
            is_search_error = (
                self.resource_type == ResourceType.FEATURE and
                self.catalog_type != CatalogType.STATIC.value and
                ('/search' in error_str.lower() or 
                 'operation canceled' in error_str.lower() or
                 'http 400' in error_str.lower() or
                 'http 404' in error_str.lower() or
                 'http 405' in error_str.lower() or  # Method Not Allowed
                 'http 501' in error_str.lower() or
                 'not found' in error_str.lower() or
                 'method not allowed' in error_str.lower())
            )
            
            if is_search_error:
                logger.warning(f"Search endpoint error detected, attempting static catalog fallback")
                logger.info(f"Original error: {error_str}")
                if self._try_static_fallback():
                    # Fallback succeeded, return success
                    return self.response is not None
                else:
                    # Fallback failed, set error message
                    self.error = (
                        f"Failed to access search endpoint.\n\n"
                        f"Error: {error_str}\n\n"
                        f"This catalog may be a static STAC catalog. "
                        f"Please try changing the connection type to 'Static Catalog (hierarchical)'."
                    )
            else:
                log(f"Unexpected error: {error_str}")
                self.error = error_str

        return self.response is not None

    def prepare_auth_properties(self, auth_config_id):
        """ Fetches the required headers and parameters
         from the QGIS Authentication method with the passed configuration id
         and return their values in a dictionary

         :param auth_config_id: Authentication method configuration id
         :type auth_config_id: str

         :returns: Authentication properties
         :rtype: dict
         """
        auth_props = {}
        auth_mgr = QgsApplication.authManager()
        auth_cfg = QgsAuthMethodConfig()
        auth_mgr.loadAuthenticationConfig(
            auth_config_id,
            auth_cfg,
            True
        )
        if auth_cfg.method() == QgsAuthMethods.API_HEADER.value:
            auth_props["headers"] = auth_cfg.configMap()
            auth_props["parameters"] = auth_cfg.configMap()

        return auth_props

    def prepare_collection_result(
            self,
            collection_response
    ):
        """ Prepares the collection result

          :param collection_response: Collection
          :type collection_response: pystac_client.CollectionClient

          :returns: Collection instance
          :rtype: Collection
          """

        spatial = vars(collection_response.extent.spatial)
        bbox = spatial.get('bbox') \
            if 'bbox' in spatial.keys() else spatial.get('bboxes')

        temporal = vars(collection_response.extent.temporal)
        interval = temporal.get('interval') \
            if 'bbox' in spatial.keys() else spatial.get('intervals')
        spatial_extent = SpatialExtent(
            bbox=bbox
        )
        temporal_extent = TemporalExtent(
            interval=interval
        )

        extent = ResourceExtent(
            spatial=spatial_extent,
            temporal=temporal_extent
        )

        links = []

        for link in collection_response.links:
            link_dict = vars(link)
            link_type = link_dict.get('type') \
                if 'type' in link_dict.keys() \
                else link_dict.get('media_type')
            resource_link = ResourceLink(
                href=link.href,
                rel=link.rel,
                title=link.title,
                type=link_type
            )
            links.append(resource_link)

        providers = []
        for provider in collection_response.providers or []:
            resource_provider = ResourceProvider(
                name=provider.name,
                description=provider.description,
                roles=provider.roles,
                url=provider.url
            )
            providers.append(resource_provider)

        # Avoid Attribute error and assign None to
        # properties that are not available.
        collection_dict = vars(collection_response)
        id = collection_dict.get('id', None)
        title = collection_dict.get('title', None)
        description = collection_dict.get('description', None)
        keywords = collection_dict.get('keywords', None)
        license = collection_dict.get('license', None)
        stac_version = collection_dict.get('stac_version', None)
        summaries = collection_dict.get('summaries', None)

        collection_result = Collection(
            id=id,
            title=title,
            description=description,
            keywords=keywords,
            license=license,
            stac_version=stac_version,
            summaries=summaries,
            extent=extent,
            links=links,
            providers=providers,
        )

        return collection_result

    def prepare_collections_results(
            self,
            collections_response
    ):
        """ Prepares the collections results

        :param collections_response: Collection generator
        :type collections_response: pystac_client.CollectionClient

        :returns: List of collections
        :rtype: list
        """
        collections = []
        for collection in collections_response:
            # Avoid Attribute error and assign None to properties that are not available
            collection_dict = vars(collection)
            id = collection_dict.get('id', None)
            title = collection_dict.get('title', None)

            collection_result = Collection(
                id=id,
                title=title,
            )
            collections.append(collection_result)
        return collections

    def prepare_items_results(self, response):
        """ Prepares the search items results

        :param response: Fetched response from the pystac-client library
        :type response: pystac_client.ItemSearch

        :returns: Collection of items in a list
        :rtype: list
        """
        self.pagination = ResourcePagination()
        count = 1
        items_generator = response.get_item_collections()
        prev_collection = None
        items_collection = None
        page = self.search_params.page \
            if self.search_params else Constants.PAGE_SIZE
        while True:
            try:
                collection = next(items_generator)
                prev_collection = collection
                if page == count:
                    items_collection = collection
                    break
                count += 1
            except StopIteration:
                self.pagination.total_pages = count
                items_collection = prev_collection
                break
        items = self.get_items_list(items_collection)
        return items

    def get_items_list(self, items_collection):
        """ Gets and prepares the items list from the
        pystac-client Collection generator

        :param items_collection: The STAC item collection generator
        :type items_collection: pystac_client.CollectionClient

        :returns: List of items
        :rtype: models.Item
        """
        items = []
        properties = None
        items_list = items_collection.items if items_collection else []

        for item in items_list:
            item_result = self._prepare_single_item(item)
            if item_result:
                items.append(item_result)

        return items
    
    def _prepare_single_item(self, item):
        """
        Prepare a single pystac.Item into a models.Item object.
        
        :param item: pystac.Item object
        :type item: pystac.Item
        
        :returns: Prepared Item object or None if error
        :rtype: models.Item or None
        """
        try:
            properties_datetime = item.properties.get("datetime")

            item_datetime = parser.parse(
                properties_datetime
            ) if properties_datetime else None

            properties_start_date = item.properties.get("start_date")
            start_date = parser.parse(
                properties_start_date,
            ) if properties_start_date else None

            properties_end_date = item.properties.get("end_date")

            end_date = parser.parse(
                properties_end_date
            ) if properties_end_date else None

            cloud_cover = item.properties.get("eo:cloud_cover")

            properties = ResourceProperties(
                resource_datetime=item_datetime,
                eo_cloud_cover=cloud_cover,
                start_date=start_date,
                end_date=end_date
            )
        except Exception as e:
            log(
                f"Error in parsing item properties datetime: {e}"
            )
            properties = None
            
        assets = []
        for key, asset in item.assets.items():
            title = asset.title if asset.title else key
            item_asset = ResourceAsset(
                href=asset.href,
                title=title,
                description=asset.description,
                type=asset.media_type,
                roles=asset.roles or []
            )
            assets.append(item_asset)
            
        item_result = Item(
            id=item.id,
            item_uuid=uuid.uuid4(),
            properties=properties,
            collection=item.collection_id,
            assets=assets,
            stac_object=item,
        )
        
        if item.geometry:
            item_result.geometry = item.geometry
            
        return item_result

    def prepare_conformance_results(self, conformance):
        """ Prepares the fetched conformance classes

        :param conformance: Fetched list of the conformance classes  API
        :type conformance: list

        :returns: Conformance classes settings instance list
        :rtype: list
        """
        conformance_classes = []
        for uri in conformance:
            parts = uri.split('/')
            name = parts[len(parts) - 1]
            conformance_instance = Conformance(
                id=uuid.uuid4(),
                name=name,
                uri=uri,
            )
            conformance_classes.append(conformance_instance)

        return conformance_classes

    def finished(self, result: bool):
        """
        Called after the task run() completes either successfully
        or upon early termination.

        :param result: Whether task completed with success
        :type result: bool
        """
        if result:
            self.response_handler(self.response, self.pagination)
        else:
            message = tr("Problem in fetching content for {}."
                         "Error details, {}").format(self.url, self.error)
            self.error_handler(message)


class NetworkFetcher(QtCore.QObject):
    """
    Handles fetching of STAC API resources that are not available
    via the pystac_client library
    """

    url: str
    response_handler: typing.Callable
    error_handler: typing.Callable

    def __init__(
            self,
            url,
            response_handler,
            error_handler
    ):
        self.url = url
        self.response_handler = response_handler
        self.error_handler = error_handler
        self.response_data = None

    def get_queryable(self, fetch_type, resource):
        """ Fetches the catalog queryable properties"""

        if fetch_type == QueryableFetchType.CATALOG:
            endpoint = "queryables"
        elif fetch_type == QueryableFetchType.COLLECTION:
            endpoint = f"collections/{resource}/queryables"
        else:
            raise NotImplementedError

        url = f"{self.url.strip('/')}/{endpoint}"
        request = QtNetwork.QNetworkRequest(
            QtCore.QUrl(
                url
            )
        )
        self.network_task(
            request,
            self.queryable_response,
            self.error_handler
        )

    def queryable_response(self, content):
        """ Callback to handle the queryable properties
        network response.

        :param content: Network response data
        :type content: QByteArray
        """
        self.response_handler(content)

    def network_task(
            self,
            request,
            handler,
            error_handler,
            auth_config=""
    ):
        """Fetches the response from the given request.

        :param request: Network request
        :type request: QNetworkRequest

        :param handler: Callback function to handle the response
        :type handler: Callable

        :param auth_config: Authentication configuration string
        :type auth_config: str
        """
        task = QgsNetworkContentFetcherTask(
            request,
            authcfg=auth_config
        )
        response_handler = partial(
            self.response,
            task,
            handler,
            error_handler

        )
        task.fetched.connect(response_handler)
        task.run()

    def response(
            self,
            task,
            handler,
            error_handler
    ):
        """ Handles the returned response

        :param task: QGIS task that fetches network content
        :type task:  QgsNetworkContentFetcherTask
        """
        reply = task.reply()
        error = reply.error()
        if error == QtNetwork.QNetworkReply.NoError:
            contents: QtCore.QByteArray = reply.readAll()
            try:
                data = json.loads(
                    contents.data().decode()
                )
                queryable = self.prepare_queryable(data)
                handler(queryable)
            except json.decoder.JSONDecodeError as err:
                log(tr("Problem parsing network response"))
        else:
            error_handler(tr("Problem fetching response from network"))

            log(tr("Problem fetching response from network"))

    def prepare_queryable(self, data):
        """ Prepares the passed data dict into a plugin Queryable instance.

        :param data: Response data
        :type data:  dict

        :returns: STAC queryable properties
        :rtype: Queryable
        """
        properties = []

        queryable_properties = data.get('properties', {})

        for key, value in queryable_properties.items():
            enum_values = value.get('enum')
            property_type = value.get('type')
            if enum_values:
                property_type = 'enum'
            if key == 'datetime':
                property_type = 'datetime'

            queryable_property = QueryableProperty(
                name=key,
                title=value.get('title'),
                description=value.get('description'),
                ref=value.get('$ref'),
                type=property_type,
                minimum=value.get('minimum'),
                maximum=value.get('maximum'),
                values=enum_values
            )
            properties.append(queryable_property)

        queryable = Queryable(
            schema=data.get('$schema'),
            id=data.get('id'),
            type=data.get('type'),
            title=data.get('title'),
            description=data.get('description'),
            properties=properties,
        )

        return queryable
