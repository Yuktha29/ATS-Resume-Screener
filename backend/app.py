from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from parser import extract_text_from_pdf
from analyzer import analyze_resume

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    if "resume" not in request.files:
        return jsonify({"error": "Resume file missing"}), 400

    resume_file = request.files["resume"]
    jd_text = request.form.get("jobDesc", "")


    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        resume_file.save(temp.name)
        extracted_text = extract_text_from_pdf(temp.name)

    result = analyze_resume(extracted_text, jd_text)
    os.remove(temp.name)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)