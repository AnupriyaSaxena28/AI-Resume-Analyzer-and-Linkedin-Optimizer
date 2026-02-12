# 🚀 AI Resume Analyzer + LinkedIn Optimizer

A **production-ready** Streamlit web application that analyzes resumes against job descriptions, provides comprehensive skill matching insights, calculates resume strength scores, and generates optimized LinkedIn profile content—all powered by AI and NLP.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-red)
![spaCy](https://img.shields.io/badge/spaCy-3.7.2-green)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## ✨ Features

### 📄 Resume Analysis
- **Upload PDF/DOCX resumes** with automatic text extraction
- **Extract clean, readable text** using PyPDF2 and python-docx
- **Real-time preview** of extracted content with word count and reading time

### 🎯 AI-Powered Skill Matching
- **500+ skills database** across 10 categories (Programming, Data, ML/AI, Cloud, etc.)
- **Intelligent n-gram matching** using spaCy PhraseMatcher
- **Categorized skill breakdown** showing matched and missing skills
- **Match percentage calculation** with visual indicators

### 📊 Comprehensive Scoring (0-100)
Resume strength score calculated across 5 components:
- **Keyword Density (30pts)**: TF-IDF analysis of top keywords
- **Skill Alignment (30pts)**: Percentage of JD skills found in resume
- **Experience Relevance (20pts)**: Years of experience and job keywords
- **Length Optimization (10pts)**: Optimal word count (400-800 words)
- **Formatting Score (10pts)**: Presence of key sections

### 💼 LinkedIn Profile Optimizer
- **Generate optimized headline** (120 characters)
- **Create compelling About section** (200-300 words)
- **Keyword suggestions** for profile visibility
- **ATS compatibility score** (0-100)

### 📈 Interactive Visualizations
- **Skill match radar chart** comparing resume vs job description
- **Keyword density bar graph** showing TF-IDF scores
- **Missing skills word cloud** for visual impact
- **Component breakdown charts** with Plotly

### 📥 Export & Download
- Download complete analysis report (TXT)
- Download LinkedIn profile content (TXT)
- Copy-paste ready optimization content

### 🎨 Premium UI/UX
- **Professional dark theme** (#1e3a8a, #3b82f6)
- **Real-time progress indicators** and loading spinners
- **Mobile-responsive design**
- **Intuitive sidebar navigation**
- **Clean card-based layout**

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Streamlit 1.31.0 |
| **NLP Engine** | spaCy 3.7.2 (en_core_web_sm) |
| **ML/Analysis** | Scikit-learn (TF-IDF) |
| **PDF Processing** | PyPDF2 3.0.1 |
| **DOCX Processing** | python-docx 1.1.0 |
| **Visualization** | Plotly 5.18.0, WordCloud 1.9.3 |
| **Grammar Check** | language-tool-python 2.8.1 |
| **Data Handling** | Pandas 2.2.0, NumPy 1.26.3 |

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

---

## 🚀 Quick Start - Local Installation

### 1. Clone or Download This Repository

```bash
cd d:/projects/AIResumeAnalyzer
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🌐 Deployment Guide

### Deploy to Streamlit Cloud (Recommended - FREE)

Streamlit Cloud offers **free hosting** for public apps with one-click deployment.

#### Steps:

1. **Push code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Sign up** at [share.streamlit.io](https://share.streamlit.io)

3. **Click "New app"**

4. **Select your repository** and branch

5. **Set main file path**: `app.py`

6. **Click "Deploy"**

✅ Your app will be live at `https://your-app-name.streamlit.app`

#### Important Notes:
- The spaCy model will be auto-installed from `requirements.txt`
- First deployment may take 3-5 minutes
- Free tier includes: Unlimited viewers, 1 GB RAM, Community support

---

### Deploy to Render (Alternative)

Render offers a free tier with Docker support.

#### Steps:

1. **Create `render.yaml`** in project root:

```yaml
services:
  - type: web
    name: ai-resume-analyzer
    env: python
    buildCommand: "pip install -r requirements.txt && python -m spacy download en_core_web_sm"
    startCommand: "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
    plan: free
```

2. **Push to GitHub**

3. **Connect repository** at [render.com](https://render.com)

4. **Select "New Web Service"**

5. **Choose your repository**

6. **Render will auto-detect** the `render.yaml` and deploy

---

### Deploy to Heroku

1. **Create `Procfile`**:
```
web: streamlit run app.py --server.port $PORT
```

2. **Create `setup.sh`**:
```bash
mkdir -p ~/.streamlit/
echo "[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml
```

3. **Deploy**:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

---

## 📖 How to Use

### Step 1: Upload Resume
1. Navigate to **"📤 Upload & Analyze"** section
2. Click the file uploader and select your resume (PDF or DOCX)
3. Wait for text extraction to complete
4. Review the preview and statistics

### Step 2: Enter Job Description
1. Scroll to the **"💼 Enter Job Description"** section
2. Paste the complete job description you're applying for
3. Optionally preview extracted skills in real-time

### Step 3: Analyze
1. Click **"⚡ Analyze Resume"** button
2. Wait for AI analysis to complete (10-20 seconds)
3. Review your results:
   - **Match Score**: Overall skill alignment percentage
   - **Resume Strength**: 0-100 score with component breakdown
   - **ATS Score**: Applicant Tracking System compatibility
   - **Matched Skills**: Skills you have that align with JD
   - **Missing Skills**: Skills to add to improve match

### Step 4: View Visualizations
Explore the three interactive tabs:
- **Skill Match Radar**: Category-wise comparison
- **Keyword Analysis**: TF-IDF keyword density comparison
- **Missing Skills Cloud**: Visual representation of gaps

### Step 5: Generate LinkedIn Content
1. Navigate to **"💼 LinkedIn Optimizer"** in the sidebar
2. Click **"✨ Generate LinkedIn Content"**
3. Copy generated content:
   - **Headline**: Optimized 120-character headline
   - **About Section**: 200-300 word professional summary
   - **Keywords**: Recommended skills to add
   - **ATS Feedback**: Actionable improvement tips

### Step 6: Download Reports
1. Go to **"📥 Downloads"** section
2. Download analysis report as TXT file
3. Download LinkedIn content for future reference

---

## 🎯 Scoring Methodology

### Resume Strength Score (0-100)

| Component | Max Points | Criteria |
|-----------|-----------|----------|
| **Keyword Density** | 30 | TF-IDF analysis of top 10 keywords from JD |
| **Skill Alignment** | 30 | Percentage of JD skills found in resume |
| **Experience Relevance** | 20 | Years mentioned, action verbs, job keywords |
| **Length Optimization** | 10 | Optimal: 400-800 words |
| **Formatting** | 10 | Presence of Education, Experience, Skills sections |

### Match Score Interpretation

- 🟢 **80-100%**: Excellent match - Apply with confidence!
- 🟡 **60-79%**: Good match - Add a few missing skills
- 🔴 **0-59%**: Needs improvement - Focus on missing skills

### ATS Compatibility Score

- ✅ **90-100**: ATS-friendly, excellent formatting
- ⚠️ **70-89**: Good, minor improvements possible
- ❌ **0-69**: May have issues, simplify formatting

---

## 📂 Project Structure

```
AIResumeAnalyzer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .streamlit/
│   └── config.toml                # Streamlit configuration (dark theme)
├── data/
│   └── skills_database.json       # 500+ skills across 10 categories
└── utils/
    ├── __init__.py                # Package initializer
    ├── text_extraction.py         # PDF/DOCX text extraction
    ├── skill_matcher.py           # spaCy-based skill extraction
    ├── scoring_engine.py          # Resume strength scoring (TF-IDF)
    └── linkedin_generator.py      # LinkedIn content generation
```

---

## 🔧 Troubleshooting

### Issue: spaCy model not found

**Solution**:
```bash
python -m spacy download en_core_web_sm
```

### Issue: PDF extraction fails

**Possible causes**:
- Corrupted PDF file
- Password-protected PDF
- Scanned PDF (image-based, not text)

**Solution**: Try converting to DOCX or use a text-based PDF

### Issue: Slow performance

**Solutions**:
- Close other applications to free up RAM
- Use shorter job descriptions
- Ensure Python 3.8+ is installed

### Issue: Streamlit not opening in browser

**Solution**:
```bash
streamlit run app.py --server.port 8502
```
Then manually navigate to `http://localhost:8502`

---

## 🎨 Customization

### Change Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#YOUR_COLOR"        # Accent color
backgroundColor = "#YOUR_COLOR"      # Main background
secondaryBackgroundColor = "#YOUR_COLOR"  # Card backgrounds
textColor = "#YOUR_COLOR"            # Text color
```

### Add More Skills

Edit `data/skills_database.json`:

```json
{
  "your_category": [
    "Skill 1",
    "Skill 2",
    "Skill 3"
  ]
}
```

### Modify Scoring Weights

Edit `utils/scoring_engine.py` and adjust `max_score` parameters in each function.

---

## 📊 Sample Output

```
🔍 ANALYSIS RESULTS

📊 MATCH SCORE: 82% ⭐⭐⭐⭐
✅ MATCHED SKILLS (9/12)
• Python ✓
• SQL ✓
• Data Analysis ✓
• Machine Learning ✓
• AWS ✓
• Docker ✓
• Git ✓
• Pandas ✓
• Tableau ✓

❌ MISSING SKILLS (3/12)
• Power BI ❌
• Kubernetes ❌
• Spark ❌

📈 RESUME STRENGTH: 87/100
Keyword Density: 28/30 ✓
Skill Alignment: 26/30 ✓
Experience: 18/20 ✓
Length: 8/10 ✓
Formatting: 7/10 ✓

🔗 LINKEDIN OPTIMIZATION
Headline: "Data Scientist | Python, ML, SQL | MS Data Science"
About: "Passionate Data Scientist with 3+ years of experience..."
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgments

- **Streamlit** for the amazing web framework
- **spaCy** for powerful NLP capabilities
- **Scikit-learn** for TF-IDF implementation
- **Plotly** for interactive visualizations

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [How to Use](#-how-to-use) guide
3. Open an issue on GitHub

---

## 🌟 Star This Project

If you find this helpful, please give it a ⭐ on GitHub!

---

**Made with ❤️ using Streamlit, spaCy, and AI**

**Version**: 1.0.0  
**Last Updated**: February 2026
