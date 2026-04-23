import spacy
from spacy.matcher import PhraseMatcher
import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath('.'))

from utils.skill_matcher import create_skill_matcher, extract_skills

def inspect_db():
    from utils.skill_matcher import load_skills_database
    skills_db = load_skills_database()
    
    # Let's find all keys related to Android
    android_skills = []
    for cat, skills in skills_db.items():
        for s in skills:
            if "Android" in s:
                android_skills.append(s)
                
    print("Android related skills in DB:", android_skills)
    
if __name__ == "__main__":
    inspect_db()
