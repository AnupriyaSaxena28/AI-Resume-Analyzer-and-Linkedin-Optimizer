"""
LinkedIn Generator Module
Generate optimized LinkedIn profile content
"""

import re
import language_tool_python


def generate_headline(resume_text, skills, max_length=120):
    """
    Generate optimized LinkedIn headline
    Format: "Role | Skill1, Skill2, Skill3 | Education/Cert"
    
    Args:
        resume_text: Resume text
        skills: List of top skills
        max_length: Maximum character length (default 120)
        
    Returns:
        str: Generated headline
    """
    # Extract role/title (look for common job titles)
    role_patterns = [
        r'(software engineer|data scientist|data analyst|web developer|'
        r'product manager|business analyst|project manager|designer|'
        r'developer|engineer|analyst|manager|consultant|specialist)',
    ]
    
    role = "Professional"
    for pattern in role_patterns:
        match = re.search(pattern, resume_text.lower())
        if match:
            role = match.group(1).title()
            break
    
    # Get top 3-4 skills
    top_skills = skills[:4] if len(skills) >= 4 else skills
    skills_str = ", ".join(top_skills)
    
    # Extract education (look for degree)
    education = ""
    edu_patterns = [
        r'(B\.?Tech|B\.?E\.?|Bachelor|Master|M\.?Tech|MBA|Ph\.?D)',
        r'(Computer Science|CS|Engineering|Business|Data Science)'
    ]
    
    for pattern in edu_patterns:
        match = re.search(pattern, resume_text, re.IGNORECASE)
        if match:
            education = match.group(1)
            break
    
    # Construct headline
    if education:
        headline = f"{role} | {skills_str} | {education}"
    else:
        headline = f"{role} | {skills_str}"
    
    # Truncate if too long
    if len(headline) > max_length:
        # Try with fewer skills
        if len(top_skills) > 2:
            skills_str = ", ".join(top_skills[:3])
            if education:
                headline = f"{role} | {skills_str} | {education}"
            else:
                headline = f"{role} | {skills_str}"
        
        # Final truncation if still too long
        if len(headline) > max_length:
            headline = headline[:max_length-3] + "..."
    
    return headline


def generate_about_section(resume_text, skills, jd_text=None):
    """
    Generate optimized About section for LinkedIn
    Length: 200-300 words
    
    Args:
        resume_text: Resume text
        skills: List of top skills
        jd_text: Optional job description for context
        
    Returns:
        str: Generated About section
    """
    # Extract key information
    role_match = re.search(
        r'(software engineer|data scientist|data analyst|web developer|'
        r'product manager|business analyst|developer|engineer|analyst)',
        resume_text.lower()
    )
    
    role = role_match.group(1).title() if role_match else "Professional"
    
    # Get top skills
    top_skills = skills[:6] if len(skills) >= 6 else skills
    
    # Extract years of experience if mentioned
    years_match = re.search(r'(\d+)\+?\s*years?', resume_text.lower())
    years_exp = years_match.group(1) if years_match else None
    
    # Build About section
    about_parts = []
    
    # Opening hook
    if years_exp:
        about_parts.append(
            f"Motivated {role} with {years_exp}+ years of experience in delivering "
            f"high-quality solutions and driving impactful results."
        )
    else:
        about_parts.append(
            f"Passionate {role} with a proven track record of delivering "
            f"innovative solutions and exceeding expectations."
        )
    
    # Skills showcase
    if len(top_skills) >= 3:
        skills_sentence = (
            f"My expertise spans across {', '.join(top_skills[:-1])}, "
            f"and {top_skills[-1]}, enabling me to tackle complex challenges "
            f"with confidence and creativity."
        )
        about_parts.append(skills_sentence)
    
    # Experience highlight
    experience_keywords = []
    keywords_to_check = [
        'developed', 'implemented', 'designed', 'managed', 'led',
        'optimized', 'analyzed', 'created', 'built', 'improved'
    ]
    
    for keyword in keywords_to_check:
        if keyword in resume_text.lower():
            experience_keywords.append(keyword)
            if len(experience_keywords) >= 3:
                break
    
    if experience_keywords:
        about_parts.append(
            f"Throughout my career, I have successfully {experience_keywords[0]} "
            f"innovative solutions, {experience_keywords[1] if len(experience_keywords) > 1 else 'delivered'} "
            f"projects on time, and consistently contributed to team success."
        )
    
    # Value proposition
    about_parts.append(
        "I thrive in collaborative environments where I can leverage my technical "
        "skills and problem-solving abilities to create meaningful impact. "
        "I'm always eager to learn new technologies and take on challenging projects."
    )
    
    # Call to action
    about_parts.append(
        "Let's connect if you're looking for a dedicated professional who brings "
        "both technical expertise and a passion for innovation to the table."
    )
    
    # Join parts
    about = "\n\n".join(about_parts)
    
    # Ensure it's within word limit (200-300 words)
    words = about.split()
    if len(words) > 300:
        about = " ".join(words[:300]) + "..."
    
    return about


