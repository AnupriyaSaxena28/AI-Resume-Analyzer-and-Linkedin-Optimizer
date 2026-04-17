"""
Scoring Engine Module
Calculate comprehensive resume strength score (0-100)
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import re


def calculate_keyword_density(resume_text, jd_text, max_score=30):
    """
    Calculate keyword density score using TF-IDF
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
        max_score: Maximum points for this component (default 30)
        
    Returns:
        tuple: (score, details dict)
    """
    try:
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(
            max_features=10,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit on both documents
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        feature_names = vectorizer.get_feature_names_out()
        
        # Get JD keywords (top TF-IDF terms)
        jd_vector = tfidf_matrix[0].toarray()[0]
        resume_vector = tfidf_matrix[1].toarray()[0]
        
        # Calculate coverage of JD keywords in resume
        keyword_coverage = 0
        for i, keyword in enumerate(feature_names):
            if jd_vector[i] > 0 and resume_vector[i] > 0:
                keyword_coverage += 1
        
        # Calculate score
        if len(feature_names) > 0:
            coverage_ratio = keyword_coverage / len(feature_names)
        else:
            coverage_ratio = 0
            
        score = coverage_ratio * max_score
        
        details = {
            "top_keywords": list(feature_names),
            "coverage": keyword_coverage,
            "total_keywords": len(feature_names)
        }
        
        return round(score, 1), details
        
    except Exception as e:
        return 0, {"error": str(e)}


def calculate_skill_alignment(resume_skills, jd_skills, max_score=30):
    """
    Calculate skill alignment score
    
    Args:
        resume_skills: List of skills from resume
        jd_skills: List of skills from job description
        max_score: Maximum points for this component (default 30)
        
    Returns:
        tuple: (score, details dict)
    """
    if len(jd_skills) == 0:
        return max_score, {"note": "No JD skills to compare"}
    
    # Calculate match percentage
    resume_skills_lower = set(s.lower() for s in resume_skills)
    jd_skills_lower = set(s.lower() for s in jd_skills)
    
    matched = resume_skills_lower.intersection(jd_skills_lower)
    match_ratio = len(matched) / len(jd_skills_lower)
    
    score = match_ratio * max_score
    
    details = {
        "matched_skills": len(matched),
        "total_jd_skills": len(jd_skills),
        "match_percentage": round(match_ratio * 100, 1)
    }
    
    return round(score, 1), details


def calculate_experience_relevance(resume_text, jd_text, max_score=20):
    """
    Calculate experience relevance score
    
    Args:
        resume_text: Resume text
        jd_text: Job description text
        max_score: Maximum points for this component (default 20)
        
    Returns:
        tuple: (score, details dict)
    """
    score = 0
    details = {}
    
    # Check for years of experience mentions
    years_pattern = r'(\d+)\+?\s*(year|yr)s?'
    resume_years = re.findall(years_pattern, resume_text.lower())
    jd_years = re.findall(years_pattern, jd_text.lower())
    
    if resume_years and jd_years:
        score += 8
        details["years_mentioned"] = True
    elif resume_years:
        score += 5
        details["years_mentioned"] = "partial"
    
    # Check for job-related keywords
    job_keywords = ['experience', 'worked', 'developed', 'managed', 'led', 
                   'implemented', 'designed', 'analyzed', 'created', 'built']
    
    job_keyword_count = sum(1 for keyword in job_keywords 
                           if keyword in resume_text.lower())
    
    # Award points based on keyword presence (max 12 points)
    keyword_score = min(12, (job_keyword_count / len(job_keywords)) * 12)
    score += keyword_score
    details["job_keywords_found"] = job_keyword_count
    
    return round(min(score, max_score), 1), details


def calculate_length_score(text, max_score=10):
    """
    Calculate length optimization score
    Ideal length: 400-800 words
    
    Args:
        text: Resume text
        max_score: Maximum points for this component (default 10)
        
    Returns:
        tuple: (score, details dict)
    """
    word_count = len(text.split())
    
    if 400 <= word_count <= 800:
        score = max_score
        feedback = "Optimal length"
    elif 300 <= word_count < 400:
        score = max_score * 0.7
        feedback = "Slightly short"
    elif 800 < word_count <= 1000:
        score = max_score * 0.7
        feedback = "Slightly long"
    elif word_count < 300:
        score = max_score * 0.3
        feedback = "Too short"
    else:  # > 1000
        score = max_score * 0.4
        feedback = "Too long"
    
    details = {
        "word_count": word_count,
        "feedback": feedback,
        "optimal_range": "400-800 words"
    }
    
    return round(score, 1), details


def calculate_formatting_score(text, max_score=10):
    """
    Calculate formatting and structure score
    
    Args:
        text: Resume text
        max_score: Maximum points for this component (default 10)
        
    Returns:
        tuple: (score, details dict)
    """
    score = 0
    details = {"sections_found": []}
    
    # Check for key sections
    sections = {
        'education': r'education|degree|university|college',
        'experience': r'experience|employment|work history',
        'skills': r'skills|technical skills|competencies',
        'contact': r'email|phone|linkedin|github'
    }
    
    for section_name, pattern in sections.items():
        if re.search(pattern, text.lower()):
            score += 2.5
            details["sections_found"].append(section_name)
    
    details["sections_count"] = len(details["sections_found"])
    
    return round(min(score, max_score), 1), details


def calculate_semantic_similarity(nlp, resume_text, jd_text, max_score=30):
    """
    Calculate semantic similarity score using spaCy word vectors
    
    Args:
        nlp: spaCy medium model with word vectors
        resume_text: Resume text
        jd_text: Job description text
        max_score: Maximum points for this component (default 30)
        
    Returns:
        tuple: (score, details dict)
    """
    try:
        # Check if nlp model has vectors
        if not nlp.vocab.vectors.length:
            return 0, {"error": "NLP model does not have word vectors"}
            
        doc_resume = nlp(resume_text)
        doc_jd = nlp(jd_text)
        
        # Calculate cosine similarity
        similarity = doc_resume.similarity(doc_jd)
        
        score = similarity * max_score
        
        details = {
            "similarity_raw": round(similarity, 3),
            "method": "spaCy en_core_web_md (300d vectors)"
        }
        
        return round(score, 1), details
        
    except Exception as e:
        return 0, {"error": str(e)}


def calculate_resume_strength(nlp, resume_text, jd_text, resume_skills, jd_skills):
    """
    Calculate total resume strength score (0-100) using semantic + keyword analysis
    
    Args:
        nlp: spaCy model
        resume_text: Resume text
        jd_text: Job description text
        resume_skills: List of skills from resume
        jd_skills: List of skills from job description
        
    Returns:
        dict: Complete scoring breakdown
    """
    # Calculate individual components
    semantic_score, semantic_details = calculate_semantic_similarity(nlp, resume_text, jd_text)
    skill_score, skill_details = calculate_skill_alignment(resume_skills, jd_skills, max_score=25)
    keyword_score, keyword_details = calculate_keyword_density(resume_text, jd_text, max_score=20)
    experience_score, experience_details = calculate_experience_relevance(resume_text, jd_text, max_score=15)
    formatting_score, formatting_details = calculate_formatting_score(resume_text, max_score=10)
    
    # Calculate total
    total_score = (semantic_score + skill_score + keyword_score + 
                  experience_score + formatting_score)
    
    # Generate feedback
    feedback = []
    
    if semantic_score >= 24:
        feedback.append("🧠 Exceptional contextual alignment with the role!")
    elif semantic_score >= 18:
        feedback.append("✅ Strong semantic match between resume and job description")
    else:
        feedback.append("💡 Consider tailoring your resume summary to better align with the job's context")

    if skill_score >= 20:
        feedback.append("✅ Excellent skill alignment!")
    elif skill_score >= 15:
        feedback.append("👍 Good skill match")
    else:
        feedback.append("⚠️ Add more relevant skills from the job description")
    
    if keyword_score >= 15:
        feedback.append("✅ Strong keyword optimization")
    else:
        feedback.append("💡 Include more core keywords mentioned in the JD")
    
    if formatting_score < 7:
        feedback.append("📋 Include clear sections: Education, Experience, Skills")
    
    return {
        "total_score": round(min(total_score, 100), 0),
        "semantic_similarity": semantic_score,
        "skill_alignment": skill_score,
        "keyword_density": keyword_score,
        "experience_relevance": experience_score,
        "formatting_score": formatting_score,
        "feedback": feedback,
        "details": {
            "semantic": semantic_details,
            "skills": skill_details,
            "keywords": keyword_details,
            "experience": experience_details,
            "formatting": formatting_details
        }
    }


def get_score_color(score):
    """
    Get color code based on score
    
    Args:
        score: Score value (0-100)
        
    Returns:
        str: Color name for visualization
    """
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"


def get_score_emoji(score):
    """
    Get emoji based on score
    
    Args:
        score: Score value (0-100)
        
    Returns:
        str: Emoji representation
    """
    if score >= 90:
        return "🟢⭐⭐⭐⭐⭐"
    elif score >= 80:
        return "🟢⭐⭐⭐⭐"
    elif score >= 70:
        return "🟡⭐⭐⭐"
    elif score >= 60:
        return "🟡⭐⭐"
    else:
        return "🔴⭐"
