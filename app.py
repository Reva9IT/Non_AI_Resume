import streamlit as st
import io
from generators.summary_generator import generate_summary
from generators.docx_generator import generate_docx
from generators.pdf_generator import generate_pdf
from generators.html_generator import generate_html

st.set_page_config(
    page_title="Resume & Portfolio Builder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #0a0a0f;
        color: #e8e8f0;
    }

    .main-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
    }

    .main-header h1 {
        font-family: 'Syne', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .main-header p {
        color: #8b8ba7;
        font-size: 1.1rem;
        font-weight: 300;
    }

    .section-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
    }

    .section-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #a78bfa;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .stTextInput > label, .stTextArea > label {
        color: #9999b3 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #e8e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 2px rgba(167,139,250,0.2) !important;
    }

    .stTextArea > div > div > textarea {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        color: #e8e8f0 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stTextArea > div > div > textarea:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 2px rgba(167,139,250,0.2) !important;
    }

    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #7c3aed, #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.9rem 2rem;
        font-family: 'Syne', sans-serif;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.05em;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 1.5rem 0;
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #6d28d9, #1d4ed8);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124,58,237,0.4);
    }

    .download-section {
        background: rgba(167,139,250,0.05);
        border: 1px solid rgba(167,139,250,0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    .download-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.1rem;
        font-weight: 700;
        color: #a78bfa;
        margin-bottom: 1rem;
        text-align: center;
    }

    .stDownloadButton > button {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 10px !important;
        color: #e8e8f0 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(167,139,250,0.15) !important;
        border-color: #a78bfa !important;
        transform: translateY(-1px) !important;
    }

    .preview-box {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
        font-size: 0.92rem;
        color: #b0b0cc;
        line-height: 1.7;
        font-style: italic;
    }

    .success-banner {
        background: linear-gradient(135deg, rgba(52,211,153,0.1), rgba(96,165,250,0.1));
        border: 1px solid rgba(52,211,153,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        color: #34d399;
        font-weight: 600;
        font-family: 'Syne', sans-serif;
        margin-bottom: 1rem;
    }

    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>Resume & Portfolio Builder</h1>
    <p>Fill in your details → Generate professional resume & portfolio instantly</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── FORM ───────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2], gap="large")

with col_left:
    # Personal Info
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👤 Personal Information</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        full_name = st.text_input("Full Name", placeholder="e.g. Aditya Sharma")
        email = st.text_input("Email", placeholder="aditya@email.com")
        linkedin = st.text_input("LinkedIn URL", placeholder="linkedin.com/in/aditya")
        personal_website = st.text_input("Personal Website", placeholder="adityasharma.dev")
    with c2:
        professional_title = st.text_input("Professional Title", placeholder="e.g. Full Stack Developer")
        phone = st.text_input("Phone", placeholder="+91 98765 43210")
        github = st.text_input("GitHub URL", placeholder="github.com/aditya")
    st.markdown('</div>', unsafe_allow_html=True)

    # Skills
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">⚡ Skills</div>', unsafe_allow_html=True)
    skills = st.text_area(
        "Skills (comma-separated)",
        placeholder="Python, React, Node.js, PostgreSQL, Docker, AWS, Machine Learning",
        height=80
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Experience
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💼 Work Experience</div>', unsafe_allow_html=True)
    experience = st.text_area(
        "Experience (one entry per line)",
        placeholder="Software Engineer at TCS (2022–Present) – Built microservices handling 1M+ requests/day\nIntern at Infosys (2021) – Developed REST APIs using Python and FastAPI",
        height=130
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Projects
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🚀 Projects</div>', unsafe_allow_html=True)
    projects = st.text_area(
        "Projects (one entry per line)",
        placeholder="AI Chatbot – Built using Python & LangChain, deployed on AWS Lambda\nE-commerce Platform – React + Node.js + MongoDB, 500+ users",
        height=130
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Education & Achievements
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🎓 Education</div>', unsafe_allow_html=True)
        education = st.text_area(
            "Education",
            placeholder="B.Tech in Computer Science\nMumbai University, 2018–2022\nCGPA: 8.7/10",
            height=110
        )
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🏆 Achievements</div>', unsafe_allow_html=True)
        achievements = st.text_area(
            "Achievements",
            placeholder="Winner – Smart India Hackathon 2022\nGoogle Cloud Certified Professional\nPublished 2 research papers",
            height=110
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Generate Button
    generate_clicked = st.button("🚀 Generate Resume & Portfolio", use_container_width=True)

# ─── RIGHT PANEL ─────────────────────────────────────────────────────────────
with col_right:
    st.markdown("### 📋 Preview & Downloads")

    if generate_clicked:
        if not full_name.strip():
            st.error("⚠️ Please enter your Full Name to continue.")
        else:
            with st.spinner("Generating your resume & portfolio..."):
                data = {
                    "full_name": full_name.strip(),
                    "professional_title": professional_title.strip() or "Professional",
                    "email": email.strip(),
                    "phone": phone.strip(),
                    "linkedin": linkedin.strip(),
                    "github": github.strip(),
                    "personal_website": personal_website.strip(),
                    "skills": [s.strip() for s in skills.split(",") if s.strip()],
                    "education": education.strip(),
                    "experience": [e.strip() for e in experience.split("\n") if e.strip()],
                    "projects": [p.strip() for p in projects.split("\n") if p.strip()],
                    "achievements": achievements.strip(),
                }

                # Generate summary
                data["summary"] = generate_summary(data)

                # Generate files
                docx_bytes = generate_docx(data)
                pdf_bytes = generate_pdf(data)
                html_bytes = generate_html(data)

            st.markdown('<div class="success-banner">✅ Files generated successfully!</div>', unsafe_allow_html=True)

            # Summary preview
            st.markdown("**📝 Generated Summary:**")
            st.markdown(f'<div class="preview-box">{data["summary"]}</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

            st.markdown('<div class="download-section">', unsafe_allow_html=True)
            st.markdown('<div class="download-title">⬇️ Download Your Files</div>', unsafe_allow_html=True)

            st.download_button(
                label="📄 Download DOCX Resume",
                data=docx_bytes,
                file_name=f"{full_name.replace(' ', '_')}_Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.download_button(
                label="📕 Download PDF Resume",
                data=pdf_bytes,
                file_name=f"{full_name.replace(' ', '_')}_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.download_button(
                label="🌐 Download Portfolio HTML",
                data=html_bytes,
                file_name=f"{full_name.replace(' ', '_')}_Portfolio.html",
                mime="text/html",
                use_container_width=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:2rem; text-align:center; color:#5a5a7a;">
            <div style="font-size:3rem; margin-bottom:1rem;">📝</div>
            <div style="font-family:'Syne',sans-serif; font-weight:600; color:#7070a0; margin-bottom:0.5rem;">
                Fill in your details on the left
            </div>
            <div style="font-size:0.9rem; line-height:1.6;">
                Your resume preview and download buttons will appear here after you click Generate.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Tips
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.82rem; color:#5a5a7a; line-height:1.8;">
        <b style="color:#8080a0;">💡 Tips for best results:</b><br>
        • List skills separated by commas<br>
        • Each experience/project on its own line<br>
        • Include numbers & impact in your entries<br>
        • Portfolio HTML works as a standalone file
    </div>
    """, unsafe_allow_html=True)
