# CourseAI — Adaptive Learning Agent

> **An AI-powered agent that intelligently analyzes academic content and reframes explanations based on a learner's proficiency level — from Beginner to Expert.**

Powered by **Meta Llama** via [IBM watsonx.ai](https://www.ibm.com/watsonx), CourseAI solves a core challenge in education: lecture notes and textbooks are written at a fixed complexity level that does not suit every student. CourseAI takes any PDF of course material and produces personalized, beautifully formatted study notes at exactly the right depth — and can generate a level-adapted quiz on the same content.

---

## Live Demo

Deployed on **Render.com** → https://course-content-simplification-agent.onrender.com

---

## Features

| Feature | Description |
|---|---|
| **Adaptive Simplification** | Rewrites academic PDFs at Beginner, Intermediate, Advanced, or Expert level |
| **Quiz Generation** | Creates a 10-question mixed quiz with a full Answer Key from the uploaded PDF |
| **Rich Markdown Rendering** | Full support for headings, bullet lists, numbered lists, tables, and code blocks |
| **Drag-and-Drop Upload** | Custom file drop-zone with live filename feedback |
| **Level Hints** | Real-time description of what each proficiency level produces |
| **Loading States** | Spinners and contextual messages for both analysis and quiz generation |
| **Quiz Modal** | Quiz opens in an animated overlay — no page navigation required |
| **Responsive UI** | Works on desktop and mobile; sticky header, scrollable output panels |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask 3.1 |
| **AI Model** | Meta Llama 3.3 70B Instruct (via `ibm-watsonx-ai`) |
| **PDF Parsing** | PyPDF2 |
| **Markdown → HTML** | `markdown` (extensions: `tables`, `fenced_code`, `nl2br`, `sane_lists`) |
| **Frontend** | Vanilla HTML/CSS/JS — no frameworks |
| **Deployment** | Render.com |

---

## Project Structure

```
CourseAI/
├── app.py                  # Flask app — routes: /, /upload, /quiz
├── config.py               # Loads IBM credentials from environment
├── requirements.txt        # Python dependencies
│
├── services/
│   ├── ibm_client.py       # IBM watsonx.ai ModelInference setup
│   ├── granite_service.py  # Calls Llama model, returns raw text
│   ├── pdf_service.py      # Extracts text from PDF using PyPDF2
│   └── prompt_service.py   # Builds level-specific prompts + quiz prompt
│
├── templates/
│   └── index.html          # Jinja2 template — upload form + results + quiz modal
│
├── static/
│   ├── style.css           # All styles — layout, output, modal, responsive
│   └── script.js           # File picker, drag-drop, form loading state, quiz fetch
│
└── uploads/                # Uploaded PDFs stored here (gitignored)
```

---

## How It Works

1. User uploads a **PDF** (lecture notes, textbook chapter, etc.) and selects a **proficiency level**.
2. Flask saves the file and stores the path in the **session**.
3. [`pdf_service.extract_text()`](services/pdf_service.py) reads all pages using PyPDF2.
4. [`prompt_service.build_prompt()`](services/prompt_service.py) constructs a detailed, level-specific system prompt instructing IBM Granite how to reframe the content.
5. [`granite_service.ask_granite()`](services/granite_service.py) sends the prompt to IBM watsonx.ai and returns the Markdown response.
6. Flask converts the Markdown to HTML (preserving bullets, tables, code) and renders it on the page.
7. Clicking **Generate Quiz** calls `/quiz` — which reuses the session-stored PDF, builds a quiz prompt, calls Granite again, and returns rendered HTML to the modal via `fetch()`.

### Proficiency Levels

| Level | Audience | Prompt strategy |
|---|---|---|
| **Beginner** | No prior knowledge | Simple English, real-life examples, jargon explained inline |
| **Intermediate** | Basic familiarity | Technical terms with brief explanations, examples where helpful |
| **Advanced** | Solid background | Professional terminology, concept relationships, practical applications |
| **Expert** | Graduate level | Precise academic language, theoretical insights, full depth |

---

## Local Setup

### Prerequisites

- Python 3.10+
- An [IBM watsonx.ai](https://www.ibm.com/watsonx) account with a project and API key
- The Meta Llama 3.3 70B Instruct model enabled in your project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/CourseAI.git
cd CourseAI
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
IBM_API_KEY=your_ibm_api_key_here
IBM_PROJECT_ID=your_watsonx_project_id_here
IBM_URL=https://us-south.ml.cloud.ibm.com
IBM_MODEL_ID=available model
```

> **Never commit `.env` to version control.** It is listed in `.gitignore`.

### 5. Run the development server

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Deploying to Render.com

The app is already deployed. For fresh deploys or re-deploys:

### Build & Start commands

| Setting | Value |
|---|---|
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python app.py` |


### Environment Variables

Set these in **Render → Your Service → Environment**:

| Key | Value |
|---|---|
| `IBM_API_KEY` | Your IBM Cloud API key |
| `IBM_PROJECT_ID` | Your watsonx.ai project ID |
| `IBM_URL` | `https://au-syd.ml.cloud.ibm.com` |
| `IBM_MODEL_ID` | e.g. `meta-llama/llama-3-3-70b-instruct` |

> Do **not** upload a `.env` file to Render — use the environment variable panel.

### Ephemeral filesystem note

Render's free tier uses an **ephemeral filesystem** — uploaded files are lost on restart. The quiz feature relies on the uploaded PDF still being on disk within the same session. For persistent storage, consider mounting a Render Disk or storing PDFs in object storage (e.g. IBM Cloud Object Storage or AWS S3).

---

## API Routes

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Renders the main upload page |
| `POST` | `/upload` | Accepts PDF + level, returns simplified notes page |
| `POST` | `/quiz` | Returns `{"html": "...", "level": "..."}` JSON — reads PDF path from session |

---

## Environment Variables Reference

| Variable | Required | Description |
|---|---|---|
| `IBM_API_KEY` | Yes | IBM Cloud API key for watsonx.ai authentication |
| `IBM_PROJECT_ID` | Yes | The watsonx.ai project that hosts your model |
| `IBM_URL` | Yes | Regional watsonx.ai endpoint URL |
| `IBM_MODEL_ID` | Yes | Granite model ID (e.g. `meta-llama/llama-3-3-70b-instruct`) |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push and open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.
