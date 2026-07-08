
from services.ibm_client import model

def ask_granite(prompt):

    params = {
    "max_new_tokens": 1024,
    "temperature": 0.3,
    "top_p": 0.9,
    "repetition_penalty": 1.05
    }

    response = model.generate_text(
    prompt=prompt,
    params=params
    )
    return response