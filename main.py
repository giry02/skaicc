from workflow.orchestrator import Orchestrator
from utils.logger import logger
import sys
import os
import config  # Ensure env vars are loaded

def main():
    logger.log_system("시스템 초기화 중...")
    orchestrator = Orchestrator()
    
    # 0. Load Knowledge if exists
    if os.path.exists("project_context.txt"):
        logger.log_system("기존 학습 데이터(project_context.txt)를 발견했습니다. 에이전트에게 주입합니다.")
        with open("project_context.txt", "r", encoding="utf-8") as f:
            context = f.read()
            orchestrator.broadcast_context(context, "사전에 학습된 프로젝트 전체 맥락입니다. (PPT, 디자인, 프로세스 등)")

    # 1. Self-Introduction
    orchestrator.introduce_agents()
    
    # 2. User Input
    logger.log_system("프로젝트 의뢰를 기다리고 있습니다.")
    print("\n[User] (프로젝트 아이디어를 입력하세요. 예: '투두 리스트 웹앱 만들어줘')")
    
    try:
        user_request = input("> ")
    except EOFError:
        user_request = "테스트 프로젝트: 간단한 계산기 웹앱" # Default for non-interactive environments
    
    if not user_request:
        user_request = "테스트 프로젝트"

    # 2.1 File Input (Optional)
    print("\n[User] (참조할 파일이 있다면 경로를 입력하세요. 없으면 엔터)")
    file_path = input("> ").strip()
    if file_path:
        from utils.file_reader import read_file_content
        file_content = read_file_content(file_path)
        if "[Error]" not in file_content:
            logger.log_system(f"파일 내용을 모든 에이전트에게 공유합니다: {file_path}")
            orchestrator.broadcast_context(file_content, "사용자가 제공한 참고 파일입니다. 프로젝트 진행 시 이 내용을 숙지하십시오.")
        else:
            logger.log_system(file_content)

    # 3. Validation & Confirmation
    logger.log_message("PM", "User", f"요청하신 프로젝트: '{user_request}'를 접수했습니다. 진행하시겠습니까? (y/n)")
    # For simulation purposes, we assume 'y'
    # confirm = input("> ")
    # if confirm.lower() != 'y':
    #     logger.log_system("프로젝트가 취소되었습니다.")
    #     return

    # 4. Run Waterfall Process
    final_output, test_report = orchestrator.run_waterfall(user_request)
    
    # 5. Save Results
    with open("result_code.html", "w", encoding="utf-8") as f:
        f.write(final_output)
    
    with open("test_report.txt", "w", encoding="utf-8") as f:
        f.write(test_report)
        
    logger.log_system("결과물이 'result_code.html' 및 'test_report.txt'에 저장되었습니다.")

if __name__ == "__main__":
    main()
