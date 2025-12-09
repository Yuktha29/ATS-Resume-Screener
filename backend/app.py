from flask import Flask, request, jsonify
import tempfile
import os
from flask_cors import CORS
from parser import extract_text_from_pdf
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)  # Allow the frontent to connect backend
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB max

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400

    file = request.files['resume']
    if file.filename.lower().endswith('.pdf') == False:
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Save to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
        file.save(temp.name)
        cur_text = extract_text_from_pdf(temp.name)
        os.unlink(temp.name)

    job_descr = request.form.get('jobDesc', '')

    # Generate proper feedback
    feedback = analyze_resume(cur_text, job_descr)
    return jsonify(feedback)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)