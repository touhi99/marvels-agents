import requests
import json 
import os

def call_api(api_suffix, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'x-api-key': os.getenv("X-API-KEY")
    }
    response = requests.get('https://api.marvelstrikeforce.com/'+api_suffix, headers=headers)
    return response.json()

def fetch_roster(access_token):
    get_roster = call_api('player/v1/roster', access_token)
    json.dump(get_roster, open('data/roster.json', 'w'))

def fetch_squad(access_token):
    get_squads = call_api('player/v1/squads', access_token)
    json.dump(get_squads, open('data/squads.json', 'w'))

def fetch_characters(access_token):
    get_characters = fetch_all_pages('game/v1/characters?abilityKits=full', access_token)
    print(f"Retrieved {len(get_characters)} characters")
    json.dump(get_characters, open('data/character.json', 'w'))

def fetch_all_pages(api_suffix, access_token):
    full_data = []
    page = 1
    per_page = 10  # Number of items per page

    while True:
        paginated_suffix = f"{api_suffix}&page={page}&perPage={per_page}"
        data = call_api(paginated_suffix, access_token)
        
        # Check if data is returned and has the expected structure
        if 'data' in data and data['data']:
            full_data.extend(data['data'])
            page += 1  # Increment to request the next page
        else:
            break  # Break loop if no more data to fetch

    return full_data