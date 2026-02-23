// [공통 UI 스크립트] AICC 멀티모달 프로젝트 전용

// 전역 변수로 모달 요소들 선언 (초기화는 loadAgentOverlay 후 진행)
let searchModal, listeningModal, resultModal, failModal, categoryModal;
let typingTextEl, cursorEl, mainContentBody, floatingBanner, robotContainer, swipeGuide, scrollContainer, spacer;

function initCommonUI(textToType) {
    // 1. 에이전트 오버레이 주입
    if (typeof AGENT_OVERLAY_HTML !== 'undefined') {
        const overlayContainer = document.createElement('div');
        overlayContainer.innerHTML = AGENT_OVERLAY_HTML;
        document.body.appendChild(overlayContainer);
    } else {
        console.warn("AGENT_OVERLAY_HTML is not defined. Make sure agent_overlay.js is included.");
    }

    // 2. 아이콘 초기화 (동적 주입된 아이콘 포함)
    lucide.createIcons();

    // 3. 요소 참조 가져오기
    typingTextEl = document.getElementById('typing-text');
    cursorEl = document.getElementById('cursor');
    mainContentBody = document.getElementById('main-content-body');
    floatingBanner = document.getElementById('floating-banner');
    robotContainer = document.getElementById('robot-container');
    swipeGuide = document.getElementById('swipe-guide');
    scrollContainer = document.getElementById('main-scroll-container');
    spacer = document.getElementById('bottom-spacer');

    searchModal = document.getElementById('search-modal');
    listeningModal = document.getElementById('listening-modal');
    resultModal = document.getElementById('result-modal');
    failModal = document.getElementById('fail-modal');
    categoryModal = document.getElementById('category-modal');

    // 4. 스와이프 이벤트 초기화
    initSwipeEvents();

    // 5. [추가] 저장된 폰트 크기 즉시 적용 (모션 깨짐 방지)
    if (window.applyCurrentFontSize) {
        window.applyCurrentFontSize();
    }

    // 6. 타이핑 효과 시작
    let typingTimer;
    let index = 0;

    function type() {
        if (!typingTextEl) return;
        if (index < textToType.length) {
            typingTextEl.innerHTML += textToType.charAt(index);
            index++;
            typingTimer = setTimeout(type, 80);
        } else {
            if (cursorEl) cursorEl.style.display = 'none';
            if (mainContentBody) {
                mainContentBody.classList.remove('opacity-0');
                mainContentBody.classList.add('animate-bounce-up');
            }
            setTimeout(showBottomElements, 300);
        }
    }

    function showBottomElements() {
        if (floatingBanner) {
            floatingBanner.classList.remove('invisible', 'pointer-events-none', 'opacity-0');
            floatingBanner.classList.add('animate-pop-out');
        }
        if (robotContainer) {
            robotContainer.classList.remove('opacity-0');
            robotContainer.classList.add('animate-bounce-up');
        }
        setTimeout(() => {
            if (swipeGuide) {
                swipeGuide.style.display = 'flex';
                swipeGuide.classList.add('animate-guide');
            }
        }, 1000);
    }

    // 전역 함수로 노출 (window 객체에 바인딩)
    window.resetMain = function (closeAll = false) {
        clearTimeout(typingTimer);
        index = 0;
        if (typingTextEl) typingTextEl.innerHTML = "";
        if (cursorEl) cursorEl.style.display = 'inline-block';
        if (mainContentBody) {
            mainContentBody.classList.add('opacity-0');
            mainContentBody.classList.remove('animate-bounce-up');
        }

        if (floatingBanner) {
            floatingBanner.classList.add('invisible', 'pointer-events-none', 'opacity-0');
            floatingBanner.classList.remove('animate-pop-out');
        }

        if (robotContainer) robotContainer.classList.add('opacity-0');
        if (swipeGuide) swipeGuide.style.display = 'none';
        if (spacer) spacer.style.height = '0';

        if (closeAll) closeAllModals();
        if (scrollContainer) scrollContainer.scrollTo({ top: 0, behavior: 'auto' });
        setTimeout(type, 300);
    };

    window.continueCounseling = function () {
        closeAllModals();
        clearTimeout(typingTimer);

        const typingArea = document.getElementById('typing-area');
        if (typingArea) typingArea.style.display = 'flex';

        if (typingTextEl) typingTextEl.innerHTML = textToType;
        if (cursorEl) cursorEl.style.display = 'none';

        if (mainContentBody) {
            mainContentBody.classList.remove('animate-bounce-up');
        }

        if (floatingBanner) floatingBanner.classList.add('invisible', 'pointer-events-none', 'opacity-0');
        if (robotContainer) robotContainer.classList.add('opacity-0');
        if (swipeGuide) swipeGuide.style.display = 'none';

        // [수정] 하단 여백(spacer) & 스크롤 로직 최종 수정 (tall screen issue fix)
        if (scrollContainer && spacer) {
            // 1. Spacer 리셋
            spacer.style.height = '0px';

            requestAnimationFrame(() => {
                const target = document.getElementById('target-anchor');
                if (!target) return;

                // 2. 높이 계산 (scrollHeight 대신 spacer.offsetTop 사용)
                // 이유: 내용이 화면보다 짧으면 scrollHeight === clientHeight가 되어버림 (오차 발생)
                const realContentHeight = spacer.offsetTop;
                const targetTop = target.offsetTop;
                const clientH = scrollContainer.clientHeight;

                // 목표: targetTop이 화면 맨 위로 올라갈 수 있도록 전체 높이 확보
                // 필요 전체 높이 = Viewport 높이(clientH) + 숨겨야 할 높이(targetTop)
                const neededTotalHeight = clientH + targetTop;

                // 필요한 Spacer = 목표 높이 - 현재 콘텐츠 높이
                let neededSpacer = neededTotalHeight - realContentHeight;

                // 음수 방지 (이미 내용이 충분히 길면 0)
                if (neededSpacer < 0) neededSpacer = 0;

                // 3. Spacer 적용
                spacer.style.height = `${neededSpacer}px`;

                // 4. 스크롤 이동
                requestAnimationFrame(() => {
                    // 즉시 이동 (사용자 반응성 우선)
                    scrollContainer.scrollTo({ top: targetTop, behavior: 'auto' });

                    // 혹시 모를 렌더링 딜레이 대비 (부드러운 보정)
                    setTimeout(() => {
                        scrollContainer.scrollTo({ top: targetTop, behavior: 'smooth' });
                    }, 50);

                    // [복구] 말풍선 및 로봇 아이콘 다시 표시
                    setTimeout(showBottomElements, 300);
                });
            });
        }
    };

    // 초기 시작
    setTimeout(type, 500);
}

