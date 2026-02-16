from agents.roles import Planner
from utils.file_reader import read_file_content
from utils.logger import logger
import os

def analyze_ppt():
    # File Path
    filename = "SKB_AICC_콜봇_멀티모달_화면기획서_v1.73_250211.pptx"
    project_root = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(project_root, "inputs", filename)
    
    logger.log_system(f"파일 분석 시작: {filename}")
    
    # Read Content
    ppt_content = read_file_content(file_path)
    if "[Error]" in ppt_content:
        logger.log_system(ppt_content)
        return

    # Initialize Planner
    planner = Planner()
    
    # Specific Instruction
    instruction = """
    위 PPT 내용을 분석해줘.
    중요한 규칙: 
    1. 'a'로 시작하는 구역(예: a01, a-section 등)은 '나중에 고도화할 예정인 미래 기능'으로 분류해.
    2. 나머지 구역은 '이미 구현된 기능'으로 분류해서 학습해.
    
    결과를 다음 형식으로 요약해줘:
    - [학습 완료] 이미 구현된 기능 요약
    - [미래 계획] 'a' 구역 (고도화 예정) 요약
    """
    
    # Run Analysis
    logger.log_action("Planner", "기획서 분석 및 학습 중...")
    analysis_result = planner.chat(f"PPT 내용:\n{ppt_content[:15000]}\n\n{instruction}") # Limit text length just in case
    
    # Output Result
    print("\n" + "="*50)
    print(analysis_result)
    print("="*50 + "\n")
    
    # Save to file
    with open("analysis_result.md", "w", encoding="utf-8") as f:
        f.write(analysis_result)
    logger.log_system("분석 결과가 'analysis_result.md'에 저장되었습니다.")

if __name__ == "__main__":
    analyze_ppt()
