from langchain_openai import AzureChatOpenAI
import os

print("endpoint:", repr(os.environ.get("azure_openai_endpoint")))
print("deployment:", repr(os.environ.get("azure_openai_deployment")))

print(os.environ["AZURE_OPENAI_ENDPOINT"])
print(os.environ["AZURE_OPENAI_DEPLOYMENT"])

model = AzureChatOpenAI(
    azure_endpoint=os.environ["azure_openai_endpoint"].strip(),
    azure_deployment=os.environ["azure_openai_deployment"].strip(),
    api_version="2024-10-21",
    temperature=0,
)

from langchain_core.messages import HumanMessage
print(model.invoke([HumanMessage(content="Say 'ping'")]))