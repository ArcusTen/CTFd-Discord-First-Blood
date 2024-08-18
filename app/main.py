import os
import json
import asyncio
from discord import Webhook, Embed
import aiohttp
import requests
from dotenv import load_dotenv

# Loading environment variables from `.env` file
load_dotenv()

CTFD_API_URL = os.getenv('CTF_URL')
CTFD_API_KEY = os.getenv('CTFD_API_KEY')
WEBHOOKS = json.loads(os.getenv('DISCORD_WEBHOOKS'))
USE_GIF = os.getenv('USE_GIF', 'False').lower() == 'true'  # Convert to boolean
FIRST_BLOOD_GIF = os.getenv('FIRST_BLOOD_GIF')
SOLVE_GIF = os.getenv('SOLVE_GIF')

firstBloods = {}
solvedChallenges = set()

async def getCTFDdata(endpoint):
    headers = {
        'Authorization': f'Token {CTFD_API_KEY}',
        'Content-Type': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{CTFD_API_URL}/api/v1/{endpoint}', headers=headers) as response:
            response.raise_for_status()
            return await response.json()

async def sendWebhook(webhook_url, embed):
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, session=session)
        await webhook.send(embed=embed)

async def announceFirstBlood(challenge_name, user_name, team_name):
    embed = Embed(
        title="🩸 First Blood!",
        description=f"**{user_name}** from team **{team_name}** got the first blood on `{challenge_name}`!",
        color=0xFF1100
    )
    if USE_GIF and FIRST_BLOOD_GIF:
        embed.set_image(url=FIRST_BLOOD_GIF)
    await sendWebhook(WEBHOOKS['first_blood'], embed)

async def announceSolve(challenge_name, user_name, team_name):
    embed = Embed(
        title="✅ Solve Reported!",
        description=f"**{user_name}** from team **{team_name}** solved `{challenge_name}`.",
        color=0x38E099
    )
    if USE_GIF and SOLVE_GIF: 
        embed.set_image(url=SOLVE_GIF)
    await sendWebhook(WEBHOOKS['solves'], embed)

async def getUserDetails(user_id):
    try:
        user_data = await getCTFDdata(f'users/{user_id}')
        return user_data['data']
    except requests.exceptions.HTTPError as e:
        print(f"Error fetching user details for ID {user_id}: {e}")
        return None

async def announceEvents():
    global firstBloods, solvedChallenges
    
    challenges = await getCTFDdata('challenges')
    challenge_data = challenges['data']
    
    for challenge in challenge_data:
        challenge_name = challenge['name']
        challenge_id = challenge['id']
        
        try:
            solves = await getCTFDdata(f'challenges/{challenge_id}/solves')
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching solves for challenge {challenge_id}: {e}")
            continue
        
        solve_data = solves.get('data', [])
        
        for solve in solve_data:
            team_name = solve.get('name', 'Unknown User')
            user_id = solve.get('account_id')
            # Incrementing user_id by 1 as admin user has id of 0 which is disturbing the sequence. Feel free to remove +1 if your setup is fine without it.
            user_details = await getUserDetails(user_id + 1)
            user_name = user_details['name'] if user_details else 'Unknown User'
            
            solve_key = f"{challenge_id}_{user_id}"
            
            if solve_key not in solvedChallenges:
                solvedChallenges.add(solve_key)
                print(f"[INFO] Challenge `{challenge_name}` solved by member `{user_name}` (Adjusted ID: {user_id})")
                
                await announceSolve(challenge_name, user_name, team_name)

                # Checking if it's the first blood
                if challenge_id not in firstBloods:
                    firstBloods[challenge_id] = user_name
                    await announceFirstBlood(challenge_name, user_name, team_name)

async def main():
    while True:
        await announceEvents()
        await asyncio.sleep(30)

if __name__ == '__main__':
    asyncio.run(main())
