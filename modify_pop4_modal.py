import requests
import re
import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: Visit Schedule Modal Generator (Refactored)]
# 이 스크립트는 'visit_schedule_modal.html' (사용자 최종 승인 버전)을 생성합니다.
# 또한, 기존에 인라인으로 포함되던 자바스크립트를 별도 파일(js/visit_reservation.js)로 분리하여
# 실제 개발 환경과 유사한 구조를 갖추도록 리팩토링되었습니다.
# =================================================================================

# 경로 설정
BASE_DIR = 'completed'
JS_DIR = os.path.join(BASE_DIR, 'js')
CSS_DIR = os.path.join(BASE_DIR, 'css')

# 폴더가 없으면 생성
os.makedirs(JS_DIR, exist_ok=True)
os.makedirs(CSS_DIR, exist_ok=True)

# 1. 원본 HTML 가져오기
print("Fetching pop4.html...")
url = 'https://giry02.dothome.co.kr/pop4.html'
try:
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    html_content = response.text
except Exception as e:
    print(f"Error fetching HTML: {e}")
    exit()

# 2. 타이핑 텍스트 변경
try:
    new_text = "원하시는 날짜와 시간을 선택해 주세요."
    html_content = re.sub(r'const\s+textToType\s*=\s*".*?";', f'const textToType = "{new_text}";', html_content)
    print("타이핑 텍스트 수정 완료.")
except Exception as e:
    print(f"Regex failed: {e}")

# 3. HTML 파싱
soup = BeautifulSoup(html_content, 'html.parser')

# 4. 헤더 수정
header = soup.find('header')
if header:
    found_text = False
    for content in header.contents:
        if isinstance(content, str) and content.strip():
            content.replace_with("방문일정 등록")
            found_text = True
            break
    if not found_text:
        h1 = header.find('h1')
        if h1:
            h1.string = "방문일정 등록"
        else:
             header.append("방문일정 등록")

# 5. 메인 컨텐츠 구성
main_body = soup.find(id='main-content-body')
target_anchor = soup.find(id='target-anchor')

