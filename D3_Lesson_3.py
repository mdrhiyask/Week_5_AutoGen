from dotenv import load_dotenv
load_dotenv()

import asyncio
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    # The AI assistant
    assistant = AssistantAgent(
    name="assistant",
    model_client=model_client,
    system_message="You help plan a small party. Ask the user short questions and suggest ideas.",
    )

    # YOU. When it is this agent's turn, a box appears for you to type.
    user = UserProxyAgent(name="user")

    # Stop when YOU type the word DONE
    team = RoundRobinGroupChat([assistant, user], termination_condition=TextMentionTermination("DONE"))

    # Try it: answer the assistant's questions. Type DONE when you are happy.
    await Console(team.run_stream(task="Help me plan a birthday party."))

if __name__ == "__main__":
    asyncio.run(main())  

    """Human in the loop concepts"""  