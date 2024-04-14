from langchain.agents import Tool
from llm_chain import get_cypher_chain


def get_tools():
    tools = [
        # Tool(
        #     name="Tasks",
        #     func=vector_qa.run,
        #     description="""Useful when you need to answer questions about descriptions of tasks.
        #     Not useful for counting the number of tasks.
        #     Use full question as input.
        #     """,
        # ),
        Tool(
            name="Graph",
            func=get_cypher_chain().run,
            description="""Useful when you need to answer questions about MSF character information ie, \
            speed, power, iso, trait etc.
            """,
        ),
    ]    
    return tools

