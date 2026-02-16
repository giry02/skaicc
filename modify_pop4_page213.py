import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: PPT Page 213 수정 (디자인 정합성 확보)]
# 1. 수정 사항: 이미지의 파란색 배경은 보이스(말덩어리)를 표시한 것으로, 
#    실제 디자인은 '화이트 클린 UI' 테마를 유지하도록 수정함.
# 2. 역할: 타 페이지(move_service_intro.html)와 동일한 헤더 및 텍스트 스타일 적용.
# =================================================================================

BASE_DIR = 'completed'
OUTPUT_FILE = os.path.join(BASE_DIR, 'page213_move_type.html')
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
    <!-- 상단 헤더 -->
    <div class="pt-4 px-4 pb-2 bg-white z-30 flex justify-between items-center h-14 shrink-0">
        <button class="p-2 -ml-2 text-gray-800 active:bg-gray-100 rounded-full transition-colors" onclick="history.back()">
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
            <!-- 타이틀 영역 (이미지의 보이스 내용을 텍스트로 반영) -->
            <div class="mb-8 pt-2" id="target-anchor">
                <h2 class="text-[20px] font-extrabold text-[#1a1a1a] leading-tight">원하시는 이동 유형을<br/>선택해 주세요.</h2>
            </div>
            
            <div class="space-y-3 mb-8">
                <!-- 이동 유형 버튼 (화이트 테마) -->
                <div class="relative group">
                    <button class="w-full py-4 px-6 rounded-xl border-2 text-[17px] font-bold transition-all flex items-center justify-start bg-white border-gray-100 text-gray-700 hover:border-gray-200 active:scale-[0.98] type-btn" onclick="selectType(this, 'same')">같은 방에서 재연결</button>
                    <button class="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-blue-500 active:bg-blue-50 rounded-full" onclick="showInfo('same')">
                        <i class="w-5 h-5" data-lucide="info"></i>
                    </button>
                </div>
                <div class="relative group">
                    <button class="w-full py-4 px-6 rounded-xl border-2 text-[17px] font-bold transition-all flex items-center justify-start bg-white border-gray-100 text-gray-700 hover:border-gray-200 active:scale-[0.98] type-btn" onclick="selectType(this, 'other')">다른 방으로 이동</button>
                    <button class="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-blue-500 active:bg-blue-50 rounded-full" onclick="showInfo('other')">
                        <i class="w-5 h-5" data-lucide="info"></i>
                    </button>
                </div>
                <div class="relative group">
                    <button class="w-full py-4 px-6 rounded-xl border-2 text-[17px] font-bold transition-all flex items-center justify-start bg-white border-gray-100 text-gray-700 hover:border-gray-200 active:scale-[0.98] type-btn" onclick="selectType(this, 'interior')">인테리어 공사 재연결</button>
                    <button class="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-blue-500 active:bg-blue-50 rounded-full" onclick="showInfo('interior')">
                        <i class="w-5 h-5" data-lucide="info"></i>
                    </button>
                </div>

                <div class="pt-6">
                    <button id="apply-btn" class="w-full bg-[#E9ECEF] text-[#ADB5BD] py-4 rounded-xl text-[19px] font-bold transition-all cursor-not-allowed shadow-lg" disabled onclick="location.href='page214_move_summary.html'">선택 완료</button>
                </div>
            </div>
        </div>
        <div class="w-full h-40 shrink-0" id="bottom-spacer"></div>
    </div>

    <!-- 상세 정보 모달 -->
    <div class="hidden fixed inset-0 z-[60] flex items-center justify-center px-6" id="info-modal">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" onclick="closeInfo()"></div>
        <div class="relative bg-white rounded-2xl w-full max-w-sm overflow-hidden flex flex-col animate-slide-up shadow-2xl">
            <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                <h3 class="text-[18px] font-bold text-gray-900" id="info-title">상세 정보</h3>
                <button class="p-1 text-gray-400" onclick="closeInfo()"><i class="w-6 h-6" data-lucide="x"></i></button>
            </div>
            <div class="p-6">
                <ul class="space-y-4">
                    <li class="flex gap-3">
                        <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-[13px] font-bold shrink-0">1</span>
                        <p class="text-gray-600 text-[14px] leading-relaxed">현관문을 통해 외부로 나가지 않고 집안내에서 설치 위치를 변경하는 경우 해당 됩니다.</p>
                    </li>
                    <li class="flex gap-3">
                        <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-[13px] font-bold shrink-0">2</span>
                        <p class="text-gray-600 text-[14px] leading-relaxed">원룸, 오피스텔 등 방 호수 또는 층이 달라지는 경우는 이사 이전 신청 접수를 해주세요.</p>
                    </li>
                    <li class="flex gap-3">
                        <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-[13px] font-bold shrink-0">3</span>
                        <p class="text-gray-600 text-[14px] leading-relaxed">PC의 무선 -> 유선 연결 방식 변경에도 일부 해당 됩니다.</p>
                    </li>
                </ul>
                <button class="w-full mt-8 py-3 bg-[#5031E5] text-white rounded-xl font-bold shadow-md active:bg-blue-700" onclick="closeInfo()">확인</button>
            </div>
        </div>
    </div>

    <!-- [컴포넌트 주입 영역] -->
    <div id="swipe-area-placeholder"></div>
    <div id="modals-placeholder"></div>

    <script src="js/common_ui.js"></script>
    <script>
        let selectedType = null;
        function selectType(el, type) {
            document.querySelectorAll('.type-btn').forEach(btn => {
                btn.classList.remove('bg-[#F0F7FF]', 'border-[#2563EB]', 'text-[#2563EB]');
                btn.classList.add('bg-white', 'border-gray-100', 'text-gray-700');
            });

            el.classList.remove('bg-white', 'border-gray-100', 'text-gray-700');
            el.classList.add('bg-[#F0F7FF]', 'border-[#2563EB]', 'text-[#2563EB]');
            selectedType = type;

            const btn = document.getElementById('apply-btn');
            btn.disabled = false;
            btn.classList.remove('bg-[#E9ECEF]', 'text-[#ADB5BD]', 'cursor-not-allowed');
            btn.classList.add('bg-[#5031E5]', 'text-white', 'shadow-lg');
            btn.classList.add('active:scale-[0.98]');
        }

        function showInfo(type) {
            const modal = document.getElementById('info-modal');
            const title = document.getElementById('info-title');
            const types = {
                'same': '같은 방에서 재연결',
                'other': '다른 방으로 이동',
                'interior': '인테리어 공사 재연결'
            };
            title.innerText = types[type] || '상세 정보';
            modal.classList.remove('hidden');
        }

        function closeInfo() {
            document.getElementById('info-modal').classList.add('hidden');
        }

        initCommonUI("가정내 이동 유형을 확인하시고");
    </script>
</body>
</html>
"""

soup = BeautifulSoup(html_template, 'html.parser')

swipe_html = load_component("swipe_area")
modals_html = load_component("modals")

if swipe_html:
    placeholder = soup.find(id="swipe-area-placeholder")
    placeholder.replace_with(BeautifulSoup(swipe_html, 'html.parser'))

if modals_html:
    placeholder = soup.find(id="modals-placeholder")
    placeholder.replace_with(BeautifulSoup(modals_html, 'html.parser'))

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(str(soup))

print(f"HTML 수정 완료 (Page 213 - Design Aligned): {OUTPUT_FILE}")
