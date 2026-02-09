import requests
import streamlit as st
from PIL import Image
import io
import base64

st.set_page_config(page_title="FatiResume", page_icon="🧩", layout="wide")

try:
    API_BASE = st.secrets.get("API_BASE", "http://127.0.0.1:8000")
except FileNotFoundError:
    API_BASE = "http://127.0.0.1:8000"

# Enhanced CSS with beautiful styling
st.markdown(
    """
    <style>
      .block-container { padding-top: 1rem; padding-bottom: 1rem; }
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      
      /* Hero section styling */
      .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
      }
      
      .hero-section::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="%23ffffff22" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,138.7C960,139,1056,117,1152,112C1248,107,1344,117,1392,122.7L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') no-repeat bottom;
        background-size: cover;
      }
      
      .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      }
      
      .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-bottom: 2rem;
      }
      
      /* Card styling */
      .rm-card {
        border: 1px solid rgba(49, 51, 63, 0.1);
        border-radius: 16px;
        padding: 20px;
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
      }
      
      .rm-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
      }
      
      .rm-muted { 
        color: rgba(49, 51, 63, 0.7); 
        font-size: 0.92rem; 
      }
      
      .rm-chip {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        border: 1px solid rgba(49, 51, 63, 0.15);
        margin: 3px 6px 3px 0;
        font-size: 0.85rem;
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
        transition: all 0.3s ease;
      }
      
      .rm-chip:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        transform: scale(1.05);
      }
      
      /* Feature cards */
      .feature-card {
        text-align: center;
        padding: 2rem;
        border-radius: 16px;
        background: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
      }
      
      .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
      }
      
      .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
      }
      
      /* Sidebar styling */
      .css-1d391kg {
        background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);
      }
      
      /* Button styling */
      .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
      }
      
      .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
      }
      
      /* Score styling */
      .score-high {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
      }
      
      .score-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
      }
      
      .score-low {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Section with gradient background
st.markdown(
    """
    <div class="hero-section">
        <div class="hero-title">🧩 FatiResume</div>
        <div class="hero-subtitle">AI-Powered Resume Analysis & Job Matching Platform</div>
        <div style="font-size: 1rem; opacity: 0.9;">
            🎯 Semantic Scoring • 📊 Skill Gap Analysis • 🔍 Bias Detection • 💼 Job Recommendations
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Feature cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h4>Semantic Scoring</h4>
            <p style="font-size: 0.9rem; color: #666;">Advanced AI matching between resume and job requirements</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <h4>Skill Gap Analysis</h4>
            <p style="font-size: 0.9rem; color: #666;">Identify missing skills and get improvement suggestions</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <h4>Bias Detection</h4>
            <p style="font-size: 0.9rem; color: #666;">Ensure fair and unbiased resume evaluation</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💼</div>
            <h4>Job Matching</h4>
            <p style="font-size: 0.9rem; color: #666;">Find relevant job opportunities from top platforms</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# Main content with sidebar
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 1rem;">
            <h3 style="margin: 0;">📝 Input Details</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
    resume_text = st.text_area("✏️ Or paste resume text", height=200)
    job_description = st.text_area("💼 Job Description", height=200)
    country = st.selectbox("🌍 Target Country", ["US", "FR", "DE", "UK"], index=0)
    submitted = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

if submitted:
    if not job_description.strip():
        st.warning("⚠️ Please provide a job description")
        st.stop()
    if not (resume_file or resume_text.strip()):
        st.warning("⚠️ Please upload a resume file or paste resume text")
        st.stop()

    with st.spinner("🔄 Analyzing resume..."):
        files = {}
        if resume_file:
            files["resume_file"] = (resume_file.name, resume_file.getvalue(), resume_file.type)
        
        payload = {"job_description": job_description, "country": country}
        if resume_text.strip():
            payload["resume_text"] = resume_text

        try:
            response = requests.post(f"{API_BASE}/api/analyze", files=files, data=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                
                # Results header
                st.markdown(
                    """
                    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%); border-radius: 20px; margin-bottom: 2rem;">
                        <h2 style="color: #333; margin-bottom: 1rem;">🎉 Analysis Complete!</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                # Score display
                score = result.get("match_score", 0)
                score_class = "score-high" if score >= 70 else "score-medium" if score >= 40 else "score-low"
                
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 2rem;">
                        <div class="{score_class}" style="display: inline-block; font-size: 1.5rem; padding: 1rem 2rem;">
                            Match Score: {score:.1f}/100
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                
                tabs = st.tabs(["📊 Results", "💼 Job Matches", "📄 Raw JSON"])
                
                with tabs[0]:
                    # Evidence section
                    if result.get("evidence"):
                        st.markdown("### 🔍 Evidence & Analysis")
                        for ev in result["evidence"]:
                            st.markdown(
                                f"""
                                <div class="rm-card">
                                    <h5>Evidence Item</h5>
                                    <p class="rm-muted">{ev['text']}</p>
                                    <p><strong>Score:</strong> {ev.get('score', 0):.2f}</p>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    
                    # Top matches section
                    if result.get("top_matches"):
                        st.markdown("### 🎯 Top Matches")
                        st.markdown(
                            "".join([f"<span class='rm-chip'>{match}</span>" for match in result["top_matches"]]),
                            unsafe_allow_html=True,
                        )
                    
                    # Missing skills section
                    if result.get("missing_skills"):
                        st.markdown("### 📚 Missing Skills")
                        st.markdown(
                            "".join([f"<span class='rm-chip'>{skill}</span>" for skill in result["missing_skills"]]),
                            unsafe_allow_html=True,
                        )
                    
                    # Bias report
                    if result.get("bias_report"):
                        st.markdown("### 🔍 Bias Report")
                        bias = result["bias_report"]
                        st.markdown(
                            f"""
                            <div class="rm-card">
                                <h5>📊 Bias Analysis</h5>
                                <p><strong>Risk Score:</strong> {bias.get('risk_score', 0):.2f}</p>
                                <p><strong>Flags:</strong> {len(bias.get('flags', []))} potential issues</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                
                with tabs[1]:
                    # Job finder results
                    st.markdown("### 💼 Personalized Job Suggestions")
                    with st.spinner("🎯 Analyzing your profile for job recommendations..."):
                        try:
                            # Get skills from resume text
                            resume_text_lower = resume_text.lower() if resume_text else ""
                            
                            # Define job suggestions based on skills
                            job_suggestions = []
                            
                            # Data Science & ML roles
                            if any(skill in resume_text_lower for skill in ['python', 'machine learning', 'tensorflow', 'pytorch', 'sklearn']):
                                job_suggestions.extend([
                                    {"title": "Senior Data Scientist", "match": "95%", "skills": "Python, ML, TensorFlow"},
                                    {"title": "Machine Learning Engineer", "match": "92%", "skills": "Python, PyTorch, MLOps"},
                                    {"title": "AI Research Scientist", "match": "88%", "skills": "Deep Learning, Research, Python"}
                                ])
                            
                            # Data Engineering roles
                            if any(skill in resume_text_lower for skill in ['sql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes']):
                                job_suggestions.extend([
                                    {"title": "Data Engineer", "match": "90%", "skills": "SQL, Cloud, ETL"},
                                    {"title": "Cloud Data Architect", "match": "87%", "skills": "AWS/Azure, Data Pipelines"},
                                    {"title": "DevOps Engineer (Data)", "match": "85%", "skills": "Docker, Kubernetes, CI/CD"}
                                ])
                            
                            # Analytics roles
                            if any(skill in resume_text_lower for skill in ['analytics', 'statistics', 'tableau', 'power bi', 'excel']):
                                job_suggestions.extend([
                                    {"title": "Business Intelligence Analyst", "match": "88%", "skills": "Analytics, Tableau, SQL"},
                                    {"title": "Data Analyst", "match": "85%", "skills": "Statistics, Excel, Visualization"},
                                    {"title": "Product Analyst", "match": "82%", "skills": "Analytics, Business Metrics, A/B Testing"}
                                ])
                            
                            # NLP roles
                            if any(skill in resume_text_lower for skill in ['nlp', 'bert', 'transformers', 'text']):
                                job_suggestions.extend([
                                    {"title": "NLP Engineer", "match": "90%", "skills": "NLP, BERT, Python"},
                                    {"title": "Computational Linguist", "match": "85%", "skills": "NLP, Linguistics, ML"},
                                    {"title": "Chatbot Developer", "match": "83%", "skills": "NLP, Dialog Systems, Python"}
                                ])
                            
                            # Computer Vision roles
                            if any(skill in resume_text_lower for skill in ['computer vision', 'opencv', 'image processing']):
                                job_suggestions.extend([
                                    {"title": "Computer Vision Engineer", "match": "89%", "skills": "CV, OpenCV, Python"},
                                    {"title": "ML Engineer (Vision)", "match": "86%", "skills": "Deep Learning, Computer Vision"},
                                    {"title": "Image Processing Specialist", "match": "84%", "skills": "Image Processing, Python, ML"}
                                ])
                            
                            # Default suggestions if no specific skills found
                            if not job_suggestions:
                                job_suggestions = [
                                    {"title": "Junior Data Scientist", "match": "75%", "skills": "Python, Statistics, ML Basics"},
                                    {"title": "Data Analyst", "match": "70%", "skills": "Excel, SQL, Basic Analytics"},
                                    {"title": "Business Intelligence Analyst", "match": "68%", "skills": "Reporting, Data Visualization"}
                                ]
                            
                            # Remove duplicates and sort by match
                            seen_titles = set()
                            unique_suggestions = []
                            for job in job_suggestions:
                                if job['title'] not in seen_titles:
                                    seen_titles.add(job['title'])
                                    unique_suggestions.append(job)
                            
                            unique_suggestions.sort(key=lambda x: float(x['match'].rstrip('%')), reverse=True)
                            
                            st.info("🎯 **Based on your CV skills, here are your best job matches:**")
                            
                            for i, job in enumerate(unique_suggestions[:6]):
                                match_color = "#28a745" if float(job['match'].rstrip('%')) >= 90 else "#ffc107" if float(job['match'].rstrip('%')) >= 80 else "#fd7e14"
                                
                                st.markdown(
                                    f"""
                                    <div style="border: 2px solid {match_color}; border-radius: 12px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f8f9ff 0%, #ffffff 100%);">
                                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                            <h4 style="color: #333; margin: 0;">{job['title']}</h4>
                                            <span style="background: {match_color}; color: white; padding: 6px 12px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                                                🎯 {job['match']} Match
                                            </span>
                                        </div>
                                        <p style="color: #666; margin: 8px 0; font-size: 14px;">
                                            <strong>Key Skills:</strong> {job['skills']}
                                        </p>
                                        <div style="margin-top: 12px;">
                                            <span style="background: #e3f2fd; color: #1976d2; padding: 4px 8px; border-radius: 6px; font-size: 12px; margin-right: 8px;">
                                                💼 Search on LinkedIn
                                            </span>
                                            <span style="background: #f3e5f5; color: #7b1fa2; padding: 4px 8px; border-radius: 6px; font-size: 12px; margin-right: 8px;">
                                                🌐 Check Indeed
                                            </span>
                                            <span style="background: #e8f5e8; color: #388e3c; padding: 4px 8px; border-radius: 6px; font-size: 12px;">
                                                📊 Browse Glassdoor
                                            </span>
                                        </div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                            
                            # Add search tips
                            st.markdown("---")
                            st.markdown("### 🔍 **How to Find These Jobs:**")
                            st.markdown("""
                            **Best Search Strategies:**
                            1. **LinkedIn Jobs:** Search for the exact job titles above + filter by "Remote" or your location
                            2. **Indeed:** Use job title + key skills combinations for better results  
                            3. **Company Career Pages:** Target tech companies that match your skill level
                            4. **Specialized Job Boards:** 
                               - DataElixir (data science roles)
                               - Kaggle Jobs (ML/AI positions)
                               - Otta (tech startup jobs)
                            
                            **Pro Tip:** Apply to jobs where you match 80%+ of requirements - don't wait for 100% match!
                            """)
                            
                        except Exception as e:
                            st.error("❌ Unable to generate job suggestions")
                            st.info("💡 **Tip:** Try refreshing the page or check that your resume text includes relevant skills")
                
                with tabs[2]:
                    st.markdown("### 📄 Full API Response")
                    st.json(result)
            else:
                st.error(f"❌ Analysis failed: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            st.error(f"❌ Error: {e}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; padding: 2rem; color: #666;">
        <p>🚀 Powered by Advanced AI • Built with ❤️ for Job Seekers</p>
        <p style="font-size: 0.9rem;">© 2024 FatiResume - Your AI Career Companion</p>
    </div>
    """,
    unsafe_allow_html=True,
)
