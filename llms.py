from langchain_openai import ChatOpenAI
import os 

def load_llm():
    llm = ChatOpenAI(model_name="gpt-4-0125-preview", openai_api_key=os.environ["OPENAI_API_KEY"])
    return llm