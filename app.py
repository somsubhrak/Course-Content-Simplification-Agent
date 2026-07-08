import markdown
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
from services.granite_service import ask_granite
from services.prompt_service import build_prompt, build_quiz_prompt
from services.pdf_service import extract_text

app = Flask(__name__)
app.secret_key = os.urandom(24)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

_MD_EXTENSIONS = ["tables", "fenced_code", "nl2br", "sane_lists"]


def _to_html(md_text):
    return markdown.markdown(md_text, extensions=_MD_EXTENSIONS)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    if "pdf" not in request.files:
        return "No file uploaded.", 400

    file = request.files["pdf"]

    if not file.filename:
        return "No selected file.", 400

    if not file.filename.endswith(".pdf"):
        return "Only PDF files are allowed.", 400

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )
    file.save(filepath)

    level = request.form.get("level", "Beginner")
    extracted_text = extract_text(filepath)

    # Store for quiz use
    session["pdf_path"] = filepath
    session["pdf_level"] = level

    prompt = build_prompt(extracted_text, level)
    try:
        result = ask_granite(prompt)
        html_result = _to_html(result)
    except Exception as e:
        result = f"Error:\n\n{str(e)}"
        html_result = f"<pre>{result}</pre>"

    return render_template("index.html", result=html_result, level=level)


@app.route("/quiz", methods=["POST"])
def quiz():
    data = request.get_json(silent=True) or {}
    pdf_path = data.get("pdf_path") or session.get("pdf_path")
    level = data.get("level") or session.get("pdf_level", "Beginner")

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"error": "No PDF available. Please upload a PDF first."}), 400

    extracted_text = extract_text(pdf_path)
    prompt = build_quiz_prompt(extracted_text, level)

    try:
        result = ask_granite(prompt)
        html_result = _to_html(result)
        return jsonify({"html": html_result, "level": level})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
