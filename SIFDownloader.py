from pystac import Collection
from pystac_client import ItemSearch
import requests
import hashlib

# COLLECTION = "https://data-portal.s5p-pal.com/api/s5p-l2/collection.json"
COLLECTION = "https://data-portal.s5p-pal.com/api/s5p-l2/L2B_SIF___/collection.json"

def get_most_recent_product(collection_url):
    collection = Collection.from_file(collection_url)
    endpoint = collection.get_single_link("search").target
    
    timefilter = "2024"
    items = ItemSearch(endpoint, datetime=timefilter).items()

    # View list of files found
    # for item in items:
        
    #     product_filename = item.properties["physical_name"]
    #     print(f"Found: {product_filename}...")

    for item in items:

        download_url = item.assets["download"].href
        product_filename = item.properties["physical_name"]
        product_hash = item.properties["hash"]

        print(f"Downloading {product_filename}...")
        r = requests.get(download_url)
    
        save_path = f"G:\\TROPOMI\\new\\{product_filename}"

        with open(save_path, "wb") as product_file:
            product_file.write(r.content)
    
        file_hash = "md5:" + hashlib.md5(open(save_path, "rb").read()).hexdigest()
        print("Checking hash...")
        assert file_hash == product_hash
        print("Product was downloaded correctly")

if __name__ == "__main__":
    get_most_recent_product(COLLECTION)