if main_body and target_anchor:
    print("UI 구성 중...")
    
    # [5-1] 설명 텍스트 (검정색 적용)
    h2 = target_anchor.find('h2')
    if h2:
        h2.clear()
        span = soup.new_tag('span', **{'class': 'text-black'})
        span.string = "{다른 방으로 이동}"
        h2.append(span)
        h2.append("에 대한")
        h2.append(soup.new_tag('br'))
        h2.append("방문 일정이에요.")
    
    # [5-2] 기존 컨텐츠 정리
    target_anchor_extracted = target_anchor.extract()
    main_body.clear()
    main_body.append(target_anchor_extracted)
    
    # [5-3] 예약 폼 UI 생성
    form_container = soup.new_tag('div', **{'class': 'mt-6'})

    # 달력 섹션
    cal_div = soup.new_tag('div', **{'class': 'mb-8'})
    cal_h = soup.new_tag('div', **{'class': 'font-bold text-lg text-[#1a1a1a] mb-4'})
    cal_h.string = "2025년 7월"
    cal_div.append(cal_h)

    days_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center mb-2'})
    for d in ['오늘', '수', '목', '금', '토', '일', '월']:
        el = soup.new_tag('div', **{'class': 'text-sm text-[#888]'})
        el.string = d
        days_row.append(el)
    cal_div.append(days_row)

    dates_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center', 'id': 'date-grid'})
    dates = [('25', True), ('26', False), ('27', False), ('28', False), ('29', False), ('30', False, True), ('1', False, True)]
    
    for d, active, *disabled in dates:
        d_wrap = soup.new_tag('div', **{'class': 'flex justify-center'})
        is_disabled = disabled[0] if disabled else False
        
        btn_cls = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors date-btn '
        if active:
            btn_cls += 'bg-white border-2 text-[#5031E5] border-[#5031E5] font-bold shadow-sm active-date' 
        elif is_disabled:
            btn_cls += 'text-gray-300 cursor-default disabled-date'
        else:
            btn_cls += 'text-[#333] hover:bg-gray-50'

        btn = soup.new_tag('button', **{'class': btn_cls})
        if is_disabled:
            btn['disabled'] = 'disabled'
        btn.string = d
        d_wrap.append(btn)
        dates_row.append(d_wrap)
    cal_div.append(dates_row)
    form_container.append(cal_div)

    # 시간 선택 섹션
    time_div = soup.new_tag('div', **{'class': 'mb-8'})
    time_h = soup.new_tag('div', **{'class': 'font-bold text-lg text-[#1a1a1a] mb-4'})
    time_h.string = "원하는 시간을 선택해주세요"
    time_div.append(time_h)

    t_grid = soup.new_tag('div', **{'class': 'grid grid-cols-4 gap-2', 'id': 'time-grid'})
    times = ['10-11시', '11-12시', ('점심', True), '13-14시', '14-15시', '15-16시', '16-17시', ('17-18시', False, True)]
    for t in times:
        txt = t[0] if isinstance(t, tuple) else t
        dis = (t[1]) if isinstance(t, tuple) and len(t)>1 else False
        act = (t[2]) if isinstance(t, tuple) and len(t)>2 else False

        t_cls = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors time-btn '
        if act:
            t_cls += 'bg-[#eff6ff] border-[#5031E5] text-[#5031E5] active-time' 
        elif dis:
            t_cls += 'bg-[#f5f5f5] text-[#aaa] border-transparent disabled-time'
        else:
            t_cls += 'bg-white border-[#ddd] text-[#444] hover:border-[#bbb]'
        
        btn = soup.new_tag('button', **{'class': t_cls})
        if dis:
            btn['disabled'] = 'disabled'
        btn.string = txt
        t_grid.append(btn)
    time_div.append(t_grid)
    form_container.append(time_div)

    # 완료 버튼
    btn_div = soup.new_tag('div', **{'class': 'mt-6'})
    sub_btn = soup.new_tag('button', **{'id': 'submit-visit-btn', 'class': 'w-full bg-[#5031E5] text-white py-4 rounded-xl text-[19px] font-bold shadow-lg hover:bg-[#4020d0] transition-colors'})
    sub_btn.string = "선택 완료"
    btn_div.append(sub_btn)
    form_container.append(btn_div)

    main_body.append(form_container)

    # 6. 모달 HTML 추가 (Tailwind 스타일)
    modal_html = """
    <div id="confirm-modal" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity opacity-0" id="modal-overlay"></div>
        <div class="relative bg-white rounded-2xl p-6 w-[85%] max-w-sm shadow-2xl transform scale-95 opacity-0 transition-all duration-300" id="modal-content">
            <div class="text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">방문 일정 확인</h3>
                <p class="text-gray-600 mb-6 text-sm leading-relaxed">
                    선택하신 일정으로 예약하시겠습니까?<br>
                    <span class="font-bold text-[#5031E5] text-base mt-2 block" id="modal-date-time"></span>
                </p>
                <div class="flex gap-3">
                    <button id="modal-cancel-btn" class="flex-1 py-3 bg-gray-100 text-gray-600 rounded-xl font-medium hover:bg-gray-200 transition-colors">취소</button>
                    <button id="modal-confirm-btn" class="flex-1 py-3 bg-[#5031E5] text-white rounded-xl font-bold hover:bg-[#4020d0] shadow-md transition-colors">확인</button>
                </div>
            </div>
        </div>
    </div>
    """
    soup.body.append(BeautifulSoup(modal_html, 'html.parser'))

    # 7. JavaScript 분리 및 저장
    # 자바스크립트 코드는 별도 파일로 저장합니다.
    js_filename = 'visit_reservation.js'
    js_path = os.path.join(JS_DIR, js_filename)
    
    js_content = """
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
    if(initialDate) selectedDate = initialDate.innerText;
    
    const initialTime = document.querySelector('.active-time');
    if(initialTime) selectedTime = initialTime.innerText;

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
        if(!selectedDate || !selectedTime) {
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
    if(submitBtn) submitBtn.addEventListener('click', openModal);
    
    const cancelBtn = document.getElementById('modal-cancel-btn');
    if(cancelBtn) cancelBtn.addEventListener('click', closeModal);
    
    const confirmBtn = document.getElementById('modal-confirm-btn');
    if(confirmBtn) confirmBtn.addEventListener('click', () => {
        closeModal();
        setTimeout(() => {
            // 실제 서비스에서는 여기서 서버로 데이터를 전송합니다.
            alert('예약이 성공적으로 완료되었습니다! (Demo)');
        }, 350);
    });
});
    """
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"JavaScript 생성 완료: {js_path}")

    # 8. HTML에 JS 파일 링크 추가
    script_tag = soup.new_tag('script', src=f'js/{js_filename}')
    soup.body.append(script_tag)

# 9. 최종 HTML 저장
output_filename = os.path.join(BASE_DIR, 'visit_schedule_modal.html')
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print(f"HTML 생성 완료: {output_filename}")