// 모달 토글 함수들
function closeAllModals() {
    [searchModal, listeningModal, resultModal, failModal, categoryModal].forEach(m => {
        if (m) m.classList.add('hidden');
    });
}

function toggleSearchModal() {
    if (!searchModal) return;
    if (searchModal.classList.contains('hidden')) {
        closeAllModals();
        searchModal.classList.remove('hidden');
        setTimeout(() => {
            const input = document.getElementById('search-input');
            if (input) input.focus();
        }, 100);
    } else {
        searchModal.classList.add('hidden');
    }
}

function toggleListeningModal() {
    if (!listeningModal) return;
    if (listeningModal.classList.contains('hidden')) {
        closeAllModals();
        listeningModal.classList.remove('hidden');
    } else {
        listeningModal.classList.add('hidden');
    }
}

function toggleResultModal() {
    if (!resultModal) return;
    if (resultModal.classList.contains('hidden')) {
        closeAllModals();
        resultModal.classList.remove('hidden');
    } else {
        resultModal.classList.add('hidden');
    }
}

function toggleFailModal() {
    if (!failModal) return;
    if (failModal.classList.contains('hidden')) {
        closeAllModals();
        failModal.classList.remove('hidden');
    } else {
        failModal.classList.add('hidden');
    }
}

function toggleCategoryModal() {
    if (!categoryModal) return;
    if (categoryModal.classList.contains('hidden')) {
        closeAllModals();
        categoryModal.classList.remove('hidden');
    } else {
        categoryModal.classList.add('hidden');
    }
}

function toggleAccordion(contentId, chevronId, closeOthers = false) {
    const content = document.getElementById(contentId);
    const chevron = document.getElementById(chevronId);

    if (closeOthers) {
        document.querySelectorAll('.accordion-content').forEach(el => {
            if (el.id !== contentId) {
                el.classList.remove('open');
                const otherChevronId = el.id.replace('content', 'chevron');
                const otherChevron = document.getElementById(otherChevronId);
                if (otherChevron) otherChevron.style.transform = 'rotate(0deg)';
            }
        });
    }

    if (content && chevron) {
        content.classList.toggle('open');
        chevron.style.transform = content.classList.contains('open') ? 'rotate(180deg)' : 'rotate(0deg)';
    }
}

function simulateSuccess() {
    if (listeningModal) listeningModal.classList.add('hidden');
    setTimeout(toggleResultModal, 200);
}

function simulateFail() {
    if (listeningModal) listeningModal.classList.add('hidden');
    setTimeout(toggleFailModal, 200);
}

function retryListening() {
    if (failModal) failModal.classList.add('hidden');
    setTimeout(toggleListeningModal, 200);
}

function handleInput(input) {
    const results = document.getElementById('search-results-container');
    const faq = document.getElementById('faq-section');
    const suggestions = document.getElementById('suggestions');
    if (!results || !faq || !suggestions) return;

    if (input.value.includes('요금')) {
        results.classList.remove('hidden');
        faq.classList.remove('hidden');
        suggestions.innerHTML = `
            <div class="px-5 py-4 border-b border-gray-50 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm"><span class="text-[#5031E5] font-bold">요금</span> 납부내역 조회</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
            <div class="px-5 py-4 border-b border-gray-50 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm">실시간 <span class="text-[#5031E5] font-bold">요금</span> 확인</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
            <div class="px-5 py-4 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm"><span class="text-[#5031E5] font-bold">요금</span>납부 방법</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
        `;
        lucide.createIcons();
    } else {
        results.classList.add('hidden');
        faq.classList.add('hidden');
    }
}

