import os

HOST = os.getenv('HOST_IP', 'localhost')
CLIENT_PORT = int(os.getenv('CLIENT_PORT', 8080))
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
APP_TOKEN = os.getenv('APP_TOKEN')
USER_TOKEN = os.getenv('USER_TOKEN')
FEED_LIMIT = int(os.getenv('FEED_LIMIT', 100))
