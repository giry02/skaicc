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

# 4. Modify Header Title (Keep as "방문일정 등록")
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
    
    # 1. Update the H2 inside target-anchor
    h2 = target_anchor.find('h2')
    if h2:
        # User wants "{다른 방으로 이동}" in BLACK.
        h2.clear()
        
        span = soup.new_tag('span', **{'class': 'text-black'}) # Explicitly black
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

    # Calendar Grid
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

    # Dates
    dates_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center'})
    dates = [('25', True), ('26', False), ('27', False), ('28', False), ('29', False), ('30', False, True), ('1', False, True)]
    # Brand Color: #5031E5
    for d, active, *disabled in dates:
        d_wrap = soup.new_tag('div', **{'class': 'flex justify-center'})
        is_disabled = disabled[0] if disabled else False
        
        btn_cls = 'w-10 h-10 flex items-center justify-center rounded-full text-[17px] transition-colors '
        if active:
            # Active: White bg, Brand Border, Brand Text
            btn_cls += 'bg-white border-2 text-[#5031E5] border-[#5031E5] font-bold shadow-sm' 
        elif is_disabled:
            btn_cls += 'text-gray-300 cursor-default'
        else:
            btn_cls += 'text-[#333] hover:bg-gray-50'

        btn = soup.new_tag('button', **{'class': btn_cls})
        btn.string = d
        d_wrap.append(btn)
        dates_row.append(d_wrap)
    cal_div.append(dates_row)
    form_container.append(cal_div)

    # Time Slots
    time_div = soup.new_tag('div', **{'class': 'mb-8'})
    time_h = soup.new_tag('div', **{'class': 'font-bold text-lg text-[#1a1a1a] mb-4'})
    time_h.string = "원하는 시간을 선택해주세요"
    time_div.append(time_h)

    t_grid = soup.new_tag('div', **{'class': 'grid grid-cols-4 gap-2'})
    times = ['10-11시', '11-12시', ('점심', True), '13-14시', '14-15시', '15-16시', '16-17시', ('17-18시', False, True)]
    for t in times:
        txt = t[0] if isinstance(t, tuple) else t
        dis = (t[1]) if isinstance(t, tuple) and len(t)>1 else False
        act = (t[2]) if isinstance(t, tuple) and len(t)>2 else False

        t_cls = 'py-3 rounded-lg border text-[15px] font-medium text-center transition-colors '
        if act:
            # Active: Brand-light bg, Brand Border, Brand Text
            t_cls += 'bg-[#eff6ff] border-[#5031E5] text-[#5031E5]' 
        elif dis:
            t_cls += 'bg-[#f5f5f5] text-[#aaa] border-transparent'
        else:
            t_cls += 'bg-white border-[#ddd] text-[#444] hover:border-[#bbb]'
        
        btn = soup.new_tag('button', **{'class': t_cls})
        btn.string = txt
        t_grid.append(btn)
    time_div.append(t_grid)
    form_container.append(time_div)

    # Button
    btn_div = soup.new_tag('div', **{'class': 'mt-6'})
    # Submit Button: Brand Background
    sub_btn = soup.new_tag('button', **{'class': 'w-full bg-[#5031E5] text-white py-4 rounded-xl text-[19px] font-bold shadow-lg hover:bg-[#4020d0] transition-colors'})
    sub_btn.string = "선택 완료"
    btn_div.append(sub_btn)
    form_container.append(btn_div)

    main_body.append(form_container)

# 6. Save
with open('visit_schedule_v5.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Done.")
