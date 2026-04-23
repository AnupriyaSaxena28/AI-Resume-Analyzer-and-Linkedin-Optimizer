"""
AI Resume Analyzer + LinkedIn Optimizer
A production-ready Streamlit web application for resume analysis and LinkedIn optimization
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import io

# Import utility modules
from utils.text_extraction import extract_text, get_word_count, estimate_reading_time
from utils.skill_matcher import (
    initialize_skill_matcher, extract_skills, categorize_skills, calculate_skill_match
)
from utils.scoring_engine import (
    calculate_resume_strength, get_score_color, get_score_emoji
)
from utils.linkedin_generator import (
    generate_headline, generate_about_section, generate_keyword_suggestions,
    calculate_ats_score, check_grammar
)


# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for professional dark theme
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #3b82f6;
        --secondary: #1e3a8a;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
    }
    
    /* Card styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #334155;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    
    /* Score indicators */
    .score-high {
        color: #10b981;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .score-medium {
        color: #f59e0b;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    .score-low {
        color: #ef4444;
        font-weight: bold;
        font-size: 1.2em;
    }
    
    /* Skill tags */
    .skill-tag {
        display: inline-block;
        background: #3b82f6;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9em;
    }
    
    .skill-tag-missing {
        background: #ef4444;
    }
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #1e3a8a 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: #1e293b;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Info boxes */
    .info-box {
        background: #1e293b;
        padding: 1rem;
        border-left: 4px solid #3b82f6;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
    }
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'nlp' not in st.session_state:
        st.session_state.nlp = None
        st.session_state.matcher = None
        st.session_state.skills_db = None
    
    if 'resume_text' not in st.session_state:
        st.session_state.resume_text = None
        st.session_state.jd_text = None
        st.session_state.resume_skills = []
        st.session_state.jd_skills = []
        st.session_state.analysis_done = False


# Main header
def show_header():
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Resume Analyzer + LinkedIn Optimizer</h1>
        <p style="font-size: 1.1em; margin-top: 0.5rem;">
            Analyze your resume, optimize for ATS, and generate LinkedIn content with AI
        </p>
    </div>
    """, unsafe_allow_html=True)


# Initialize skill matcher (with caching)
@st.cache_resource
def load_skill_matcher():
    """Load and cache the skill matcher"""
    with st.spinner("🔧 Initializing AI models... This may take a minute on first run."):
        return initialize_skill_matcher()


# Section 1: Resume Upload
def resume_upload_section():
    st.header("📤 Upload Your Resume")
    
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF or DOCX)",
        type=['pdf', 'docx', 'doc'],
        help="Upload your resume in PDF or DOCX format"
    )
    
    if uploaded_file is not None:
        file_type = uploaded_file.name.split('.')[-1]
        
        with st.spinner("📄 Extracting text from your resume..."):
            try:
                resume_text = extract_text(uploaded_file, file_type)
                st.session_state.resume_text = resume_text
                
                # Success message
                st.success(f"✅ Resume uploaded successfully! ({file_type.upper()})")
                
                # Stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Word Count", get_word_count(resume_text))
                with col2:
                    st.metric("Est. Reading Time", f"{estimate_reading_time(resume_text)} min")
                with col3:
                    st.metric("Characters", len(resume_text))
                
                # Preview
                with st.expander("📝 Preview Extracted Text"):
                    st.text_area(
                        "Resume Content",
                        resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text,
                        height=200,
                        disabled=True
                    )
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.session_state.resume_text = None
    
    return st.session_state.resume_text


# Section 2: Job Description Input
def job_description_section():
    st.header("💼 Enter Job Description")
    
    jd_text = st.text_area(
        "Paste the job description here",
        height=200,
        placeholder="Paste the complete job description you're applying for...",
        help="Include the full job description for best results"
    )
    
    if jd_text:
        if len(jd_text) >= 10:
            st.session_state.jd_text = jd_text
            
            # Stats
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Word Count", get_word_count(jd_text))
            with col2:
                st.metric("Characters", len(jd_text))
            
            # Real-time skill preview
            if st.checkbox("🔍 Preview Skills in JD", value=False):
                with st.spinner("Extracting skills..."):
                    nlp, matcher, skills_db = load_skill_matcher()
                    jd_skills = extract_skills(jd_text, matcher, nlp)
                    
                    if jd_skills:
                        st.info(f"Found {len(jd_skills)} skills in job description")
                        st.write(", ".join(jd_skills[:20]))
        else:
            st.warning("⚠️ Job description is too short. Please enter at least 10 characters.")
    
    return st.session_state.jd_text


