import httpx, asyncio

async def t():
    async with httpx.AsyncClient() as client:
        r = await client.get("https://site.api.espn.com/apis/site/v2/sports/football/nfl/athletes?limit=1")
        print(r)

asyncio.run(t())
