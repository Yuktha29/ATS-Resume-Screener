import joblib
import random
import re

# Load models
try:
    category_model = joblib.load('category_predictor.pkl')
    category_vectorizer = joblib.load('category_vectorizer.pkl')
    USE_CATEGORY_MODEL = True
except FileNotFoundError:
    print("Category model not found")
    USE_CATEGORY_MODEL = False

def analyze_resume(resume_text, job_desc_text):
    # Normalize input
    resume_lower = resume_text.lower() if resume_text else ""
    words = resume_lower.split()
    word_count = len(words)

    # --- 1. Basic validity: is this even a resume? ---
    resume_keywords = [
        'experience', 'education', 'skills', 'work', 'project',
        'degree', 'bachelor', 'master', 'resume', 'cv', 'employment'
    ]
    is_resume = any(kw in resume_lower for kw in resume_keywords)

    if not is_resume or word_count < 30:
        return {
            "overallScore": 20,
            "summary": "This document does not appear to be a standard resume. It may be missing key sections like work experience or education.",
            "categories": [
                {"title": "Content Relevance", "score": 20, "issues": [{"type": "warning", "message": "No resume-like structure detected"}]},
                {"title": "Formatting & Structure", "score": 25, "issues": [{"type": "warning", "message": "Document too short or lacks standard sections"}]},
                {"title": "Professional Impact", "score": 20, "issues": [{"type": "warning", "message": "Unable to assess relevance without resume content"}]}
            ],
            "suggestions": [
                "Ensure you're uploading a resume (not a cover letter, image, or unrelated document).",
                "Include industry standard sections: Work Experience, Education, Skills.",
                "Use professional language and clear section headers."
            ]
        }

    # --- 2. Predict resume category ---
    predicted_category = "Other"
    category_score = 0
    if USE_CATEGORY_MODEL:
        try:
            X = category_vectorizer.transform([resume_text])
            proba = category_model.predict_proba(X)[0]
            predicted_category = category_model.classes_[proba.argmax()]
            category_score = int(proba.max() * 50)  # 0–50 for category match
        except Exception as e:
            print("❌ Category prediction failed:", e)

    # --- 3. Job description–aware scoring ---
    if job_desc_text and job_desc_text.strip():
        # Extract keywords from both
        job_words = set(re.findall(r'\b[a-z]{3,}\b', job_desc_text.lower()))
        resume_words = set(re.findall(r'\b[a-z]{3,}\b', resume_lower))
        overlap = resume_words & job_words
        match_ratio = len(overlap) / max(len(job_words), 1) if job_words else 0
        keyword_score = int(match_ratio * 30)  # 0–30 for keyword match
        overall_score = min(95, max(30, category_score + keyword_score))
        summary = f"This resume scored {overall_score}/100 based on alignment with the provided job description."
    else:
        # Fallback: score by completeness + category confidence
        completeness = sum([
            bool(re.search(r'\b(experience|work|employment)\b', resume_lower)),
            bool(re.search(r'\b(education|degree|university|college|bachelor|master)\b', resume_lower)),
            bool(re.search(r'\b(skills|technologies|tools|languages|frameworks)\b', resume_lower)),
            bool(re.search(r'\b(increased|improved|developed|led|reduced|optimized|launched)\b', resume_lower))
        ])
        completeness_score = 10 * completeness  # 0–40
        overall_score = min(95, max(30, category_score + completeness_score))
        summary = f"This resume scored {overall_score}/100 based on its predicted category ({predicted_category}) and completeness."

    # --- 4. Fairness adjustment ---
    fairness_boost = 0
    if word_count < 200:
        fairness_boost = random.randint(2, 5)
    elif "linkedin" in resume_lower or "github" in resume_lower:
        fairness_boost = random.randint(1, 3)

    overall_score = min(95, max(30, overall_score + fairness_boost + random.randint(-2, 2)))

    # --- 5. Build dynamic feedback ---
    categories = []
    suggestions = []

    # Content Completeness
    content_issues = []
    has_experience = bool(re.search(r'\b(experience|work|employment)\b', resume_lower))
    has_education = bool(re.search(r'\b(education|degree|university|college|bachelor|master)\b', resume_lower))
    has_skills = bool(re.search(r'\b(skills|technologies|tools|languages|frameworks)\b', resume_lower))
    has_achievements = bool(re.search(r'\b(increased|improved|developed|led|reduced|optimized|launched)\b', resume_lower))

    if not has_experience:
        content_issues.append({"type": "warning", "message": "Work experience section missing"})
        suggestions.append("Add a 'Work Experience' section with your past roles.")
    if not has_education:
        content_issues.append({"type": "warning", "message": "Education details not found"})
        suggestions.append("Include your degree, university, and graduation year.")
    if not has_skills:
        content_issues.append({"type": "warning", "message": "Technical skills not listed"})
        suggestions.append("List relevant tools, languages, and frameworks used.")
    if not has_achievements:
        content_issues.append({"type": "warning", "message": "Lacks quantified achievements"})
        suggestions.append("Use action verbs and metrics (e.g., 'optimized API latency by 40%').")

    if not content_issues:
        content_issues.append({"type": "success", "message": "Resume contains all key sections"})

    categories.append({
        "title": "Content Completeness",
        "score": min(90, max(40, overall_score - 5)),
        "issues": content_issues
    })

    # Formatting & Structure
    formatting_issues = []
    if word_count < 150:
        formatting_issues.append({"type": "warning", "message": "Resume is too brief (<150 words)"})
    if word_count > 600:
        formatting_issues.append({"type": "warning", "message": "Resume may be too long (>600 words)"})

    has_dates = bool(re.search(r'\b(19|20)\d{2}\b|(\d{1,2}[/-]\d{4})|([A-Za-z]+\s+\d{4})', resume_text))
    if not has_dates:
        formatting_issues.append({"type": "warning", "message": "Missing dates in work/education history"})

    if not formatting_issues:
        formatting_issues.append({"type": "success", "message": "Good length and structure"})

    categories.append({
        "title": "Formatting & Structure",
        "score": min(85, max(45, overall_score - random.randint(0, 8))),
        "issues": formatting_issues
    })

    # Professional Impact
    impact_issues = []
    if has_achievements:
        impact_issues.append({"type": "success", "message": "Strong action verbs and results"})
    else:
        impact_issues.append({"type": "warning", "message": "Focus on outcomes, not just duties"})

    categories.append({
        "title": "Professional Impact",
        "score": min(90, max(50, overall_score)),
        "issues": impact_issues
    })

    # Final suggestions
    if not suggestions:
        suggestions = [
            "Quantify achievements with metrics (e.g., 'improved runtimes by 25%').",
            "Use consistent formatting for dates, job titles, and company names.",
            "Tailor your resume to the job by including relevant keywords."
        ]

    return {
        "overallScore": overall_score,
        "summary": summary,
        "categories": categories,
        "suggestions": suggestions,
        "predictedCategory": predicted_category  # ← Add this for frontend display
    }