from strands import Agent
from strands.models.litellm import LiteLLMModel

model = LiteLLMModel(
    model_id="groq/openai/gpt-oss-20b"
)

agent = Agent(model=model, system_prompt="You are a helpful assistant.")
response = agent("What is 2+2?")
print(response)