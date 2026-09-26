
import os
import re
import streamlit as st
import numpy as np
import faiss
import torch

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 CareerAI")
st.subheader("AI Career Guidance, Skill-Gap Analysis & Personalized Roadmap")

st.write(
    "Upload a resume and select a target career. CareerAI analyzes your "
    "background, identifies existing skills and skill gaps, and generates "
    "a personalized learning roadmap."
)

st.divider()


# ============================================================
# PATHS
# ============================================================

PROJECT_PATH = "."
KNOWLEDGE_PATH = "."


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

documents_text = []
document_names = []

for filename in os.listdir(KNOWLEDGE_PATH):
    if filename.endswith(".txt"):
        file_path = os.path.join(KNOWLEDGE_PATH, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        documents_text.append(text)
        document_names.append(filename)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


embedding_model = load_embedding_model()


# ============================================================
# LOAD FAISS INDEX
# ============================================================

index_path = os.path.join(KNOWLEDGE_PATH, "career_index.faiss")

index = faiss.read_index(index_path)


# ============================================================
# LOAD LLM
# ============================================================

@st.cache_resource


    def load_llm():
    return None


# ============================================================
# PDF TEXT EXTRACTION
# ============================================================

def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


# ============================================================
# PROFILE EXTRACTION
# ============================================================

def extract_candidate_profile(resume_text):

    text = resume_text.lower()

    skill_categories = {

        "Programming & Technology": [
            "python", "java", "c++", "c", "javascript",
            "html", "css", "sql", "git", "docker", "api"
        ],

        "AI & Machine Learning": [
            "machine learning", "deep learning",
            "neural networks", "natural language processing",
            "nlp", "bert", "transformers",
            "tensorflow", "pytorch", "computer vision"
        ],

        "Data": [
            "data science", "data analysis", "pandas",
            "numpy", "statistics", "data visualization",
            "excel", "power bi", "tableau"
        ],

        "Business & Commerce": [
            "accounting", "finance", "financial analysis",
            "business analysis", "marketing", "sales", "economics"
        ],

        "Legal": [
            "legal research", "contract", "contracts",
            "litigation", "compliance", "legal writing",
            "case analysis"
        ],

        "Communication & Professional": [
            "communication", "leadership", "teamwork",
            "problem solving", "research", "writing",
            "presentation", "project management"
        ]
    }

    profile = {
        "education": [],
        "skills": {},
        "projects": [],
        "career_interests": []
    }

    education_patterns = [
        r"\bb\.?tech\b",
        r"\bb\.?e\b",
        r"\bb\.?sc\b",
        r"\bb\.?com\b",
        r"\bb\.?a\b",
        r"\bm\.?tech\b",
        r"\bm\.?sc\b",
        r"\bm\.?com\b",
        r"\bmba\b",
        r"\bllb\b",
        r"\bllm\b",
        r"\bphd\b"
    ]

    education_found = set()

    for pattern in education_patterns:

        matches = re.findall(pattern, text)

        for match in matches:

            normalized = re.sub(r"\\s+", "", match.lower())

            if normalized in ["b.tech", "btech"]:
                education_found.add("B.TECH")
            elif normalized in ["m.tech", "mtech"]:
                education_found.add("M.TECH")
            elif normalized in ["b.sc", "bsc"]:
                education_found.add("B.SC")
            elif normalized in ["m.sc", "msc"]:
                education_found.add("M.SC")
            elif normalized in ["b.com", "bcom"]:
                education_found.add("B.COM")
            elif normalized in ["m.com", "mcom"]:
                education_found.add("M.COM")
            elif normalized == "mba":
                education_found.add("MBA")
            elif normalized == "llb":
                education_found.add("LLB")
            elif normalized == "llm":
                education_found.add("LLM")
            elif normalized == "phd":
                education_found.add("PHD")
            elif normalized in ["b.e", "be"]:
                education_found.add("B.E")
            elif normalized in ["b.a", "ba"]:
                education_found.add("B.A")

    profile["education"] = sorted(education_found)

    for category, skills in skill_categories.items():

        found = []

        for skill in skills:

            if skill.lower() in text:
                found.append(skill)

        if found:
            profile["skills"][category] = found

    project_section = re.search(
        r"projects?(.*?)(career interest|current level|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if project_section:

        project_text = project_section.group(1).strip()

        for line in project_text.split("\n"):

            line = line.strip()

            if line:
                profile["projects"].append(line)

    interest_section = re.search(
        r"career interest[s]?(.*?)(current level|$)",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if interest_section:

        interests = interest_section.group(1)

        for line in interests.split("\n"):

            line = line.strip()

            if line:
                profile["career_interests"].append(line)

    return profile


# ============================================================
# CAREER SKILL REQUIREMENTS
# ============================================================

career_skill_requirements = {

    "AI/ML Engineer": [
        "python",
        "machine learning",
        "deep learning",
        "neural networks",
        "nlp",
        "transformers",
        "statistics",
        "data processing",
        "model evaluation",
        "api",
        "deployment",
        "git",
        "docker"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "statistics",
        "probability",
        "data analysis",
        "machine learning",
        "pandas",
        "numpy",
        "data visualization"
    ],

    "Data Analyst": [
        "sql",
        "excel",
        "python",
        "data cleaning",
        "statistics",
        "power bi",
        "tableau",
        "data visualization",
        "business analysis"
    ],

    "Software Engineer": [
        "c++",
        "java",
        "python",
        "data structures",
        "algorithms",
        "object-oriented programming",
        "sql",
        "git",
        "software development"
    ]
}


# ============================================================
# SEMANTIC SEARCH
# ============================================================

def search_career_knowledge(query, top_k=2):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    ).astype("float32")

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, idx in zip(
        distances[0],
        indices[0]
    ):

        results.append({
            "document": document_names[idx],
            "distance": float(distance),
            "content": documents_text[idx]
        })

    return results


# ============================================================
# LLM RESPONSE
# ============================================================

    ]

    formatted_prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        

    with torch.no_grad()
def generate_ai_response(prompt, max_new_tokens=600):
    return """
### 🤖 CareerAI Guidance

Based on the resume analysis and career knowledge, CareerAI has identified
the candidate's current profile, relevant skills, and areas for improvement.

### Recommended Approach

1. Strengthen the missing or weak skills.
2. Build 2–3 practical projects demonstrating those skills.
3. Practice interview questions related to the target career.
4. Progress from basic concepts to advanced concepts.
5. Keep your resume and GitHub portfolio updated.

### Important

This guidance is generated from the candidate profile and CareerAI
knowledge base. It is educational guidance and is not a guaranteed
career outcome.
"""

    

    


# ============================================================
# USER INTERFACE
# ============================================================

st.header("📄 Step 1 — Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)


if uploaded_file:

    resume_text = extract_text_from_pdf(uploaded_file)

    candidate_profile = extract_candidate_profile(resume_text)

    st.success("✅ Resume successfully analyzed.")

    st.divider()

    st.header("🎯 Step 2 — Select Target Career")

    target_career = st.selectbox(
        "Which career do you want to analyze?",
        list(career_skill_requirements.keys())
    )

    if st.button(
        "🚀 Analyze My Career",
        type="primary"
    ):

        # ----------------------------------------------------
        # Candidate skills
        # ----------------------------------------------------

        candidate_skills = set()

        for category, skills in candidate_profile["skills"].items():

            for skill in skills:

                candidate_skills.add(skill.lower())


        # ----------------------------------------------------
        # Skill gap analysis
        # ----------------------------------------------------

        requirements = career_skill_requirements[target_career]

        matched = []

        missing = []

        for required_skill in requirements:

            if required_skill in candidate_skills:
                matched.append(required_skill)

            else:
                missing.append(required_skill)


        # ----------------------------------------------------
        # RAG retrieval
        # ----------------------------------------------------

        query = f"""
        Career: {target_career}

        Candidate skills:
        {list(candidate_skills)}

        What skills, concepts, tools, projects and learning areas
        are important for this career?
        """

        retrieved_results = search_career_knowledge(
            query,
            top_k=2
        )

        context = ""

        for result in retrieved_results:

            context += f"""
SOURCE: {result['document']}

{result['content']}

-------------------------
"""


        # ----------------------------------------------------
        # Candidate profile text
        # ----------------------------------------------------

        education = (
            ", ".join(candidate_profile["education"])
            if candidate_profile["education"]
            else "Not provided"
        )

        projects = (
            ", ".join(candidate_profile["projects"])
            if candidate_profile["projects"]
            else "Not provided"
        )

        interests = (
            ", ".join(candidate_profile["career_interests"])
            if candidate_profile["career_interests"]
            else "Not provided"
        )


        # ----------------------------------------------------
        # AI prompt
        # ----------------------------------------------------

        prompt = f"""

You are CareerAI.

Analyze this candidate for the target career:

TARGET CAREER:
{target_career}

EDUCATION:
{education}

SKILLS:
{list(candidate_skills)}

PROJECTS:
{projects}

CAREER INTERESTS:
{interests}

MATCHED SKILLS:
{matched}

SKILLS TO DEVELOP:
{missing}

RELEVANT CAREER KNOWLEDGE:
{context}

Create a practical personalized report.

Use EXACTLY these sections:

CANDIDATE SUMMARY

EXISTING STRENGTHS

SKILL GAPS

WHY THIS CAREER COULD MATCH

PERSONALIZED LEARNING ROADMAP

RECOMMENDED PROJECTS

NEXT STEPS

Rules:
- Do not invent candidate information.
- Do not assume a career only from the degree.
- Use the candidate's skills, projects and interests.
- Explain skill gaps clearly.
- Give beginner-friendly practical steps.
- Make the roadmap progressive.
- Do not guarantee employment.
"""


        # ----------------------------------------------------
        # Generate AI guidance
        # ----------------------------------------------------

        with st.spinner(
            "🤖 CareerAI is analyzing your profile..."
        ):

            ai_response = generate_ai_response(
                prompt,
                max_new_tokens=700
            )


        # ====================================================
        # RESULTS DASHBOARD
        # ====================================================

        st.divider()

        st.header("📊 CareerAI Analysis")

        st.info(
            f"🎯 **Target Career:** {target_career}"
        )


        # ----------------------------------------------------
        # Candidate profile
        # ----------------------------------------------------

        st.subheader("👤 Candidate Profile")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Education",
                education
            )

        with col2:

            st.metric(
                "Skills Detected",
                len(candidate_skills)
            )

        with col3:

            st.metric(
                "Projects",
                len(candidate_profile["projects"])
            )


        # ----------------------------------------------------
        # Existing skills
        # ----------------------------------------------------

        st.subheader("✅ Skills You Already Have")

        if matched:

            skill_text = " • ".join(
                skill.title()
                for skill in matched
            )

            st.success(skill_text)

        else:

            st.warning(
                "No direct matching skills were detected."
            )


        # ----------------------------------------------------
        # Skill gaps
        # ----------------------------------------------------

        st.subheader("⚠️ Skills You Need to Develop")

        if missing:

            for skill in missing:

                st.write(
                    f"🔸 **{skill.title()}**"
                )

        else:

            st.success(
                "No major skill gaps detected from the selected requirements."
            )


        # ----------------------------------------------------
        # Skill gap progress
        # ----------------------------------------------------

        st.subheader("📈 Current Skill Match")

        total = len(requirements)

        match_percentage = (
            len(matched) / total * 100
            if total > 0
            else 0
        )

        st.progress(
            int(match_percentage)
        )

        st.write(
            f"**{len(matched)} of {total} required skills detected "
            f"({match_percentage:.0f}%)**"
        )


        # ----------------------------------------------------
        # AI Guidance
        # ----------------------------------------------------

        st.divider()

        st.header("🤖 Personalized AI Guidance")

        st.markdown(ai_response)


        # ----------------------------------------------------
        # RAG evidence
        # ----------------------------------------------------

        with st.expander(
            "🔎 View Career Knowledge Retrieved by CareerAI"
        ):

            for result in retrieved_results:

                st.markdown(
                    f"**Source:** `{result['document']}`"
                )

                st.write(
                    result["content"]
                )

                st.divider()


        st.caption(
            "CareerAI provides AI-generated guidance for educational "
            "and career-planning purposes. Recommendations are not "
            "guarantees of employment."
        )

else:

    st.info(
        "👆 Upload a PDF resume above to begin your CareerAI analysis."
    )
