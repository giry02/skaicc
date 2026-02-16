import os
import google.generativeai as genai
import base64
from utils.logger import logger
from PIL import Image

class BaseAgent:
    def __init__(self, name, role, system_prompt):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        # Gemini history format is different, but we'll adapt.
        # We'll store history for logging, but Gemini manages session object better.
        self.history = [] 
        
        # Load API Key
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash') # The most stable Free Tier model
            # Create a chat session with system instruction if possible, or just start chat
            self.chat_session = self.model.start_chat(history=[])
            # Send system prompt as first message (partial workaround as system instruction support varies)
            self.chat_session.send_message(f"System Role: {role}\nInstructions: {system_prompt}")
        else:
            self.model = None
            logger.log_system(f"Warning: No GOOGLE_API_KEY found. Agent {self.name} will use Mock Mode.")

    def _encode_image(self, image_path):
        # Gemini accepts PIL Image directly or mime types
        try:
             return Image.open(image_path)
        except Exception as e:
             logger.log_system(f"이미지 로드 실패: {e}")
             return None

    def think(self, context):
        """Simulates the thinking process."""
        thought = f"{context}에 대해 어떻게 처리할지 고민 중..."
        logger.log_thought(self.role, thought)
        return thought

    def chat(self, user_input, image_path=None):
        """Sends a message to the LLM and gets a response. Supports Image input."""
        
        # Log the action
        if image_path:
             logger.log_action(self.role, f"메시지(이미지 포함) 처리 중...")
        else:
             logger.log_action(self.role, f"메시지 처리 중: {user_input[:50]}...")

        response_text = ""
        
        if self.model:
            try:
                # Prepare content
                content_parts = []
                
                # Image Content
                if image_path and os.path.exists(image_path):
                    img = self._encode_image(image_path)
                    if img:
                        content_parts.append(img)
                        logger.log_action(self.role, f"이미지 분석 중: {os.path.basename(image_path)}")
                
                # Text Content
                content_parts.append(str(user_input))

                # Debug log
                # logger.log_system(f"Debug: calling Gemini with {len(content_parts)} parts")
                
                response = self.chat_session.send_message(content_parts)
                response_text = response.text
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                logger.log_system(f"Error calling Gemini LLM: {e}\n{error_trace}")
                response_text = "죄송합니다. 오류가 발생하여 응답할 수 없습니다."
        else:
            # Mock Response for testing without API Key
            response_text = f"[{self.role}] 가상 응답입니다. (API Key 없음)"

        # Log completion
        # logger.log_message(self.role, "User", response_text[:50] + "...")
        return response_text

    def send_message(self, recipient_agent, message):
        """Sends a message to another agent and logs it."""
        logger.log_message(self.role, recipient_agent.role, message)
        response = recipient_agent.receive_message(self, message)
        return response

    def receive_message(self, sender_agent, message):
        """Receives a message from another agent."""
        # Here we could process the message with the LLM
        response = self.chat(f"[{sender_agent.role}로부터의 메시지]: {message}")
        logger.log_message(self.role, sender_agent.role, response) # Reply log
        return response
