from dotenv import load_dotenv
load_dotenv()

import json
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main():

    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    """ agent = AssistantAgent(name="assistant", model_client=model_client,
                       system_message="You are a helpful assistant with a good memory.")

    # Tell the agent a fact in this conversation
    await agent.run(task="Remember that my favourite number is 7.")

    # SAVE the state to a file
    state = await agent.save_state()
    with open("agent_state.json", "w") as f:
        json.dump(state, f)

    #print("Saved the conversation to agent_state.json")"""

    # Imagine the program closed. Now we make a NEW agent and LOAD the saved state.
    new_agent = AssistantAgent(name="assistant", model_client=model_client,
                           system_message="You are a helpful assistant with a good memory.")

    with open("agent_state.json") as f:
        saved = json.load(f)

    await new_agent.load_state(saved)     # load the old conversation

    # It should still remember the favourite number
    result = await new_agent.run(task="What is my favourite number?")
    print(result.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())  

    """ Managing states """  