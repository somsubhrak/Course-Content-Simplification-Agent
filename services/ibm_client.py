from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from config import (
    IBM_API_KEY,
    IBM_PROJECT_ID,
    IBM_URL,
    IBM_MODEL_ID,
)

credentials = Credentials(
    api_key=IBM_API_KEY,
    url=IBM_URL
)

model = ModelInference(
    model_id=IBM_MODEL_ID,
    credentials=credentials,
    project_id=IBM_PROJECT_ID
)