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


def extract_athlete_id(espn_id: str):
    """
    Supports BOTH:
    - ESPN UID: s:20~l:28~a:4431452
    - Numeric ID: 4431452
    """
    if "~a:" in espn_id:
        return espn_id.split("~a:")[-1]
    return espn_id

async def get_player_details(espn_id: str):
    athlete_id = extract_athlete_id(espn_id)
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


async def get_player_stats(espn_id: str):
    athlete_id = extract_athlete_id(espn_id)
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

async def get_player_team(espn_id: str):
    # Convert ESPN UID → numeric athlete ID
    athlete_id = extract_athlete_id(espn_id)

    # Step 1: fetch athlete metadata
    url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{athlete_id}?enable=team"

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code != 200:
            return None

        data = r.json()

    # Step 2: extract the $ref link
    team_ref = data.get("team", {}).get("$ref")
    if not team_ref:
        return None

    # Step 3: fetch the actual team object
    async with httpx.AsyncClient() as client:
        team_res = await client.get(team_ref)
        if team_res.status_code != 200:
            return None

        team_data = team_res.json()

    # Step 4: extract fields
    return {
        "team_name": team_data.get("name"),
        "team_logo": team_data.get("logos", [{}])[0].get("href"),
        "team_abbrev": team_data.get("abbreviation"),
        "team_id": team_data.get("id"),
    }

async def search_players_by_name(query: str):
    print("SEARCH FUNCTION HIT WITH:", query)

    params = {"query": query, "limit": 10}
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

            espn_id = item.get("uid")

            # Base player object (your original fields)
            player = {
                "espn_id": espn_id,
                "full_name": item.get("displayName"),
                "team": item.get("subtitle"),  # ESPN search team (often wrong or null)
                "image": item.get("image", {}).get("default"),
                "player_url": item.get("link", {}).get("web"),
            }

            # ⭐ ENRICH WITH REAL TEAM DATA FROM CORE API
            team_info = await get_player_team(espn_id)

            if team_info:
                player["team"] = team_info["team_name"]
                player["team_logo"] = team_info["team_logo"]
                player["team_abbrev"] = team_info["team_abbrev"]
                player["team_id"] = team_info["team_id"]
            else:
                player["team"] = "N/A"
                player["team_logo"] = None
                player["team_abbrev"] = None
                player["team_id"] = None

            results.append(player)

    return results



async def get_full_player_card(espn_id: str):
    details = await get_player_details(espn_id)
    stats = await get_player_stats(espn_id)
    team_info = await get_player_team(espn_id)

    if team_info:
        details["team"] = team_info.get("team_name")
        details["team_logo"] = team_info.get("team_logo")
        details["team_abbrev"] = team_info.get("team_abbrev")
        details["team_id"] = team_info.get("team_id")

    return {
        "details": details,
        "stats": stats
    }