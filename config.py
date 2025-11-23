# backend/config.py

import os
from langchain_openai import AzureChatOpenAI

AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")

# This is the **deployment name**, not the base model name.
# Whatever you created in Azure portal like "gpt-5-nano" or "gpt-4o-mini-1"
AZURE_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt5-nano-deployment")

query = AzureChatOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    temperature=0,
)