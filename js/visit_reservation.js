
/**
 * [방문 일정 예약 로직]
 * 이 파일은 visit_schedule_modal.html의 인터랙티브 기능을 담당합니다.
 * 주요 기능:
 * 1. 날짜 및 시간 선택 (클릭 시 활성 상태 토글)
 * 2. 선택된 데이터 저장 (selectedDate, selectedTime)
 * 3. 완료 버튼 클릭 시 모달창 제어
 */

document.addEventListener('DOMContentLoaded', () => {
    let selectedDate = '25'; // 기본 선택값 (이미지와 동일하게)
    let selectedTime = null;

    // 초기 활성 상태 확인
    const initialDate = document.querySelector('.active-date');
    if (initialDate) selectedDate = initialDate.innerText;

    const initialTime = document.querySelector('.active-time');
    if (initialTime) selectedTime = initialTime.innerText;

    // [날짜 선택 핸들러]
    const dateBtns = document.querySelectorAll('.date-btn:not(.disabled-date)');
    dateBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // 모든 날짜 버튼 초기화 (Inactive 스타일 적용)
            dateBtns.forEach(b => {
                b.className = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors date-btn text-[#333] hover:bg-gray-50';
            });
            // 클릭된 버튼 활성화 (Active 스타일 적용 - 브랜드 컬러)
            e.target.className = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors date-btn bg-white border-2 text-[#5031E5] border-[#5031E5] font-bold shadow-sm active-date';
            selectedDate = e.target.innerText;
        });
    });

    // [시간 선택 핸들러]
    const timeBtns = document.querySelectorAll('.time-btn:not(.disabled-time)');
    timeBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // 모든 시간 버튼 초기화
            timeBtns.forEach(b => {
                b.className = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors time-btn bg-white border-[#ddd] text-[#444] hover:border-[#bbb]';
            });
            // 클릭된 버튼 활성화
            e.target.className = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors time-btn bg-[#eff6ff] border-[#5031E5] text-[#5031E5] active-time';
            selectedTime = e.target.innerText;
        });
    });

    // [모달 제어 로직]
    const modal = document.getElementById('confirm-modal');
    const overlay = document.getElementById('modal-overlay');
    const content = document.getElementById('modal-content');
    const modalText = document.getElementById('modal-date-time');

    function openModal() {
        if (!selectedDate || !selectedTime) {
            alert('날짜와 시간을 모두 선택해주세요.');
            return;
        }
        modalText.innerText = `2025년 7월 ${selectedDate}일 ${selectedTime}`;
        modal.classList.remove('hidden');

        // 애니메이션 효과 (Fade In)
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

    // 이벤트 리스너 연결
    const submitBtn = document.getElementById('submit-visit-btn');
    if (submitBtn) submitBtn.addEventListener('click', openModal);

    const cancelBtn = document.getElementById('modal-cancel-btn');
    if (cancelBtn) cancelBtn.addEventListener('click', closeModal);

    const confirmBtn = document.getElementById('modal-confirm-btn');
    if (confirmBtn) confirmBtn.addEventListener('click', () => {
        closeModal();
        setTimeout(() => {
            // 시나리오 흐름에 따라 217페이지(최종 확인)로 이동합니다.
            location.href = 'page217_schedule_confirm.html';
        }, 350);
    });
});
