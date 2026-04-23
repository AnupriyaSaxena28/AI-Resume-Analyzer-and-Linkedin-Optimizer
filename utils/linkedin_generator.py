"""
LinkedIn Generator Module
Generate optimized LinkedIn profile content
"""

import re
import language_tool_python


def generate_headline(resume_text, skills, max_length=220):
    """
    Generate optimized, long and descriptive LinkedIn headline with dynamic content
    
    Args:
        resume_text: Resume text
        skills: List of top skills
        max_length: Maximum character length (default 220 for modern LinkedIn)
        
    Returns:
        str: Generated headline (single descriptive option)
    """
    # Extract role/title with more comprehensive patterns
    role_patterns = [
        r'(senior software engineer|lead data scientist|senior data analyst|'
        r'senior web developer|senior product manager|lead engineer|'
        r'software engineer|data scientist|data analyst|web developer|'
        r'full stack developer|frontend developer|backend developer|'
        r'product manager|business analyst|project manager|ui/ux designer|'
        r'machine learning engineer|devops engineer|cloud architect|'
        r'developer|engineer|analyst|manager|consultant|specialist|architect)',
    ]
    
    role = None
    for pattern in role_patterns:
        match = re.search(pattern, resume_text.lower())
        if match:
            role = match.group(1).title()
            break
    
    if not role:
        role = "Professional"
    
    # Extract years of experience
    years_match = re.search(r'(\d+)\+?\s*(year|yr)s?\s*(of\s*)?(experience|exp)', resume_text.lower())
    years_exp = years_match.group(1) if years_match else None
    
    # Extract certifications
    cert_patterns = [
        r'(AWS Certified|Google Cloud|Azure|PMP|Certified|Certification)',
        r'(Scrum Master|Product Owner|Six Sigma)',
    ]
    certifications = []
    for pattern in cert_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        certifications.extend(matches)
    
    # Extract achievements
    achievement_patterns = [
        r'(\d+%)\s*(improvement|increase|growth|revenue|efficiency)',
        r'(led|managed)\s*team\s*of\s*(\d+)',
        r'(\$\d+[MK]?)\s*(revenue|savings|budget)',
    ]
    achievements = []
    for pattern in achievement_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        if matches:
            achievements.append(' '.join(filter(None, matches[0])))
    
    # Define descriptive "mission" or "impact" tags based on role
    mission_statement = ""
    lower_role = role.lower()
    if 'data' in lower_role:
        mission_statement = "Transforming Data into Actionable Insights"
    elif 'engineer' in lower_role or 'developer' in lower_role:
        mission_statement = "Building Scalable, High-Impact Technical Solutions"
    elif 'manager' in lower_role:
        mission_statement = "Driving Product Excellence & Team Success"
    elif 'design' in lower_role or 'ux' in lower_role:
        mission_statement = "Crafting User-Centric Digital Experiences"
    else:
        mission_statement = "Passionate about Innovation & Results"

    # Get more skills for a longer headline
    top_skills = skills[:6] if len(skills) >= 6 else skills
    
    # Build headline parts
    headline_parts = []
    
    # 1. Role & Seniority
    if years_exp and int(years_exp) >= 5:
        headline_parts.append(f"{role} ({years_exp}+ Years of Experience)")
    else:
        headline_parts.append(role)
        
    # 2. Mission Statement (adds descriptiveness)
    headline_parts.append(mission_statement)
    
    # 3. Comprehensive Skills
    if top_skills:
        headline_parts.append("Expertise: " + ", ".join(top_skills))
        
    # 4. Certifications or Achievements
    if certifications:
        headline_parts.append(certifications[0])
    elif achievements:
        headline_parts.append(f"Proven Impact: {achievements[0]}")
        
    # Final assembly with a professional separator
    headline = " | ".join(headline_parts)
    
    # If still too long, intelligently trim from the end of the skills part or others
    while len(headline) > max_length and len(headline_parts) > 1:
        # Try shortening the skills list first
        if "Expertise: " in headline_parts[2] and "," in headline_parts[2]:
            current_skills = headline_parts[2].replace("Expertise: ", "").split(", ")
            if len(current_skills) > 1:
                headline_parts[2] = "Expertise: " + ", ".join(current_skills[:-1])
            else:
                headline_parts.pop(2)
        else:
            headline_parts.pop()
        headline = " | ".join(headline_parts)
        
    if len(headline) > max_length:
        headline = headline[:max_length-3] + "..."
        
    return headline


