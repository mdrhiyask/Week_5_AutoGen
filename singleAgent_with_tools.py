import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

# Define a tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny and 22°C."

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    
    # Create an agent with the tool attached
    agent = AssistantAgent(
        name="weather_assistant",
        model_client=model_client,
        tools=[get_weather],
        system_message="You are a helpful assistant that provides weather updates."
    )

    response = await agent.run(task="What's the weather in Chennai?")
    print(response.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())