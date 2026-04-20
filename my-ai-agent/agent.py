import os
import datetime
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- AGENT CONFIGURATION --- #

# Define the Persona / System Prompt
SYSTEM_PROMPT = """You are a highly capable, autonomous AI Assistant.
Your goal is to converse with the user naturally and effectively.
You have access to tools that you should use whenever necessary to accomplish tasks.
Always be concise, professional, and clear in your responses.
"""

# --- TOOLS REGISTRY --- #

def get_current_time() -> str:
    """Returns the exact current date and time."""
    now = datetime.datetime.now()
    return f"The current system time is {now.strftime('%Y-%m-%d %H:%M:%S')}"

# Note: The google-genai library will automatically inspect the type hints 
# and docstrings of the functions in this list to teach the agent how to use them!
AGENT_TOOLS = [
    get_current_time
]

# --- MAIN AGENT LOOP --- #

def run_agent():
    """Initializes the connection and runs the continuous terminal chat loop."""
    # Ensure API key exists
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("❗ Error: Please set your GEMINI_API_KEY in the .env file.")
        print("Hint: Copy .env.example to .env and insert your actual Google Gemini API key.")
        return

    # Initialize the Gemini GenAI client
    client = genai.Client(api_key=api_key)
    
    # Configure the Chat session with our system profile and tools
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=AGENT_TOOLS,
        temperature=0.7,
    )
    
    print("\n" + "="*50)
    print("🤖 AI AGENT CLI HAS STARTED")
    print("="*50)
    print("Type your message and hit Enter. Type 'exit' or 'quit' to stop.\n")
    
    try:
        # Start a persistent chat session to maintain conversation history (memory)
        chat = client.chats.create(model="gemini-2.5-flash", config=config)
        
        while True:
            # 1. Wait for user input
            user_input = input("\n👤 You: ")
            
            # Allow graceful exit
            if user_input.lower().strip() in ["exit", "quit", "q"]:
                print("\nAgent shutting down. Goodbye!")
                break
                
            if not user_input.strip():
                continue
                
            print("🤖 Agent is thinking...")
            
            # 2. Send the message. The SDK natively handles the tool-calling loop.
            # If the model decides to use 'get_current_time', the SDK will execute it 
            # and pipe the result back to the model automatically!
            response = chat.send_message(user_input)
            
            # 3. Print the final response
            print(f"🤖 Agent: {response.text}")
            
    except Exception as e:
        print(f"\n❗ Oops, an error occurred: {e}")

if __name__ == "__main__":
    run_agent()