# Section 3: Analysis Dashboard
def analysis_dashboard_section(resume_text, jd_text):
    st.header("🔍 Match Analysis")
    
    if st.button("⚡ Analyze Resume", type="primary", use_container_width=True):
        with st.spinner("🤖 AI is analyzing your resume... Please wait."):
            try:
                # Load skill matcher
                nlp, matcher, skills_db = load_skill_matcher()
                
                # Extract skills
                progress = st.progress(0)
                progress.progress(20)
                
                resume_skills = extract_skills(resume_text, matcher, nlp)
                st.session_state.resume_skills = resume_skills
                progress.progress(40)
                
                jd_skills = extract_skills(jd_text, matcher, nlp)
                st.session_state.jd_skills = jd_skills
                progress.progress(60)
                
                # Calculate match
                skill_match = calculate_skill_match(resume_skills, jd_skills)
                progress.progress(80)
                
                # Calculate resume strength
                resume_score = calculate_resume_strength(
                    nlp, resume_text, jd_text, resume_skills, jd_skills
                )
                progress.progress(100)
                
                # Store in session state
                st.session_state.skill_match = skill_match
                st.session_state.resume_score = resume_score
                st.session_state.analysis_done = True
                
                st.success("✅ Analysis complete!")
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                return
    
    # Display results if analysis done
    if st.session_state.get('analysis_done', False):
        display_analysis_results()


def display_analysis_results():
    """Display comprehensive analysis results"""
    
    skill_match = st.session_state.skill_match
    resume_score = st.session_state.resume_score
    
    st.markdown("---")
    
    # Match Score Card
    st.subheader("📊 MATCH SCORE")
    
    match_pct = skill_match['match_percentage']
    score_emoji = "🟢" if match_pct >= 80 else "🟡" if match_pct >= 60 else "🔴"
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Match Score",
            f"{match_pct}% {score_emoji}",
            delta=f"{skill_match['total_matched']}/{skill_match['total_jd_skills']} skills"
        )
    
    with col2:
        st.metric(
            "Resume Strength",
            f"{int(resume_score['total_score'])}/100 {get_score_emoji(resume_score['total_score'])}"
        )
    
    with col3:
        ats_score, _ = calculate_ats_score(st.session_state.resume_text)
        st.metric(
            "ATS Score",
            f"{ats_score}/100"
        )
    
    st.markdown("---")
    
    # Two column layout for skills
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Matched Skills")
        if skill_match['matched_skills']:
            # Categorize matched skills
            categorized = categorize_skills(
                skill_match['matched_skills'],
                st.session_state.skills_db
            )
            
            for category, skills in categorized.items():
                with st.expander(f"📁 {category.replace('_', ' ').title()} ({len(skills)})"):
                    for skill in skills:
                        st.markdown(f"✓ {skill}")
        else:
            st.info("No matched skills found")
    
    with col2:
        st.subheader("❌ Missing Skills")
        if skill_match['missing_skills']:
            # Show missing skills
            for skill in skill_match['missing_skills'][:15]:
                st.markdown(f"• {skill}")
            
            if len(skill_match['missing_skills']) > 15:
                st.info(f"+ {len(skill_match['missing_skills']) - 15} more...")
        else:
            st.success("🎉 You have all required skills!")
    
    st.markdown("---")
    
    # Resume Strength Breakdown
    st.subheader("📈 Resume Strength Breakdown")
    
    # Component scores
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create bar chart
        components = {
            'Semantic Similarity': resume_score['semantic_similarity'],
            'Skill Alignment': resume_score['skill_alignment'],
            'Keyword Density': resume_score['keyword_density'],
            'Experience Relevance': resume_score['experience_relevance'],
            'Formatting': resume_score['formatting_score']
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(components.values()),
                y=list(components.keys()),
                orientation='h',
                marker=dict(
                    color=list(components.values()),
                    colorscale='Viridis',
                    line=dict(width=0)
                ),
                text=[f"{v:.1f}" for v in components.values()],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Score Components",
            xaxis_title="Points",
            yaxis_title="",
            height=300,
            template="plotly_dark",
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Feedback")
        for feedback in resume_score['feedback']:
            st.markdown(f"• {feedback}")
    
    st.markdown("---")
    
    # Visualizations
    st.subheader("📊 Visual Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Skill Match Radar", "Keyword Analysis", "Missing Skills Cloud"])
    
    with tab1:
        # Radar chart for skill categories
        create_skill_radar_chart()
    
    with tab2:
        # Keyword density comparison
        create_keyword_chart()
    
    with tab3:
        # Word cloud of missing skills
        create_missing_skills_wordcloud()