def generate_keyword_suggestions(resume_skills, jd_skills):
    """
    Generate keyword suggestions for LinkedIn profile
    
    Args:
        resume_skills: List of skills from resume
        jd_skills: List of skills from job description
        
    Returns:
        list: Top keyword suggestions
    """
    # Find skills in JD but not in resume
    resume_skills_lower = set(s.lower() for s in resume_skills)
    
    suggestions = []
    for skill in jd_skills:
        if skill.lower() not in resume_skills_lower:
            suggestions.append(skill)
    
    # Return top 10
    return suggestions[:10]


def calculate_ats_score(resume_text):
    """
    Calculate ATS compatibility score (0-100)
    
    Args:
        resume_text: Resume text
        
    Returns:
        tuple: (score, feedback list)
    """
    score = 0
    feedback = []
    
    # Check for standard sections (40 points)
    sections = {
        'Contact': r'email|phone|linkedin',
        'Experience': r'experience|employment|work history',
        'Education': r'education|degree|university',
        'Skills': r'skills|technical skills'
    }
    
    sections_found = 0
    for section_name, pattern in sections.items():
        if re.search(pattern, resume_text.lower()):
            sections_found += 1
            score += 10
        else:
            feedback.append(f"❌ Add {section_name} section")
    
    if sections_found == 4:
        feedback.append("✅ All standard sections present")
    
    # Check for simple formatting (30 points)
    # Good: Avoid complex tables, graphics mentions
    complex_indicators = ['table', 'image', 'graphic', 'chart']
    has_complex = any(indicator in resume_text.lower() 
                     for indicator in complex_indicators)
    
    if not has_complex:
        score += 30
        feedback.append("✅ Simple, ATS-friendly formatting")
    else:
        score += 15
        feedback.append("⚠️ May contain complex formatting")
    
    # Check for contact information (20 points)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    has_email = re.search(email_pattern, resume_text)
    has_phone = re.search(phone_pattern, resume_text)
    
    if has_email and has_phone:
        score += 20
        feedback.append("✅ Contact information present")
    elif has_email or has_phone:
        score += 10
        feedback.append("⚠️ Add both email and phone")
    else:
        feedback.append("❌ Add contact information")
    
    # Check for professional keywords (10 points)
    professional_keywords = [
        'achieved', 'improved', 'developed', 'managed', 'led',
        'designed', 'implemented', 'analyzed', 'created'
    ]
    
    keyword_count = sum(1 for kw in professional_keywords 
                       if kw in resume_text.lower())
    
    if keyword_count >= 5:
        score += 10
        feedback.append("✅ Strong action verbs usage")
    elif keyword_count >= 3:
        score += 5
        feedback.append("👍 Good use of action verbs")
    else:
        feedback.append("💡 Use more action verbs")
    
    return min(score, 100), feedback


def check_grammar(text, max_errors_to_show=5):
    """
    Check grammar using language-tool-python
    
    Args:
        text: Text to check
        max_errors_to_show: Maximum errors to display
        
    Returns:
        tuple: (error_count, error_messages)
    """
    try:
        tool = language_tool_python.LanguageTool('en-US')
        matches = tool.check(text)
        
        error_count = len(matches)
        error_messages = []
        
        for match in matches[:max_errors_to_show]:
            error_messages.append({
                "message": match.message,
                "context": match.context,
                "suggestions": match.replacements[:3]
            })
        
        tool.close()
        
        return error_count, error_messages
        
    except Exception as e:
        return 0, [{"message": f"Grammar check unavailable: {str(e)}"}]
