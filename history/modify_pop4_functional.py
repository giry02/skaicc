import requests
import re
from bs4 import BeautifulSoup

# 1. Fetch directly from URL
print("Fetching pop4.html...")
url = 'https://giry02.dothome.co.kr/pop4.html'
response = requests.get(url)
response.encoding = response.apparent_encoding
html_content = response.text

# 2. Modify JavaScript `textToType`
try:
    new_text = "원하시는 날짜와 시간을 선택해 주세요."
    html_content = re.sub(r'const\s+textToType\s*=\s*".*?";', f'const textToType = "{new_text}";', html_content)
    print("Updated typing text.")
except Exception as e:
    print(f"Regex failed: {e}")

# 3. Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# 4. Modify Header Title
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

# 5. Modify Main Body Content
main_body = soup.find(id='main-content-body')
target_anchor = soup.find(id='target-anchor')

if main_body and target_anchor:
    print("Found main-content-body and target-anchor...")
    
    # 1. Update H2 (Black text)
    h2 = target_anchor.find('h2')
    if h2:
        h2.clear()
        span = soup.new_tag('span', **{'class': 'text-black'})
        span.string = "{다른 방으로 이동}"
        h2.append(span)
        h2.append("에 대한")
        h2.append(soup.new_tag('br'))
        h2.append("방문 일정이에요.")
    
    # 2. Clear content after target_anchor
    target_anchor_extracted = target_anchor.extract()
    main_body.clear()
    main_body.append(target_anchor_extracted)
    
    # 3. Create Container for Calendar/Time UI
    form_container = soup.new_tag('div', **{'class': 'mt-6'})

    # Calendar Section
    cal_div = soup.new_tag('div', **{'class': 'mb-8'})
    cal_h = soup.new_tag('div', **{'class': 'font-bold text-lg text-[#1a1a1a] mb-4'})
    cal_h.string = "2025년 7월"
    cal_div.append(cal_h)

    # Days
    days_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center mb-2'})
    for d in ['오늘', '수', '목', '금', '토', '일', '월']:
        el = soup.new_tag('div', **{'class': 'text-sm text-[#888]'})
        el.string = d
        days_row.append(el)
    cal_div.append(days_row)

    # Dates Grid (Add ID for JS)
    dates_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center', 'id': 'date-grid'})
    dates = [('25', True), ('26', False), ('27', False), ('28', False), ('29', False), ('30', False, True), ('1', False, True)]
    
    for d, active, *disabled in dates:
        d_wrap = soup.new_tag('div', **{'class': 'flex justify-center'})
        is_disabled = disabled[0] if disabled else False
        
        # Base classes (layout only)
        # We will manage color classes in JS or inline for initial state
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

    # Time Slots Section
    time_div = soup.new_tag('div', **{'class': 'mb-8'})
    time_h = soup.new_tag('div', **{'class': 'font-bold text-lg text-[#1a1a1a] mb-4'})
    time_h.string = "원하는 시간을 선택해주세요"
    time_div.append(time_h)

    # Time Grid (Add ID)
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

    # Button
    btn_div = soup.new_tag('div', **{'class': 'mt-6'})
    sub_btn = soup.new_tag('button', **{'id': 'submit-visit-btn', 'class': 'w-full bg-[#5031E5] text-white py-4 rounded-xl text-[19px] font-bold shadow-lg hover:bg-[#4020d0] transition-colors'})
    sub_btn.string = "선택 완료"
    btn_div.append(sub_btn)
    form_container.append(btn_div)

    main_body.append(form_container)

    # 4. Inject JavaScript for Interactivity
    script = soup.new_tag('script')
    script.string = """
    document.addEventListener('DOMContentLoaded', () => {
        let selectedDate = '25'; // Default
        let selectedTime = null; // No default time? Or image had one? Image had '17-18'.
        // Let's assume no default time for better UX flow, or set defaults if buttons are active.
        
        // Check initial active states
        const initialDate = document.querySelector('.active-date');
        if(initialDate) selectedDate = initialDate.innerText;
        
        const initialTime = document.querySelector('.active-time');
        if(initialTime) selectedTime = initialTime.innerText;

        // Date Logic
        const dateBtns = document.querySelectorAll('.date-btn:not(.disabled-date)');
        dateBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Reset all
                dateBtns.forEach(b => {
                    b.className = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors date-btn text-[#333] hover:bg-gray-50';
                });
                // Set active
                e.target.className = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors date-btn bg-white border-2 text-[#5031E5] border-[#5031E5] font-bold shadow-sm active-date';
                selectedDate = e.target.innerText;
            });
        });

        // Time Logic
        const timeBtns = document.querySelectorAll('.time-btn:not(.disabled-time)');
        timeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Reset all
                timeBtns.forEach(b => {
                    b.className = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors time-btn bg-white border-[#ddd] text-[#444] hover:border-[#bbb]';
                });
                // Set active
                e.target.className = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors time-btn bg-[#eff6ff] border-[#5031E5] text-[#5031E5] active-time';
                selectedTime = e.target.innerText;
            });
        });

        // Submit Logic
        const submitBtn = document.getElementById('submit-visit-btn');
        submitBtn.addEventListener('click', () => {
            if(!selectedDate || !selectedTime) {
                alert('날짜와 시간을 모두 선택해주세요.');
                return;
            }
            alert(`[예약 확인]\\n날짜: 2025년 7월 ${selectedDate}일\\n시간: ${selectedTime}\\n\\n선택이 완료되었습니다.`);
        });
    });
    """
    soup.body.append(script)

# 6. Save
with open('visit_schedule_complete.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Done.")
