import pandas as pd
from tqdm import tqdm
import re

resumes = pd.read_csv("resume_dataset.csv")
jobs = pd.read_csv("job_title_des.csv")

def extract_keywords(text):
    if not isinstance(text, str):
        return set()
    text = text.lower()
    words = re.findall(r"[a-zA-Z]+", text)
    return {w for w in words if len(w) > 3}

pairs = []
print("Building training pairs...")

for _, r in tqdm(resumes.iterrows(), total=len(resumes)):
    resume_text = r["Resume_str"]
    resume_keywords = extract_keywords(resume_text)

    sample_jobs = jobs.sample(3)

    for _, j in sample_jobs.iterrows():
        jd_text = j["Job Description"]
        job_keywords = extract_keywords(jd_text)

        overlap = resume_keywords.intersection(job_keywords)
        label = 1 if len(overlap) >= 5 else 0

        pairs.append([resume_text, jd_text, label])

df = pd.DataFrame(pairs, columns=["resume_text", "jd_text", "label"])
df.to_csv("training_pairs.csv", index=False)

print("Saved training_pairs.csv with", len(df), "rows")