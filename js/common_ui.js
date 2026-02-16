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

    // 5. 타이핑 효과 시작
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
        if (typingTextEl) typingTextEl.innerHTML = textToType;
        if (cursorEl) cursorEl.style.display = 'none';

        if (mainContentBody) {
            mainContentBody.classList.remove('animate-bounce-up');
            mainContentBody.classList.add('opacity-0');
        }

        if (floatingBanner) floatingBanner.classList.add('invisible', 'pointer-events-none', 'opacity-0');
        if (robotContainer) robotContainer.classList.add('opacity-0');
        if (swipeGuide) swipeGuide.style.display = 'none';
        if (spacer) spacer.style.height = '120px';

        const target = document.getElementById('target-anchor');
        if (scrollContainer && target) {
            scrollContainer.scrollTo({ top: target.offsetTop, behavior: 'auto' });
        }

        setTimeout(() => {
            if (mainContentBody) {
                mainContentBody.classList.remove('opacity-0');
                mainContentBody.classList.add('animate-bounce-up');
            }
            setTimeout(showBottomElements, 300);
        }, 50);
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
