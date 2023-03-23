from os import getenv
from dotenv import load_dotenv
load_dotenv()

MONGODB_URL = f"mongodb://{getenv('MONGO_USERNAME')}:{getenv('MONGO_PASSWORD')}@{getenv('MONGO_HOST')}:{getenv('MONGO_SERVICE_PORT')}"