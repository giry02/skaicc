import sys
import os
import glob

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from workflow.orchestrator import Orchestrator
from utils.file_reader import read_file_content
from utils.logger import logger
import config  # Ensure environment variables are loaded

def analyze_all_inputs():
    project_root = os.path.dirname(os.path.abspath(__file__))
    inputs_dir = os.path.join(project_root, "inputs")
    
    if not os.path.exists(inputs_dir):
        logger.log_system(f"inputs 폴더가 없습니다: {inputs_dir}")
        return

    # Initialize Orchestrator to access agents
    orchestrator = Orchestrator()
    planner = orchestrator.planner
    
    knowledge_base = []

    # 1. Process PPTX Files
    pptx_files = glob.glob(os.path.join(inputs_dir, "*.pptx"))
    for pptx_path in pptx_files:
        logger.log_system(f"PPT 파일 분석 중: {os.path.basename(pptx_path)}")
        content = read_file_content(pptx_path)
        if "[Error]" not in content:
             knowledge_base.append(f"--- PPT Content: {os.path.basename(pptx_path)} ---\n{content[:10000]}...") # Limit text
        else:
             logger.log_system(f"PPT 읽기 실패: {content}")

    # 2. Process Specific Scenario Images
    special_images = [
        "멀티모달-프로세스-시나리오.png", 
        "SKB-멀티모달_콜봇(내부 작업용).png"
    ]
    
    for img_name in special_images:
        img_path = os.path.join(inputs_dir, img_name)
        if os.path.exists(img_path):
            logger.log_system(f"주요 시나리오 이미지 분석 중: {img_name}")
            # Ask Planner to analyze the image
            analysis = planner.chat(
                "이 이미지는 '멀티모달 프로세스 시나리오' 또는 '내부 작업용 프로세스'입니다. 단계별 흐름을 상세히 분석해서 설명해줘.",
                image_path=img_path
            )
            knowledge_base.append(f"--- Image Analysis: {img_name} ---\n{analysis}")

    # 3. Process Design Drafts (FD*.png)
    # Since there are many, we process a few representative ones or batch them?
    # For now, let's pick the first 5 to understand the style.
    fd_files = glob.glob(os.path.join(inputs_dir, "FD*.png"))
    fd_files.sort() # Ensure consistent order
    
    if fd_files:
        logger.log_system(f"디자인 시안(FD) {len(fd_files)}개 발견. 주요 샘플 3개만 상세 분석합니다.")
        
        for i, fd_path in enumerate(fd_files[:3]):
            filename = os.path.basename(fd_path)
            logger.log_system(f"디자인 시안 분석 중 ({i+1}/3): {filename}")
            style_analysis = planner.chat(
                "이것은 이전 디자인 시안(FD)입니다. UI 레이아웃, 컬러톤, 폰트 스타일 등을 분석해서 '디자인 스타일 가이드' 참고용으로 정리해줘.",
                image_path=fd_path
            )
            knowledge_base.append(f"--- Design Draft Analysis: {filename} ---\n{style_analysis}")

    # 4. Broadcast Knowledge
    combined_knowledge = "\n\n".join(knowledge_base)
    
    instruction = """
    [전체 학습 지시사항]
    위 내용은 프로젝트의 기획서(PPT), 프로세스 시나리오(이미지), 디자인 시안(이미지)을 분석한 결과입니다.
    
    1. PPT 내용에서 'a' 구역은 '미래 고도화' 대상입니다. 이는 제외하고 구현 범위를 잡으세요.
    2. '프로세스 시나리오'의 흐름을 숙지하여 개발 로직에 반영하세요.
    3. '디자인 시안'의 스타일을 참고하여 퍼블리싱 및 디자인 작업을 수행하세요.
    """
    
    # Save Knowledge for main.py to usage
    with open("project_context.txt", "w", encoding="utf-8") as f:
        f.write(combined_knowledge)
    logger.log_system("전체 문맥 데이터가 'project_context.txt'에 저장되었습니다.")

    # 4. Broadcast Knowledge (This only affects current process, but good for testing)
    orchestrator.broadcast_context(combined_knowledge, instruction)
    
    # 5. Final Report by Planner
    logger.log_system("--- 최종 분석 리포트 생성 ---")
    final_report = planner.chat("""
    지금까지 학습한 모든 내용(PPT, 프로세스 이미지, 디자인 시안)을 종합하여 다음 내용을 정리해:
    1. [프로세스 요약] 멀티모달 콜봇의 핵심 작동 흐름
    2. [구현 범위] 현재 구현해야 할 기능 목록 (a구역 제외)
    3. [디자인 컨셉] 유지해야 할 디자인 톤앤매너
    """)
    
    with open("comprehensive_analysis.md", "w", encoding="utf-8") as f:
        f.write("# 종합 분석 리포트\n\n")
        f.write(final_report)
    
    logger.log_system("분석 완료! 결과는 'comprehensive_analysis.md'에 저장됨.")

if __name__ == "__main__":
    try:
        analyze_all_inputs()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
