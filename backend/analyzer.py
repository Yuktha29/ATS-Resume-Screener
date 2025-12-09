import re
import random

def analyze_resume(resume_text, job_desc_text):
    resume_lower = resume_text.lower()
    words = resume_lower.split()
    char_ctr = len(resume_text)
    word_ctr = len(words)

    #Basic validity checks for if the doc is a resume
    is_resume = any(kw in resume_lower for kw in [
        'experience', 'education', 'skills', 'work', 'project', 'degree', 'bachelor', 'resume', 'cv'
    ])

    if not is_resume or word_ctr < 30:
        return {
            "overallScore": 20,
            "summary": "This document does not appear to be a standard resume. It may be missing soem sections like work experience or education.",
            "categories": [
                {"title": "Content Relevance", "score": 20, "issues": [{"type": "warning", "message": "No resuem-like structure detected"}]},
                {"title": "Formatting & Structure", "score": 25, "issues": [{"type": "warning", "message": "Document too short or lacks standard sections"}]},
                {"title": "Professional Impact", "score": 20, "issues": [{"type": "warning", "message": "Unable to assess relevance without resume content"}]}
            ],
            "suggestions": [
                "Ensure you're uploading a resume (not a cover letter, image, or unrelated document).",
                "Include indusry standard sections: Work Experience, Education, Skills.",
                "Use professional language and clear section starters."
            ]
        }

    # Section detection
    section_keywords = {
        "experience": r"\b(experience|work|employment)\b",
        "education": r"\b(education|degree|university|college|bachelor|master)\b",
        "skills": r"\b(skills|technologies|tools|languages|frameworks)\b",
        "achievements": r"\b(increased|improved|developed|led|reduced|optimized|launched)\b"
    }

    section_present = {}
    for key, pat in section_keywords.items():
        section_present[key] = bool(re.search(pat, resume_lower))

    has_expirience = section_present["experience"]
    has_education = section_present["education"]
    has_skills = section_present["skills"]
    has_achv = section_present["achievements"]

    #Job description processing 
    if job_desc_text.strip():
        job_words = set(re.findall(r'\b[a-z]{3,}\b', job_desc_text.lower()))
        resume_words = set(re.findall(r'\b[a-z]{3,}\b', resume_lower))
        overlap = resume_words & job_words
        match_ratio = len(overlap) / max(len(job_words), 1)
        base_score = min(95, max(50, int(match_ratio * 80 + 20)))
    else:
        # Score based on completeness
        completeness = sum([has_expirience, has_education, has_skills, has_achv])
        base_score = 50 + (completeness * 10)  # 50 to 90

    overall_score = min(95, max(30, base_score + random.randint(-5, 5)))

    # Dynamic issues per section tailored to resumes
    categories = []
    suggestions = []

    # Content Relevance
    content_issues = []
    if not has_expirience:
        content_issues.append({"type": "warning", "message": "Work experience section missing"})
        suggestions.append("Add a 'Work Experience' section with your past roles.")
    if not has_education:
        content_issues.append({"type": "warning", "message": "Education details not found"})
        suggestions.append("Include your degree, university, and graduation year.")
    if not has_skills:
        content_issues.append({"type": "warning", "message": "Technical skills not listed"})
        suggestions.append("List relevant tools, languages, and frameworks used.")
    if not has_achv:
        content_issues.append({"type": "warning", "message": "Lacks quantified achievements"})
        suggestions.append("Use action verbs and metrics (e.g., 'optimized API latency by 40%').")

    if not content_issues:
        content_issues.append({"type": "success", "message": "Resume contains all key sections"})
        
    temp_cat = max(40, overall_score - 5)
    categories.append({
        "title": "Content Completeness",
        "score": min(90, temp_cat),
        "issues": content_issues
    })

    # Formatting and Structure
    formatting_issues = []
    if word_ctr < 150:
        formatting_issues.append({"type": "warning", "message": "Resume is too brief (<150 words)"})
    if word_ctr > 600:
        formatting_issues.append({"type": "warning", "message": "Resume may be too long (>600 words)"})
    
    #Check for dates
    has_dates = bool(re.search(r'\b(19|20)\d{2}\b|(\d{1,2}/\d{4})', resume_text))
    if not has_dates:
        formatting_issues.append({"type": "warning", "message": "Missing dates in work/education history"})

    if not formatting_issues:
        formatting_issues.append({"type": "success", "message": "Good length and structure"})

    categories.append({
        "title": "Formatting & Structure",
        "score": min(85, max(45, overall_score - random.randint(0, 8))),
        "issues": formatting_issues
    })

    #Professional Impact (use strong action verbs)
    impact_issues = []
    if has_achv:
        impact_issues.append({"type": "success", "message": "Strong action verbs and results"})
    else:
        impact_issues.append({"type": "warning", "message": "Focus on outcomes, not just duties"})
        
    temp_score = max(50, overall_score)
    categories.append({
        "title": "Professional Impact",
        "score": min(90, temp_score),
        "issues": impact_issues
    })

    # Final suggestions output
    if not suggestions:
        suggestions = [
            "Quantify achievements with metrics (e.g., 'reduced costs by 25%').",
            "Use consistent formatting for dates, job titles, and company names.",
            "Tailor your resume to the job by including relevant keywords."
        ]

    return {
        "overallScore": overall_score,
        "summary": f"This resume scored {overall_score}/100 based on completenesss, relevance, and structure.",
        "categories": categories,
        "suggestions": suggestions
    }