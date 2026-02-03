import requests
import json

# Test Maxar static catalog structure - including sub-collection with items
urls = [
    "https://maxar-opendata.s3.amazonaws.com/events/catalog.json",
    "https://maxar-opendata.s3.amazonaws.com/events/Emilia-Romagna-Italy-flooding-may23/collection.json",
    "https://maxar-opendata.s3.amazonaws.com/events/Emilia-Romagna-Italy-flooding-may23/ard/acquisition_collections/10300100BF164000_collection.json",
]

for url in urls:
    print(f"\n{'='*80}")
    print(f"URL: {url}")
    print('='*80)
    
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        
        print(f"Type: {data.get('type')}")
        print(f"STAC Version: {data.get('stac_version')}")
        
        links = data.get('links', [])
        print(f"\nTotal links: {len(links)}")
        
        # Count by rel type
        rel_types = {}
        for link in links:
            rel = link.get('rel', 'unknown')
            rel_types[rel] = rel_types.get(rel, 0) + 1
        
        print("\nLinks by type:")
        for rel, count in sorted(rel_types.items()):
            print(f"  {rel}: {count}")
        
        # Show first 3 item links if any
        item_links = [l for l in links if l.get('rel') == 'item']
        if item_links:
            print(f"\nFirst 3 item links:")
            for link in item_links[:3]:
                print(f"  {link.get('href')}")
        
        # Show first 3 child links if any
        child_links = [l for l in links if l.get('rel') == 'child']
        if child_links:
            print(f"\nFirst 3 child links:")
            for link in child_links[:3]:
                print(f"  {link.get('href')}")
                
    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "="*80)
