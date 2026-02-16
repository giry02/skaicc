import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
LLM_MODEL = "gpt-4o"  # Default model

# System Configuration
project_root = os.path.dirname(os.path.abspath(__file__))
logs_dir = os.path.join(project_root, "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