def generate_about_section(resume_text, skills, jd_text=None):
    """
    Generate personalized, unique About section for LinkedIn
    Dynamically extracts actual content from resume
    Length: 200-300 words
    
    Args:
        resume_text: Resume text
        skills: List of top skills
        jd_text: Optional job description for context
        
    Returns:
        str: Generated About section with unique content
    """
    about_parts = []
    
    # === PART 1: Extract Resume Details ===
    
    # Extract role/title
    role_patterns = [
        r'(senior software engineer|lead data scientist|senior data analyst|'
        r'software engineer|data scientist|data analyst|web developer|'
        r'full stack developer|machine learning engineer|'
        r'product manager|business analyst|developer|engineer|analyst)',
    ]
    
    role = None
    for pattern in role_patterns:
        match = re.search(pattern, resume_text.lower())
        if match:
            role = match.group(1).title()
            break
    
    if not role:
        role = "Professional"
    
    # Extract years of experience
    years_match = re.search(r'(\d+)\+?\s*(year|yr)s?\s*(of\s*)?(experience|exp)', resume_text.lower())
    years_exp = int(years_match.group(1)) if years_match else None
    
    # Extract education details
    education_info = []
    edu_patterns = [
        r'(Bachelor|Master|Ph\.?D|MBA|B\.?Tech|M\.?Tech|B\.?E\.?|M\.?Sc|B\.?Sc)\s*(of|in|degree)?\s*([A-Za-z\s]+)',
        r'(Computer Science|Data Science|Engineering|Business|Information Technology|CS)',
        r'(University|College|Institute)\s*of\s*([A-Za-z\s]+)',
    ]
    
    for pattern in edu_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        if matches:
            education_info.extend([m if isinstance(m, str) else ' '.join(m) for m in matches[:2]])
    
    # Extract actual project descriptions or achievements
    project_sentences = []
    achievement_patterns = [
        r'(developed|built|created|designed|implemented)\s+([^.]{20,100})',
        r'(achieved|improved|increased|reduced|optimized)\s+([^.]{20,100})',
        r'(led|managed|coordinated)\s+(a\s+)?team\s+([^.]{10,80})',
    ]
    
    for pattern in achievement_patterns:
        matches = re.findall(pattern, resume_text, re.IGNORECASE)
        for match in matches[:3]:
            sentence = ' '.join(match).strip()
            if len(sentence) > 20:
                project_sentences.append(sentence)
    
    # Extract technologies/tools mentioned
    tech_mentions = []
    for skill in skills[:8]:
        # Count how many times skill appears in resume
        count = len(re.findall(r'\b' + re.escape(skill.lower()) + r'\b', resume_text.lower()))
        if count > 0:
            tech_mentions.append((skill, count))
    
    # Sort by frequency
    tech_mentions.sort(key=lambda x: x[1], reverse=True)
    primary_skills = [t[0] for t in tech_mentions[:4]]
    
    # Extract industry or domain
    industry_keywords = {
        'finance': ['finance', 'banking', 'trading', 'investment'],
        'healthcare': ['healthcare', 'medical', 'hospital', 'clinical'],
        'e-commerce': ['e-commerce', 'retail', 'online shopping', 'marketplace'],
        'technology': ['saas', 'cloud', 'software', 'platform'],
        'education': ['education', 'learning', 'teaching', 'training'],
    }
    
    industry = None
    for ind, keywords in industry_keywords.items():
        if any(kw in resume_text.lower() for kw in keywords):
            industry = ind
            break
    
    # === PART 2: Build Dynamic About Section ===
    
    # Opening: Vary based on experience level
    if years_exp and years_exp >= 7:
        opening_templates = [
            f"As a seasoned {role} with {years_exp}+ years of experience, I specialize in transforming complex challenges into elegant, scalable solutions.",
            f"With over {years_exp} years in the industry, I've evolved into a {role} who thrives on innovation and delivering measurable impact.",
            f"I'm a {role} with {years_exp}+ years of hands-on experience building solutions that drive business growth and technical excellence.",
        ]
        about_parts.append(opening_templates[hash(resume_text) % len(opening_templates)])
    elif years_exp and years_exp >= 3:
        opening_templates = [
            f"I'm a results-driven {role} with {years_exp}+ years of experience creating innovative solutions and exceeding project goals.",
            f"As a dedicated {role} with {years_exp} years in the field, I bring both technical expertise and a passion for problem-solving to every project.",
            f"With {years_exp}+ years as a {role}, I've developed a strong track record of delivering high-quality solutions and driving team success.",
        ]
        about_parts.append(opening_templates[hash(resume_text) % len(opening_templates)])
    else:
        opening_templates = [
            f"I'm an enthusiastic {role} passionate about leveraging technology to solve real-world problems and create value.",
            f"As a motivated {role}, I combine technical skills with creative problem-solving to build impactful solutions.",
            f"I'm a {role} driven by curiosity and a commitment to continuous learning in the ever-evolving tech landscape.",
        ]
        about_parts.append(opening_templates[hash(resume_text) % len(opening_templates)])
    
    # Experience & Skills: Use actual extracted achievements
    if project_sentences:
        # Pick 1-2 most relevant project descriptions
        selected_projects = project_sentences[:2]
        experience_para = "In my professional journey, I have " + selected_projects[0]
        if len(selected_projects) > 1:
            experience_para += f", and {selected_projects[1]}"
        experience_para += "."
        about_parts.append(experience_para)
    else:
        # Fallback if no projects extracted
        if primary_skills:
            about_parts.append(
                f"My technical toolkit includes {', '.join(primary_skills[:-1])}, and {primary_skills[-1]}, "
                f"which I leverage to build robust, efficient solutions."
            )
    
    # Domain expertise (if detected)
    if industry:
        domain_sentences = {
            'finance': "I have deep experience in the financial sector, where precision and security are paramount.",
            'healthcare': "I'm passionate about healthcare technology and improving patient outcomes through innovation.",
            'e-commerce': "I specialize in e-commerce solutions, focusing on user experience and conversion optimization.",
            'technology': "I thrive in fast-paced tech environments, building scalable cloud-native applications.",
            'education': "I'm committed to education technology that makes learning accessible and engaging.",
        }
        about_parts.append(domain_sentences.get(industry, ""))
    
    # Education highlight (if available)
    if education_info:
        edu_text = education_info[0]
        about_parts.append(
            f"My academic foundation in {edu_text} provides the theoretical grounding "
            f"that complements my hands-on experience."
        )
    
    # What drives you (varied endings)
    motivation_templates = [
        "What drives me is the opportunity to work on challenging problems that push the boundaries of what's possible, "
        "while collaborating with talented teams to achieve ambitious goals.",
        
        "I'm energized by environments where innovation is encouraged, and where technology is used as a tool "
        "to create meaningful impact for users and businesses alike.",
        
        "I believe in the power of continuous learning and staying ahead of industry trends to deliver "
        "cutting-edge solutions that stand the test of time.",
    ]
    about_parts.append(motivation_templates[hash(resume_text) % len(motivation_templates)])
    
    # Call to action (varied)
    cta_templates = [
        "I'm always interested in connecting with fellow professionals, exploring new opportunities, "
        "and discussing how technology can solve tomorrow's challenges. Let's connect!",
        
        "Whether you're looking to collaborate on innovative projects or simply want to exchange ideas "
        "about the latest in tech, I'd love to hear from you. Feel free to reach out!",
        
        "I'm open to new opportunities where I can contribute my skills and continue growing as a professional. "
        "Let's connect and explore how we can create value together!",
    ]
    about_parts.append(cta_templates[hash(resume_text) % len(cta_templates)])
    
    # === PART 3: Assemble and Optimize ===
    
    # Remove empty parts
    about_parts = [part for part in about_parts if part and part.strip()]
    
    # Join with paragraph breaks
    about = "\n\n".join(about_parts)
    
    # Word count optimization (200-300 words)
    words = about.split()
    word_count = len(words)
    
    if word_count > 300:
        # Remove least important paragraph (usually domain or education)
        if len(about_parts) > 4:
            about_parts.pop(-2)  # Remove second-to-last paragraph
            about = "\n\n".join(about_parts)
            words = about.split()
    
    if len(words) > 300:
        # Truncate to 300 words
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
        'Contact': r'email|phone|linkedin|linked in|github|git hub',
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
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    
    has_email = re.search(email_pattern, resume_text)
    has_phone = re.search(phone_pattern, resume_text)
    
    # If the regex didn't find the 'Contact' section title but found actual contact info, correct the feedback
    contact_missing_msg = "❌ Add Contact section"
    if (has_email or has_phone) and contact_missing_msg in feedback:
        feedback.remove(contact_missing_msg)
        sections_found += 1
        score += 10
        if sections_found == 4 and "✅ All standard sections present" not in feedback:
            feedback.append("✅ All standard sections present")

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
