import re
from joblib import load


clf_model = load("resume_model.pkl")
clf_vectorizer = load("vectorizer.pkl")

def clean_text(t):
    if not isinstance(t, str):
        return ""
    t = re.sub(r"\s+", " ", t)
    return t.strip().lower()

def extract_keywords(text):
    """Extract basic keywords from any text."""
    text = clean_text(text)
    words = re.findall(r"[a-zA-Z]+", text)
    return set(w for w in words if len(w) > 3)

def analyze_resume(resume_text, job_desc):
    resume_text = clean_text(resume_text)
    job_desc = clean_text(job_desc)


    resume_vec = clf_vectorizer.transform([resume_text])
    predicted_category = clf_model.predict(resume_vec)[0]
    predicted_category_lower = predicted_category.lower()

    jd_keywords = extract_keywords(job_desc)
    resume_keywords = extract_keywords(resume_text)

    if predicted_category_lower in job_desc:
        category_score = 45
    else:
        if any(word in job_desc for word in predicted_category_lower.split()):
            category_score = 30
        else:
            category_score = 10

    overlap = resume_keywords.intersection(jd_keywords)
    if len(jd_keywords) > 0:
        overlap_ratio = len(overlap) / len(jd_keywords)
    else:
        overlap_ratio = 0

    overlap_score = int(min(40, overlap_ratio * 40 * 3))   

    bonus = 0

    if re.search(r"\d+%", resume_text):
        bonus += 5
    if 200 < len(resume_text.split()) < 1500:
        bonus += 5


    final_score = max(0, min(100, category_score + overlap_score + bonus))

    summary = f"Predicted Resume Category: {predicted_category} — Match Score: {final_score}%"

    suggestions = []
    if category_score < 30:
        suggestions.append("Your resume does not strongly match the job category. Consider emphasizing relevant skills.")
    if overlap_score < 20:
        suggestions.append("Add more keywords that appear in the job description.")
    if bonus < 5:
        suggestions.append("Include measurable achievements using percentages or numbers.")

    suggestions.append("Ensure clean formatting and clear section headings.")

    categories = [
        {
            "title": "Category Match",
            "score": category_score,
            "issues": [
                {
                    "type": "success" if category_score > 30 else "warning",
                    "message": f"Category match score is {category_score}/50"
                }
            ]
        },
        {
            "title": "Keyword Relevance",
            "score": overlap_score,
            "issues": [
                {
                    "type": "success" if overlap_score > 20 else "warning",
                    "message": f"Keyword overlap with job description: {len(overlap)} keywords"
                }
            ]
        },
        {
            "title": "Professional Impact",
            "score": bonus,
            "issues": [
                {
                    "type": "success" if bonus == 10 else "warning",
                    "message": "Resume impact score based on metrics and length."
                }
            ]
        },
    ]

    return {
        "overallScore": final_score,
        "summary": summary,
        "categories": categories,
        "suggestions": suggestions,
    }