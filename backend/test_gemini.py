import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("API Key not found in .env")
else:
    genai.configure(api_key=api_key)
    print("Listing ALL models:")
    try:
        models = genai.list_models()
        for m in models:
            print(f"- Name: {m.name}, Methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"Error: {e}")
