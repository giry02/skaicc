from agents.base_agent import BaseAgent
from agents.prompts import *
from utils.logger import logger

class ProjectManager(BaseAgent):
    def __init__(self):
        super().__init__("Project Manager", "PM", PM_PROMPT)

    def create_project_plan(self, user_request):
        self.think(f"사용자 요청('{user_request}') 분석 및 프로젝트 계획 수립")
        plan = self.chat(f"사용자 요청: {user_request}\n위 요청에 대한 전체 프로젝트 계획과 일정을 수립해줘.")
        return plan

class ProjectLeader(BaseAgent):
    def __init__(self):
        super().__init__("Project Leader", "PL", PL_PROMPT)

    def assign_tasks(self, plan):
        self.think("프로젝트 계획을 바탕으로 팀원 업무 분장")
        assignments = self.chat(f"프로젝트 계획: {plan}\n각 팀원(기획, 디자인, 퍼블리싱, 개발, QA)에게 구체적인 업무를 지시해줘.")
        return assignments

class Planner(BaseAgent):
    def __init__(self):
        super().__init__("Planner", "Planner", PLANNER_PROMPT)

    def create_spec(self, idea):
        self.think("아이디어 구체화 및 상세 기획안 작성")
        spec = self.chat(f"아이디어: {idea}\n개발자와 상의할 수 있도록 상세 기획안(기능 명세, 화면 구성 등)을 작성해줘. 논리적 근거를 포함해야 해.")
        return spec

    def consult_feasibility(self, developer_agent, spec):
        self.think("개발자에게 기술적 실현 가능성 문의")
        query = f"이 기획안({spec[:100]}...)의 기술적 실현 가능성을 검토해줘."
        response = self.send_message(developer_agent, query)
        return response

class Designer(BaseAgent):
    def __init__(self):
        super().__init__("Designer", "Designer", DESIGNER_PROMPT)

    def create_style_guide(self, spec):
        self.think("기획안을 바탕으로 디자인 스타일 가이드 작성")
        guide = self.chat(f"기획안: {spec}\n사용자에게 제안할 디자인 스타일 가이드(색상, 폰트, 무드 등)를 작성해줘.")
        return guide

class Publisher(BaseAgent):
    def __init__(self):
        super().__init__("Publisher", "Publisher", PUBLISHER_PROMPT)

    def publish_html(self, design_guide, spec):
        self.think("디자인 가이드와 기획안을 바탕으로 HTML/CSS 코딩")
        code = self.chat(f"디자인 가이드: {design_guide}\n기획안: {spec}\nHTML/CSS 코드를 작성해줘. 주석을 꼼꼼히 달고 재사용성을 고려해.")
        return code

class Developer(BaseAgent):
    def __init__(self):
        super().__init__("Developer", "Developer", DEVELOPER_PROMPT)

    def check_feasibility(self, spec_summary):
        self.think("기획안 기술적 검토")
        check = self.chat(f"기획안 요약: {spec_summary}\n이 기능이 기술적으로 가능한지, 보안 이슈는 없는지 검토해줘.")
        return check

    def write_logic(self, html_code, spec):
        self.think("HTML 코드에 기능 로직 구현")
        code = self.chat(f"HTML 코드: {html_code}\n기획안: {spec}\n필요한 JavaScript 또는 Python 로직을 구현해줘. 보안을 고려하고 한글 주석을 달아.")
        return code

    def receive_message(self, sender_agent, message):
        # Override to specifically handle feasibility checks
        if "실현 가능성" in message:
            return self.check_feasibility(message)
        return super().receive_message(sender_agent, message)

class QA(BaseAgent):
    def __init__(self):
        super().__init__("QA", "QA", QA_PROMPT)

    def review_code(self, code):
        self.think("코드 품질 및 보안 취약점 점검")
        review = self.chat(f"코드: {code}\n버그나 보안 취약점이 있는지 리뷰해줘.")
        return review

class Tester(BaseAgent):
    def __init__(self):
        super().__init__("Tester", "Tester", QA_PROMPT) # Reusing QA prompt for now but acting as Tester

    def test_scenario(self, review_result):
        self.think("테스트 시나리오 실행")
        test_report = self.chat(f"QA 리뷰: {review_result}\n실제 사용 관점에서 테스트 시나리오를 짜고 예상되는 문제를 보고해줘.")
        return test_report
