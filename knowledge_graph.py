#neo4j
from neo4j import GraphDatabase
import re

class GraphDBManager:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]  # Return a list of records

    def write_query(self, query, parameters=None):
        with self.driver.session() as session:
            session.write_transaction(self._execute_query, query, parameters)

    @staticmethod
    def _execute_query(tx, query, parameters):
        tx.run(query, parameters)


    def common_traits_among_high_level_characters(self, limit=10):
        #get most trait 
        query = """
        MATCH (c:Character)-[:HAS_TRAIT]->(t:Trait)
        WHERE c.level > 50
        WITH t, COUNT(c) AS NumCharacters
        RETURN t.name AS Trait, NumCharacters ORDER BY NumCharacters DESC LIMIT {limit}
        """
        return self.run_query(query)

    def find_characters_by_trait(self, trait):
        #Get all the characters given a trait name
        query = """
        MATCH (c:Character)-[:HAS_TRAIT]->(t:Trait {name: $trait_name})
        RETURN c.name AS CharacterName, c.id AS CharacterID
        """
        parameters = {'trait_name': trait}
        return self.run_query(query, parameters)

    def find_characters_by_attribute(self, attribute, top=True, limit=15):
        # find list of characters given attribute name
        if attribute not in ['accuracy', 'armor', 'blockAmount', 'critChance', 'critDamageBonus', 'damage', 
                             'focus', 'gearTier', 'healer', 'health', 'level', 'power', 'resist', 'speed']:
            raise ValueError(f"Invalid attribute: {attribute}. Check your attribute name and try again.")

        order_direction = "DESC" if top else "ASC"
        query = f"""
        MATCH (c:Character)
        WHERE c.{attribute} IS NOT NULL
        RETURN c.name AS CharacterName, c.{attribute} AS AttributeValue
        ORDER BY c.{attribute} {order_direction}
        LIMIT {limit}
        """
        return self.run_query(query)
    
    def find_related_characters(self, character_name):
        #find related relationship char given a char
        query = """
        MATCH (c1:Character {name: $character_name})-[:HAS_TRAIT|HAS_ABILITY]->(x)<-[:HAS_TRAIT|HAS_ABILITY]-(c2:Character)
        WHERE c1 <> c2
        RETURN c2.name AS RelatedCharacter, collect(x.name) AS SharedFeatures
        """
        return self.run_query(query, parameters={"character_name": character_name})
    
    def find_ability_descriptions_by_keyword(self, character_name, keyword):
        #Given char name, find abilities that has keywords ie, Bleed, Trauma etc.
        query = """
        MATCH (c:Character {name: $character_name})-[:HAS_ABILITY]->(a:AbilityKit)
        WHERE a.description CONTAINS $keyword
        RETURN a.type AS AbilityType, a.name AS AbilityName, a.description AS Description
        """
        parameters = {
            'character_name': character_name,
            'keyword': keyword
        }
        return self.run_query(query, parameters)

    def get_character_iso_stats(self, character_name):
        #Given char find its ISO properties
        query = """
        MATCH (c:Character {name: $character_name})-[:HAS_ISO8]->(isoNode)
        RETURN 
        isoNode.matrix AS Matrix, 
        isoNode.active AS Active, 
        apoc.coll.min([
            isoNode.damage, 
            isoNode.armor, 
            isoNode.focus, 
            isoNode.health, 
            isoNode.resist
        ]) AS IsoValue
        """
        parameters = {
            'character_name': character_name
        }
        results = self.run_query(query, parameters)
        return results  # This will return a list of records with the matrix, active type, and minimum stat value

def clean_html(raw_html):
    """Utility function to remove HTML tags from descriptions."""
    clean_text = re.sub(r'<.*?>', '', raw_html)
    return clean_text

