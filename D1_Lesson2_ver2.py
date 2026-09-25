import asyncio
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

load_dotenv()

# Build the model client
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

async def main():
    # Ask the brain one simple question
    reply = await model_client.create(
        [UserMessage(content="Say hello in 3 words.", source="user")]
    )
    print(reply.content)

# Run the async main function
if __name__ == "__main__":
    asyncio.run(main())