import os
import re
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: PPT Page 212 구현 (컴포넌트화 및 공용화 완료 버전)]
# 1. 공용화: CSS, JS, HTML 컴포넌트(Footer, Modals)를 외부 파일에서 로드.
# 2. 일관성: 모든 페이지가 동일한 Footer 디자인과 인터랙션 DNA를 공유.
# =================================================================================

BASE_DIR = 'completed'
OUTPUT_FILE = os.path.join(BASE_DIR, 'move_service_intro.html')
COMPONENTS_DIR = os.path.join(BASE_DIR, 'components')
JS_DIR = os.path.join(BASE_DIR, 'js')

def load_component(name):
    path = os.path.join(COMPONENTS_DIR, f"{name}.html")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

# 1. 기본 HTML 뼈대 생성
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
        <button class="p-2 -ml-2 text-gray-800 active:bg-gray-100 rounded-full transition-colors">
            <i class="w-7 h-7" data-lucide="chevron-left"></i>
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
            <div class="flex flex-col h-full bg-white px-1">
                <div class="mb-8 pt-2" id="target-anchor">
                    <h2 class="text-[20px] font-extrabold text-[#1a1a1a] leading-tight"><span class="text-black">이동 및 서비스를</span><br/>확인하고 신청해 주세요.</h2>
                </div>
                <div class="mt-8 mb-8 flex-1">
                    <div class="flex justify-center mb-8">
                        <div class="w-32 h-32 bg-gray-50 rounded-full flex items-center justify-center border border-gray-100">
                            <span class="text-4xl">📺</span>
                        </div>
                    </div>
                    <div class="bg-[#F8F9FA] rounded-xl p-6 border border-gray-100">
                        <h3 class="font-bold text-gray-900 mb-3">안내 사항</h3>
                        <ul class="text-sm text-gray-600 space-y-2 list-disc list-inside">
                            <li>댁내에서 기기 위치를 변경해 드립니다.</li>
                            <li>전문 엔지니어가 방문하여 안전하게 설치해 드립니다.</li>
                            <li>서비스 이용료가 발생할 수 있습니다.</li>
                        </ul>
                    </div>
                </div>
                <div class="mt-auto pt-4 pb-6">
                    <button class="w-full bg-[#5031E5] text-white py-4 rounded-xl text-[19px] font-bold shadow-lg hover:bg-[#4020d0] transition-colors" id="apply-btn" onclick="location.href='page213_move_selection.html'">신청하기</button>
                </div>
            </div>
        </div>
        <div class="w-full h-0 shrink-0" id="bottom-spacer"></div>
    </div>

    <!-- [컴포넌트 주입 영역] -->
    <div id="swipe-area-placeholder"></div>
    <div id="modals-placeholder"></div>

    <script src="js/common_ui.js"></script>
    <script>
        // 페이지 개별 설정 및 UI 초기화
        const pageText = "서비스 내용을 확인해 주세요.";
        initCommonUI(pageText);
    </script>
</body>
</html>
"""

soup = BeautifulSoup(html_template, 'html.parser')

# 2. 컴포넌트 로드 및 주입
print("Loading UI components...")
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

print(f"HTML 생성 완료 (컴포넌트화): {OUTPUT_FILE}")
