import os
import sys
import asyncio
import threading
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from utils.logger import logger
from workflow.orchestrator import Orchestrator
import config

# Global state
orchestrator = None # Will be initialized per request or globally
current_chat_id = None
loop = None
application = None

# Input handling state
user_input_event = threading.Event()
user_input_value = None
is_waiting_for_input = False

def telegram_log_callback(entry):
    """Callback function to send logs to Telegram."""
    global current_chat_id, loop
    if current_chat_id and loop:
        # [Mobile Optimization] Strict Filter Logic
        if entry['type'] == 'system':
             # Only show SERIOUS errors. Ignore general system info like "context sharing".
             if any(keyword in entry['content'] for keyword in ["Error", "Warning", "오류", "Fatal"]):
                  message = f"🚨 *System*: {entry['content']}"
             else:
                  return
        elif entry['type'] == 'message':
            # Only show messages directed to User
            if entry.get('receiver') == 'User':
                message = f"🗣️ *{entry['sender']}*: {entry['content']}"
            else:
                return
        else:
            # Ignore 'action', 'thought', etc. completely
            return
            
        if message:
            asyncio.run_coroutine_threadsafe(
                send_telegram_message(current_chat_id, message), 
                loop
            )

async def send_telegram_message(chat_id, text):
    """Sends a message to Telegram (Async)."""
    try:
        max_len = 4000
        for i in range(0, len(text), max_len):
            await application.bot.send_message(chat_id=chat_id, text=text[i:i+max_len])
    except Exception as e:
        print(f"Failed to send telegram message: {e}")

def telegram_input_handler(prompt):
    """
    Custom input handler for Orchestrator.
    This runs in the Orchestrator thread.
    """
    global current_chat_id, loop, user_input_event, user_input_value, is_waiting_for_input
    
    # 1. Send the prompt to Telegram
    asyncio.run_coroutine_threadsafe(
        send_telegram_message(current_chat_id, f"❓ {prompt}"), 
        loop
    )
    
    # 2. Wait for user input
    logger.log_system("사용자 입력을 기다리는 중...")
    is_waiting_for_input = True
    user_input_event.clear()
    user_input_event.wait() # Blocks here until set() is called in handle_message
    
    # 3. Return the input
    is_waiting_for_input = False
    return user_input_value

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command."""
    global current_chat_id
    current_chat_id = update.effective_chat.id
    logger.register_callback(telegram_log_callback)
    
    welcome_msg = (
        "👋 안녕하세요! **Multi-Agent Dev Team** 모바일 인터페이스입니다.\n\n"
        "저는 당신의 프로젝트 매니저 **Captain Jack**과 연결해 드립니다.\n"
        "명령을 내리시려면 텍스트를 입력해주세요.\n"
        "(예: '투두 리스트 앱 만들어줘', '현재 진행 상황 알려줘')"
    )
    await context.bot.send_message(chat_id=current_chat_id, text=welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for incoming text messages."""
    global current_chat_id, user_input_event, user_input_value, is_waiting_for_input
    current_chat_id = update.effective_chat.id
    user_text = update.message.text
    
    # If the orchestrator is waiting for input, provide it
    if is_waiting_for_input:
        user_input_value = user_text
        user_input_event.set() # Unblock the orchestrator thread
        # Acknowledge receipt (optional, maybe too chatty)
        # await context.bot.send_message(chat_id=current_chat_id, text="✅ 입력 확인")
        return

    # Otherwise, start a new workflow
    await context.bot.send_message(chat_id=current_chat_id, text=f"✅ '{user_text}' 접수 완료. 에이전트팀을 소집합니다...")
    
    # Run Orchestrator in a separate thread
    thread = threading.Thread(target=run_orchestrator, args=(user_text,))
    thread.start()

def run_orchestrator(user_request):
    """Runs the orchestrator workflow."""
    global orchestrator
    try:
        # Initialize Orchestrator with our custom input handler
        orchestrator = Orchestrator(input_handler=telegram_input_handler)
        
        # Check context
        if os.path.exists("project_context.txt"):
             with open("project_context.txt", "r", encoding="utf-8") as f:
                context = f.read()
                orchestrator.broadcast_context(context, "사전에 학습된 프로젝트 전체 맥락")

        # Start Waterfall
        final_output, test_report = orchestrator.run_waterfall(user_request)
        
        # Save Results
        with open("result_code.html", "w", encoding="utf-8") as f:
            f.write(final_output)
        
        logger.log_system("결과물이 생성되었습니다. PC에서 result_code.html을 확인하세요.")
        
    except Exception as e:
        import traceback
        trace = traceback.format_exc()
        logger.log_system(f"오류 발생: {str(e)}\n{trace}")

if __name__ == '__main__':
    if not config.TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found.")
        sys.exit(1)

    print("🤖 Telegram Bot Starting...")
    
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    print("✅ Bot is polling...")
    application.run_polling()
