from langchain.agents import initialize_agent
from langchain.agents import AgentType
from tools import get_tools
from llm_chain import load_llm


def agent_executor_func():
    mrkl = initialize_agent(
        get_tools(), 
        load_llm(),
        agent=AgentType.OPENAI_FUNCTIONS, 
        verbose=True
    )
    return mrkl