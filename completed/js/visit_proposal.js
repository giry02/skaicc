
/**
 * [방문 일정 예약 로직 - AI 제안 버전]
 * visit_schedule_proposal.html의 기능을 담당합니다.
 * 주요 기능:
 * 1. 가로 스크롤 날짜 선택 (selectDate)
 * 2. 칩 스타일 시간 선택 (selectTime)
 * 3. 인라인 onclick 핸들러 사용
 */

let selectedDate = '25';
let selectedDay = '금';
let selectedTime = null;

// [날짜 선택 함수]
function selectDate(el) {
    if(el.getAttribute('data-disabled')) return;
    
    // 초기화
    document.querySelectorAll('.date-card').forEach(c => {
        if(!c.getAttribute('data-disabled')) {
            c.className = 'flex-shrink-0 flex flex-col items-center justify-center w-[60px] h-[80px] rounded-2xl border transition-all cursor-pointer snap-start date-card bg-white border-gray-200 text-gray-500 hover:border-[#5031E5] hover:text-[#5031E5]';
        }
    });
    
    // 활성화 (브랜드 컬러 배경)
    el.className = 'flex-shrink-0 flex flex-col items-center justify-center w-[60px] h-[80px] rounded-2xl border transition-all cursor-pointer snap-start date-card bg-[#5031E5] border-[#5031E5] text-white shadow-lg shadow-purple-200 ring-2 ring-offset-2 ring-[#5031E5] active-date-card';
    
    // 데이터 저장
    selectedDay = el.querySelector('span:nth-child(1)').innerText;
    selectedDate = el.querySelector('span:nth-child(2)').innerText;
}

// [시간 선택 함수]
function selectTime(el) {
    if(el.getAttribute('data-disabled')) return;
    
    // 초기화
    document.querySelectorAll('.time-card').forEach(c => {
        if(!c.getAttribute('data-disabled')) {
            c.className = 'relative flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all cursor-pointer time-card bg-white border-gray-200 text-gray-600 hover:border-[#5031E5] hover:text-[#5031E5]';
        }
    });
    
    // 활성화
    el.className = 'relative flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all cursor-pointer time-card bg-[#eff6ff] border-[#5031E5] text-[#5031E5] ring-1 ring-[#5031E5] font-bold shadow-sm';
    
    selectedTime = el.querySelector('span').innerText;
}

document.addEventListener('DOMContentLoaded', () => {
    // [모달 로직]
    const modal = document.getElementById('confirm-modal');
    const overlay = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');
    const modalText = document.getElementById('modal-date-time');

    function openModal() {
        if(!selectedDate || !selectedTime) {
            alert('날짜와 시간을 선택해주세요.');
            return;
        }
        modalText.innerText = `7월 ${selectedDate}일 (${selectedDay}) ${selectedTime}`;
        modal.classList.remove('hidden');
        setTimeout(() => {
            overlay.classList.remove('opacity-0');
            content.classList.remove('opacity-0', 'scale-95');
            content.classList.add('scale-100');
        }, 10);
    }

    function closeModal() {
        overlay.classList.add('opacity-0');
        content.classList.add('opacity-0', 'scale-95');
        content.classList.remove('scale-100');
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 300);
    }

    const submitBtn = document.getElementById('submit-visit-btn');
    if(submitBtn) submitBtn.addEventListener('click', openModal);
    
    const cancelBtn = document.getElementById('modal-cancel-btn');
    if(cancelBtn) cancelBtn.addEventListener('click', closeModal);
    
    const confirmBtn = document.getElementById('modal-confirm-btn');
    if(confirmBtn) confirmBtn.addEventListener('click', () => {
        closeModal();
        setTimeout(() => {
            alert('예약이 성공적으로 완료되었습니다! (Demo)');
        }, 350);
    });
});
    