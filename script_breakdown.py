import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def extract_actors_and_lines(scene_text):
    actors = set()
    lines = []
    current_actor = None
    dialogue = []

    for line in scene_text.split('\n'):
        line = line.strip()
        if re.match(r'^[A-Z][A-Z ]*$', line):  # Improved regex for actor names
            if current_actor:
                lines.append((current_actor, "\n".join(dialogue)))
            current_actor = line
            actors.add(current_actor)
            dialogue = []
        else:
            if current_actor:
                dialogue.append(line)
    
    if current_actor:
        lines.append((current_actor, "\n".join(dialogue)))
    
    return list(actors), lines

def parse_script(text):
    scenes = []
    scene_text = ""
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line.startswith("INT.") or line.startswith("EXT."):
            if scene_text:
                scenes.append(scene_text.strip())
                scene_text = ""
            scene_text = line
        else:
            scene_text += "\n" + line
    
    if scene_text:
        scenes.append(scene_text.strip())
    
    parsed_scenes = []
    for scene in scenes:
        actors, lines = extract_actors_and_lines(scene)
        scene_type = "INT." if "INT." in scene else "EXT."
        parsed_scenes.append({
            'scene': scene,
            'scene_type': scene_type,
            'actors': actors,
            'lines': lines
        })
    
    return parsed_scenes

def breakdown_script(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    scenes = parse_script(text)
    return scenes
