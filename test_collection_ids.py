import requests
import json

# Test what collection IDs are actually used in Maxar catalog

print("="*80)
print("TESTING MAXAR COLLECTION IDS")
print("="*80)

# 1. Get root catalog
print("\n1. ROOT CATALOG:")
r = requests.get("https://maxar-opendata.s3.amazonaws.com/events/catalog.json")
catalog = r.json()
print(f"   Type: {catalog.get('type')}")
print(f"   ID: {catalog.get('id')}")

# Find Emilia-Romagna link
emilia_link = None
for link in catalog.get('links', []):
    if 'Emilia-Romagna' in link.get('href', ''):
        emilia_link = link.get('href')
        print(f"\n   Found Emilia-Romagna link: {emilia_link}")
        break

# 2. Get Emilia-Romagna collection
if emilia_link:
    print("\n2. EMILIA-ROMAGNA COLLECTION:")
    full_url = f"https://maxar-opendata.s3.amazonaws.com/events/{emilia_link}"
    r = requests.get(full_url)
    collection = r.json()
    print(f"   Type: {collection.get('type')}")
    print(f"   ID: '{collection.get('id')}'")  # THIS IS KEY!
    print(f"   Title: {collection.get('title')}")
    
    # Get first sub-collection
    sub_link = None
    for link in collection.get('links', []):
        if link.get('rel') == 'child':
            sub_link = link.get('href')
            print(f"\n   First sub-collection link: {sub_link}")
            break
    
    # 3. Get sub-collection
    if sub_link:
        print("\n3. SUB-COLLECTION (acquisition):")
        # Build full URL (sub_link is relative)
        base_url = "https://maxar-opendata.s3.amazonaws.com/events/Emilia-Romagna-Italy-flooding-may23/"
        full_sub_url = base_url + sub_link
        r = requests.get(full_sub_url)
        sub_collection = r.json()
        print(f"   Type: {sub_collection.get('type')}")
        print(f"   ID: '{sub_collection.get('id')}'")
        print(f"   Title: {sub_collection.get('title')}")
        
        # Get first item
        item_link = None
        for link in sub_collection.get('links', []):
            if link.get('rel') == 'item':
                item_link = link.get('href')
                print(f"\n   First item link: {item_link}")
                break
        
        # 4. Get item
        if item_link:
            print("\n4. ITEM:")
            # Build full URL (item_link is relative)
            base_sub_url = "https://maxar-opendata.s3.amazonaws.com/events/Emilia-Romagna-Italy-flooding-may23/ard/acquisition_collections/"
            full_item_url = base_sub_url + item_link
            r = requests.get(full_item_url)
            item = r.json()
            print(f"   Type: {item.get('type')}")
            print(f"   ID: '{item.get('id')}'")
            print(f"   Collection ID: '{item.get('collection')}'")  # THIS IS KEY!
            print(f"   Properties collection: '{item.get('properties', {}).get('collection')}'")

print("\n" + "="*80)
print("KEY FINDINGS:")
print("- Check if collection.id matches item.collection")
print("- This determines what filter value to use")
print("="*80)
