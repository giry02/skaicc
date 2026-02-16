from utils.logger import logger
import os

print("Testing logger...")
logger.log_system("Logger test message")

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "chat_history.json")
if os.path.exists(log_path):
    print(f"SUCCESS: Log file created at {log_path}")
    with open(log_path, 'r', encoding='utf-8') as f:
        print(f"Content: {f.read()}")
else:
    print(f"FAILURE: Log file not found at {log_path}")
