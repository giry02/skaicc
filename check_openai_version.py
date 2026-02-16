
import openai
import os
import sys

print(f"Python executable: {sys.executable}")
print(f"OpenAI version: {openai.__version__}")

try:
    from openai import OpenAI
    print("Successfully imported OpenAI client class.")
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    print("Client initialized.")
    
    # Try a simple call
    # response = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": "Hello"}]
    # )
    # print("Call successful.")
except ImportError:
    print("Could not import OpenAI client class (maybe version < 1.0.0?)")
except Exception as e:
    print(f"Error: {e}")

try:
    print("Checking for legacy ChatCompletion usage...")
    openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello"}])
except Exception as e:
    print(f"Legacy call failed as expected (or not?): {e}")
