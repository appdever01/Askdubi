import requests

BASE_API_URL = "https://dimgrey-goldfinch-342565.hostingersite.com/wp-json/wp/v2" 

# Function to get available car brands from the REST API
def get_car_brands():
    response = requests.get(f"{BASE_API_URL}/mw-category?parent=0")
    if response.status_code == 200:
        return {brand['id']: brand['name'] for brand in response.json()}  # Creating a dictionary of ID : Name
    else:
        print(f"Error fetching car brands: {response.status_code}")
        return []
    
# print(get_car_brands())


# Function to get car models based on brand
def get_car_models(parentId):
    response = requests.get(f"{BASE_API_URL}/mw-category?parent={parentId}")
    if response.status_code == 200:
        models = {brandModel['id']: brandModel['name'] for brandModel in response.json()}  # Creating a dictionary of ID : Name
        return models
    else:
        print(f"Error fetching car models for brand {parentId}: {response.status_code}")
        return {}

# print(get_car_models(145))

def get_rendered_media(media_url):
    response = requests.get(media_url)
    if response.status_code == 200:
        media_data = response.json()
        return media_data['guid']['rendered']
    else:
        return None
    
def upload_to_imgur(url):
    """Uploads an image to Imgur and returns the download URL.

    Args:
        url: The URL of the image to upload.

    Returns:
        The download URL of the uploaded image, or None if the upload failed.
    """
    client_id = "77c0482b196b9f7"
    headers = {"Authorization": f"Client-ID {client_id}"}
    data = {"image": url}
    response = requests.post("https://api.imgur.com/3/upload", headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["data"]["link"]
    else:
        print(f"Error uploading image: {response.status_code}")
        return None


# Function to get car listings based on selected options
def get_car_results(brandId, modelId, year):
    response = requests.get(f"{BASE_API_URL}/mx-listings")
    if response.status_code == 200:
        car_listings = response.json()
        filtered_listings = [listing for listing in car_listings if modelId in listing.get('mw-category', []) and brandId in listing.get('mw-category', []) and year in listing.get('mw_year')]
        result = [{'id': listing['id'], 'name': listing['title']['rendered'].title(), 
                   'mw_condition': listing.get('mw_condition'), 'mw_year': listing.get('mw_year'), 
                   'mw_transmission': listing.get('mw_transmission'), 'mw_fueltype': listing.get('mw_fueltype'), 
                   'mw_price': listing.get('mw_price'), 'mw_enginesize': listing.get('mw_enginesize'), 
                   'mw_street_addr': listing.get('mw_street_addr'), 'mw_loc': listing.get('mw_loc'), 'link': listing.get('link'),
                   'image': upload_to_imgur(get_rendered_media(listing['_links']['wp:featuredmedia'][0]['href']))} for listing in filtered_listings]
        return result
    else:
        print(f"Error fetching car results: {response.status_code}")
        return []
    
# print(get_car_results(149,252,'2020'))

def get_car_years(brandId, modelId):
    """Extracts all years from car listings matching the given brand and model."""
    response = requests.get(f"{BASE_API_URL}/mx-listings")
    if response.status_code == 200:
        car_listings = response.json()
        filtered_listings = [listing for listing in car_listings if modelId in listing.get('mw-category', []) and brandId in listing.get('mw-category', [])]
        years = [listing.get('mw_year') for listing in filtered_listings if listing.get('mw_year')]
        return years
    else:
        print(f"Error fetching car results: {response.status_code}")
        return []

# print(get_car_years(149, 252))

def get_car_addresses(brandId, modelId, year):
    """Extracts all addresses from car listings matching the given brand, model, and year."""
    response = requests.get(f"{BASE_API_URL}/mx-listings")
    if response.status_code == 200:
        car_listings = response.json()
        filtered_listings = [listing for listing in car_listings if modelId in listing.get('mw-category', []) and brandId in listing.get('mw-category', []) and year in listing.get('mw_year')]
        addresses = [listing.get('mw_street_addr') for listing in filtered_listings if listing.get('mw_street_addr')]
        return addresses
    else:
        print(f"Error fetching car results: {response.status_code}")
        return []

# print(get_car_addresses(149,252,'2020'))