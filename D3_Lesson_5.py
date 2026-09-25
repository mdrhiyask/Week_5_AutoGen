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

    # The AI interviewer with clear instructions (prompt engineering!)
    interviewer = AssistantAgent(
                        name="interviewer",
                        model_client=model_client,
                        system_message=(
        "You are a friendly job interviewer for a beginner Python developer role. "
        "Ask ONE short question at a time and wait for the answer. "
        "Ask 3 questions in total. After the 3rd answer, give short, kind feedback "
        "and finish with the exact words: END OF INTERVIEW."
    ),
    )

    # You answer the questions
    candidate = UserProxyAgent(name="candidate")

    # Stop when the interviewer says END OF INTERVIEW
    interview = RoundRobinGroupChat(
    [interviewer, candidate],
    termination_condition=TextMentionTermination("END OF INTERVIEW"),
    )

    # Start the interview. Type your answers when the box appears.
    await Console(interview.run_stream(task="Please start the interview."))
if __name__ == "__main__":
    asyncio.run(main())  

    """ AI Interviewer Project"""      