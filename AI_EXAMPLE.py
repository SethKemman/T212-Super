from T212_Super import Client
from dotenv import load_dotenv
from google import genai
import json
import os

client = Client()

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

aiClient = genai.Client(api_key=GEMINI_API_KEY)

def ReadableJSON(arg):
    return json.dumps(arg, indent=3, sort_keys=False)

x = ReadableJSON(client.positions.getPositions())

#x = ReadableJSON(client.account.summary())

#Normal interaction example
#interaction = aiClient.interactions.create(model="gemini-3.8-flash",
#    input=f"You are a financial advisor. Take a neutral, unbiased stance. See my portfolio: {x}. Based on recent movement and news of the stock. What would you adivse me to do for each position and why? BUY/HOLD/SELL?"
#    )

#Streaming interaction example
stream = aiClient.interactions.create(
    model="gemini-3.8-flash",
    input=f"You are a financial advisor. Take a neutral, unbiased stance. See my portfolio: {x}. Based on recent movement and news of the stock. What would you adivse me to do for each position and why? BUY/HOLD/SELL?",
    stream=True,
)
print(chr(27) + "[2J")

usage = None

for event in stream:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            print(event.delta.text, end="", flush=True)
    elif event.event_type == "interaction.completed":
        usage = event.interaction.usage
    elif event.event_type == "step.stop" and getattr(event, "usage", None):
        usage = event.usage

print("")
tokenpricepermillion = 0.75
if usage:
    print("\n--- Token Usage ---")
    print(f"Input tokens:  {usage.total_input_tokens}")
    print(f"Output tokens: {usage.total_output_tokens}")
    print(f"Total tokens:  {usage.total_tokens}; ${((usage.total_tokens / 1000000) * 0.75)}")
