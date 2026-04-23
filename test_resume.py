import spacy
from spacy.matcher import PhraseMatcher
import sys
import os
import json

# Add project root to sys.path
sys.path.insert(0, os.path.abspath('.'))

from utils.skill_matcher import create_skill_matcher, extract_skills
from utils.text_extraction import clean_text

def test_resume_text():
    nlp = spacy.load("en_core_web_md")
    
    from utils.skill_matcher import load_skills_database
    skills_db = load_skills_database()
    
    matcher, base_skills = create_skill_matcher(nlp, skills_db)
    
    raw_text = """
    ScheduleGPT (AI-Powered) | Jetpack Compose, Gemini API, Kotlin, Firebase | GitHub
    • Developed an AI-driven tool demonstrating advanced Mobile Application Development skills,
    using Gemini API for automated scheduling.
    """
    
    cleaned = clean_text(raw_text)
    print("Cleaned text:", cleaned)
    
    found_skills = extract_skills(cleaned, matcher, nlp)
    
    print("\nExtracted skills:", found_skills)
    
if __name__ == "__main__":
    test_resume_text()
