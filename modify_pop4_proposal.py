import requests
import re
import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: Visit Schedule Proposal Generator (Refactored)]
# 이 스크립트는 'visit_schedule_proposal.html' (AI 디자인 제안 버전)을 생성합니다.
# 또한, 자바스크립트를 별도 파일(js/visit_proposal.js)로 분리하여 저장합니다.
# =================================================================================

# 경로 설정
BASE_DIR = 'completed'
JS_DIR = os.path.join(BASE_DIR, 'js')
CSS_DIR = os.path.join(BASE_DIR, 'css')

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
    print(f"Error: {e}")
    exit()

# 2. 타이핑 텍스트 변경
try:
    new_text = "편안한 방문 일정을 선택해 주세요."
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

# 5. UI 교체 (AI Design Proposal)
main_body = soup.find(id='main-content-body')
target_anchor = soup.find(id='target-anchor')

if main_body and target_anchor:
    print("UI 구성 중 (AI Design)...")
    
    h2 = target_anchor.find('h2')
    if h2:
        h2.clear()
        span = soup.new_tag('span', **{'class': 'text-black'})
        span.string = "{다른 방으로 이동}"
        h2.append(span)
        h2.append("에 대한")
        h2.append(soup.new_tag('br'))
        h2.append("방문 일정이에요.")

    target_anchor_extracted = target_anchor.extract()
    main_body.clear()
    
    wrapper = soup.new_tag('div', **{'class': 'flex flex-col h-full bg-white'}) # Ensure white bg
    wrapper.append(target_anchor_extracted)
    
    # 가로 스크롤 날짜 섹션
    date_section = soup.new_tag('div', **{'class': 'mt-6 mb-8'})
    date_label = soup.new_tag('h3', **{'class': 'text-lg font-bold text-gray-900 mb-4 px-1'}) 
    date_label.string = "날짜 선택 (2025.07)"
    date_section.append(date_label)
    
    scroll_container = soup.new_tag('div', **{'class': 'flex overflow-x-auto space-x-3 pb-4 px-1 -mx-1 snap-x'})
    
    dates = [
        ('금', '25', True), ('토', '26', False), ('일', '27', False),
        ('월', '28', False), ('화', '29', False), ('수', '30', False, True), ('목', '1', False, True),
        ('금', '2', False, True), ('토', '3', False), ('일', '4', False)
    ]
    
    for day, date, active, *disabled in dates:
        is_disabled = disabled[0] if disabled else False
        
        cont_cls = 'flex-shrink-0 flex flex-col items-center justify-center w-[60px] h-[80px] rounded-2xl border transition-all cursor-pointer snap-start date-card '
        
        if active:
            cont_cls += 'bg-[#5031E5] border-[#5031E5] text-white shadow-lg shadow-purple-200 ring-2 ring-offset-2 ring-[#5031E5] active-date-card'
        elif is_disabled:
            cont_cls += 'bg-gray-50 border-gray-100 text-gray-300 cursor-default'
        else:
            cont_cls += 'bg-white border-gray-200 text-gray-500 hover:border-[#5031E5] hover:text-[#5031E5]'

        btn = soup.new_tag('div', **{'class': cont_cls})
        if is_disabled:
            btn['data-disabled'] = 'true'
        else:
            btn['onclick'] = 'selectDate(this)' 
        
        d_span = soup.new_tag('span', **{'class': 'text-xs mb-1 font-medium'})
        d_span.string = day
        n_span = soup.new_tag('span', **{'class': 'text-xl font-bold'})
        n_span.string = date
        
        btn.append(d_span)
        btn.append(n_span)
        scroll_container.append(btn)
        
    date_section.append(scroll_container)
    wrapper.append(date_section)

    # 칩 스타일 시간 섹션
    time_section = soup.new_tag('div', **{'class': 'mb-8'})
    time_label = soup.new_tag('h3', **{'class': 'text-lg font-bold text-gray-900 mb-4 px-1'}) 
    time_label.string = "시간 선택"
    time_section.append(time_label)
    
    time_grid = soup.new_tag('div', **{'class': 'grid grid-cols-3 gap-3'})
    
    times = ['10:00', '11:00', '12:00 (점심)', '13:00', '14:00', '15:00', '16:00', '17:00']
    
    for t in times:
        is_lunch = '점심' in t
        display_t = t.replace(' (점심)', '')
        sub_text = '점심시간' if is_lunch else ''
        
        t_cls = 'relative flex flex-col items-center justify-center p-3 rounded-xl border text-center transition-all cursor-pointer time-card '
        if is_lunch:
            t_cls += 'bg-gray-50 border-gray-100 text-gray-300 cursor-not-allowed'
        else:
            t_cls += 'bg-white border-gray-200 text-gray-600 hover:border-[#5031E5] hover:text-[#5031E5]'
            
        btn = soup.new_tag('div', **{'class': t_cls})
        if is_lunch:
            btn['data-disabled'] = 'true'
        else:
            btn['onclick'] = 'selectTime(this)'
            
        main_t = soup.new_tag('span', **{'class': 'text-[15px] font-bold'})
        main_t.string = display_t
        btn.append(main_t)
        
        if sub_text:
            sub = soup.new_tag('span', **{'class': 'text-[10px] mt-1'})
            sub.string = sub_text
            btn.append(sub)
            
        time_grid.append(btn)
        
    time_section.append(time_grid)
    wrapper.append(time_section)

    # 하단 버튼
    btn_div = soup.new_tag('div', **{'class': 'mt-auto pt-4'})
    sub_btn = soup.new_tag('button', **{'id': 'submit-visit-btn', 'class': 'w-full bg-[#5031E5] text-white py-4 rounded-xl text-lg font-bold shadow-xl shadow-indigo-200 transform active:scale-95 transition-all'})
    sub_btn.string = "예약 완료하기"
    btn_div.append(sub_btn)
    wrapper.append(btn_div)
    
    main_body.append(wrapper)

    # 6. 모달 HTML
    modal_html = """
    <div id="confirm-modal" class="fixed inset-0 z-50 flex items-center justify-center hidden">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity opacity-0" id="modal-overlay"></div>
        <div class="relative bg-white rounded-3xl p-8 w-[85%] max-w-sm shadow-2xl transform scale-95 opacity-0 transition-all duration-300" id="modal-content">
            <div class="text-center">
                <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">📅</div>
                <h3 class="text-xl font-bold text-gray-900 mb-2">예약 확인</h3>
                <p class="text-gray-500 mb-8 leading-relaxed">
                    아래 일정으로 방문을 예약하시겠습니까?<br>
                    <span class="font-bold text-[#5031E5] text-lg mt-2 block" id="modal-date-time"></span>
                </p>
                <div class="flex flex-col gap-3">
                    <button id="modal-confirm-btn" class="w-full py-4 bg-[#5031E5] text-white rounded-xl font-bold shadow-lg hover:bg-[#4020d0] transition-colors">네, 예약할게요</button>
                    <button id="modal-cancel-btn" class="w-full py-4 bg-transparent text-gray-400 font-medium hover:text-gray-600 transition-colors">나중에 할게요</button>
                </div>
            </div>
        </div>
    </div>
    """
    soup.body.append(BeautifulSoup(modal_html, 'html.parser'))

    # 7. JavaScript 분리
    js_filename = 'visit_proposal.js'
    js_path = os.path.join(JS_DIR, js_filename)
    
    js_content = """
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
    """
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"JavaScript 생성 완료: {js_path}")

    # 8. HTML에 JS 파일 링크 추가
    script_tag = soup.new_tag('script', src=f'js/{js_filename}')
    soup.body.append(script_tag)

# 9. 최종 저장
output_filename = os.path.join(BASE_DIR, 'visit_schedule_proposal.html')
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print(f"HTML 생성 완료: {output_filename}")
