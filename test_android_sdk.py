import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from utils.skill_matcher import create_skill_matcher, extract_skills, load_skills_database
import spacy

nlp = spacy.load("en_core_web_md")
skills_db = load_skills_database()
matcher, _ = create_skill_matcher(nlp, skills_db)

text = "utilizing Android SDK and Ola Maps for real-time tracking"
print("Extracted from 'Android SDK':", extract_skills(text, matcher, nlp))
