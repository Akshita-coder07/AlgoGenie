import os
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from config.constant import MODEL
load_dotenv()


api_key = os.getenv('GROQ_API_KEY')

def get_model_client():
    model_client = OpenAIChatCompletionClient(
        model=MODEL, 
        api_key=api_key,
        base_url='https://api.groq.com/openai/v1',
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown"
        }
    )
    return model_client