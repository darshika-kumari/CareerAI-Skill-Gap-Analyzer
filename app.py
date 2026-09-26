import os
import re
import streamlit as st
import numpy as np
import faiss

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareerAI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 CareerAI")
st.subheader(
    "AI Career Guidance, Skill-Gap Analysis & Personalized Roadmap"
)

st.write(
    "Upload a resume and select a target career. CareerAI analyzes "
    "education, skills, projects and interests to identify strengths, "
    "skill gaps and a personalized learning roadmap."
)

st.divider()


# ============================================================
# PATHS
# ============================================================

KNOWLEDGE_PATH = "."


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

documents_text = []
document_names = []

for filename in sorted(os.listdir(KNOWLEDGE_PATH)):

    if filename.endswith(".txt"):

        file_path = os.path.join(
            KNOWLEDGE_PATH,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            documents_text.append(f.read())

        document_names.append(filename)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


embedding_model = load_embedding_model()


# ============================================================
# LOAD FAISS INDEX
# ============================================================

index_path = os.path.join(
    KNOWLEDGE_PATH,
    "career_index.faiss"
)

index = faiss.read_index(index_path)


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
# SKILL DEFINITIONS
# ============================================================

skill_variants = {

    "python": [
        "python"
    ],

    "java": [
        "java"
    ],

    "c++": [
        "c++",
        "cpp"
    ],

    "javascript": [
        "javascript",
        "java script"
    ],

    "html": [
        "html"
    ],

    "css": [
        "css"
    ],

    "sql": [
        "sql",
        "mysql",
        "postgresql",
        "postgres"
    ],

    "git": [
        "git",
        "version control"
    ],

    "docker": [
        "docker"
    ],

    "api": [
        "api",
        "apis",
        "application programming interface"
    ],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "neural networks": [
        "neural networks",
        "neural network"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "transformers": [
        "transformers",
        "transformer"
    ],

    "bert": [
        "bert"
    ],

    "tensorflow": [
        "tensorflow"
    ],

    "pytorch": [
        "pytorch"
    ],

    "computer vision": [
        "computer vision"
    ],

    "data science": [
        "data science",
        "data-science"
    ],

    "data analysis": [
        "data analysis",
        "data analytics"
    ],

    "pandas": [
        "pandas"
    ],

    "numpy": [
        "numpy"
    ],

    "statistics": [
        "statistics",
        "statistical analysis"
    ],

    "probability": [
        "probability"
    ],

    "data visualization": [
        "data visualization",
        "data visualisation"
    ],

    "excel": [
        "excel",
        "microsoft excel"
    ],

    "power bi": [
        "power bi",
        "powerbi"
    ],

    "tableau": [
        "tableau"
    ],

    "data processing": [
        "data processing",
        "data preprocessing",
        "data pre-processing"
    ],

    "data cleaning": [
        "data cleaning",
        "data cleansing"
    ],

    "model evaluation": [
        "model evaluation",
        "model validation",
        "model performance evaluation"
    ],

    "deployment": [
        "deployment",
        "model deployment",
        "deploying"
    ],

    "data structures": [
        "data structures",
        "data structure"
    ],

    "algorithms": [
        "algorithms",
        "algorithm"
    ],

    "object-oriented programming": [
        "object-oriented programming",
        "object oriented programming",
        "oops",
        "oop"
    ],

    "software development": [
        "software development",
        "software engineering"
    ],

    "business analysis": [
        "business analysis"
    ]
}


# ============================================================
# CAREER REQUIREMENTS
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
# SKILL NORMALIZATION
# ============================================================

def normalize_skill(skill):

    skill = skill.lower().strip()

    for canonical, variants in skill_variants.items():

        if skill in variants:

            return canonical

    return skill


# ============================================================
# SKILL DETECTION
# ============================================================

def detect_skills(text):

    text_lower = text.lower()

    detected = set()

    for canonical, variants in skill_variants.items():

        for variant in variants:

            variant_lower = variant.lower()

            if variant_lower in text_lower:

                detected.add(canonical)

                break

    return detected


# ============================================================
# PROFILE EXTRACTION
# ============================================================

def extract_candidate_profile(resume_text):

    text = resume_text.lower()

    profile = {

        "education": [],
        "skills": [],
        "projects": [],
        "career_interests": []
    }


    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education_patterns = {

        "B.TECH": [
            r"\bb\.?\s*tech\b",
            r"\bbtech\b",
            r"\bbachelor of technology\b"
        ],

        "B.E": [
            r"\bb\.?\s*e\b",
            r"\bbe\b",
            r"\bbachelor of engineering\b"
        ],

        "B.SC": [
            r"\bb\.?\s*sc\b",
            r"\bbsc\b",
            r"\bbachelor of science\b"
        ],

        "B.COM": [
            r"\bb\.?\s*com\b",
            r"\bbcom\b",
            r"\bbachelor of commerce\b"
        ],

        "B.A": [
            r"\bb\.?\s*a\b",
            r"\bba\b",
            r"\bbachelor of arts\b"
        ],

        "M.TECH": [
            r"\bm\.?\s*tech\b",
            r"\bmtech\b",
            r"\bmaster of technology\b"
        ],

        "M.SC": [
            r"\bm\.?\s*sc\b",
            r"\bmsc\b",
            r"\bmaster of science\b"
        ],

        "MBA": [
            r"\bmba\b",
            r"\bmaster of business administration\b"
        ],

        "LLB": [
            r"\bllb\b",
            r"\bbachelor of laws\b"
        ],

        "LLM": [
            r"\bllm\b",
            r"\bmaster of laws\b"
        ],

        "PHD": [
            r"\bphd\b",
            r"\bdoctor of philosophy\b"
        ]
    }


    for education, patterns in education_patterns.items():

        for pattern in patterns:

            if re.search(pattern, text):

                profile["education"].append(
                    education
                )

                break


    # --------------------------------------------------------
    # Skills
    # --------------------------------------------------------

    profile["skills"] = sorted(
        detect_skills(resume_text)
    )


    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    project_section = re.search(
        r"(?:projects?|academic projects?|personal projects?)"
        r"(.*?)(?:experience|education|certifications?|"
        r"skills|career interests?|current level|$)",
        resume_text,
        re.IGNORECASE | re.DOTALL
    )

    if project_section:

        project_text = project_section.group(1)

        lines = project_text.splitlines()

        for line in lines:

            line = line.strip()

            line = re.sub(
                r"^[•\-●▪]+\s*",
                "",
                line
            )

            if len(line) > 8:

                profile["projects"].append(
                    line
                )


    # --------------------------------------------------------
    # Career interests
    # --------------------------------------------------------

    interest_section = re.search(
        r"career interests?(.*?)(?:current level|experience|"
        r"education|projects?|skills|$)",
        resume_text,
        re.IGNORECASE | re.DOTALL
    )

    if interest_section:

        interest_text = interest_section.group(1)

        for line in interest_text.splitlines():

            line = line.strip()

            if len(line) > 2:

                profile["career_interests"].append(
                    line
                )


    return profile


# ============================================================
# CAREER KNOWLEDGE SEARCH
# ============================================================

def search_career_knowledge(
    query,
    top_k=2
):

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

        if idx < 0:
            continue

        if idx >= len(documents_text):
            continue

        results.append({

            "document":
                document_names[idx],

            "distance":
                float(distance),

            "content":
                documents_text[idx]
        })


    return results


# ============================================================
# SKILL EXPLANATIONS
# ============================================================

skill_explanations = {

    "python":
        "Python is commonly used for data analysis, machine learning and automation.",

    "sql":
        "SQL is important for querying, joining and analyzing structured data.",

    "statistics":
        "Statistics helps you understand distributions, uncertainty, relationships and model results.",

    "probability":
        "Probability provides the mathematical foundation for uncertainty and many machine-learning methods.",

    "data analysis":
        "Data analysis involves cleaning, exploring and interpreting datasets to find useful patterns.",

    "machine learning":
        "Machine learning is needed to build predictive models from data.",

    "pandas":
        "Pandas is widely used for data cleaning, transformation and tabular analysis.",

    "numpy":
        "NumPy provides numerical arrays and mathematical operations used throughout the Python data ecosystem.",

    "data visualization":
        "Visualization helps communicate patterns, trends, distributions and model results.",

    "deep learning":
        "Deep learning is important for neural-network-based systems such as advanced NLP and computer vision models.",

    "neural networks":
        "Neural networks provide the foundation for many modern deep-learning systems.",

    "nlp":
        "NLP is useful when working with text, language understanding, classification and language models.",

    "transformers":
        "Transformers are widely used in modern NLP and many generative-AI systems.",

    "statistics":
        "Statistics is essential for understanding data, uncertainty and model performance.",

    "data processing":
        "Data processing converts raw data into a form suitable for analysis or machine learning.",

    "model evaluation":
        "Model evaluation helps determine whether a machine-learning model performs reliably.",

    "api":
        "APIs allow machine-learning functionality to be integrated into applications.",

    "deployment":
        "Deployment is required to make a trained model usable by real applications or users.",

    "git":
        "Git is important for version control and maintaining reproducible software projects.",

    "docker":
        "Docker helps package applications and their dependencies for consistent deployment.",

    "data structures":
        "Data structures help organize data efficiently and are important for software engineering.",

    "algorithms":
        "Algorithms provide systematic methods for solving computational problems.",

    "object-oriented programming":
        "Object-oriented programming helps structure larger software systems using reusable components.",

    "software development":
        "Software development involves designing, implementing, testing and maintaining applications."
}


# ============================================================
# PROJECT RECOMMENDATIONS
# ============================================================

project_recommendations = {

    "Data Scientist": [

        "Build an end-to-end student performance prediction project using Python, Pandas, visualization and machine learning.",

        "Build a customer or sales analysis project using SQL and Python, including data cleaning, exploratory analysis and visual dashboards.",

        "Build a classification project where you compare multiple models and explain their evaluation metrics."
    ],

    "AI/ML Engineer": [

        "Build an NLP classification system using BERT or another transformer model.",

        "Build an end-to-end machine-learning API and deploy it as a small web application.",

        "Build a complete ML pipeline covering data preprocessing, training, evaluation, model saving and deployment."
    ],

    "Data Analyst": [

        "Build an SQL-based business analytics project with joins, aggregations and meaningful business questions.",

        "Create an interactive Power BI or Tableau dashboard from a real dataset.",

        "Build a Python data-cleaning and exploratory-analysis project with clear visual conclusions."
    ],

    "Software Engineer": [

        "Build a practical application using object-oriented programming and a database.",

        "Create a DSA-focused project demonstrating efficient searching, sorting and data structures.",

        "Build and document a complete software application using Git and a clear project structure."
    ]
}


# ============================================================
# DYNAMIC AI-STYLE GUIDANCE
# ============================================================

def generate_ai_response(
    target_career,
    profile,
    matched,
    missing,
    retrieved_results
):

    education = profile["education"]

    skills = profile["skills"]

    projects = profile["projects"]

    interests = profile["career_interests"]


    # --------------------------------------------------------
    # Candidate summary
    # --------------------------------------------------------

    education_text = (
        ", ".join(education)
        if education
        else "Education information was not clearly detected."
    )

    skills_text = (
        ", ".join(
            skill.title()
            for skill in skills
        )
        if skills
        else "No predefined technical skills were detected."
    )


    project_count = len(projects)


    report = f"""
## 🧠 Candidate Summary

CareerAI analyzed the uploaded resume for the target career **{target_career}**.

**Education detected:** {education_text}

**Skills detected:** {skills_text}

**Projects detected:** {project_count}

"""


    if interests:

        report += (
            "**Career interests detected:** "
            + ", ".join(interests)
            + "\n\n"
        )


    # --------------------------------------------------------
    # Existing strengths
    # --------------------------------------------------------

    report += "## ✅ Existing Strengths\n\n"

    if matched:

        report += (
            "The resume contains the following skills that directly "
            "match the selected career requirements:\n\n"
        )

        for skill in matched:

            report += (
                f"- **{skill.title()}**"
            )

            if skill in skill_explanations:

                report += (
                    f" — {skill_explanations[skill]}"
                )

            report += "\n"

    else:

        report += (
            "No direct matches were detected against the predefined "
            "requirements. This does not mean the candidate has no "
            "relevant abilities; it means the resume text did not "
            "contain the required terms clearly enough.\n"
        )


    # --------------------------------------------------------
    # Skill gaps
    # --------------------------------------------------------

    report += "\n## ⚠️ Skill Gaps\n\n"

    if missing:

        report += (
            "CareerAI identified the following areas that should be "
            "developed for the selected career:\n\n"
        )

        for skill in missing:

            report += (
                f"### 🔸 {skill.title()}\n"
            )

            explanation = skill_explanations.get(
                skill,
                "This skill is part of the selected career's current requirement profile."
            )

            report += (
                f"{explanation}\n\n"
            )

    else:

        report += (
            "The detected profile covers all predefined requirements "
            "for this career.\n"
        )


    # --------------------------------------------------------
    # Career fit explanation
    # --------------------------------------------------------

    report += "\n## 🎯 Why This Career Could Match\n\n"

    if matched:

        report += (
            f"The resume already demonstrates {len(matched)} "
            f"of the {len(matched) + len(missing)} predefined "
            f"career skills. These existing skills provide a starting "
            f"point for progressing toward **{target_career}**.\n\n"
        )

    else:

        report += (
            f"The current resume does not provide enough detected "
            f"evidence to establish a strong skill match with "
            f"**{target_career}**. The identified gaps provide a "
            f"clear learning path if the candidate wants to pursue "
            f"this direction.\n\n"
        )


    # --------------------------------------------------------
    # Learning roadmap
    # --------------------------------------------------------

    report += "## 🗺️ Personalized Learning Roadmap\n\n"

    if target_career == "Data Scientist":

        roadmap = [

            (
                "Phase 1 — Python & Data Handling",
                "Strengthen Python, Pandas and NumPy. Practice loading datasets, "
                "handling missing values, filtering data and creating reusable analysis code."
            ),

            (
                "Phase 2 — Statistics & Probability",
                "Study descriptive statistics, distributions, correlation, probability, "
                "hypothesis testing and basic statistical interpretation."
            ),

            (
                "Phase 3 — Data Analysis & Visualization",
                "Practice exploratory data analysis and create meaningful visualizations "
                "using Matplotlib, Seaborn or similar tools."
            ),

            (
                "Phase 4 — Machine Learning",
                "Learn regression, classification, feature engineering, train/test splitting, "
                "cross-validation and common machine-learning algorithms."
            ),

            (
                "Phase 5 — Model Evaluation",
                "Learn accuracy, precision, recall, F1-score, MAE, MSE, RMSE and R², "
                "and understand when each metric is appropriate."
            ),

            (
                "Phase 6 — Portfolio",
                "Create 2–3 complete projects and document the problem, dataset, methodology, "
                "results and limitations in GitHub."
            )
        ]

    elif target_career == "AI/ML Engineer":

        roadmap = [

            (
                "Phase 1 — Python & Data Processing",
                "Strengthen Python, NumPy, Pandas and practical data preprocessing."
            ),

            (
                "Phase 2 — Machine Learning",
                "Learn supervised and unsupervised learning, feature engineering, "
                "training and validation."
            ),

            (
                "Phase 3 — Deep Learning",
                "Learn neural networks, backpropagation, activation functions, "
                "loss functions and optimization."
            ),

            (
                "Phase 4 — NLP & Transformers",
                "Study NLP fundamentals, embeddings, attention, transformers and "
                "BERT-style models."
            ),

            (
                "Phase 5 — Model Evaluation",
                "Learn how to evaluate models properly and analyze errors rather than "
                "relying only on a single accuracy number."
            ),

            (
                "Phase 6 — Deployment",
                "Learn APIs, model serving, Git and Docker, then deploy at least one "
                "machine-learning project."
            )
        ]

    elif target_career == "Data Analyst":

        roadmap = [

            (
                "Phase 1 — SQL",
                "Practice SELECT, WHERE, GROUP BY, JOIN, subqueries and window functions."
            ),

            (
                "Phase 2 — Excel & Data Cleaning",
                "Learn formulas, pivot tables, data cleaning and structured reporting."
            ),

            (
                "Phase 3 — Python Analysis",
                "Use Pandas and Python for data cleaning, exploration and automation."
            ),

            (
                "Phase 4 — Statistics",
                "Understand averages, distributions, correlation and basic statistical reasoning."
            ),

            (
                "Phase 5 — Visualization",
                "Create dashboards and visual stories using Power BI or Tableau."
            ),

            (
                "Phase 6 — Portfolio",
                "Build business-focused projects where every visualization answers a specific question."
            )
        ]

    else:

        roadmap = [

            (
                "Phase 1 — Programming",
                "Strengthen one primary programming language and write clean, modular code."
            ),

            (
                "Phase 2 — Data Structures",
                "Practice arrays, strings, linked lists, stacks, queues, trees, graphs and hashing."
            ),

            (
                "Phase 3 — Algorithms",
                "Study searching, sorting, recursion, greedy methods and basic dynamic programming."
            ),

            (
                "Phase 4 — OOP & Software Design",
                "Learn classes, inheritance, abstraction, encapsulation and reusable software components."
            ),

            (
                "Phase 5 — Development Tools",
                "Use Git, databases, testing and a structured development workflow."
            ),

            (
                "Phase 6 — Portfolio",
                "Build and document complete applications that demonstrate practical engineering skills."
            )
        ]


    for title, description in roadmap:

        report += (
            f"### {title}\n"
            f"{description}\n\n"
        )


    # --------------------------------------------------------
    # Recommended projects
    # --------------------------------------------------------

    report += "## 🚀 Recommended Projects\n\n"

    for project in project_recommendations[target_career]:

        report += f"- {project}\n"


    # --------------------------------------------------------
    # Existing project analysis
    # --------------------------------------------------------

    if projects:

        report += "\n### Your Existing Projects\n\n"

        report += (
            "Your detected projects can become stronger portfolio "
            "evidence if each project clearly documents the problem, "
            "dataset, technology used, methodology, evaluation results "
            "and final outcome.\n\n"
        )

        for project in projects[:8]:

            report += (
                f"- {project}\n"
            )


    # --------------------------------------------------------
    # Knowledge retrieved
    # --------------------------------------------------------

    report += "\n## 📚 Career Knowledge Used\n\n"

    if retrieved_results:

        report += (
            "CareerAI retrieved relevant career information from its "
            "knowledge base and used it to structure the analysis.\n\n"
        )

        for result in retrieved_results:

            report += (
                f"- **{result['document']}**\n"
            )

    else:

        report += (
            "No additional career document was retrieved.\n"
        )


    # --------------------------------------------------------
    # Next steps
    # --------------------------------------------------------

    report += "\n## ✅ Your Next Steps\n\n"

    if missing:

        first_three = missing[:3]

        for number, skill in enumerate(
            first_three,
            start=1
        ):

            report += (
                f"{number}. Start with **{skill.title()}** "
                "and build one small practical exercise.\n"
            )

    report += (
        f"{len(first_three) + 1 if missing else 1}. "
        "Build or improve a project that demonstrates the newly learned skills.\n"
    )

    report += (
        f"{len(first_three) + 2 if missing else 2}. "
        "Document the project clearly on GitHub.\n"
    )

    report += (
        f"{len(first_three) + 3 if missing else 3}. "
        "Review the remaining skill gaps and repeat the process progressively.\n"
    )


    report += """
    
## ⚠️ Important

CareerAI provides AI-generated educational and career-planning
guidance. The analysis is based on information detected from the
uploaded resume and the application's career knowledge base.
Recommendations are not guarantees of employment or career outcomes.
"""

    return report


# ============================================================
# USER INTERFACE
# ============================================================

st.header("📄 Step 1 — Upload Your Resume")

uploaded_file = st.file_uploader(
    "Upload your resume in PDF format",
    type=["pdf"]
)


if uploaded_file:

    resume_text = extract_text_from_pdf(
        uploaded_file
    )

    if not resume_text:

        st.error(
            "Could not extract readable text from this PDF."
        )

        st.stop()


    candidate_profile = extract_candidate_profile(
        resume_text
    )

    st.success(
        "✅ Resume successfully analyzed."
    )

    st.divider()

    st.header(
        "🎯 Step 2 — Select Target Career"
    )

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

        for skill in candidate_profile["skills"]:

            candidate_skills.add(
                normalize_skill(skill)
            )


        # ----------------------------------------------------
        # Skill gap analysis
        # ----------------------------------------------------

        requirements = career_skill_requirements[
            target_career
        ]

        matched = []

        missing = []


        for required_skill in requirements:

            normalized_required = normalize_skill(
                required_skill
            )

            if normalized_required in candidate_skills:

                matched.append(
                    required_skill
                )

            else:

                missing.append(
                    required_skill
                )


        # ----------------------------------------------------
        # RAG retrieval
        # ----------------------------------------------------

        query = f"""
        Career: {target_career}

        Candidate skills:
        {list(candidate_skills)}

        Missing skills:
        {missing}

        Candidate projects:
        {candidate_profile["projects"]}

        Explain the skills, concepts, tools, projects and learning
        areas important for this career.
        """


        retrieved_results = search_career_knowledge(
            query,
            top_k=2
        )


        # ----------------------------------------------------
        # Generate dynamic guidance
        # ----------------------------------------------------

        with st.spinner(
            "🤖 CareerAI is analyzing your profile..."
        ):

            ai_response = generate_ai_response(
                target_career,
                candidate_profile,
                matched,
                missing,
                retrieved_results
            )


        # ====================================================
        # RESULTS DASHBOARD
        # ====================================================

        st.divider()

        st.header(
            "📊 CareerAI Analysis"
        )

        st.info(
            f"🎯 **Target Career:** {target_career}"
        )


        # ----------------------------------------------------
        # Candidate profile
        # ----------------------------------------------------

        st.subheader(
            "👤 Candidate Profile"
        )

        col1, col2, col3 = st.columns(3)


        with col1:

            education_display = (
                ", ".join(
                    candidate_profile["education"]
                )
                if candidate_profile["education"]
                else "Not detected"
            )

            st.metric(
                "Education",
                education_display
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
        # All detected skills
        # ----------------------------------------------------

        st.subheader(
            "🧩 Skills Detected From Resume"
        )

        if candidate_skills:

            skill_display = " • ".join(
                skill.title()
                for skill in sorted(candidate_skills)
            )

            st.info(
                skill_display
            )

        else:

            st.warning(
                "No predefined technical skills were detected."
            )


        # ----------------------------------------------------
        # Existing matching skills
        # ----------------------------------------------------

        st.subheader(
            "✅ Skills You Already Have"
        )

        if matched:

            skill_text = " • ".join(
                skill.title()
                for skill in matched
            )

            st.success(
                skill_text
            )

        else:

            st.warning(
                "No direct matching skills were detected."
            )


        # ----------------------------------------------------
        # Skill gaps
        # ----------------------------------------------------

        st.subheader(
            "⚠️ Skills You Need to Develop"
        )

        if missing:

            for skill in missing:

                explanation = skill_explanations.get(
                    skill,
                    "This skill is included in the selected career requirements."
                )

                st.write(
                    f"🔸 **{skill.title()}** — {explanation}"
                )

        else:

            st.success(
                "No major predefined skill gaps detected."
            )


        # ----------------------------------------------------
        # Skill match
        # ----------------------------------------------------

        st.subheader(
            "📈 Current Skill Match"
        )

        total = len(requirements)

        match_percentage = (
            len(matched) / total * 100
            if total
            else 0
        )

        st.progress(
            int(match_percentage)
        )

        st.write(
            f"**{len(matched)} of {total} required skills "
            f"detected ({match_percentage:.0f}%)**"
        )


        # ----------------------------------------------------
        # Personalized guidance
        # ----------------------------------------------------

        st.divider()

        st.header(
            "🤖 Personalized AI Guidance"
        )

        st.markdown(
            ai_response
        )


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