def create_skill_radar_chart():
    """Create radar chart for skill match by category"""
    
    resume_skills = st.session_state.resume_skills
    jd_skills = st.session_state.jd_skills
    skills_db = st.session_state.skills_db
    
    # Categorize both sets
    resume_categorized = categorize_skills(resume_skills, skills_db)
    jd_categorized = categorize_skills(jd_skills, skills_db)
    
    # Get all categories
    all_categories = set(list(resume_categorized.keys()) + list(jd_categorized.keys()))
    
    if not all_categories:
        st.info("No categorized skills to display")
        return
    
    categories = []
    resume_counts = []
    jd_counts = []
    
    for cat in all_categories:
        categories.append(cat.replace('_', ' ').title())
        resume_counts.append(len(resume_categorized.get(cat, [])))
        jd_counts.append(len(jd_categorized.get(cat, [])))
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=jd_counts,
        theta=categories,
        fill='toself',
        name='Job Description',
        line=dict(color='#ef4444')
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=resume_counts,
        theta=categories,
        fill='toself',
        name='Your Resume',
        line=dict(color='#10b981')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max(max(jd_counts), max(resume_counts)) + 1])
        ),
        showlegend=True,
        template="plotly_dark",
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)


def create_keyword_chart():
    """Create keyword density comparison chart"""
    
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        resume_text = st.session_state.resume_text
        jd_text = st.session_state.jd_text
        
        # Extract top keywords
        vectorizer = TfidfVectorizer(max_features=10, stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform([jd_text, resume_text])
        feature_names = vectorizer.get_feature_names_out()
        
        jd_scores = tfidf_matrix[0].toarray()[0]
        resume_scores = tfidf_matrix[1].toarray()[0]
        
        # Create DataFrame
        df = pd.DataFrame({
            'Keyword': feature_names,
            'Job Description': jd_scores,
            'Your Resume': resume_scores
        })
        
        # Sort by JD score
        df = df.sort_values('Job Description', ascending=True)
        
        # Create grouped bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=df['Keyword'],
            x=df['Job Description'],
            name='Job Description',
            orientation='h',
            marker=dict(color='#ef4444')
        ))
        
        fig.add_trace(go.Bar(
            y=df['Keyword'],
            x=df['Your Resume'],
            name='Your Resume',
            orientation='h',
            marker=dict(color='#10b981')
        ))
        
        fig.update_layout(
            title="Top Keywords Comparison (TF-IDF)",
            xaxis_title="Importance Score",
            yaxis_title="Keywords",
            barmode='group',
            template="plotly_dark",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating keyword chart: {str(e)}")


def create_missing_skills_wordcloud():
    """Create word cloud of missing skills"""
    
    missing_skills = st.session_state.skill_match.get('missing_skills', [])
    
    if not missing_skills:
        st.success("🎉 No missing skills! You're well-aligned with the job description.")
        return
    
    try:
        # Create word cloud
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='#0f172a',
            colormap='Reds',
            relative_scaling=0.5,
            min_font_size=10
        ).generate(' '.join(missing_skills))
        
        # Display
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        plt.tight_layout(pad=0)
        
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Error creating word cloud: {str(e)}")


