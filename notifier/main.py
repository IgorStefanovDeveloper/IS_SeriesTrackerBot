import os
from api_service.api_clients import TMDbClient

API_KEY_TMDB = os.getenv("API_KEY_TMDB")
tmdb_client = TMDbClient(API_KEY_TMDB)

async def fetch_series_api_id(series_name):
    results = await tmdb_client.search_series(series_name)
    if results["results"]:
        return results["results"][0]["id"]  # Возвращаем ID первого результата
    return None
