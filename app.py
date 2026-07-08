import markdown
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from services.granite_service import ask_granite
from services.prompt_service import build_prompt
from services.pdf_service import extract_text

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    print("Upload route called")
    if "pdf" not in request.files:
        print("No PDF")
        return "No file uploaded."

    file = request.files["pdf"]

    if not file.filename:
        return "No selected file."

    if not file.filename.endswith(".pdf"):
        return "Only PDF files are allowed."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        secure_filename(file.filename)
    )

    file.save(filepath)

    level = request.form["level"]
    extracted_text = extract_text(filepath)

    prompt = build_prompt(extracted_text, level)
    try:
        result = ask_granite(prompt)
        html_result = markdown.markdown(
        result,
         extensions=["tables", "fenced_code"])
    except Exception as e:
        result = f"Error:\n\n{str(e)}"
        html_result = f"<pre>{result}</pre>"
    return render_template("index.html", result=html_result, level=level)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)