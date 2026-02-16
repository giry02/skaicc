from agents.roles import *
from utils.logger import logger
import time

class Orchestrator:
    def __init__(self, input_handler=None):
        self.input_handler = input_handler if input_handler else input
        self.pm = ProjectManager()
        self.pl = ProjectLeader()
        self.planner = Planner()
        self.designer = Designer()
        self.publisher = Publisher()
        self.developer = Developer()
        self.qa = QA()
        self.tester = Tester()
        self.all_agents = [self.pm, self.pl, self.planner, self.designer, self.publisher, self.developer, self.qa, self.tester]

    def introduce_agents(self):
        logger.log_system("팀원들이 자기소개를 시작합니다.")
        for agent in self.all_agents:
            logger.log_action(agent.role, f"안녕하세요! 저는 {agent.role}입니다. {agent.system_prompt.splitlines()[2]}")
            time.sleep(0.5)

    def broadcast_context(self, context_text, instruction=""):
        """
        Sends a shared context/knowledge to ALL agents.
        """
        logger.log_system("📢 [전체 공지] 모든 에이전트에게 배경 지식을 공유합니다...")
        
        full_message = f"""
[공유된 배경 지식(Context)]
{context_text}

[지시사항]
{instruction}
"""
        
        for agent in self.all_agents:
            # We inject this into their history as a system or user message
            agent.history.append({"role": "user", "content": f"시스템 알림: 다음 배경 지식을 학습하십시오.\n{full_message}"})
            logger.log_action(agent.role, "배경 지식 학습 완료.")

    def ask_user(self, agent_role, question):
        """Asks the user a question and waits for input."""
        logger.log_message(agent_role, "User", question)
        print(f"\n[{agent_role}가 묻습니다] {question}")
        response = self.input_handler(f"[{agent_role}에게 답변] > ")
        logger.log_message("User", agent_role, response)
        return response

    def run_waterfall(self, user_request):
        logger.log_system("=== 폭포수(Waterfall) 개발 프로세스 시작 ===")
        
        # Step 1: Planning
        logger.log_system("--- 1단계: 기획 (Planning) ---")
        project_plan = self.pm.create_project_plan(user_request)
        
        # Interactive Check
        self.ask_user("PM", f"프로젝트 계획을 세웠습니다.\n{project_plan[:100]}...\n이대로 진행할까요?")
        
        task_assignment = self.pl.assign_tasks(project_plan)
        logger.log_message("PM", "User", f"업무 분장 완료: {task_assignment[:100]}...")

        detailed_spec = self.planner.create_spec(user_request)
        
        # Interactive Check
        user_feedback = self.ask_user("Planner", f"기획안이 나왔습니다.\n{detailed_spec[:100]}...\n수정할 부분이 있나요? (없으면 엔터)")
        if user_feedback.strip():
             detailed_spec = self.planner.create_spec(f"{user_request} (수정 요청: {user_feedback})")

        # Feasibility check loop
        check_count = 0
        while check_count < 2:
            feasibility = self.planner.consult_feasibility(self.developer, detailed_spec)
            if "불가능" in feasibility or "어렵" in feasibility:
                logger.log_action("Planner", "개발자 의견 반영하여 기획 수정 중...")
                detailed_spec = self.planner.create_spec(f"{user_request} (수정 요청: {feasibility})")
                check_count += 1
            else:
                break

        # Step 2: Design
        logger.log_system("--- 2단계: 디자인 (Design) ---")
        style_guide = self.designer.create_style_guide(detailed_spec)
        
        # Interactive Check
        self.ask_user("Designer", f"스타일 가이드 어때요? (예: {style_guide[:50]}...)\n마음에 드시나요?")

        # Step 3: Publishing
        logger.log_system("--- 3단계: 퍼블리싱 (Publishing) ---")
        html_code = self.publisher.publish_html(style_guide, detailed_spec)
        
        # Step 4: Development
        logger.log_system("--- 4단계: 개발 (Development) ---")
        final_code = self.developer.write_logic(html_code, detailed_spec)

        # Step 5: Test & QA
        logger.log_system("--- 5단계: 테스트 (QA/Test) ---")
        code_review = self.qa.review_code(final_code)
        test_report = self.tester.test_scenario(code_review)

        # Final Report
        logger.log_system("=== 프로젝트 완료 보고 ===")
        self.ask_user("PM", "프로젝트가 성공적으로 완료되었습니다. 최종 결과물과 테스트 리포트를 확인해주세요.")
        
        return final_code, test_report
