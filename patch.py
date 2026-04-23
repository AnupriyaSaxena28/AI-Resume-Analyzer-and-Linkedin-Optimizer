import os
import sys

# Write a log to disk from within app.py
from utils.skill_matcher import create_skill_matcher

import utils.skill_matcher

# Let's dynamically patch extract_skills in utils.skill_matcher to log what it's finding
original_extract = utils.skill_matcher.extract_skills

def patched_extract(text, matcher, nlp):
    skills = original_extract(text, matcher, nlp)
    with open("skills_debug.log", "a", encoding="utf-8") as f:
        f.write(f"TEXT EXTRACTED: {text[:100]}...\n")
        f.write(f"SKILLS FOUND: {skills}\n\n")
    return skills

utils.skill_matcher.extract_skills = patched_extract
print("Patched successfully")
