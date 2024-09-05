# script_pyhon/utils/script_parser.py
import spacy
import re

nlp = spacy.load("en_core_web_sm")

def parse(script_content):
    # Basic script parsing
    scenes = re.split(r'\n(?=INT\.|EXT\.)', script_content)
    parsed_scenes = []
    
    for scene in scenes:
        doc = nlp(scene)
        parsed_scenes.append({
            'content': scene,
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        })
    
    return parsed_scenes

# script_analysis/utils/character_analyzer.py
from collections import Counter

def analyze(parsed_script):
    characters = []
    character_mentions = Counter()
    
    for scene in parsed_script:
        for entity, label in scene['entities']:
            if label == 'PERSON':
                character_mentions[entity] += 1
    
    for character, mentions in character_mentions.items():
        if mentions > len(parsed_script) * 0.5:
            importance = 'lead'
        elif mentions > len(parsed_script) * 0.2:
            importance = 'supporting'
        else:
            importance = 'minor'
        
        characters.append({
            'name': character,
            'importance': importance,
            'mentions': mentions
        })
    
    return characters

# script_analysis/utils/scene_breakdown.py
import re

def breakdown(parsed_script):
    scenes = []
    for i, scene in enumerate(parsed_script, 1):
        location_match = re.search(r'(INT\.|EXT\.)\s+(.*?)\s*-', scene['content'])
        location = location_match.group(2) if location_match else 'Unknown'
        
        scenes.append({
            'number': i,
            'location': location,
            'description': scene['content'][:200]  # First 200 characters as description
        })
    
    return scenes

# script_analysis/utils/element_extractor.py
import re

def extract(parsed_script):
    elements = []
    categories = {
        'prop': r'\b(props?|objects?)\b',
        'costume': r'\b(costumes?|outfits?|wear(s|ing)?)\b',
        'special_effect': r'\b(special effects?|sfx)\b',
        'stunt': r'\b(stunts?|action sequences?)\b',
        'vehicle': r'\b(cars?|vehicles?|motorcycles?|trucks?)\b',
        'animal': r'\b(animals?|dogs?|cats?|horses?)\b',
        'vfx': r'\b(vfx|visual effects?|cgi)\b'
    }
    
    for scene in parsed_script:
        for category, pattern in categories.items():
            matches = re.findall(pattern, scene['content'], re.IGNORECASE)
            for match in matches:
                elements.append({
                    'category': category,
                    'description': match
                })
    
    return elements

# script_analysis/utils/budget_estimator.py
def estimate(script, characters, scenes, elements):
    # This is a very simplified budget estimation
    # In a real-world scenario, you'd need much more complex logic and probably
    # integration with external data sources for accurate cost estimation
    
    base_cost = 100000  # Base cost for any production
    
    # Estimate based on number of characters
    character_cost = sum(50000 if char['importance'] == 'lead' else 
                         20000 if char['importance'] == 'supporting' else 
                         5000 for char in characters)
    
    # Estimate based on number of scenes
    scene_cost = len(scenes) * 5000
    
    # Estimate based on special elements
    element_costs = {
        'prop': 500,
        'costume': 1000,
        'special_effect': 10000,
        'stunt': 5000,
        'vehicle': 2000,
        'animal': 3000,
        'vfx': 15000
    }
    element_cost = sum(element_costs.get(elem['category'], 0) for elem in elements)
    
    total_estimate = base_cost + character_cost + scene_cost + element_cost
    
    return {
        'total_estimate': total_estimate,
        'breakdown': {
            'base_cost': base_cost,
            'character_cost': character_cost,
            'scene_cost': scene_cost,
            'element_cost': element_cost
        }
    }

def recalculate(budget, adjustments):
    # In a real-world scenario, this function would take detailed adjustments
    # and recalculate the budget accordingly
    
    # For this example, we'll just apply a simple percentage adjustment
    adjustment_percentage = float(adjustments) / 100
    
    new_total = budget.total_estimate * (1 + adjustment_percentage)
    new_breakdown = {
        key: value * (1 + adjustment_percentage)
        for key, value in budget.breakdown.items()
    }
    
    return {
        'total_estimate': new_total,
        'breakdown': new_breakdown
    }