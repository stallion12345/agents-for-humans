from dotenv import load_dotenv
load_dotenv()

from strands import Agent
from strands.models.litellm import LiteLLMModel
from tools import (
    qualify_full_enquiry,
    count_weekly_enquiries_by_category,
    recommend_restock,
)

model = LiteLLMModel(model_id="groq/openai/gpt-oss-20b")

# Agent 1+2 combined: intake + qualification
intake_qualify_agent = Agent(
    model=model,
    system_prompt=(
        "You are the enquiry intake and qualification agent for O.C. Manjos. "
        "Call qualify_full_enquiry with the customer's enquiry text, then state "
        "clearly whether it's qualified and why. Use ₦ for currency. Currently "
        "only handles A&B brand Distribution Boards — if a customer names a "
        "different brand, say pricing isn't available for that brand yet."
    ),
    tools=[qualify_full_enquiry],
)

# Agent 3: restock recommendation
restock_agent = Agent(
    model=model,
    system_prompt=(
        "You are the restock recommendation agent for O.C. Manjos. Call "
        "count_weekly_enquiries_by_category, then for Distribution Board "
        "specifically call recommend_restock with that count. State clearly "
        "whether a restock is recommended, the quantity, and why. Use ₦."
    ),
    tools=[count_weekly_enquiries_by_category, recommend_restock],
)

def run_pipeline(enquiry_text: str):
    print("=== INTAKE & QUALIFICATION ===")
    qualify_result = intake_qualify_agent(enquiry_text)
    print(qualify_result)

    print("\n=== RESTOCK CHECK ===")
    restock_result = restock_agent("Check if this category needs restocking based on this week's enquiries.")
    print(restock_result)

if __name__ == "__main__":
    run_pipeline("A customer asked: 'Do you have A&B Distribution Board D8 three phase plastic base, I need 3 units'")