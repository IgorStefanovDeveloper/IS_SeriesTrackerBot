import os
from api_service.api_clients import TMDbClient

API_KEY_TMDB = os.getenv("API_KEY_TMDB")
tmdb_client = TMDbClient(API_KEY_TMDB)

def search_series(query):
    return tmdb_client.search_series(query)
