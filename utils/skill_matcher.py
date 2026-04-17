"""
Skill Matcher Module
Extracts skills from text using spaCy and custom pattern matching
"""

import json
import os
import spacy
from spacy.matcher import PhraseMatcher


def load_skills_database():
    """
    Load skills database from JSON file
    
    Returns:
        dict: Skills database with categories
    """
    try:
        # Get the path to skills_database.json
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(current_dir, 'data', 'skills_database.json')
        
        with open(db_path, 'r', encoding='utf-8') as f:
            skills_db = json.load(f)
        
        return skills_db
    except Exception as e:
        raise Exception(f"Error loading skills database: {str(e)}")


def create_skill_matcher(nlp, skills_db):
    """
    Create PhraseMatcher with all skills from database
    
    Args:
        nlp: spaCy language model
        skills_db: Skills database dictionary
        
    Returns:
        tuple: (PhraseMatcher, flat list of all skills)
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    all_skills = []
    
    # Flatten all skills from all categories
    for category, skills in skills_db.items():
        all_skills.extend(skills)
    
    # Remove duplicates while preserving order
    all_skills = list(dict.fromkeys(all_skills))
    
    # Create patterns for matching
    patterns = [nlp.make_doc(skill) for skill in all_skills]
    matcher.add("SKILLS", patterns)
    
    return matcher, all_skills


def extract_skills(text, matcher, nlp):
    """
    Extract unique skills from text
    
    Args:
        text: Input text to analyze
        matcher: PhraseMatcher object
        nlp: spaCy language model
        
    Returns:
        list: List of unique extracted skills
    """
    # Create normalized map of text
    # This helps match "Node.js" with "NodeJS" or "C++" with "C Plus Plus" if needed
    # For now, we use the direct phrase matcher but we could add fuzzy matching here
    
    doc = nlp(text)
    matches = matcher(doc)
    
    # Extract matched skills (avoiding duplicates)
    found_skills = set()
    for match_id, start, end in matches:
        skill = doc[start:end].text
        found_skills.add(skill)
    
    # Secondary check: Look for variations in unmatched skills
    # e.g. "ReactJS" in text might match "React.js" in DB
    
    # normalize text: remove non-alphanumeric, lowercase
    text_normalized = "".join(c for c in text.lower() if c.isalnum())
    
    # Get all skills from pattern matcher (we access the vocab)
    # This is tricky without passing the full DB, but we can infer from existing matches
    # or better, do a simple robust check on the text for common variations
    
    # For now, let's keep it simple: relying on the extensive spaCy phrase matcher is best
    # The phrase matcher already handles case-insensitive matching
    
    return sorted(list(found_skills))


def categorize_skills(skills, skills_db):
    """
    Map extracted skills to their categories
    
    Args:
        skills: List of extracted skills
        skills_db: Skills database dictionary
        
    Returns:
        dict: Skills organized by category
    """
    categorized = {}
    
    for skill in skills:
        for category, category_skills in skills_db.items():
            # Case-insensitive matching
            if any(skill.lower() == s.lower() for s in category_skills):
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(skill)
                break
    
    return categorized


def calculate_skill_match(resume_skills, jd_skills):
    """
    Calculate skill match between resume and job description
    
    Args:
        resume_skills: List of skills from resume
        jd_skills: List of skills from job description
        
    Returns:
        dict: Match analysis with matched/missing skills and percentage
    """
    # Convert to lowercase for comparison
    resume_skills_lower = set(s.lower() for s in resume_skills)
    jd_skills_lower = set(s.lower() for s in jd_skills)
    
    # Find matched skills
    matched_skills_lower = resume_skills_lower.intersection(jd_skills_lower)
    
    # Find missing skills
    missing_skills_lower = jd_skills_lower - resume_skills_lower
    
    # Get original case versions
    matched_skills = [s for s in jd_skills if s.lower() in matched_skills_lower]
    missing_skills = [s for s in jd_skills if s.lower() in missing_skills_lower]
    
    # Calculate match percentage
    if len(jd_skills) > 0:
        match_percentage = (len(matched_skills) / len(jd_skills)) * 100
    else:
        match_percentage = 0.0
    
    return {
        "matched_skills": sorted(matched_skills),
        "missing_skills": sorted(missing_skills),
        "match_percentage": round(match_percentage, 1),
        "total_jd_skills": len(jd_skills),
        "total_matched": len(matched_skills),
        "total_missing": len(missing_skills)
    }


def initialize_skill_matcher():
    """
    Initialize spaCy model and skill matcher
    
    Returns:
        tuple: (nlp model, matcher, skills_db)
    """
    try:
        # Load spaCy model (medium with word vectors)
        try:
            nlp = spacy.load("en_core_web_md")
        except:
            # If model not found, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_md"], check=True)
            nlp = spacy.load("en_core_web_md")
        
        # Load skills database
        skills_db = load_skills_database()
        
        # Create matcher
        matcher, all_skills = create_skill_matcher(nlp, skills_db)
        
        return nlp, matcher, skills_db
        
    except Exception as e:
        raise Exception(f"Error initializing skill matcher: {str(e)}")
