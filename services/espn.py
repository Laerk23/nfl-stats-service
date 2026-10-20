import httpx

print("USING ESPN.PY FROM:", __file__)

SEARCH_URL = "https://search-api.espn.com/v1/search"


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
        "limit": 50,
        "type": "player",
        "sport": "football",
        "league": "nfl"
    }

    data = await _get(SEARCH_URL, params=params)
    if not data or "results" not in data:
        print("NO RESULTS FOUND")
        return []

    results = []

    for item in data["results"]:
        # ESPN search API returns clean player objects
        athlete = item.get("athlete", {})
        if not athlete:
            continue

        results.append({
            "espn_id": athlete.get("id"),
            "full_name": athlete.get("fullName"),
            "team": athlete.get("team", {}).get("displayName"),
            "position": athlete.get("position", {}).get("abbreviation"),
        })

    return results
