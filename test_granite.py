from services.granite_service import ask_granite

prompt = """
Say exactly:

IBM Granite connection successful!

Then introduce yourself in one sentence.
"""

response = ask_granite(prompt)

print(response)