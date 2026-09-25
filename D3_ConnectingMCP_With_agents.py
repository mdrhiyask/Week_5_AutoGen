from dotenv import load_dotenv
load_dotenv()

import asyncio
import sys
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools

async def main():

    # The OpenAI brain (same as every other notebook)
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    # 1) How to start our MCP server.
    #    We use sys.executable (the SAME Python running this notebook) so the
    #    server starts with the same packages installed. Do NOT just write "python"
    #    - that can pick a different Python that does not have the mcp library.
    #    read_timeout_seconds is raised to 30 so a slow first start does not time out.
    server = StdioServerParams(
        command=sys.executable,
        args=["my_mcp_server.py"],
        read_timeout_seconds=30,
    )
    # 2) Connect and collect the tools it offers
    tools = await mcp_server_tools(server)
    print("Tools from MCP server:", [t.name for t in tools])

    # 3) Give the MCP tools to the agent
    shopper = AssistantAgent(
        name="shopper",
        model_client=model_client,
        tools=tools,                    # <-- tools that came from the MCP server
        reflect_on_tool_use=True,       # turn the tool result into a nice sentence
        system_message="You help with grocery prices. Use your tools to check prices.",
    )

    # 4) Ask something that needs the tool
    result = await shopper.run(task="What is the price of milk today?")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())  

    """ Connecting MCP With Agents"""     