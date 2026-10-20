from fastapi import FastAPI, Query
from services.espn import search_players_by_name

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/players/search")
async def search_players(q: str = Query(..., min_length=2)):
    return await search_players_by_name(q)
