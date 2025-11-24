from langchain_openai import AzureChatOpenAI
import os

print(os.environ["AZURE_OPENAI_ENDPOINT"])
print(os.environ["AZURE_OPENAI_DEPLOYMENT"])

model = AzureChatOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    api_version="2024-10-21",
)

from langchain_core.messages import HumanMessage

print(model.invoke([HumanMessage(content="Say 'ping'")]))
