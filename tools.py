#define tools
from langchain.agents import tool
import json

@tool
def get_character_data(data_file, char: str) -> dict:
    """Returns the character given by its name/id. Character name can be whitespace seperated but in data may be together or vice versa 
    so if an entry is not found, please try either with adding a whitespace or removing. For example, if input is Invisible woman, search 'Invisible Woman' or 'InvisibleWoman' whichever returns a hit"""
    with open('tmp/roster.json') as f:
        data = json.load(f)
    # Normalize the input char by removing spaces
    normalized_char = char.replace(" ", "").lower()
    # Search for the character data by ID, ignoring spaces
    for item in data["data"]:
        normalized_id = item["id"].replace(" ", "").lower()
        if normalized_char in normalized_id:
            return item
    # Return None or an empty dict if the character is not found
    return None

#get_character_data.invoke("SpiderMan")
def get_tools():
    tools = [get_character_data]
    return tools