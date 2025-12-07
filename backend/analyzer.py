# backend/analyzer.py
import re
import random

def analyze_resume(resume_text, job_desc_text):
    if not job_desc_text.strip():
        job_desc_text = "software engineer python javascript react data analysis problem solving"

    # Normalize and extract words
    def extract_keywords(text):
        return set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))

    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc_text)

    if not job_keywords:
        job_keywords = {"software", "engineer", "development"}

    # Compute match ratio
    matches = resume_keywords & job_keywords
    match_ratio = len(matches) / len(job_keywords) if job_keywords else 0
    base_score = min(95, max(60, int(match_ratio * 100)))

    # Simulate fairness adjustment (from your proposal)
    fairness_offset = random.randint(-3, +4)
    overall_score = min(100, max(50, base_score + fairness_offset))

    # Generate feedback based on missing keywords
    missing = list(job_keywords - resume_keywords)[:3]
    suggestions = [
        "Add quantifiable metrics to your achievements",
        "Use consistent formatting for dates and job titles"
    ]
    if missing:
        suggestions.insert(0, f"Consider adding keywords like: {', '.join(missing[:2])}")

    return {
        "overallScore": overall_score,
        "summary": f"Your resume shows a {overall_score}% match for this role based on keyword alignment.",
        "categories": [
            {
                "title": "Content Relevance",
                "score": overall_score,
                "issues": [
                    {"type": "success" if overall_score > 75 else "warning",
                     "message": "Alignment with provided job description"}
                ]
            },
            {
                "title": "Formatting & Structure",
                "score": min(90, overall_score + 5),
                "issues": [{"type": "warning", "message": "Inconsistent date formatting"}]
            },
            {
                "title": "Professional Impact",
                "score": min(88, overall_score + 3),
                "issues": [{"type": "success", "message": "Clear role alignment"}]
            }
        ],
        "suggestions": suggestions
    }