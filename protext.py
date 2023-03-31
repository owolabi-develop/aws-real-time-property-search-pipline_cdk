from faker import Faker
import random
import json
from pprint import pprint
from datetime import datetime

fake = Faker()



def generate_property():
    """Generate a fake real estate property."""
    property_types = ['SINGLE_FAMILY', 'CONDO', 'TOWNHOUSE']
    property_statuses = ['For Sale', 'Sold', 'Pending']

    property_details = {
        "property_url": fake.url(),
        "mls": "SDCA",
        "mls_id": fake.random_number(digits=9),
        "status": random.choice(property_statuses),  # Random status
        "style": {
            "name": random.choice(property_types),
            "value": random.choice(property_types)
        },
        "street": fake.street_address(),
        "unit": fake.random_int(min=1, max=100) if random.choice([True, False]) else None,  # Randomly assign a unit number or None
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip_code": fake.zipcode(),
        "beds": fake.random_int(min=1, max=5),
        "full_baths": fake.random_int(min=1, max=3),
        "half_baths": fake.random_int(min=0, max=1) if random.choice([True, False]) else None,  # Randomly assign a half bath or None
        "sqft": fake.random_int(min=800, max=5000),
        "year_built": fake.random_int(min=1900, max=2022),
        "days_on_mls": fake.random_int(min=1, max=100),
        "list_price": fake.random_int(min=50000, max=2000000),
        "list_date": fake.date_this_year().strftime('%Y-%m-%d'),
        "sold_price": fake.random_int(min=50000, max=2000000),
        "last_sold_date": fake.date_this_year().strftime('%Y-%m-%d'),
        "lot_sqft": fake.random_int(min=2000, max=10000),
        "price_per_sqft": fake.random_int(min=50, max=500),
        "latitude": float(fake.latitude()),
        "longitude": float(fake.longitude()),
        "stories": fake.random_int(min=1, max=3),
        "hoa_fee": fake.random_int(min=0, max=500),
        "parking_garage": fake.random_int(min=0, max=3),
        "primary_photo": fake.image_url(width=480, height=360),  # Generating a fake primary photo URL
        "alt_photos": None  # No alternative photos for now
    }
    return property_details

def generate_properties(num_properties):
    """Generate multiple fake real estate properties."""
    properties = [generate_property() for _ in range(num_properties)]
    return properties

if __name__ == "__main__":
    num_properties = 200
    properties = generate_properties(num_properties)

    pprint(properties,indent=4)
