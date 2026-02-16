
import asyncio
import sys
import unittest
from unittest.mock import MagicMock, patch

# Adjust path to import telegram_interface
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import telegram_interface

class TestTelegramFilter(unittest.TestCase):
    def setUp(self):
        # Mock global variables
        telegram_interface.current_chat_id = 12345
        telegram_interface.loop = asyncio.new_event_loop()
        
        # Mock application.bot.send_message
        telegram_interface.application = MagicMock()
        telegram_interface.application.bot.send_message = MagicMock()

    def tearDown(self):
        telegram_interface.loop.close()

    def test_filter_user_message(self):
        """Test that messages TO User are sent."""
        entry = {
            'type': 'message',
            'sender': 'PM',
            'receiver': 'User',
            'content': 'Hello User'
        }
        
        # We need to mock send_telegram_message to verify it was called, 
        # or mock asyncio.run_coroutine_threadsafe
        with patch('asyncio.run_coroutine_threadsafe') as mock_run:
            telegram_interface.telegram_log_callback(entry)
            mock_run.assert_called_once()
            
    def test_filter_internal_message(self):
        """Test that messages TO other agents are ignored."""
        entry = {
            'type': 'message',
            'sender': 'PM',
            'receiver': 'Developer',
            'content': 'Check this spec'
        }
        
        with patch('asyncio.run_coroutine_threadsafe') as mock_run:
            telegram_interface.telegram_log_callback(entry)
            mock_run.assert_not_called()

    def test_filter_system_log(self):
        """Test that normal system logs are ignored."""
        entry = {
            'type': 'system',
            'content': 'System initializing...'
        }
        
        with patch('asyncio.run_coroutine_threadsafe') as mock_run:
            telegram_interface.telegram_log_callback(entry)
            mock_run.assert_not_called()

    def test_allow_error_log(self):
        """Test that Error system logs are allowed."""
        entry = {
            'type': 'system',
            'content': 'Error: Something went wrong'
        }
        
        with patch('asyncio.run_coroutine_threadsafe') as mock_run:
            telegram_interface.telegram_log_callback(entry)
            mock_run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
