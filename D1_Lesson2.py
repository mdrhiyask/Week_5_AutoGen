from dotenv import load_dotenv
load_dotenv()

# Build the model client (the wire to the brain)
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage

model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")

# Ask the brain one simple question
reply =  await model_client.create(
    [UserMessage(content="Say hello in 3 words.", source="user")]
)

print(reply.content)


