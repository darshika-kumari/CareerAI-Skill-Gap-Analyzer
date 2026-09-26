# 🎯 CareerAI — AI Career Guidance & Skill-Gap Analysis

CareerAI is an AI-powered career guidance system that analyzes a user's resume, identifies existing skills and skill gaps, and generates a personalized learning roadmap for a selected career.

The system combines **NLP, semantic embeddings, FAISS-based retrieval, a career knowledge base, and personalized career analysis** to provide practical career guidance.

---

## 🚀 Live Demo — Practical Implementation

### 👉 [**Try CareerAI Online**](https://careerai-skill-gap-analyzer-pqs8mqyrpdvyympqxnmesk.streamlit.app/)

The live application allows users to experience the practical implementation of CareerAI directly in a web browser.

### How to use the application

1. Upload your resume in PDF format.
2. Select your target career.
3. Click **Analyze My Career**.
4. CareerAI analyzes your profile.
5. View detected skills and existing strengths.
6. View career-specific skill gaps.
7. View the current skill-match analysis.
8. Receive a personalized learning roadmap.
9. Get recommended projects.
10. Explore the career knowledge retrieved by the system.

---

## 🧠 Project Objective

The main objective of CareerAI is to help users understand:

* What skills they already have
* What skills they need to develop
* How their current profile relates to a selected career
* What they should learn next
* Which projects can strengthen their portfolio
* How they can progressively prepare for their target career

CareerAI considers information detected from the user's **education, skills, projects, and career interests** rather than relying only on a degree-to-career mapping.

---

## 🔄 System Workflow

```text
             ┌─────────────────┐
             │   Resume PDF    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Resume Parsing  │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Profile         │
             │ Extraction      │
             └────────┬────────┘
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
     Education     Skills      Projects
          │           │           │
          └───────────┼───────────┘
                      ▼
             ┌─────────────────┐
             │ Target Career   │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Skill Matching  │
             └────────┬────────┘
                      │
              ┌───────┴────────┐
              ▼                ▼
        Existing Skills     Skill Gaps
              │                │
              └───────┬────────┘
                      ▼
             ┌─────────────────┐
             │ FAISS Semantic  │
             │ Search / RAG    │
             └────────┬────────┘
                      │
                      ▼
             ┌─────────────────┐
             │ Personalized    │
             │ Guidance        │
             └────────┬────────┘
                      │
          ┌───────────┼────────────┐
          ▼           ▼            ▼
       Roadmap     Projects     Next Steps
```

---

## ✨ Key Features

### 📄 Resume Analysis

CareerAI accepts a resume in PDF format and extracts relevant information such as:

* Education
* Technical skills
* Projects
* Career interests

### 🧩 Skill Detection

The system identifies technical and professional skills from the uploaded resume.

Examples include:

* Python
* C++
* Java
* SQL
* Machine Learning
* Deep Learning
* NLP
* Transformers
* Pandas
* NumPy
* Statistics
* Data Visualization
* Git
* Docker
* APIs

### 🎯 Career-Specific Analysis

The current system supports analysis for:

* AI/ML Engineer
* Data Scientist
* Data Analyst
* Software Engineer

### 📊 Skill-Gap Analysis

CareerAI compares the detected candidate skills with the requirements of the selected career.

It displays:

**Existing Skills → Required Skills → Missing Skills**

### 📈 Skill Match

The application calculates a current skill-match percentage based on the predefined requirements for the selected career.

### 🗺️ Personalized Learning Roadmap

The system generates a progressive roadmap based on the selected career and identified skill gaps.

### 🚀 Project Recommendations

CareerAI recommends practical projects that can help the user develop and demonstrate the required skills.

### 🔎 RAG-Based Career Knowledge Retrieval

CareerAI uses a career knowledge base and semantic retrieval to obtain relevant career information.

The project uses:

* Sentence Transformers
* Embeddings
* FAISS
* Career knowledge documents

### 🤖 Personalized Career Guidance

The final report combines the candidate profile, skill analysis, career requirements, and retrieved career knowledge to generate personalized guidance.

---

## 🧠 RAG Architecture

CareerAI uses a Retrieval-Augmented Generation-style workflow:

```text
Resume
   ↓
Profile Extraction
   ↓
Candidate Skills
   ↓
Target Career
   ↓
Career Query
   ↓
Sentence Transformer Embeddings
   ↓
FAISS Semantic Search
   ↓
Relevant Career Knowledge
   ↓
Personalized Career Analysis
   ↓
Learning Roadmap + Projects + Next Steps
```

---

## 🛠️ Technology Stack

| Technology            | Purpose                             |
| --------------------- | ----------------------------------- |
| Python                | Core programming language           |
| Streamlit             | Web application                     |
| Sentence Transformers | Semantic embeddings                 |
| FAISS                 | Vector similarity search            |
| NLP                   | Resume and skill analysis           |
| PyPDF                 | PDF resume extraction               |
| NumPy                 | Numerical processing                |
| RAG                   | Career knowledge retrieval          |
| GitHub                | Version control and project hosting |

---

## 📂 Project Structure

```text
CareerAI-Skill-Gap-Analyzer/
│
├── app.py
├── requirements.txt
│
├── ai_ml_engineer.txt
├── data_analyst.txt
├── data_scientist.txt
├── software_engineer.txt
│
├── career_index.faiss
├── sample_resume.txt
│
├── CareerAI_Skill_Gap_Analyzer_GitHub
│
└── README.md
```

---

## 📊 Example Analysis

For an AI/ML Engineer career, CareerAI can identify existing skills such as:

```text
Python
Machine Learning
```
