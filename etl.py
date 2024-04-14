import json
from knowledge_graph import GraphDBManager, build_characters_kg, build_roster_kg
from msf_api import fetch_roster, fetch_squad, fetch_characters
import os
from langchain.graphs import Neo4jGraph

def load_json_data(filename, directory='data'):
    """Loads JSON data from a specified file within a directory."""
    file_path = os.path.join(directory, filename)
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred while reading {file_path}: {e}")
        return None
    
def fetch_data(access_token):
    fetch_roster(access_token)
    fetch_squad(access_token)
    fetch_characters(access_token)

def build_kg():
    db_manager = GraphDBManager(os.getenv('uri'), os.getenv('username'), os.getenv('password'))

    get_characters = load_json_data('character.json')
    if get_characters is not None:
        print("Loaded character data successfully.")
    else:
        print("Failed to load character data.")

    build_characters_kg(db_manager, get_characters)

    get_roster = load_json_data('roster.json')
    if get_roster is not None:
        print("Loaded roster data successfully.")
    else:
        print("Failed to load roster data.")
    build_roster_kg(db_manager, get_roster['data'])


def load_graph():
    url = os.getenv('uri')
    username = os.getenv('username')
    password = os.getenv('password')

    graph = Neo4jGraph(
        url=url, 
        username=username, 
        password=password
    )
    return graph