import logging
import sys
import json
import os
import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define Role Colors
ROLE_COLORS = {
    "PM": Fore.BLUE,
    "Captain Jack": Fore.BLUE,
    "PL": Fore.CYAN,
    "Planner": Fore.GREEN,
    "Alice": Fore.GREEN,
    "Designer": Fore.MAGENTA,
    "Diva": Fore.MAGENTA,
    "Publisher": Fore.YELLOW,
    "Pixel": Fore.YELLOW,
    "Developer": Fore.RED,
    "Neo": Fore.RED,
    "QA": Fore.LIGHTRED_EX,
    "Sniper": Fore.LIGHTRED_EX,
    "Tester": Fore.LIGHTGREEN_EX,
    "User": Fore.WHITE,
    "System": Fore.LIGHTBLACK_EX
}

class AgentLogger:
    def __init__(self, name="AgentSystem"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.callbacks = []  # List of callback functions for external outputs (e.g., Telegram)
        
        # Force UTF-8 for console output on Windows
        if sys.platform == 'win32':
            sys.stdout.reconfigure(encoding='utf-8')

        # Stream Handler (Console)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)

        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs", "chat_history.json")
        self._init_json_log()

    def _init_json_log(self):
        """Initializes the JSON log file."""
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _log_to_json(self, entry):
        """Appends a log entry to the JSON file."""
        try:
            with open(self.log_file, 'r+', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                
                data.append(entry)
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.truncate()
        except Exception as e:
            pass # Fail silently for JSON logging to avoid breaking main flow

    def log_thought(self, role, thought):
        """Logs the internal thought process of an agent."""
        color = ROLE_COLORS.get(role, Fore.WHITE)
        self.logger.info(f"{color}[{role}] 💭 {thought}{Style.RESET_ALL}")
        
        self._log_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "thought",
            "role": role,
            "content": thought
        })
        
        self._trigger_callbacks({
            "type": "thought",
            "role": role,
            "content": thought
        })

    def _trigger_callbacks(self, entry):
        """Executes all registered callbacks with the log entry."""
        for callback in self.callbacks:
            try:
                callback(entry)
            except Exception:
                pass  # Ignore callback errors to keep system stable
    
    def register_callback(self, callback):
        """Registers a function to be called on new log events."""
        self.callbacks.append(callback)

    def log_action(self, role, action):
        """Logs an action taken by an agent."""
        color = ROLE_COLORS.get(role, Fore.WHITE)
        self.logger.info(f"{color}[{role}] ⚙️ {action}{Style.RESET_ALL}")

        self._log_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "action",
            "role": role,
            "content": action
        })
        
        self._trigger_callbacks({
            "type": "action",
            "role": role,
            "content": action
        })

    def log_message(self, sender, receiver, message):
        """Logs a message sent from one agent to another."""
        color = ROLE_COLORS.get(sender, Fore.WHITE)
        self.logger.info(f"{color}[{sender} -> {receiver}] 💬 \"{message}\"{Style.RESET_ALL}")

        self._log_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "message",
            "sender": sender,
            "receiver": receiver,
            "content": message
        })
        
        self._trigger_callbacks({
            "type": "message",
            "sender": sender,
            "receiver": receiver,
            "content": message
        })

    def log_system(self, message):
        """Logs a system message."""
        self.logger.info(f"{Fore.LIGHTBLACK_EX}[System] 📢 {message}{Style.RESET_ALL}")

        self._log_to_json({
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "system",
            "role": "System",
            "content": message
        })
        
        self._trigger_callbacks({
            "type": "system",
            "role": "System",
            "content": message
        })

# Global Info Logger
logger = AgentLogger()
