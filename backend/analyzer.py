import re
from joblib import load

clf_model = load("match_model.pkl")
clf_vectorizer = load("match_vectorizer.pkl")

def clean_text(t):
    if not isinstance(t, str):
        return ""
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower()

def extract_keywords(text):
    text = clean_text(text)
    words = re.findall(r"[a-zA-Z]+", text)
    return set(w for w in words if len(w) > 3)

def detect_resume_structure(text):
    """Check if text looks like a real resume."""
    text = text.lower()
    
    indicators = [
        "experience", "education", "skills",
        "projects", "contact", "summary",
        "activities", "certifications", "work"
    ]

    count = sum(1 for word in indicators if word in text)

    return count  

def analyze_resume(resume_text, job_desc):
    resume_text = clean_text(resume_text)
    job_desc = clean_text(job_desc)


    structure_score = detect_resume_structure(resume_text)
    if structure_score == 0:
       
        return {
            "overallScore": 5,
            "summary": "Document does not appear to be a resume.",
            "categories": [],
            "suggestions": [
                "Upload a real resume instead of an essay or unrelated document."
            ]
        }


    combined = resume_text + " " + job_desc
    features = clf_vectorizer.transform([combined])

    prob = clf_model.predict_proba(features)[0][1]
    ml_score = int(prob * 100)

   
    adjusted_ml_score = int(ml_score * 0.5)  

 
    jd_keywords = extract_keywords(job_desc)
    resume_keywords = extract_keywords(resume_text)

    overlap = resume_keywords.intersection(jd_keywords)

    if len(jd_keywords) > 0:
        overlap_ratio = len(overlap) / len(jd_keywords)
    else:
        overlap_ratio = 0

    keyword_score = int(min(25, overlap_ratio * 25 * 2))  


    bonus = 0
    if re.search(r"\d+%", resume_text):
        bonus += 5
    if 200 < len(resume_text.split()) < 1200:
        bonus += 5


    structure_bonus = min(structure_score * 3, 15)  


    final_score = min(100, adjusted_ml_score + keyword_score + bonus + structure_bonus)

    summary = f"Resume-to-job match score: {final_score}%"

    suggestions = []
    if structure_score < 2:
        suggestions.append("Add core resume sections: Experience, Education, Skills.")
    if keyword_score < 10:
        suggestions.append("Your resume does not mention enough job-specific keywords.")
    if ml_score < 50:
        suggestions.append("Content does not strongly match the job description.")
    if bonus < 5:
        suggestions.append("Add measurable achievements with numbers.")

    suggestions.append("Keep formatting clean and professional.")

    categories = [
        {"title": "ML Match Score", "score": adjusted_ml_score, "issues": []},
        {"title": "Keyword Relevance", "score": keyword_score, "issues": []},
        {"title": "Resume Structure", "score": structure_bonus, "issues": []},
        {"title": "Impact Metrics Bonus", "score": bonus, "issues": []},
    ]

    return {
        "overallScore": final_score,
        "summary": summary,
        "categories": categories,
        "suggestions": suggestions
    }
