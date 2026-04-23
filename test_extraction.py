import sys
import os
import spacy
from spacy.matcher import PhraseMatcher
import json
import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s\.\,\-\(\)\:\;\@\+\#\/\&]', '', text)
    text = text.strip()
    return text

def test_extract():
    text = "Java, Kotlin, C, C++, Python"
    text = clean_text(text)
    print(f"Cleaned text: {text}")
    
    try:
        nlp = spacy.load("en_core_web_md")
    except:
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"], check=True)
        nlp = spacy.load("en_core_web_md")
        
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    
    all_skills = ["Java", "Kotlin", "C", "C++", "Python"]
    
    patterns = [nlp.make_doc(skill) for skill in all_skills]
    matcher.add("SKILLS", patterns)
    
    doc = nlp(text)
    print("Tokens:")
    for token in doc:
        print(f"  [{token.text}]")
        
    matches = matcher(doc)
    
    found_skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        found_skills.add(skill)
        
    print(f"Found skills: {found_skills}")

if __name__ == "__main__":
    test_extract()
