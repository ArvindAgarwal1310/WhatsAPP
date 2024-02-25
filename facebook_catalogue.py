from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.productcatalog import ProductCatalog
from facebook_business.adobjects.productitem import ProductItem
from facebook_business.adobjects.productset import ProductSet
from facebook_business.adobjects.productfeed import ProductFeed
from facebook_business.adobjects.productfeedupload import ProductFeedUpload
from facebook_business.adobjects.producteventstat import ProductEventStat
from facebook_business.exceptions import FacebookRequestError
from dotenv import load_dotenv
import os

load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")


# Set up your app credentials
app_id = APP_ID
app_secret = APP_SECRET
access_token = ACCESS_TOKEN
FacebookAdsApi.init(app_id, app_secret, access_token)

# Create a Product Catalog
catalog = ProductCatalog(parent_id='me')
catalog[ProductCatalog.Field.name] = 'My Catalog'
catalog.remote_create()

# Create a Product Feed
feed = ProductFeed(parent_id=catalog.get_id_assured())
feed[ProductFeed.Field.name] = 'My Product Feed'
feed[ProductFeed.Field.schedule] = {'interval': 'DAILY'}
feed.remote_create()

# Upload Products to the Product Feed (sample product)
product = ProductItem(parent_id=feed.get_id_assured())
product[ProductItem.Field.title] = 'Sample Product'
product[ProductItem.Field.description] = 'This is a sample product description.'
product[ProductItem.Field.price] = '10.99'
product[ProductItem.Field.brand] = 'Sample Brand'
product[ProductItem.Field.availability] = 'in stock'
product.remote_create()

# Create a Product Set
product_set = ProductSet(parent_id=catalog.get_id_assured())
product_set[ProductSet.Field.name] = 'My Product Set'
product_set[ProductSet.Field.filter] = {'retailer_id': {'is_any': ['<YOUR_RETAILER_ID>']}}
product_set.remote_create()

print("Catalog, feed, product, and product set created successfully!")
