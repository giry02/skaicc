// [공통 UI 스크립트] AICC 멀티모달 프로젝트 전용
function initCommonUI(textToType) {
    lucide.createIcons();

    const typingTextEl = document.getElementById('typing-text');
    const cursorEl = document.getElementById('cursor');
    const mainContentBody = document.getElementById('main-content-body');
    const floatingBanner = document.getElementById('floating-banner');
    const robotContainer = document.getElementById('robot-container');
    const swipeGuide = document.getElementById('swipe-guide');
    const scrollContainer = document.getElementById('main-scroll-container');
    const spacer = document.getElementById('bottom-spacer');

    let typingTimer;
    let index = 0;

    function type() {
        if (index < textToType.length) {
            typingTextEl.innerHTML += textToType.charAt(index);
            index++;
            typingTimer = setTimeout(type, 80);
        } else {
            cursorEl.style.display = 'none';
            mainContentBody.classList.remove('opacity-0');
            mainContentBody.classList.add('animate-bounce-up');
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

    // 전역 함수로 노출
    window.resetMain = function(closeAll = false) {
        clearTimeout(typingTimer);
        index = 0;
        typingTextEl.innerHTML = "";
        cursorEl.style.display = 'inline-block';
        mainContentBody.classList.add('opacity-0');
        mainContentBody.classList.remove('animate-bounce-up');

        if (floatingBanner) {
            floatingBanner.classList.add('invisible', 'pointer-events-none', 'opacity-0');
            floatingBanner.classList.remove('animate-pop-out');
        }

        if (robotContainer) robotContainer.classList.add('opacity-0');
        if (swipeGuide) swipeGuide.style.display = 'none';
        if (spacer) spacer.style.height = '0';
        
        if (closeAll) closeAllModals();
        scrollContainer.scrollTo({ top: 0, behavior: 'auto' });
        setTimeout(type, 300);
    };

    window.continueCounseling = function() {
        closeAllModals();
        clearTimeout(typingTimer);
        typingTextEl.innerHTML = textToType;
        cursorEl.style.display = 'none';
        mainContentBody.classList.remove('animate-bounce-up');
        mainContentBody.classList.add('opacity-0');

        if (floatingBanner) floatingBanner.classList.add('invisible', 'pointer-events-none', 'opacity-0');
        if (robotContainer) robotContainer.classList.add('opacity-0');
        if (swipeGuide) swipeGuide.style.display = 'none';
        if (spacer) spacer.style.height = '600px';

        const target = document.getElementById('target-anchor');
        if (scrollContainer && target) {
            scrollContainer.scrollTo({ top: target.offsetTop, behavior: 'auto' });
        }

        setTimeout(() => {
            mainContentBody.classList.remove('opacity-0');
            mainContentBody.classList.add('animate-bounce-up');
            setTimeout(showBottomElements, 300);
        }, 50);
    };

    // 초기 시작
    setTimeout(type, 500);
}

// 모달 토글 함수들
const searchModal = document.getElementById('search-modal');
const listeningModal = document.getElementById('listening-modal');
const resultModal = document.getElementById('result-modal');
const failModal = document.getElementById('fail-modal');
const categoryModal = document.getElementById('category-modal');

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

function toggleAccordion(contentId, chevronId) {
    const content = document.getElementById(contentId);
    const chevron = document.getElementById(chevronId);
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
            <div class="px-5 py-4 border-b border-gray-50 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm"><span class="text-[#5031E5] font-bold">요금</span> 조회/납부</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
            <div class="px-5 py-4 border-b border-gray-50 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm"><span class="text-[#5031E5] font-bold">요금</span> 안내서</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
            <div class="px-5 py-4 border-b border-gray-50 flex justify-between items-center group cursor-pointer" onclick="toggleResultModal()"><span class="text-gray-700 font-medium text-sm"><span class="text-[#5031E5] font-bold">요금</span> 납부내역 조회</span><i data-lucide="chevron-right" class="w-4 h-4 text-gray-300"></i></div>
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

window.addEventListener('load', initSwipeEvents);
