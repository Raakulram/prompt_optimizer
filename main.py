from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY missing in .env")

print("✅ API KEY LOADED")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """You are a Prompt Optimizer Agent.

Convert vague prompts into structured prompts.

Output format:

=== Structured Prompt ===
Role:
Objective:
Context:
Instructions:
Constraints:
Output Format:
=========================
"""

@app.post("/optimize")
def optimize(req: PromptRequest):
    try:
        full_prompt = SYSTEM_PROMPT + "\nUser Prompt: " + req.prompt

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=full_prompt
        )

        return {"result": response.text}

    except Exception as e:
        print("ERROR:", e)
        return {"result": f"Error: {str(e)}"}