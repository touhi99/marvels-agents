from langchain_openai import ChatOpenAI
from langchain.chains import GraphCypherQAChain
import os 
from etl import load_graph

def load_llm(temperature=0.1):
    #gpt-4-turbo 
    #gpt-4-0125-preview
    llm = ChatOpenAI(model_name="gpt-4-turbo", openai_api_key=os.environ["OPENAI_API_KEY"], temperature=temperature)
    return llm

def get_cypher_chain():
    graph = load_graph()
    graph.refresh_schema()
    cypher_chain = GraphCypherQAChain.from_llm(
        cypher_llm = load_llm(temperature=0),
        qa_llm = load_llm(temperature=0.2), graph=graph, verbose=True
    )
    return cypher_chain
