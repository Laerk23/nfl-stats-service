from fastapi import FastAPI
import requests

app = FastAPI()

PLAYERS_CACHE = None

def load_players():
    global PLAYERS_CACHE
    if PLAYERS_CACHE is None:
        resp = requests.get("https://api.sleeper.app/v1/players/nfl")
        resp.raise_for_status()
        PLAYERS_CACHE = resp.json()
    return PLAYERS_CACHE


@app.get('/')

def root():
    return {'message': 'NFL Stats API running'}