# Section 4: LinkedIn Optimizer
def linkedin_optimizer_section():
    st.header("💼 LinkedIn Profile Optimizer")
    
    if not st.session_state.get('analysis_done', False):
        st.info("👆 Please complete the resume analysis first to generate LinkedIn content.")
        return
    
    resume_text = st.session_state.resume_text
    resume_skills = st.session_state.resume_skills
    jd_text = st.session_state.jd_text
    jd_skills = st.session_state.jd_skills
    
    st.markdown("Generate optimized LinkedIn profile content based on your resume:")
    
    if st.button("✨ Generate LinkedIn Content", type="primary", use_container_width=True):
        with st.spinner("🤖 Crafting your LinkedIn profile..."):
            try:
                # Generate headline (now returns single string)
                headline = generate_headline(resume_text, resume_skills[:5])
                
                # Generate about section
                about = generate_about_section(resume_text, resume_skills, jd_text)
                
                # Get keyword suggestions
                keywords = generate_keyword_suggestions(resume_skills, jd_skills)
                
                # Calculate ATS score
                ats_score, ats_feedback = calculate_ats_score(resume_text)
                
                # Store in session state
                st.session_state.linkedin_content = {
                    'headline': headline,
                    'about': about,
                    'keywords': keywords,
                    'ats_score': ats_score,
                    'ats_feedback': ats_feedback
                }
                
                st.success("✅ LinkedIn content generated!")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
    
    # Display LinkedIn content
    if 'linkedin_content' in st.session_state:
        content = st.session_state.linkedin_content
        
        st.markdown("---")
        
        # Headline
        st.subheader("📝 Optimized Headline")
        
        headline = content['headline']
        
        st.info(f"Character count: {len(headline)}/220")
        
        headline_box = st.text_area(
            "LinkedIn Headline",
            value=headline,
            height=60,
            help="Copy this to your LinkedIn profile"
        )
        
        if st.button("📋 Copy Headline", key="copy_headline"):
            st.success("✅ Headline copied! (Use Ctrl+C to copy from the text box)")
        
        st.markdown("---")
        
        # About Section
        st.subheader("📄 About Section")
        word_count = len(content['about'].split())
        st.info(f"Word count: {word_count}")
        
        about_box = st.text_area(
            "LinkedIn About",
            value=content['about'],
            height=300,
            help="Copy this to your LinkedIn 'About' section"
        )
        
        if st.button("📋 Copy About Section", key="copy_about"):
            st.success("✅ About section copied! (Use Ctrl+C to copy from the text box)")
        
        st.markdown("---")
        
        # Keyword Suggestions
        st.subheader("🔑 Recommended Keywords")
        
        if content['keywords']:
            st.write("Add these keywords to boost your profile visibility:")
            
            cols = st.columns(3)
            for idx, keyword in enumerate(content['keywords'][:12]):
                with cols[idx % 3]:
                    st.markdown(f"• **{keyword}**")
        else:
            st.success("Your resume already covers all key job description keywords!")
        
        st.markdown("---")
        
        # ATS Score
        st.subheader("🤖 ATS Compatibility Score")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("ATS Score", f"{content['ats_score']}/100")
        
        with col2:
            st.markdown("**Feedback:**")
            for feedback in content['ats_feedback']:
                st.markdown(f"• {feedback}")


