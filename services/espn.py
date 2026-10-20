import httpx
from typing import Optional, List, Dict

BASE_URL = "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl"


async def _get(url: str, params: Optional[dict] = None) -> Optional[dict]:
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
        if r.status_code != 200:
            return None
        return r.json()


async def get_player_by_id(espn_id: int) -> Optional[dict]:
    url = f"{BASE_URL}/athletes/{espn_id}"
    data = await _get(url)
    if not data:
        return None

    return {
        "espn_id": espn_id,
        "full_name": data.get("fullName"),
        "short_name": data.get("shortName"),
        "position": data.get("position", {}).get("abbreviation"),
        "team": data.get("team", {}).get("displayName"),
        "jersey": data.get("jersey"),
        "status": data.get("status", {}).get("type", {}).get("name"),
    }


async def search_players_by_name(query: str) -> List[Dict]:
    # ESPN search endpoint (public JSON)
    search_url = "https://site.web.api.espn.com/apis/search/v2"
    params = {
        "q": query,
        "type": "players",
        "league": "nfl",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(search_url, params=params)
        if r.status_code != 200:
            return []

        data = r.json()

    results = []
    for item in data.get("results", []):
        if item.get("type") != "player":
            continue

        athlete = item.get("athlete", {})
        results.append({
            "espn_id": athlete.get("id"),
            "full_name": athlete.get("fullName"),
            "team": athlete.get("team", {}).get("displayName"),
            "position": athlete.get("position", {}).get("abbreviation"),
        })

    return results


async def get_player_statistics(
    espn_id: int,
    season: Optional[int] = None,
    week: Optional[int] = None,
) -> Optional[dict]:
    url = f"{BASE_URL}/athletes/{espn_id}/statistics"
    params = {}

    if season is not None:
        params["season"] = season
    if week is not None:
        params["week"] = week

    data = await _get(url, params=params)
    if not data:
        return None

    # ESPN returns a bunch of stat groups; we’ll flatten the useful ones
    stats_groups = data.get("splits", {}).get("categories", [])
    out = {"espn_id": espn_id, "season": season, "week": week, "categories": []}

    for cat in stats_groups:
        cat_name = cat.get("name")
        for stat in cat.get("stats", []):
            out["categories"].append({
                "category": cat_name,
                "name": stat.get("name"),
                "display_name": stat.get("displayName"),
                "value": stat.get("value"),
            })

    return out


async def get_week_leaders(
    season: int,
    week: int,
    stat_type: str = "passing",
) -> List[Dict]:
    # ESPN weekly leaders endpoint via scoreboard
    # We’ll hit the scoreboard and derive leaders from player stats
    scoreboard_url = f"{BASE_URL}/seasons/{season}/types/2/weeks/{week}/events"

    events = await _get(scoreboard_url)
    if not events:
        return []

    leaders: Dict[int, Dict] = {}

    for item in events.get("items", []):
        # each event has competitions -> competitors -> athletes with stats
        comp_data = await _get(item.get("$ref"))
        if not comp_data:
            continue

        for comp in comp_data.get("competitions", []):
            for team in comp.get("competitors", []):
                for athlete in team.get("athletes", []):
                    stats = athlete.get("statistics", [])
                    espn_id = int(athlete.get("id"))

                    value = 0
                    for stat_group in stats:
                        for s in stat_group.get("stats", []):
                            name = s.get("name")
                            if stat_type == "passing" and name == "passingYards":
                                value += s.get("value", 0)
                            elif stat_type == "rushing" and name == "rushingYards":
                                value += s.get("value", 0)
                            elif stat_type == "receiving" and name == "receivingYards":
                                value += s.get("value", 0)

                    if value <= 0:
                        continue

                    if espn_id not in leaders or value > leaders[espn_id]["value"]:
                        leaders[espn_id] = {
                            "espn_id": espn_id,
                            "full_name": athlete.get("fullName"),
                            "team": team.get("team", {}).get("displayName"),
                            "value": value,
                        }

    # sort by value desc
    return sorted(leaders.values(), key=lambda x: x["value"], reverse=True)
