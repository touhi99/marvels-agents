from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools_old import get_tools
from llm_chain import load_llm
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)


def agent_executor_func():
    llm = load_llm()
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an MSF assistant, you are asked to use when finding a character and their info. Character name can be with whitespace seperated but in data may be together or vice versa.\
                so if an entry is not found, please try either with adding a whitespace or removing. For example, if input is Invisible woman, search 'Invisible Woman' or 'InvisibleWoman' whichever returns a hit",
            ),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    tools = get_tools()
    llm_with_tools = llm.bind_tools(tools)

    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
    )


    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor