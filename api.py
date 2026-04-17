from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import io
import spacy

# Import utils
from utils.text_extraction import extract_text, get_word_count, estimate_reading_time
from utils.skill_matcher import initialize_skill_matcher, extract_skills, calculate_skill_match
from utils.scoring_engine import calculate_resume_strength
from utils.linkedin_generator import generate_headline, generate_about_section, generate_keyword_suggestions, calculate_ats_score

app = FastAPI(
    title="AI Resume Analyzer API",
    description="API for analyzing resumes and generating LinkedIn content",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI models at startup
nlp = None
matcher = None
skills_db = None

@app.on_event("startup")
async def startup_event():
    global nlp, matcher, skills_db
    try:
        nlp, matcher, skills_db = initialize_skill_matcher()
        print("✅ AI Models initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize AI models: {str(e)}")

@app.get("/")
def read_root():
    return {"status": "online", "message": "AI Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Analyze resume against job description
    """
    try:
        # 1. Extract text from uploaded file
        file_content = await resume_file.read()
        file_obj = io.BytesIO(file_content)
        
        # Determine file type
        filename = resume_file.filename
        file_type = filename.split('.')[-1].lower() if '.' in filename else ''
        
        if file_type not in ['pdf', 'docx', 'doc']:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload PDF or DOCX.")
            
        resume_text = extract_text(file_obj, file_type)
        
        # 2. Extract skills
        resume_skills = extract_skills(resume_text, matcher, nlp)
        jd_skills = extract_skills(job_description, matcher, nlp)
        
        # 3. Calculate match
        match_analysis = calculate_skill_match(resume_skills, jd_skills)
        
        # 4. Calculate score
        scores = calculate_resume_strength(resume_text, job_description, resume_skills, jd_skills)
        
        # 5. Text stats
        text_stats = {
            "word_count": get_word_count(resume_text),
            "reading_time_min": estimate_reading_time(resume_text)
        }
        
        return {
            "text_stats": text_stats,
            "skills": {
                "resume_skills": resume_skills,
                "jd_skills": jd_skills
            },
            "match_analysis": match_analysis,
            "scores": scores
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/linkedin-optimize")
async def optimize_linkedin(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Generate LinkedIn profile content
    """
    try:
        # Reuse extraction logic (in a real app, you might want to separate or cache this)
        file_content = await resume_file.read()
        file_obj = io.BytesIO(file_content)
        filename = resume_file.filename
        file_type = filename.split('.')[-1].lower() if '.' in filename else ''
        
        resume_text = extract_text(file_obj, file_type)
        resume_skills = extract_skills(resume_text, matcher, nlp)
        jd_skills = extract_skills(job_description, matcher, nlp)
        
        # Generate content
        headline_options = generate_headline(resume_text, resume_skills[:5])
        about_section = generate_about_section(resume_text, resume_skills, job_description)
        keywords = generate_keyword_suggestions(resume_skills, jd_skills)
        ats_score, ats_feedback = calculate_ats_score(resume_text)
        
        return {
            "headline_options": headline_options,
            "about_section": about_section,
            "recommended_keywords": keywords,
            "ats_score": {
                "score": ats_score,
                "feedback": ats_feedback
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
