#define tools
from langchain.agents import tool
import json
from rapidfuzz import process, fuzz

@tool
def get_character_data(char: str) -> dict:
    """Returns the character given by its name/id. Character name can be whitespace seperated but in data may be together or vice versa 
    so if an entry is not found, please try either with adding a whitespace or removing. For example, if input is Invisible woman, search 'Invisible Woman' or 'InvisibleWoman' whichever returns a hit"""
    with open('tmp/roster.json') as f:
        data = json.load(f)
    # Extract all character names or IDs to a list for fuzzy matching
    character_names = [item["id"] for item in data["data"]]
    
    # Use fuzzy matching to find the best match for the input character name
    best_match = process.extractOne(char, character_names, scorer=fuzz.WRatio)
    
    if best_match and best_match[1] > 80:
        for item in data["data"]:
            if item["id"] == best_match[0]:
                return item
    
    return None

@tool
def get_top_characters_by_attribute(search_attribute: str, top_n: int = 10) -> list:
    """Returns the top N characters sorted by a given attribute."""
    with open('tmp/roster.json') as f:
        data = json.load(f)

    attribute_names = ["power", "level", "gearTier", "activeYellow", "activeRed", "gearSlots", "iso8", "stats"] 
    
    # Use fuzzy matching to find the best match for the input attribute name
    best_attribute_match = process.extractOne(search_attribute, attribute_names, scorer=fuzz.WRatio)
    
    if best_attribute_match and best_attribute_match[1] > 80: 
        # Sort characters by the matched attribute
        sorted_characters = sorted(data["data"], key=lambda x: x.get(best_attribute_match[0], 0), reverse=True)
        return sorted_characters[:top_n]
    
    return []

# Example usage to get the top 5 characters by power
#top_characters_by_power = get_top_characters_by_attribute('power', 5)

#get_character_data.invoke("SpiderMan")
def get_tools():
    tools = [get_character_data, get_top_characters_by_attribute]
    return tools