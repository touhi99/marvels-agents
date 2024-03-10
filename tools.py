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

@tool
def get_top_characters_by_attribute(attribute: str, top_n: int = 10) -> list:
    """Returns the top N characters sorted by a given attribute."""
    with open('tmp/roster.json') as f:
        data = json.load(f)

    # Ensure the characters are sorted by the specified attribute in descending order
    sorted_characters = sorted(data["data"], key=lambda x: x.get(attribute, 0), reverse=True)

    # Return the top N characters
    return sorted_characters[:top_n]

# Example usage to get the top 5 characters by power
#top_characters_by_power = get_top_characters_by_attribute('power', 5)

#get_character_data.invoke("SpiderMan")
def get_tools():
    tools = [get_character_data, get_top_characters_by_attribute]
    return tools