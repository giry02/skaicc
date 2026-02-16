import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: PPT Page 214 구현 (컴포넌트화 및 공용화 완료 버전)]
# 1. 공용화: CSS, JS, HTML 컴포넌트를 사용하여 중복 제거 및 일관성 확보.
# 2. 역할: Page 214 특화 컨텐츠(신청 내역 및 유의사항) 주입.
# =================================================================================

BASE_DIR = 'completed'
OUTPUT_FILE = os.path.join(BASE_DIR, 'page214_move_summary.html')
COMPONENTS_DIR = os.path.join(BASE_DIR, 'components')

def load_component(name):
    path = os.path.join(COMPONENTS_DIR, f"{name}.html")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# 1. 기본 HTML 뼈대 생성 (공통 레이아웃 반영)
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
    <!-- 상단 헤더 -->
    <div class="pt-4 px-4 pb-2 bg-white z-30 flex justify-between items-center h-14 shrink-0">
        <button class="p-2 -ml-2 text-gray-800 active:bg-gray-100 rounded-full transition-colors" onclick="history.back()">
            <i class="w-7 h-7" data-lucide="chevron-left"></i>
        </button>
        <h1 class="text-[18px] font-bold text-gray-900">신청 내용 확인</h1>
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
            <div class="mb-8 pt-2" id="target-anchor">
                <h2 class="text-[20px] font-extrabold text-[#1a1a1a] leading-tight">신청을 완료해<br/>주시기 바랍니다.</h2>
            </div>
            
            <div class="flex-1">
                <!-- 신청 내역 카드 -->
                <div class="bg-gray-50 rounded-2xl p-6 border border-gray-100 mb-6">
                    <div class="space-y-4">
                        <div class="flex justify-between items-start">
                            <span class="text-gray-500 font-medium">신청 서비스</span>
                            <span class="text-gray-900 font-bold text-right text-[15px]">가정 내 PC/TV 이동</span>
                        </div>
                        <div class="w-full h-[1px] bg-gray-200"></div>
                        <div class="flex justify-between items-start">
                            <span class="text-gray-500 font-medium">상세 안내</span>
                            <div class="text-right">
                                <p class="text-gray-900 font-bold text-[15px]">댁내 거실 -> 침실 1</p>
                                <p class="text-gray-400 text-[13px] mt-1">전문 엔지니어 방문 설치</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 안내 및 유의사항 -->
                <div class="flex gap-2 items-start bg-blue-50/50 rounded-xl p-4 border border-blue-100/50">
                    <i class="w-5 h-5 text-blue-500 shrink-0 mt-0.5" data-lucide="info"></i>
                    <div class="text-[14px] text-blue-800 leading-relaxed font-medium">
                        <p>전문 기사가 방문하여 기기 이동 및 배선 정리를 도와드립니다.</p>
                        <p class="mt-1 opacity-70">※ 셋톱박스 및 공유기 등 장비 이동 포함</p>
                    </div>
                </div>

                <!-- 하단 버튼 -->
                <div class="mt-10 mb-8">
                    <button class="w-full bg-[#5031E5] text-white py-4 rounded-xl text-[19px] font-bold shadow-lg hover:bg-[#4020d0] transition-colors" onclick="location.href='visit_schedule_modal.html'">신청하기</button>
                </div>
            </div>
        </div>
        <div class="w-full h-40 shrink-0" id="bottom-spacer"></div>
    </div>

    <!-- [컴포넌트 주입 영역] -->
    <div id="swipe-area-placeholder"></div>
    <div id="modals-placeholder"></div>

    <script src="js/common_ui.js"></script>
    <script>
        // 공통 UI 초기화
        initCommonUI("신청 내용을 확인해 주세요.");
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

print(f"HTML 생성 완료 (Page 214): {OUTPUT_FILE}")
