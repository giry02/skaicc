import sys
import os

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from workflow.orchestrator import Orchestrator
    from utils.file_reader import read_file_content
    from utils.logger import logger
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"sys.path: {sys.path}")
    sys.exit(1)

def learn_and_analyze():
    print("스크립트 시작...")
    
    # 1. Load File
    filename = "SKB_AICC_콜봇_멀티모달_화면기획서_v1.73_250211.pptx"
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "inputs", filename)
    
    logger.log_system(f"파일 로딩 시도: {file_path}")
    
    # Check file existence explicitly
    if not os.path.exists(file_path):
        logger.log_system(f"파일이 존재하지 않습니다: {file_path}")
        return

    ppt_content = read_file_content(file_path)
    
    if "[Error]" in ppt_content:
        logger.log_system(ppt_content)
        if "python-pptx" in ppt_content:
             print("Please run: pip install python-pptx")
        return

    # 2. Add specific instructions
    instruction = """
    [중요 규칙]
    1. 'a'로 시작하는 구역 ID(예: a01, a-02 등)는 '추후 고도화 예정'인 기능입니다. 지금은 구현하지 않습니다.
    2. 그 외 나머지 구역은 '이미 구현된 기능'입니다. 이 내용을 바탕으로 업무를 수행하십시오.
    3. 전체 내용을 숙지하고 팀원들과 협업 시 참고하십시오.
    """

    # 3. Initialize & Broadcast
    orchestrator = Orchestrator()
    # orchestrator.introduce_agents() # Skip intro for speed
    
    orchestrator.broadcast_context(ppt_content[:15000], instruction) 

    # 4. Planner Analysis Task
    logger.log_system("--- Planner에게 분석 요청 ---")
    planner = orchestrator.planner
    analysis_prompt = """
    학습한 기획서 내용을 바탕으로 다음 두 가지를 정리해서 보고해줘:
    1. [구현됨] 우리가 이미 가지고 있는 기능 목록
    2. [미래/고도화] 'a' 구역으로 분류된, 나중에 개발할 기능 목록
    """
    
    analysis_result = planner.chat(analysis_prompt)

    # Save format
    with open("multimodal_analysis.md", "w", encoding="utf-8") as f:
        f.write("# 멀티모달 기획서 분석 리포트\n\n")
        f.write(analysis_result)
    
    logger.log_system("분석 결과가 'multimodal_analysis.md'에 저장되었습니다.")
    print("분석 완료.")

if __name__ == "__main__":
    try:
        learn_and_analyze()
    except Exception as e:
        print(f"Runtime Error: {e}")
        import traceback
        traceback.print_exc()
