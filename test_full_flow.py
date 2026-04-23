import spacy
from spacy.matcher import PhraseMatcher
import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath('.'))

from utils.skill_matcher import create_skill_matcher, extract_skills, calculate_skill_match

def test_full_flow():
    nlp = spacy.load("en_core_web_md")
    
    # Minimal skills db
    skills_db = {
        "test": ["Mobile Development", "Android Development", "Java", "Kotlin", "Android Studio"]
    }
    
    matcher, base_skills = create_skill_matcher(nlp, skills_db)
    
    text = "Developed an AI-driven tool demonstrating advanced Mobile Application Development skills."
    
    found_skills = extract_skills(text, matcher, nlp)
    
    print(f"Base skills: {base_skills}")
    print(f"Extracted skills from text: {found_skills}")
    
    jd_text = "Looking for someone with Mobile Development experience."
    jd_skills = extract_skills(jd_text, matcher, nlp)
    print(f"Extracted skills from JD: {jd_skills}")
    
    match_results = calculate_skill_match(found_skills, jd_skills)
    print(f"Missing skills: {match_results['missing_skills']}")

if __name__ == "__main__":
    test_full_flow()
