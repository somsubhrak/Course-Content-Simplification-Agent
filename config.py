import os
from dotenv import load_dotenv

load_dotenv()

IBM_API_KEY: str = os.environ["IBM_API_KEY"]
IBM_PROJECT_ID: str = os.environ["IBM_PROJECT_ID"]
IBM_URL: str = os.environ["IBM_URL"]
IBM_MODEL_ID: str = os.environ["IBM_MODEL_ID"]