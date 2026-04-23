"""
Skill Matcher Module
Extracts skills from text using spaCy and custom pattern matching
"""

import json
import os
import spacy
from spacy.matcher import PhraseMatcher
import re


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
    Create PhraseMatcher mapping aliases back to specific base skills.
    
    Args:
        nlp: spaCy language model
        skills_db: Skills database dictionary
        
    Returns:
        tuple: (PhraseMatcher, list of base skills)
    """
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    all_skills = []
    
    # Flatten all skills from all categories
    for category, skills in skills_db.items():
        all_skills.extend(skills)
    
    # Remove duplicates while preserving order
    base_skills = list(dict.fromkeys(all_skills))
    
    # Add each base skill to the matcher with its own identity string to map variations back
    for skill in base_skills:
        skill_lower = skill.lower()
        variations = set([skill])
        
        # Handle JS frameworks (React.js -> ReactJS)
        if ".js" in skill_lower:
            variations.add(skill.replace(".js", "JS"))
            variations.add(skill.replace(".js", " js"))
        # Handle spaced phrases (Full Stack -> FullStack)
        if " " in skill:
            variations.add(skill.replace(" ", ""))
            variations.add(skill.replace(" ", "-"))
            
        # Handle strictly CamelCase skills (e.g. JavaScript -> Java Script) to combat auto-splitting text cleaners
        camel_split = re.sub(r'([a-z])([A-Z])', r'\1 \2', skill)
        if camel_split != skill:
            variations.add(camel_split)
            
        # Handle development aliases (e.g. Mobile Development -> Mobile Application Development)
        if " Development" in skill:
            variations.add(skill.replace(" Development", " Application Development"))
            variations.add(skill.replace(" Development", " App Development"))
            
        # Handle hyphenated phrases (Full-Stack -> Full Stack)
        if "-" in skill:
            variations.add(skill.replace("-", ""))
            variations.add(skill.replace("-", " "))
            
        patterns = [nlp.make_doc(v) for v in variations]
        matcher.add(skill, patterns) # skill serves as match_id
    
    return matcher, base_skills


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
    doc = nlp(text)
    matches = matcher(doc)
    
    # Extract matched canonical skills (avoiding duplicates)
    found_skills = set()
    for match_id, start, end in matches:
        canonical_skill = nlp.vocab.strings[match_id]
        if canonical_skill != "SKILLS": # Safeguard
            found_skills.add(canonical_skill)
        else:
            found_skills.add(doc[start:end].text)
    
    # Secondary check: Look for variations in unmatched skills
    # e.g. "ReactJS" in text might match "React.js" in DB
    
    # normalize text: remove non-alphanumeric, lowercase
    text_normalized = "".join(c for c in text.lower() if c.isalnum())
    
    # Get all skills from pattern matcher (we access the vocab)
    # This is tricky without passing the full DB, but we can infer from existing matches
    # or better, do a simple robust check on the text for common variations
    
    # For now, let's keep it simple: relying on the extensive spaCy phrase matcher is best
    # The phrase matcher already handles case-insensitive matching
    
    skills_list = sorted(list(found_skills))
    
    # DEBUG: write to log
    try:
        with open("skills_debug.log", "a", encoding="utf-8") as f:
            f.write(f"--- EXTRACT_SKILLS CALLED ---\n")
            f.write(f"TEXT FULL: {text}\n")
            f.write(f"FOUND SKILLS: {skills_list}\n\n")
    except:
        pass
        
    return skills_list


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
    # Note: Matching 75% or more of the JD skills is typically considered a perfect fit
    if len(jd_skills) > 0:
        expected_skills = max(1, len(jd_skills) * 0.75)  # 75% coverage = 100% score
        match_percentage = min(100.0, (len(matched_skills) / expected_skills) * 100)
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
