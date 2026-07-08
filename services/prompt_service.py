def build_prompt(text, level):

    level = level.lower().strip()

    if level == "beginner":

        return f"""
You are an experienced university professor and educational content creator.

Your task is to convert the following academic notes into beginner-friendly study material.
Output Format:

- Use Markdown.
- Use # for main headings.
- Use ## for subheadings.
- Use bullet lists.
- Use numbered lists where appropriate.
- Use tables if useful.
- Do not output HTML.

Requirements:

- Explain every concept in very simple English.
- Assume the student has no prior knowledge.
- Preserve every important topic from the original notes.
- Do NOT omit any concept.
- Explain technical terms immediately after introducing them.
- Use short paragraphs.
- Use bullet points wherever appropriate.
- Give simple real-life examples.
- Explain why each concept is important.
- Make the content engaging and easy to read.
- Produce detailed study notes rather than a short summary.
- Cover the entire document.

Course Material:

{text}
"""

    elif level == "intermediate":

        return f"""
You are a university professor.

Rewrite the following academic notes for an intermediate learner.

Requirements:

- Preserve all important concepts.
- Explain complex ideas clearly.
- Use proper technical terminology with explanations.
- Organize the output using headings and bullet points.
- Add examples where they improve understanding.
- Do not oversimplify.
- Produce detailed study notes.

Course Material:

{text}
"""

    elif level == "advanced":

        return f"""
You are an expert academic instructor.

Rewrite the following notes for an advanced university student.

Requirements:

- Preserve all technical accuracy.
- Use professional terminology.
- Expand important concepts with additional explanation.
- Explain relationships between concepts.
- Use headings and bullet points.
- Add practical applications where appropriate.
- Produce comprehensive notes suitable for revision.

Course Material:

{text}
"""

    elif level == "expert":

        return f"""
You are writing graduate-level academic material.

Requirements:

- Preserve all technical details.
- Use precise academic terminology.
- Do not simplify concepts unless necessary.
- Expand important ideas using deeper explanations.
- Maintain formal academic writing.
- Organize using clear headings.
- Produce complete lecture-quality notes.
- Include theoretical insights wherever possible.

Course Material:

{text}
"""

    else:

        return f"""
Explain the following academic content clearly.

{text}
"""