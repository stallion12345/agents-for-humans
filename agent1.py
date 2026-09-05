from dotenv import load_dotenv
load_dotenv()

import os
print("KEY LOADED:", os.getenv("GROQ_API_KEY"))
from strands import Agent
from strands.models.litellm import LiteLLMModel
from tools import extract_product_keyword, find_price, map_keyword_to_tier

model = LiteLLMModel(model_id="groq/openai/gpt-oss-20b")

agent1 = Agent(
    model=model,
    system_prompt=(
        "You are the enquiry intake agent for O.C. Manjos, an electrical merchant. "
        "Given a customer enquiry, extract the product being asked about, "
        "look up its price, and determine its qualification tier. "
        "Use your tools to do this — don't guess prices or categories yourself."
    ),
    tools=[extract_product_keyword, find_price, map_keyword_to_tier],
)

response = agent1("A customer asked: 'Do you have 1.5mm cable?'")
print(response)