# Section 5: Downloads
def download_section():
    st.header("📥 Download Results")
    
    if not st.session_state.get('analysis_done', False):
        st.info("Complete the analysis to enable downloads.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Download analysis report
        if st.button("📄 Download Analysis Report", use_container_width=True):
            report = generate_analysis_report()
            st.download_button(
                label="💾 Save Report (TXT)",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        # Download LinkedIn content
        if 'linkedin_content' in st.session_state:
            if st.button("💼 Download LinkedIn Content", use_container_width=True):
                linkedin_text = generate_linkedin_download()
                st.download_button(
                    label="💾 Save LinkedIn Content (TXT)",
                    data=linkedin_text,
                    file_name="linkedin_profile_content.txt",
                    mime="text/plain",
                    use_container_width=True
                )


def generate_analysis_report():
    """Generate text report of analysis"""
    
    skill_match = st.session_state.skill_match
    resume_score = st.session_state.resume_score
    
    report = f"""
AI RESUME ANALYZER - ANALYSIS REPORT
{'='*60}

MATCH ANALYSIS
--------------
Match Score: {skill_match['match_percentage']}%
Matched Skills: {skill_match['total_matched']}/{skill_match['total_jd_skills']}

MATCHED SKILLS ({skill_match['total_matched']}):
{', '.join(skill_match['matched_skills'])}

MISSING SKILLS ({skill_match['total_missing']}):
{', '.join(skill_match['missing_skills'])}

RESUME STRENGTH SCORE
--------------------
Total Score: {int(resume_score['total_score'])}/100

Component Breakdown:
- Semantic Similarity: {resume_score.get('semantic_similarity', 0)}/30
- Skill Alignment: {resume_score.get('skill_alignment', 0)}/25
- Keyword Density: {resume_score.get('keyword_density', 0)}/20
- Experience Relevance: {resume_score.get('experience_relevance', 0)}/15
- Formatting Check: {resume_score.get('formatting_score', 0)}/10

FEEDBACK:
{chr(10).join('- ' + f for f in resume_score['feedback'])}

{'='*60}
Generated by AI Resume Analyzer
"""
    
    return report


def generate_linkedin_download():
    """Generate LinkedIn content for download"""
    
    content = st.session_state.linkedin_content
    
    text = f"""
LINKEDIN PROFILE OPTIMIZATION
{'='*60}

HEADLINE OPTIONS
----------------
Professional: {content.get('headline_options', {}).get('Professional', content['headline'])}
Specialist:   {content.get('headline_options', {}).get('Specialist', '-')}
Impact:       {content.get('headline_options', {}).get('Impact', '-')}

SELECTED HEADLINE ({len(content['headline'])} characters):
{content['headline']}

{'='*60}

ABOUT SECTION:
{content['about']}

{'='*60}

RECOMMENDED KEYWORDS:
{', '.join(content['keywords']) if content['keywords'] else 'All keywords covered!'}

{'='*60}

ATS COMPATIBILITY SCORE: {content['ats_score']}/100

FEEDBACK:
{chr(10).join('- ' + f for f in content['ats_feedback'])}

{'='*60}
Generated by AI Resume Analyzer
"""
    
    return text


# Sidebar
def sidebar():
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/resume.png", width=80)
        st.title("Navigation")
        
        page = st.radio(
            "Go to:",
            ["📤 Upload & Analyze", "💼 LinkedIn Optimizer", "📥 Downloads", "ℹ️ About"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Stats
        if st.session_state.resume_text:
            st.success("✅ Resume uploaded")
        else:
            st.info("📄 No resume uploaded")
        
        if st.session_state.jd_text:
            st.success("✅ JD provided")
        else:
            st.info("💼 No JD provided")
        
        if st.session_state.get('analysis_done'):
            st.success("✅ Analysis complete")
        else:
            st.info("🔍 Analysis pending")
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Start Over", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in ['nlp', 'matcher', 'skills_db']:
                    del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        st.caption("Made with ❤️ using Streamlit & AI")
        
        return page


# Main app
def main():
    # Initialize
    apply_custom_css()
    init_session_state()
    
    # Load skill matcher once
    if st.session_state.nlp is None:
        try:
            nlp, matcher, skills_db = load_skill_matcher()
            st.session_state.nlp = nlp
            st.session_state.matcher = matcher
            st.session_state.skills_db = skills_db
        except Exception as e:
            st.error(f"Failed to initialize AI models: {str(e)}")
            st.stop()
    
    # Header
    show_header()
    
    # Sidebar
    page = sidebar()
    
    # Main content based on page
    if page == "📤 Upload & Analyze":
        resume_text = resume_upload_section()
        
        st.markdown("---")
        
        jd_text = job_description_section()
        
        st.markdown("---")
        
        if resume_text and jd_text:
            analysis_dashboard_section(resume_text, jd_text)
        else:
            if not resume_text:
                st.info("👆 Please upload your resume to begin analysis.")
            if not jd_text:
                st.info("👆 Please enter a job description matched with the resume to begin analysis.")
    
    elif page == "💼 LinkedIn Optimizer":
        linkedin_optimizer_section()
    
    elif page == "📥 Downloads":
        download_section()
    
    elif page == "ℹ️ About":
        st.header("ℹ️ About This App")
        
        st.markdown("""
        ### 🚀 AI Resume Analyzer + LinkedIn Optimizer
        
        A production-ready web application that helps you:
        
        - **📄 Analyze Your Resume**: Upload PDF/DOCX and get instant analysis
        - **🎯 Match with Job Descriptions**: See exactly which skills match and which are missing
        - **📊 Resume Strength Score**: Get a comprehensive 0-100 score across 5 key metrics
        - **💼 LinkedIn Optimization**: Generate optimized headline and About section
        - **🤖 ATS Compatibility**: Check how well your resume works with ATS systems
        - **📈 Visual Analytics**: Interactive charts, radar graphs, and word clouds
        
        ### 🛠️ Technology Stack
        
        - **Frontend**: Streamlit
        - **NLP**: spaCy (en_core_web_sm)
        - **ML**: Scikit-learn (TF-IDF)
        - **Visualization**: Plotly, WordCloud
        - **Document Processing**: PyPDF2, python-docx
        
        ### 📊 Scoring Components
        
        1. **Keyword Density (30pts)**: TF-IDF analysis of top keywords
        2. **Skill Alignment (30pts)**: Percentage of JD skills in resume
        3. **Experience Relevance (20pts)**: Years of experience and job keywords
        4. **Length Optimization (10pts)**: Optimal word count (400-800 words)
        5. **Formatting (10pts)**: Presence of key sections
        
        ### 🎨 Features
        
        - ✅ 500+ Skills Database across 10 categories
        - ✅ Real-time skill extraction
        - ✅ Interactive visualizations
        - ✅ ATS compatibility checking
        - ✅ Grammar checking (optional)
        - ✅ Download reports and LinkedIn content
        - ✅ Professional dark theme
        - ✅ Mobile responsive design
        
        ### 📝 How to Use
        
        1. Upload your resume (PDF or DOCX)
        2. Paste the job description you're applying for
        3. Click "Analyze Resume" to get instant insights
        4. Navigate to LinkedIn Optimizer to generate profile content
        5. Download your analysis report and LinkedIn content
        
        ---
        
        **Version**: 1.0.0  
        **Built with**: ❤️ and AI
        """)


if __name__ == "__main__":
    main()
