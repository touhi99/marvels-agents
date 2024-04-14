import os
from langchain.agents import Tool, tool
from llm_chain import get_cypher_chain
from knowledge_graph import GraphDBManager

db_manager = GraphDBManager(os.getenv('uri'), os.getenv('username'), os.getenv('password'))


@tool
def get_iso_tools(character: str):
    """Given a chacaracter name, gets their ISO values"""
    character = character.title()
    iso_stats = db_manager.get_character_iso_stats(character)
    results = []
    for record in iso_stats:
        result = f"Matrix: {record['Matrix']}, Active: {record['Active']}, Iso Stat Value: {record['IsoValue']}"
        #print(result)
        results.append(result)
    return results

@tool
def get_char_by_attributes(attributes: str, top: bool=True, limit: int=10) -> list:
    """Given attribute name, get X number of characters, ordered by top (true/false)"""
    top_attr_char = db_manager.find_characters_by_attribute(attributes, top=top, limit=limit)
    results = []
    print("Top Speed Characters:")
    for character in top_attr_char:
        result = f"Character: {character['CharacterName']}, Speed: {character['AttributeValue']}"
        print(result)
        results.append(result)
    return results

@tool 
def get_char_by_trait(trait: str) -> list:
    """Given a trait name, get all the characters for this trait"""
    trait = trait.upper()
    traited_character = db_manager.find_characters_by_trait(trait)
    results = []
    for character in traited_character:
        result = f"Trait: {character['CharacterName']}"
        print(result)
        results.append(result)
    return results

@tool
def get_related_char(character_name:str) -> list:
    """Given a character, get most related characters"""
    character_name = character_name.title()
    related_char = db_manager.find_related_characters(character_name=character_name)
    return related_char

@tool
def get_common_traits(limit:int=10) -> list:
    """Get most common X number of traits"""
    common_trait = db_manager.common_traits_among_high_level_characters(limit=limit)
    return common_trait

@tool
def get_ability_desc_of_char(character:str, keyword:str) -> list:
    """Given a character and an ability keyword, return the ability where character has the keyword"""
    character = character.title()
    keyword = keyword.title()
    results = db_manager.find_ability_descriptions_by_keyword(character, keyword)
    abilities = []
    for result in results:
        ability = f"Ability Type: {result['AbilityType']}, Ability Name: {result['AbilityName']}, Description: {result['Description']}"
        print(ability)
        abilities.append(ability)
    return abilities

@tool
def get_ability_cost_of_char(character:str, abilities:list) -> list:
    """Given character name and list of available abilities [basic, ultimate, special, passive],\
    return how much start and cost energy for the abilities"""
    character = character.title()
    energy_details = db_manager.get_ability_energy(character, abilities)
    return energy_details

def get_tools():
    tools = [
        # Tool(
        #     name="Tasks",
        #     func=vector_qa.run,
        #     description="""Useful when you need to answer questions about descriptions of tasks.
        #     Not useful for counting the number of tasks.
        #     Use full question as input.
        #     """,
        # ),
        get_iso_tools,
        get_char_by_attributes,
        get_char_by_trait,
        get_common_traits,
        get_related_char,
        get_ability_desc_of_char,
        get_ability_cost_of_char,
        Tool(
            name="Graph",
            func=get_cypher_chain().run,
            description="""Useful when you need to answer questions about MSF character information  ie, speed, power, iso, trait etc. \
            which are not already pre-defined tools.""",
        ),
    ]    
    return tools

