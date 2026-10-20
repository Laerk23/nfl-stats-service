from fastapi import FastAPI
from services.espn import search_players_by_name, get_player_details, get_player_stats

app = FastAPI()


@app.get("/players/search")
async def search_players(q: str):
    return await search_players_by_name(q)


@app.get("/players/{espn_id}/details")
async def player_details(espn_id: str):
    return await get_player_details(espn_id)


@app.get("/players/{espn_id}/stats")
async def player_stats(espn_id: str):
    return await get_player_stats(espn_id)
