import aiohttp
import os

class TMDbClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.themoviedb.org/3"

    async def search_series(self, series_name):
        async with aiohttp.ClientSession() as session:
            params = {'api_key': self.api_key, 'query': series_name}
            async with session.get(f"{self.base_url}/search/tv", params=params) as response:
                return await response.json()

    async def get_series_details(self, series_id):
        async with aiohttp.ClientSession() as session:
            params = {'api_key': self.api_key}
            async with session.get(f"{self.base_url}/tv/{series_id}", params=params) as response:
                return await response.json()
