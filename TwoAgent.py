import asyncio
from dotenv import load_dotenv
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

async def main():
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

    writer = AssistantAgent(
        name="Writer",
        model_client=model_client,
        system_message=(
            "You are a creative technical writer. Write short, engaging "
            "explainers on complex topics. Take feedback from the Critic and adjust."
        ),
    )

    critic = AssistantAgent(
        name="Critic",
        model_client=model_client,
        system_message=(
            "You are a sharp editor. Review the Writer's draft for clarity, "
            "conciseness, and tone. Point out 1-2 specific improvements."
        ),
    )

    termination = MaxMessageTermination(max_messages=3)

    team = RoundRobinGroupChat(
        participants=[writer, critic],
        termination_condition=termination,
    )

    task = "Write a 2-sentence explanation of quantum computing for a 10-year-old."
    
    async for message in team.run_stream(task=task):
        # Check if the yielded object is a conversation message with a source
        if hasattr(message, "source"):
            print(f"\n--- [{message.source}] ---")
            print(message.content)
        else:
            # This handles the final TaskResult object at the end
            print("\n--- [Task Complete] ---")
            print(f"Stop Reason: {message.stop_reason}")

if __name__ == "__main__":
    asyncio.run(main())