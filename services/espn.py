import httpx

print("USING ESPN.PY FROM:", __file__)

SEARCH_URL = "https://site.web.api.espn.com/apis/search/v2"


async def _get(url: str, params=None):
    async with httpx.AsyncClient(timeout=10, http2=False, verify=False) as client:
        r = await client.get(url, params=params, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print("ERROR:", r.status_code, url)
            return None
        return r.json()


async def search_players_by_name(query: str):
    print("SEARCH FUNCTION HIT WITH:", query)

    params = {
        "query": query,
        "limit": 10
    }

    data = await _get(SEARCH_URL, params=params)
    if not data or "results" not in data:
        print("NO RESULTS FOUND")
        return []

    results = []

    for group in data["results"]:
        if group.get("type") != "player":
            continue

        for item in group.get("contents", []):
            # Only NFL players
            if item.get("description") != "NFL":
                continue

            results.append({
                "espn_id": item.get("uid"),
                "full_name": item.get("displayName"),
                "team": item.get("subtitle"),
                "image": item.get("image", {}).get("default"),
                "player_url": item.get("link", {}).get("web"),
            })

    return results

async def get_player_details(espn_uid: str):
    athlete_id = espn_uid.split("~a:")[-1]
    url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athlete_id}"

    async with httpx.AsyncClient(timeout=10, verify=False) as client:
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print("DETAILS ERROR:", r.status_code)
            return None

        data = r.json()

    return {
        "id": athlete_id,
        "full_name": data.get("fullName"),
        "short_name": data.get("shortName"),
        "age": data.get("age"),
        "birth_date": data.get("birthDate"),
        "height": data.get("displayHeight"),
        "weight": data.get("displayWeight"),
        "college": data.get("college", {}).get("displayName") if data.get("college") else None,
        "draft": data.get("draft", {}).get("displayText") if data.get("draft") else None,
        "position": data.get("position", {}).get("displayName") if data.get("position") else None,
        "team": data.get("team", {}).get("displayName") if data.get("team") else None,
        "headshot": data.get("headshot", {}).get("href") if data.get("headshot") else None,
    }

import httpx

async def get_player_stats(espn_uid: str):
    athlete_id = espn_uid.split("~a:")[-1]

    url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athlete_id}/statistics"

    async with httpx.AsyncClient(timeout=10, verify=False) as client:
        r = await client.get(url, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            print("STATS ERROR:", r.status_code)
            return None

        stats_root = r.json()

    categories = stats_root.get("splits", {}).get("categories", [])
    parsed = {}

    for cat in categories:
        name = cat.get("name")
        stats = {}

        for stat in cat.get("stats", []):
            stats[stat.get("name")] = stat.get("value")

        parsed[name] = stats

    return parsed
