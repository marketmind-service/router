import os
from langchain_openai import AzureChatOpenAI

query = AzureChatOpenAI(
    azure_endpoint=os.environ.get("endpoint"),
    api_version="2025-08-07",
    temperature=0,
)