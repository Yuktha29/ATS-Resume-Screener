from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from parser import extract_text_from_pdf
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)  # Allow frontend (localhost:3000) to call backend
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files['resume']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
        file.save(tmp.name)
        text = extract_text_from_pdf(tmp.name)
        os.unlink(tmp.name)

    # Optional: get job description from form data
    job_desc = request.form.get('jobDesc', '')

    # Generate feedback
    feedback = analyze_resume(text, job_desc)
    return jsonify(feedback)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)