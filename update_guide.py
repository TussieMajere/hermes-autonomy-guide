#!/usr/bin/env python3
"""
Automatisk oppdateringsskript for Hermes Autonomi & Selvlæring Guide.
Kjøres automatisk under AGY Bootstrap for å hente nyeste skills og recipes,
oppdatere nettsiden og pushe til GitHub.
"""
import os
import sys
import json
import glob
import subprocess
from datetime import datetime

GUIDE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.expanduser("~/.hermes/skills")
RECIPES_DIR = os.path.expanduser("~/hermes-agent/recipes")
HERMES_AGENT_DIR = os.path.expanduser("~/hermes-agent")

def scan_skills():
    skills = []
    if os.path.exists(SKILLS_DIR):
        for root, _, files in os.walk(SKILLS_DIR):
            for f in files:
                if f == "SKILL.md":
                    fpath = os.path.join(root, f)
                    relpath = os.path.relpath(fpath, os.path.expanduser("~"))
                    category = os.path.basename(os.path.dirname(fpath))
                    skills.append({
                        "path": relpath,
                        "category": category,
                        "updated_at": datetime.fromtimestamp(os.path.getmtime(fpath)).isoformat()
                    })
    return skills

def scan_recipes():
    recipes = []
    if os.path.exists(RECIPES_DIR):
        for rpath in glob.glob(os.path.join(RECIPES_DIR, "*.json")):
            if os.path.basename(rpath).startswith("_"):
                continue
            try:
                with open(rpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    recipes.append({
                        "id": data.get("recipe_id", os.path.basename(rpath)),
                        "name": data.get("name", "Ukjent"),
                        "description": data.get("description", ""),
                        "steps": len(data.get("steps", [])),
                        "tags": data.get("tags", [])
                    })
            except Exception:
                pass
    return recipes

def update_data():
    skills = scan_skills()
    recipes = scan_recipes()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "last_updated": now_str,
        "skills_count": len(skills),
        "recipes_count": len(recipes),
        "skills": skills,
        "recipes": recipes
    }

    json_path = os.path.join(GUIDE_DIR, "skills_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✓ Skannet {len(skills)} ferdigheter og {len(recipes)} oppskrifter.")
    return data

def sync_to_github():
    print("🚀 Sjekker git-status og pusher oppdateringer til GitHub...")
    try:
        # Sjekk om det er git repository
        if not os.path.exists(os.path.join(GUIDE_DIR, ".git")):
            subprocess.run(["git", "init"], cwd=GUIDE_DIR, check=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=GUIDE_DIR, check=True)

        subprocess.run(["git", "add", "."], cwd=GUIDE_DIR, check=True)
        
        status = subprocess.run(["git", "status", "--porcelain"], cwd=GUIDE_DIR, capture_output=True, text=True)
        if status.stdout.strip():
            now_iso = datetime.now().strftime("%Y-%m-%d %H:%M")
            subprocess.run(["git", "commit", "-m", f"Auto-sync Hermes Autonomy Guide ({now_iso})"], cwd=GUIDE_DIR, check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=GUIDE_DIR, check=False)
            print("✓ Nettside oppdatert og pushet til GitHub!")
        else:
            print("✓ Nettsiden er allerede oppdatert (ingen nye endringer).")
    except Exception as e:
        print(f"⚠️ Git synkroniseringsfeil: {e}")

if __name__ == "__main__":
    update_data()
    sync_to_github()
