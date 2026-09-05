from dotenv import load_dotenv
load_dotenv()

from strands import Agent
from strands.models.litellm import LiteLLMModel
from tools import qualify_full_enquiry

model = LiteLLMModel(model_id="groq/openai/gpt-oss-20b")

agent2 = Agent(
    model=model,
    system_prompt=(
        "You are the qualification agent for O.C. Manjos, an electrical merchant. "
        "Call qualify_full_enquiry with the customer's enquiry text, then state "
        "clearly whether it's qualified and why, using the tool's output. Use ₦ "
        "for currency, always. Currently only handles A&B brand Distribution "
        "Boards — if a customer names a different brand, say pricing isn't "
        "available for that brand yet rather than guessing."
    ),
    tools=[qualify_full_enquiry],
)

test_enquiries = [
    "A customer asked: 'Do you have A&B Distribution Board D8 three phase plastic base, I need 3 units'",
    "A customer asked: 'I need A&B Distribution Board D6 single phase iron base'",
    "A customer asked: 'Do you have ABB D8 three phase distribution board'",
]

for enquiry in test_enquiries:
    print(f"\n--- {enquiry} ---")
    response = agent2(enquiry)
    print(response)