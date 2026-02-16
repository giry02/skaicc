import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: PPT Page 217 구현 (방문 일정 확인 및 전송)]
# 1. 디자인 규칙: 집 모양 로고(Home), 상단 타이틀, 2줄 규칙(타이핑 후 바운스).
# 2. 바운스 텍스트 크기: 24px (유저 요청에 따른 2px 하향 조정 반영).
# =================================================================================

BASE_DIR = 'completed'
OUTPUT_FILE = os.path.join(BASE_DIR, 'page217_schedule_confirm.html')
COMPONENTS_DIR = os.path.join(BASE_DIR, 'components')

def load_component(name):
    path = os.path.join(COMPONENTS_DIR, f"{name}.html")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

html_template = """<!DOCTYPE html>
<html class="h-full" lang="ko">
<head>
    <meta charset="utf-8"/>
    <meta content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" name="viewport"/>
    <title>SK브로드밴드 AI상담사 콜비</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet"/>
    <link rel="stylesheet" href="css/common.css">
</head>
<body class="h-full w-full bg-white overflow-hidden flex flex-col">
    <!-- 상단 헤더 (집 모양 로고 반영) -->
    <div class="pt-4 px-4 pb-2 bg-white z-30 flex justify-between items-center h-14 shrink-0">
        <button class="p-2 -ml-2 text-gray-800 active:bg-gray-100 rounded-full transition-colors" onclick="location.href='move_service_intro.html'">
            <i class="w-7 h-7" data-lucide="home"></i>
        </button>
        <h1 class="text-[18px] font-bold text-gray-900">가정 내 PC/TV 이동</h1>
        <div class="flex items-center gap-1 cursor-pointer px-2 py-1" onclick="resetMain(true)">
            <span class="text-sm font-bold text-gray-900">종료</span>
            <i class="text-gray-900 w-4 h-4" data-lucide="phone-off"></i>
        </div>
    </div>

    <!-- 메인 컨테이너 -->
    <div class="flex-1 overflow-y-auto scrollbar-hide px-6 pt-4 relative flex flex-col scroll-smooth" id="main-scroll-container">
        <!-- 타이핑 텍스트 영역 -->
        <div class="min-h-[30px] flex items-center justify-start mb-2 shrink-0" id="typing-area">
            <span class="text-[#2563EB] font-bold text-[17px]" id="typing-text"></span>
            <span class="inline-block w-[2px] h-5 bg-[#2563EB] ml-1 cursor-blink" id="cursor"></span>
        </div>

        <!-- 바운스 콘텐츠 -->
        <div class="w-full opacity-0" id="main-content-body">
            <div class="mb-5 pt-1" id="target-anchor">
                <h2 class="text-[20px] font-extrabold text-[#1a1a1a] leading-tight">서비스 매니저에게 전달 사항이 있다면<br/>작성 후 상담예약하기를 눌러주세요.</h2>
            </div>
            
            <div class="flex-1 pb-4">
                <!-- 방문 일정 정보 카드 (사용자 요청에 따라 더 컴팩트하게 변경) -->
                <div class="bg-gray-50 rounded-2xl p-5 border border-gray-100 mb-5">
                    <div class="flex flex-col gap-4">
                        <div class="flex justify-between items-center">
                            <span class="text-gray-500 font-medium text-[14px]">방문희망일</span>
                            <span class="text-gray-900 font-bold text-[16px]">2025.10.10(월)</span>
                        </div>
                        <div class="w-full h-[1px] bg-gray-200 opacity-60"></div>
                        <div class="flex justify-between items-center">
                            <span class="text-gray-500 font-medium text-[14px] shrink-0">방문희망시간</span>
                            <div class="flex gap-1.5 overflow-x-auto scrollbar-hide">
                                <span class="bg-white border border-gray-200 px-2 py-1 rounded text-gray-700 font-bold text-[12px] whitespace-nowrap">13~14시</span>
                                <span class="bg-white border border-gray-200 px-2 py-1 rounded text-gray-700 font-bold text-[12px] whitespace-nowrap">14~15시</span>
                                <span class="bg-white border border-gray-200 px-2 py-1 rounded text-gray-700 font-bold text-[12px] whitespace-nowrap">15~16시</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 전달 사항 입력 영역 (상단 여백 및 높이 줄임) -->
                <div class="mb-6">
                    <label class="block text-gray-900 font-bold mb-2 text-[15px]">서비스 매니저 전달사항</label>
                    <textarea class="w-full h-24 bg-white border border-gray-200 rounded-xl p-4 text-[14px] focus:border-[#5031E5] focus:ring-1 focus:ring-[#5031E5] outline-none transition-all resize-none placeholder-gray-300" placeholder="전달하실 내용이 있다면 적어주세요."></textarea>
                </div>

                <!-- 하단 버튼 세트 (간격 최적화) -->
                <div class="space-y-2">
                    <button class="w-full bg-[#5031E5] text-white py-4 rounded-xl text-[18px] font-bold shadow-lg hover:bg-[#4020d0] active:scale-[0.98] transition-all" onclick="location.href='#'">상담예약하기</button>
                    <button class="w-full bg-white text-gray-400 border border-gray-100 py-3.5 rounded-xl text-[16px] font-bold hover:bg-gray-50 active:scale-[0.98] transition-all" onclick="history.back()">취소하기</button>
                </div>
            </div>
        </div>
        <div class="w-full h-20 shrink-0" id="bottom-spacer"></div>
    </div>

    <!-- [컴포넌트 주입 영역] -->
    <div id="swipe-area-placeholder"></div>
    <div id="modals-placeholder"></div>

    <script src="js/common_ui.js"></script>
    <script>
        // 공통 UI 초기화 (첫 줄 타이핑 텍스트 입력)
        initCommonUI("신청하신 내용이 맞는 지 확인해 주세요.");
    </script>
</body>
</html>
"""

soup = BeautifulSoup(html_template, 'html.parser')

# 2. 컴포넌트 로드 및 주입
swipe_html = load_component("swipe_area")
modals_html = load_component("modals")

if swipe_html:
    placeholder = soup.find(id="swipe-area-placeholder")
    placeholder.replace_with(BeautifulSoup(swipe_html, 'html.parser'))

if modals_html:
    placeholder = soup.find(id="modals-placeholder")
    placeholder.replace_with(BeautifulSoup(modals_html, 'html.parser'))

# 3. 저장
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f"HTML 생성 완료 (Page 217): {OUTPUT_FILE}")
