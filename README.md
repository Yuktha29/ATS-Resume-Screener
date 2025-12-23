AI Resume Screener — Machine Learning Resume Analyzer

This project is an AI-powered resume analysis web application. It allows users to upload a PDF resume and also paste a job description. The backend uses a machine-learning model (Logistic Regression + TF-IDF) trained on real resume/job description datasets from "Kaggle" to compute a score, generate feedback, and provided suggestions.

The system consists of:
- Backend: Python + Flask, ML classifier, resume text extraction
- Frontend: React-based UI for upload, job description input, and score visualization
- ML: Resume–JD matching model using TF-IDF + Logistic Regression

nyone can clone and run this project locally by following the instructions below.

1. Clone the Repository
- git clone <https://github.com/Yuktha29/ATS-Resume-Screener.git>


2. Setup & Run the Backend 
- cd backend

Create virtual environment:
- python3 -m venv .venv
- source .venv/bin/activate

Install dependencies: 
- pip install -r requirements.txt
- pip install flask-cors pdfplumber tqdm

Confirm required CSV datasets exist

Inside backend/, you must have:
- resume_dataset.csv
- job_title_des.csv

Build training pairs:
- python3 build_pairs.py


This creates:
- training_pairs.csv

Then, Train the ML model:
- python3 train_match_model.py


This generates:
- match_model.pkl
- match_vectorizer.pkl

Start the backend server:
- python3 app.py


Backend will run at:
- http://localhost:5001

3. Setup & Run the Frontend (React.js):
- Open a second terminal window.

Navigate to frontend folder:
- cd frontend

Install dependencies:
- npm install

Start the development server
- npm start

Finally, AI Resume Screener will show up.

Now, you can upload your Resume, type in a Job description and hit "Analyze". The Resume Screener will screen your resume based on the give Job description. As a result you will get a score and feedback.
# Start the Flask server
python3 app.py

-------------------------
cd frontend

# Install dependencies
npm install

# Start the React app
npm start

## Project Attribution & Contributions

This is a public showcase copy of a collaborative academic group project.

The project was developed by a team as part of a course assignment.  
This repository is shared publicly to demonstrate my participation, understanding of the system, and ability to run, explain, and work with a full-stack ML application.

### My Contributions
- Participated in project setup, execution, and testing
- Worked with the existing ML pipeline and backend to understand data flow and scoring logic
- Assisted with running experiments, validating outputs, and debugging issues
- Contributed to documentation, cleanup, and preparation of a public-ready version of the project
- Gained hands-on experience working with Flask, React, and ML-based resume analysis systems

### Note
Core model design and dataset preparation were collaborative efforts by the team.
