import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

def add(a: int, b: int) -> int:
    """Add two numbers and return the result."""
    print ('addition')
    return a + b

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    math_agent = AssistantAgent(
        name="math_agent",
        model_client=model_client,
        tools=[add],
        reflect_on_tool_use=True,
        system_message="You are a math helper. Use your tools to calculate.",
    )

    # Clean indentation (4 spaces inside main):
    result = await math_agent.run(task="What is 124 - 376?")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())