function initSwipeEvents() {
    let startY = 0;
    const swipeArea = document.getElementById('swipe-area');
    if (swipeArea) {
        swipeArea.addEventListener('touchstart', (e) => { startY = e.touches[0].clientY; }, { passive: true });
        swipeArea.addEventListener('touchend', (e) => {
            if (startY - e.changedTouches[0].clientY > 30) toggleSearchModal();
        }, { passive: true });
    }
}

// 창 로드 시 이벤트 리스너 제거 (initCommonUI 내부에서 처리)
// window.addEventListener('load', initSwipeEvents);

// [공통] 폰트 크기 조절 함수 (3단계: 기본 -> 크게 -> 아주 크게)
// Step 0: 기본 (Original)
// Step 1: 크게 (+4px)
// Step 2: 아주 크게 (+8px)
window.currentFontStep = parseInt(localStorage.getItem('fontStep')) || 0; // 0, 1, 2
window.originalFontSizes = new Map(); // 요소별 초기 폰트 크기 저장

window.adjustFontSize = function (direction) {
    // 방향에 따라 단계 조절 (1: 증가, -1: 감소)
    let nextStep = window.currentFontStep + direction;

    // 단계 제한 (0 ~ 2)
    if (nextStep < 0) nextStep = 0;
    if (nextStep > 2) nextStep = 2;

    // 단계가 변하지 않았으면 리턴
    if (nextStep === window.currentFontStep) return;

    window.currentFontStep = nextStep;
    localStorage.setItem('fontStep', window.currentFontStep); // 상태 저장 (localStorage 사용)

    window.applyCurrentFontSize(); // 적용

    // 디버깅용 로그
    console.log(`Font Resized: Step ${window.currentFontStep}`);
};

// 3. 현재 설정된 폰트 크기 적용 (로직 분리)
window.applyCurrentFontSize = function () {
    const sizeOffset = window.currentFontStep * 4; // 단계당 4px 씩 증가

    // Typing Text 영역과 Main Content 영역 모두 포함
    const targets = [
        document.getElementById('typing-text'),
        document.getElementById('main-content-body'),
        document.getElementById('time-modal'),
        document.getElementById('confirm-modal')
    ];

    targets.forEach(target => {
        if (!target) return;

        // 타겟이 단일 텍스트 요소인 경우 (typing-text)
        if (target.id === 'typing-text') {
            // 초기 크기 저장 (최초 1회만, 이미 스타일이 적용되어 있어도 원본 계산을 위해 최초 한번만 수행해야 함)
            // 주의: 페이지 이동 시 스타일은 초기화되므로 매번 다시 캡처해도 되지만, 
            // 이미 apply가 된 상태에서 호출될 경우를 대비해 flag 검사 필요.
            // 다만 여기서는 Map에 없으면 캡처하므로, 페이지 로드 후 최초 실행 시 캡처됨.
            if (!window.originalFontSizes.has(target)) {
                const style = window.getComputedStyle(target);
                window.originalFontSizes.set(target, parseFloat(style.fontSize));
            }

            const baseSize = window.originalFontSizes.get(target);
            const newSize = baseSize + sizeOffset;
            target.style.fontSize = `${newSize}px`;

            // 커서 크기도 같이 조정
            const cursor = document.getElementById('cursor');
            if (cursor) cursor.style.height = `${newSize + 4}px`;
        }
        // 타겟이 컨테이너인 경우 (main-content-body)
        else {
            const elements = target.querySelectorAll('*');
            elements.forEach(el => {
                // 텍스트가 직접 포함된 요소만 (공백 제외)
                if (el.childNodes.length > 0) {
                    let hasText = false;
                    for (let i = 0; i < el.childNodes.length; i++) {
                        if (el.childNodes[i].nodeType === Node.TEXT_NODE && el.childNodes[i].textContent.trim().length > 0) {
                            hasText = true;
                            break;
                        }
                    }

                    if (hasText) {
                        // 초기 크기 저장 (최초 1회)
                        if (!window.originalFontSizes.has(el)) {
                            const style = window.getComputedStyle(el);
                            window.originalFontSizes.set(el, parseFloat(style.fontSize));
                        }

                        const baseSize = window.originalFontSizes.get(el);
                        // baseSize가 유효할 때만 적용
                        if (!isNaN(baseSize)) {
                            const newSize = baseSize + sizeOffset;
                            el.style.fontSize = `${newSize}px`;
                        }
                    }
                }
            });
        }
    });
};

// 페이지 로드 시 저장된 폰트 크기 적용
document.addEventListener('DOMContentLoaded', () => {
    window.applyCurrentFontSize();
});
