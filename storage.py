import json
import os
from datetime import datetime

DATA_DIR = 'data'
SECTIONS_FILE = os.path.join(DATA_DIR, 'sections.json')
TEMPLATES_DIR = os.path.join(DATA_DIR, 'templates')
RESPONSES_DIR = os.path.join(DATA_DIR, 'responses')

def init_storage():
    for d in [DATA_DIR, TEMPLATES_DIR, RESPONSES_DIR]:
        if not os.path.exists(d):
            os.makedirs(d)
    if not os.path.exists(SECTIONS_FILE):
        with open(SECTIONS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# --- SECTIONS ---
def get_sections():
    if not os.path.exists(SECTIONS_FILE): return []
    with open(SECTIONS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_sections(sections):
    with open(SECTIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=4, ensure_ascii=False)

def add_section(name):
    sections = get_sections()
    if name not in sections:
        sections.append(name)
        save_sections(sections)

def delete_section(name):
    sections = get_sections()
    if name in sections:
        sections.remove(name)
        save_sections(sections)
        # Optionally delete section responses
        section_dir = os.path.join(RESPONSES_DIR, name.replace(' ', '_'))
        if os.path.exists(section_dir):
            import shutil
            shutil.rmtree(section_dir)

# --- TEMPLATES ---
def get_template(theme_id, version=None):
    filepath = os.path.join(TEMPLATES_DIR, f"theme_{theme_id}.json")
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f:
        versions = json.load(f)
        if version is None:
            return versions[-1] if versions else None
        for v in versions:
            if v['version'] == version: return v
    return None

def get_all_active_templates():
    templates = []
    for i in range(1, 5):
        t = get_template(i)
        if t: templates.append(t)
    return templates

def save_template_version(theme_id, structure, version=None):
    filepath = os.path.join(TEMPLATES_DIR, f"theme_{theme_id}.json")
    versions = []
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            versions = json.load(f)

    if version is None:
        version = (versions[-1]['version'] + 1) if versions else 1

    new_v = {
        "theme": theme_id,
        "version": version,
        "structure": structure,
        "created_at": datetime.now().isoformat()
    }
    versions.append(new_v)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(versions, f, indent=4, ensure_ascii=False)
    return new_v

# --- RESPONSES ---
def get_response(section_name, theme_id, template_version=None):
    section_dir = os.path.join(RESPONSES_DIR, section_name.replace(' ', '_'))
    filepath = os.path.join(section_dir, f"theme_{theme_id}.json")
    if not os.path.exists(filepath): return None
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # On retourne la réponse. Si on veut gérer l'historique par section aussi :
        # Pour le moment on garde une seule réponse par thème par section.
        return data

def save_response(section_name, theme_id, template_id, template_version, data):
    section_dir = os.path.join(RESPONSES_DIR, section_name.replace(' ', '_'))
    if not os.path.exists(section_dir):
        os.makedirs(section_dir)

    filepath = os.path.join(section_dir, f"theme_{theme_id}.json")
    response = {
        "section_name": section_name,
        "theme": theme_id,
        "template_version": template_version,
        "data": data,
        "last_updated": datetime.now().isoformat()
    }
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(response, f, indent=4, ensure_ascii=False)
    return response

def get_all_responses_for_section(section_name):
    responses = {}
    for i in range(1, 5):
        resp = get_response(section_name, i)
        if resp:
            responses[i] = resp
    return responses
