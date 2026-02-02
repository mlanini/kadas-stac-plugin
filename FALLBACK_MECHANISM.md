# Automatic Static Catalog Fallback

## Overview

Il plugin KADAS STAC implementa un **meccanismo di fallback automatico intelligente** che rileva quando un catalogo STAC configurato come "API" è in realtà un **catalogo statico** e passa automaticamente alla navigazione gerarchica.

## Problema

Molti cataloghi STAC pubblici sono **cataloghi statici** (file JSON con link gerarchici) ma vengono erroneamente configurati come **STAC API** (endpoint con `/search`). Quando il plugin tenta di eseguire una ricerca su un catalogo statico, ottiene errori come:

- `HTTP 404: Not Found` - endpoint `/search` non esiste
- `HTTP 501: Not Implemented` - `/search` non implementato
- `Operation canceled` - timeout della richiesta a `/search`
- `NotImplementedError` - pystac_client rileva che non è un'API

## Soluzione: Fallback Automatico

### Funzionamento

1. **Tentativo iniziale**: Il plugin prova a usare `Client.search()` (modalità API)

2. **Rilevamento errore**: Se la ricerca fallisce con uno di questi pattern:
   - `NotImplementedError` (pystac_client)
   - `Operation canceled` (timeout Qt)
   - `HTTP 404` o `HTTP 501` (endpoint mancante)
   - Messaggio contenente `/search` o `not found`

3. **Fallback automatico**: Il plugin passa automaticamente a modalità statica:
   ```python
   items = get_all_items_recursive(
       client,
       max_items=100,
       max_depth=3,
       collection_filter=selected_collections
   )
   ```

4. **Navigazione ricorsiva**: Percorre la gerarchia del catalogo:
   - Livello 0: Root catalog
   - Livello 1: Event/Theme collections
   - Livello 2: Data collections
   - Livello 3: Items

5. **Messaggio all'utente**: Se il fallback ha successo, mostra un warning:
   ```
   ⚠️ This catalog should be configured as 'Static Catalog' type in connection settings
   ```

### Codice

```python
def _try_static_fallback(self):
    """
    Try to fetch items using static catalog navigation as fallback.
    
    Returns:
        bool: True if fallback succeeded, False otherwise
    """
    logger.warning(f"Attempting static catalog fallback for {self.url}")
    logger.info("Auto-switching to static catalog navigation (recursive get_items)")
    
    try:
        # Get collection filter from search params
        collection_filter = None
        if self.search_params and hasattr(self.search_params, 'collections'):
            collection_filter = self.search_params.collections
            logger.info(f"Applying collection filter: {collection_filter}")
        
        # Recursive navigation with safety limits
        items = get_all_items_recursive(
            self.client, 
            max_items=100, 
            max_depth=3,
            collection_filter=collection_filter
        )
        
        # Convert to plugin models
        self.response = [self._prepare_single_item(item) for item in items if item]
        self.response = [r for r in self.response if r is not None]
        
        # Create pagination
        self.pagination = ResourcePagination(
            total_items=len(self.response),
            total_pages=1,
            current_page=1,
            page_size=len(self.response)
        )
        
        logger.info(f"✅ Static catalog fallback successful: {len(self.response)} items")
        logger.warning(f"⚠️ Catalog should be configured as 'Static Catalog' type")
        return True
        
    except Exception as fallback_error:
        logger.error(f"❌ Static catalog fallback failed: {str(fallback_error)}")
        return False
```

## Esempi di Cataloghi Interessati

### Digital Earth Africa
- **URL**: `https://explorer.digitalearth.africa/stac/`
- **Problema**: Endpoint `/search` restituisce "Operation canceled"
- **Tipo reale**: Catalogo statico
- **Fallback**: ✅ Funziona con navigazione ricorsiva

### Digital Earth Australia  
- **URL**: `https://explorer.sandbox.dea.ga.gov.au/stac/`
- **Problema**: Stesso comportamento
- **Tipo reale**: Catalogo statico
- **Fallback**: ✅ Funziona con navigazione ricorsiva

### Maxar Open Data
- **URL**: `https://maxar-opendata.s3.amazonaws.com/events/catalog.json`
- **Problema**: NotImplementedError su `.search()`
- **Tipo reale**: Catalogo statico gerarchico (3 livelli)
- **Fallback**: ✅ Funziona con max_depth=3

## Limiti di Sicurezza

Per evitare loop infiniti e timeout, il fallback ha limiti:

- **Max Items**: 100 items totali
- **Max Depth**: 3 livelli di profondità
- **Collection Filter**: Solo le collezioni selezionate dall'utente

## Best Practice

### Per gli Utenti

1. **Primo utilizzo**: Lascia che il fallback automatico rilevi il tipo
2. **Dopo il warning**: Edita la connessione e cambia tipo a "Static Catalog"
3. **Performance**: I cataloghi statici configurati correttamente sono più veloci

### Per gli Sviluppatori

1. **Aggiungi nuovi cataloghi**: Specifica sempre `catalog_type`:
   ```python
   {
       "name": "My Static Catalog",
       "url": "https://example.com/catalog.json",
       "catalog_type": CatalogType.STATIC.value,  # ← Importante!
   }
   ```

2. **Testa il fallback**: Verifica che il meccanismo funzioni con:
   ```python
   # Forza errore per testare fallback
   raise NotImplementedError("Test fallback")
   ```

3. **Log dettagliati**: Il fallback genera log completi:
   - `[WARNING]` Attempting static catalog fallback
   - `[INFO]` Collection filter applied
   - `[INFO]` ✅ Fallback successful: N items
   - `[WARNING]` ⚠️ Should be configured as Static Catalog

## Messaggi di Errore

### Fallback Riuscito
```
⚠️ This catalog should be configured as 'Static Catalog' type in connection settings
```
→ **Azione**: Edita la connessione e cambia tipo

### Fallback Fallito
```
Failed to access search endpoint.

Error: HTTP None: Operation canceled

This catalog may be a static STAC catalog. 
Please try changing the connection type to 'Static Catalog (hierarchical)'.
```
→ **Azione**: Configura manualmente come Static Catalog

## Versione

- **Implementato in**: v1.1.2
- **File**: `src/kadas_stac/api/network.py`
- **Funzione**: `_try_static_fallback()`, linee 106-146
- **Exception handlers**: linee 367-380 (NotImplementedError), 422-444 (Exception)

## Riferimenti

- [STAC Specification](https://github.com/radiantearth/stac-spec)
- [Static vs API Catalogs](https://github.com/radiantearth/stac-spec/blob/master/overview.md#static-and-dynamic-catalogs)
- [pystac_client Documentation](https://pystac-client.readthedocs.io/)
