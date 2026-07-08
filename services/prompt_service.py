_MARKDOWN_FORMAT = """
Output Format Rules (follow exactly):
- Output valid Markdown only. Do NOT output HTML.
- Use # for main headings, ## for subheadings, ### for sub-subheadings.
- Use bullet lists (- item) and numbered lists (1. item) appropriately.
- Use **bold** for key terms.
- Use tables (| col | col | syntax) where comparisons or structured data are useful.
- Separate sections with a blank line.
- Do not output raw LaTeX or code unless the source material contains code.
"""


def build_prompt(text, level):

    level = level.lower().strip()

    if level == "beginner":

        return f"""You are an experienced university professor and educational content creator.

Your task is to convert the following academic notes into beginner-friendly study material.

{_MARKDOWN_FORMAT}

Requirements:
- Explain every concept in very simple English.
- Assume the student has no prior knowledge.
- Preserve every important topic from the original notes — do NOT omit any concept.
- Explain technical terms immediately after introducing them.
- Use short paragraphs and bullet points wherever appropriate.
- Give simple real-life examples for each concept.
- Explain why each concept is important.
- Make the content engaging and easy to read.
- Produce detailed study notes rather than a short summary.
- Cover the entire document.

Course Material:

{text}
"""

    elif level == "intermediate":

        return f"""You are a university professor.

Rewrite the following academic notes for an intermediate learner who has basic familiarity with the subject.

{_MARKDOWN_FORMAT}

Requirements:
- Preserve all important concepts.
- Explain complex ideas clearly using proper technical terminology with brief explanations.
- Organize the output using headings and bullet points.
- Add examples where they improve understanding.
- Do not oversimplify — the reader has foundational knowledge.
- Produce detailed study notes that cover the entire document.

Course Material:

{text}
"""

    elif level == "advanced":

        return f"""You are an expert academic instructor.

Rewrite the following notes for an advanced university student with solid subject knowledge.

{_MARKDOWN_FORMAT}

Requirements:
- Preserve all technical accuracy and use professional terminology.
- Expand important concepts with deeper explanations.
- Explain relationships and dependencies between concepts.
- Add practical applications where appropriate.
- Produce comprehensive notes suitable for exam revision.
- Cover the entire document.

Course Material:

{text}
"""

    elif level == "expert":

        return f"""You are writing graduate-level academic material for an expert audience.

{_MARKDOWN_FORMAT}

Requirements:
- Preserve all technical details with precise academic terminology.
- Do not simplify concepts — the audience is deeply familiar with the subject.
- Expand important ideas using deeper explanations, theoretical insights, and nuances.
- Maintain formal academic writing style.
- Organize using clear headings and structured lists.
- Produce complete lecture-quality notes that cover the entire document.

Course Material:

{text}
"""

    else:

        return f"""Explain the following academic content clearly using Markdown headings and bullet points.

{text}
"""


def build_quiz_prompt(text, level):

    level = level.lower().strip()

    level_desc = {
        "beginner": "a beginner with no prior knowledge — use simple language and straightforward questions",
        "intermediate": "an intermediate learner with basic subject knowledge — mix conceptual and applied questions",
        "advanced": "an advanced student with solid subject knowledge — include analytical and application questions",
        "expert": "an expert/graduate-level student — include deep conceptual, critical-thinking, and edge-case questions",
    }.get(level, "a general learner")

    return f"""You are an expert university professor creating a quiz based on the provided course material.

The quiz is for {level_desc}.

Output Format Rules (follow exactly):
- Output valid Markdown only. Do NOT output HTML.
- Number each question: 1., 2., 3., etc.
- For multiple-choice questions use this exact format:
  A) option
  B) option
  C) option
  D) option
- After ALL questions, add a section headed: ## Answer Key
- In the Answer Key, list: 1. A) correct answer text, 2. C) correct answer text, etc.
- Include a one-sentence explanation for each answer in the Answer Key.

Requirements:
- Generate exactly 10 questions based on the course material below.
- Mix question types: multiple-choice (at least 6) and short-answer (up to 4).
- Questions must cover the key concepts from the material.
- Do not invent facts not present in the material.
- Vary difficulty across the questions to suit the stated level.

Course Material:

{text}
"""
