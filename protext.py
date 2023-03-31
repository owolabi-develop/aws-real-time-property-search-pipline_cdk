from homeharvest import scrape_property
from datetime import datetime
import json
from pprint import pprint
import random
locations = ['Dallas, TX',"San Diego, CA"]
listing_types = ["sold","for_sale","for_rent","pending"]
past_days = [_ for _ in range(10,50)]


properties = scrape_property(
  radius=30.5,
  location=random.choice(locations),
  listing_type=random.choice(listing_types),  # or (for_sale, for_rent, pending)
  past_days=random.choice(past_days),  # sold in last 30 days - listed in last 30 days if (for_sale, for_rent)
  
 
)


# Export to csv
properties.to_json(orient='records',indent=5)

data = json.loads(properties.to_json(orient='records'))

for datas in data:
    prop = json.dumps(datas).encode('utf-8')
    
    pprint(datas,indent=4)