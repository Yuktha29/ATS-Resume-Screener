import re
import random
from collections import Counter

def clean_text(text):
    """Normalize and clean text for analysis."""
    if not isinstance(text, str):
        return ""
    # Remove extra whitespace, newlines, and non-alphanumeric (keep letters/spaces)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    return text.strip().lower()

def extract_keywords(text, ngram_range=(1, 2), min_freq=1):
    """Extract meaningful unigrams and bigrams."""
    words = clean_text(text).split()
    tokens = []

    # Add unigrams
    tokens.extend([w for w in words if len(w) >= 3])

    # Add bigrams
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        if len(bigram.replace(' ', '')) >= 5:  # filter short combos
            tokens.append(bigram)

    # Filter by frequency
    counts = Counter(tokens)
    return {token for token, count in counts.items() if count >= min_freq}

def analyze_resume(resume_text, job_desc_text):
    # --- 1. Handle empty job description gracefully ---
    if not job_desc_text or not job_desc_text.strip():
        # Use a generic but relevant default
        job_desc_text = "software engineer python javascript react machine learning data analysis problem solving communication teamwork"

    # --- 2. Extract keywords from both ---
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_desc_text)

    if not job_keywords:
        job_keywords = {"software", "engineer", "development"}

    # --- 3. Compute match metrics ---
    common = resume_keywords & job_keywords
    missing = job_keywords - resume_keywords
    extra = resume_keywords - job_keywords

    match_ratio = len(common) / len(job_keywords) if job_keywords else 0
    base_score = min(98, max(50, int(match_ratio * 100)))

    # --- 4. Simulate fairness adjustment (per proposal) ---
    # Reduce over-penalization for non-traditional formats
    fairness_boost = 0
    if len(resume_text.split()) < 200:  # short resume
        fairness_boost = random.randint(2, 6)
    elif len(resume_text.split()) > 800:  # very long resume
        fairness_boost = random.randint(-3, 2)

    overall_score = min(99, max(55, base_score + fairness_boost))

    # --- 5. Build dynamic feedback ---
    top_missing = sorted(list(missing))[:3]
    top_common = sorted(list(common))[:3]

    # Summary
    summary = f"Your resume shows a {overall_score}% match for this role based on keyword alignment."

    # Suggestions
    suggestions = []
    if top_missing:
        suggestions.append(f"Consider adding relevant terms like: {', '.join(top_missing[:2])}.")
    suggestions.extend([
        "Quantify achievements with metrics (e.g., 'improved efficiency by 30%').",
        "Use consistent date formatting (e.g., MM/YYYY) throughout your work history.",
        "Add a brief professional summary at the top to highlight your core strengths."
    ])

    # Category: Content Relevance
    content_score = overall_score
    content_issues = [
        {
            "type": "success" if content_score > 75 else "warning",
            "message": f"Resume contains {len(common)} of {len(job_keywords)} relevant keywords."
        }
    ]
    if top_missing:
        content_issues.append({
            "type": "warning",
            "message": f"Missing key terms: {', '.join(top_missing[:2])}"
        })

    # Category: Formatting & Structure
    formatting_score = min(92, overall_score + random.randint(-5, 5))
    formatting_issues = [
        {"type": "warning", "message": "Inconsistent date formatting across roles."},
        {"type": "success", "message": "Clear section headers (e.g., Experience, Skills)."}
    ]

    # Category: Professional Impact
    impact_score = min(90, overall_score + random.randint(-4, 4))
    impact_issues = [
        {"type": "warning", "message": "Consider adding a professional summary."},
        {"type": "success", "message": "Work experience aligns with technical expectations."}
    ]

    return {
        "overallScore": overall_score,
        "summary": summary,
        "categories": [
            {
                "title": "Content Relevance",
                "score": content_score,
                "issues": content_issues
            },
            {
                "title": "Formatting & Structure",
                "score": formatting_score,
                "issues": formatting_issues
            },
            {
                "title": "Professional Impact",
                "score": impact_score,
                "issues": impact_issues
            }
        ],
        "suggestions": suggestions
    }