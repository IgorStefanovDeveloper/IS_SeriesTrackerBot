import aiohttp

class TMDbClient:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, api_key):
        self.api_key = api_key

    async def search_series(self, query):
        url = f"{self.BASE_URL}/search/tv?api_key={self.api_key}&query={query}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()
