from dotenv import load_dotenv
load_dotenv()

import json
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    idea_agent = AssistantAgent(name="idea_agent", model_client=model_client,
                            system_message="Suggest one simple business idea, or improve it if asked.")
    critic = AssistantAgent(name="critic", model_client=model_client,
                        system_message="If the idea is realistic, reply APPROVE. Else suggest one improvement.")

    team = RoundRobinGroupChat(
             [idea_agent, critic],
             termination_condition=TextMentionTermination("APPROVE") | MaxMessageTermination(6),
    )

    # Watch the WHOLE TEAM work live, member by member
    await Console(team.run_stream(task="Give me a small business idea for a college student."))

if __name__ == "__main__":
    asyncio.run(main())  

    """ Observing Team Agents """  