def build_characters_kg(graph_db, character_data):
    for char in character_data:
        if char.get('status') != 'playable':
            continue
        
        traits = [trait for trait in char.get('traits', []) if trait.get('name') is not None]
        
        ability_kits = {}
        for kit_type in ['basic', 'special', 'ultimate', 'passive']:
            if kit_type in char.get("abilityKit", {}):
                kit_data = char["abilityKit"][kit_type]
                levels = kit_data.get("levels", {})
                if levels:
                    max_level_key = max(
                        (lvl for lvl, details in levels.items() if "description" in details),
                        key=int,  # Using the level number as the key
                        default=None
                    )
                    if max_level_key:
                        last_level_description = clean_html(levels[max_level_key]["description"])
                        ability_kits[kit_type] = {
                            "type": kit_type,
                            "name": kit_data["name"],
                            "description": last_level_description
                        }

        graph_db.run_query("""
            MERGE (c:Character {id: $id})
            SET c.name = $name, c.description = $description, c.portrait = $portrait
            WITH c
            UNWIND $traits as trait
            MERGE (t:Trait {id: trait.id})
            ON CREATE SET t.name = trait.name
            MERGE (c)-[:HAS_TRAIT]->(t)
            WITH c, t
            UNWIND $ability_kits as kit
            MERGE (a:AbilityKit {characterId: $id, type: kit.type})
            ON CREATE SET a.name = kit.name, a.description = kit.description
            ON MATCH SET a.name = kit.name, a.description = kit.description
            MERGE (c)-[:HAS_ABILITY]->(a)
        """, parameters={
            "id": char['id'],
            "name": char.get('name', 'Unknown Name'),
            "description": clean_html(char.get('description', 'No description available')),
            "portrait": char.get('portrait', ''),
            "traits": traits,
            "ability_kits": list(ability_kits.values())
        })

def build_roster_kg(graph_db, roster_data):
    for char in roster_data:
        stats = char.get('stats', {})
        
        # Ensure we parse each expected stat or set a default value (e.g., 0)
        health = stats.get('health', 0)
        damage = stats.get('damage', 0)
        armor = stats.get('armor', 0)
        focus = stats.get('focus', 0)
        resist = stats.get('resist', 0)
        critDamageBonus = stats.get('critDamageBonus', 0)
        critChance = stats.get('critChance', 0)
        speed = stats.get('speed', 0)
        blockAmount = stats.get('blockAmount', 0)
        accuracy = stats.get('accuracy', 100)  # assuming 100 as default for accuracy if not specified

        iso8 = char.get('iso8', {})  # Pass iso8 as a dictionary

        # Update the query to set each stat as a separate property
        graph_db.run_query("""
            MERGE (c:Character {id: $id})
            SET c.level = $level, c.activeYellow = $activeYellow, c.activeRed = $activeRed, 
                c.gearTier = $gearTier, c.basic = $basic, c.special = $special, 
                c.ultimate = $ultimate, c.passive = $passive, c.power = $power,
                c.health = $health, c.damage = $damage, c.armor = $armor, c.focus = $focus,
                c.resist = $resist, c.critDamageBonus = $critDamageBonus, c.critChance = $critChance,
                c.speed = $speed, c.blockAmount = $blockAmount, c.accuracy = $accuracy
            MERGE (isoNode:ISO8 {characterId: $id}) ON CREATE SET isoNode = $iso8 ON MATCH SET isoNode += $iso8
            MERGE (c)-[:HAS_ISO8]->(isoNode)
        """, parameters={
            "id": char['id'], 
            "level": char.get('level'), 
            "activeYellow": char.get('activeYellow'),
            "activeRed": char.get('activeRed'), 
            "gearTier": char.get('gearTier'), 
            "basic": char.get('basic'),
            "special": char.get('special'), 
            "ultimate": char.get('ultimate'), 
            "passive": char.get('passive'),
            "power": char.get('power'), 
            "health": health, 
            "damage": damage, 
            "armor": armor, 
            "focus": focus, 
            "resist": resist, 
            "critDamageBonus": critDamageBonus, 
            "critChance": critChance, 
            "speed": speed, 
            "blockAmount": blockAmount, 
            "accuracy": accuracy,
            "iso8": iso8
        })

