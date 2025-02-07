from aiohttp import web
from api_clients import TMDbClient
import os

API_KEY_TMDB = os.getenv("API_KEY_TMDB")
tmdb_client = TMDbClient(API_KEY_TMDB)

# Эндпоинт для поиска сериала
async def fetch_series(request):
    series_name = request.query.get("name")
    if series_name:
        result = await tmdb_client.search_series(series_name)
        return web.json_response(result)
    return web.json_response({"error": "Series name not provided"}, status=400)

# Эндпоинт для получения подробностей о сериале
async def fetch_series_details(request):
    series_id = request.match_info.get('series_id')
    if series_id:
        result = await tmdb_client.get_series_details(series_id)
        return web.json_response(result)
    return web.json_response({"error": "Series ID not provided"}, status=400)

# Запуск приложения
app = web.Application()
app.add_routes([
    web.get('/get_series', fetch_series),
    web.get('/get_series_details/{series_id}', fetch_series_details),
])

if __name__ == '__main__':
    web.run_app(app, port=5000)
