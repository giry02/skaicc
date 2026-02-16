import requests
import re
from bs4 import BeautifulSoup

# 1. Fetch directly from URL (Skip local file issues)
print("Fetching pop4.html...")
url = 'https://giry02.dothome.co.kr/pop4.html'
response = requests.get(url)
response.encoding = response.apparent_encoding # Auto-detect encoding (likely utf-8 or euc-kr)
html_content = response.text

# 2. Modify JavaScript `textToType` using Regex
# Replace warning: regex on HTML might be brittle if script is minified, but pop4 seems formatted.
# textToType = "..."
try:
    new_text = "원하시는 날짜와 시간을 선택해 주세요."
    # Use re.DOTALL if needed, but usually it's one line.
    # Pattern: const textToType = "ANYTHING";
    html_content = re.sub(r'const\s+textToType\s*=\s*".*?";', f'const textToType = "{new_text}";', html_content)
    print("Updated typing text.")
except Exception as e:
    print(f"Regex failed: {e}")

# 3. Parse with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# 4. Modify Header
# Try to find header by tag or class.
header = soup.find('header')
if not header:
    # Try finding by text "SK브로드밴드" or similar if known, or just look for top bar container.
    # pop4 seems to have <header> based on general HTML structure.
    pass

if header:
    # Clear and set new title
    # But preserve class attributes!
    # If header has children, maybe keep the 'Back' or 'Close' button?
    # User said "Header title put".
    # We will look for <h1> or class 'title'.
    h1 = header.find('h1')
    if h1:
        h1.string = "방문일정 등록"
    else:
        # If no h1, assume simple header
        # Check if there is a span for title
        # Just append text
        # But we should be careful not to duplicate.
        # Let's see if we can just set textContent of the text node.
        # Simpler: Clear header content and rebuild standard header: Title + Close.
        # BUT user said "design maintained". So re-using existing classes is best.
        # We will assume header TEXT is the title.
        # We'll replace the first text node.
        found_text = False
        for content in header.contents:
            if isinstance(content, str) and content.strip():
                content.replace_with("방문일정 등록")
                found_text = True
                break
        if not found_text:
            header.append("방문일정 등록")

# 5. Modify Main Body
main_body = soup.find(id='main-content-body')
if main_body:
    print("Found main-content-body, replacing content...")
    main_body.clear()

    # Container for Form
    # Use standard div
    container = soup.new_tag('div', **{'class': 'px-6 py-4'})
    
    # 1. Title "가정 내 PC/TV 이동" (User said "Title... top put, bottom don't put" but confusing.
    # If header has "방문일정 등록", maybe content needs subtitle?
    # Image has "가정 내 PC/TV 이동".
    # I will add it.
    title_div = soup.new_tag('div', **{'class': 'mb-6'})
    h2 = soup.new_tag('h2', **{'class': 'text-xl font-bold text-gray-900 mb-1'})
    h2.string = "가정 내 PC/TV 이동"
    title_div.append(h2)
    
    desc_p = soup.new_tag('h3', **{'class': 'text-sm text-gray-500'})
    desc_p.append("{다른 방으로 이동}에 대한 방문 일정이에요.")
    title_div.append(desc_p)
    container.append(title_div)

    # 2. Calendar Grid
    cal_div = soup.new_tag('div', **{'class': 'mb-8'})
    cal_h = soup.new_tag('div', **{'class': 'font-bold text-base mb-3'})
    cal_h.string = "2025년 7월"
    cal_div.append(cal_h)

    # Days
    days_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center mb-2'})
    for d in ['오늘', '수', '목', '금', '토', '일', '월']:
        el = soup.new_tag('div', **{'class': 'text-xs text-gray-400'})
        el.string = d
        days_row.append(el)
    cal_div.append(days_row)

    # Dates
    dates_row = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center'})
    # 25(Fri) ...
    # Active: 25. Check styles.
    # We use Tailwind classes.
    # Circle for date?
    dates = [('25', True), ('26', False), ('27', False), ('28', False), ('29', False), ('30', False, True), ('1', False, True)]
    for d, active, *disabled in dates:
        d_wrap = soup.new_tag('div', **{'class': 'flex justify-center'})
        is_disabled = disabled[0] if disabled else False
        
        btn_cls = 'w-8 h-8 flex items-center justify-center rounded-full text-sm transition-colors '
        if active:
            btn_cls += 'bg-white border text-purple-600 border-purple-600 font-bold shadow-sm' 
            # Note: Image showed purple border/text for selected ("오늘").
        elif is_disabled:
            btn_cls += 'text-gray-300'
        else:
            btn_cls += 'text-gray-700 hover:bg-gray-100'

        btn = soup.new_tag('button', **{'class': btn_cls})
        btn.string = d
        d_wrap.append(btn)
        dates_row.append(d_wrap)
    cal_div.append(dates_row)
    container.append(cal_div)

    # 3. Time Slots
    time_div = soup.new_tag('div', **{'class': 'mb-8'})
    time_h = soup.new_tag('div', **{'class': 'font-bold text-base mb-3'})
    time_h.string = "원하는 시간을 선택해주세요"
    time_div.append(time_h)

    # Grid 4 cols
    t_grid = soup.new_tag('div', **{'class': 'grid grid-cols-4 gap-2'})
    times = ['10-11시', '11-12시', ('점심', True), '13-14시', '14-15시', '15-16시', '16-17시', ('17-18시', False, True)]
    for t in times:
        txt = t[0] if isinstance(t, tuple) else t
        dis = (t[1]) if isinstance(t, tuple) and len(t)>1 else False
        act = (t[2]) if isinstance(t, tuple) and len(t)>2 else False

        t_cls = 'py-2 rounded border text-xs font-medium text-center transition-colors '
        if act:
            t_cls += 'bg-blue-50 border-blue-500 text-blue-600'
        elif dis:
            t_cls += 'bg-gray-100 text-gray-400 border-transparent'
        else:
            t_cls += 'bg-white border-gray-200 text-gray-600 hover:border-gray-300'
        
        btn = soup.new_tag('button', **{'class': t_cls})
        btn.string = txt
        t_grid.append(btn)
    time_div.append(t_grid)
    container.append(time_div)

    # 4. Bottom Button "선택 완료"
    # User said "Keep bottom modal button", but we are replacing content.
    # The 'Review' image had "선택 완료" at the bottom of standard content.
    # We add it here.
    btn_div = soup.new_tag('div', **{'class': 'mt-4'})
    sub_btn = soup.new_tag('button', **{'class': 'w-full bg-[#003366] text-white py-4 rounded-xl text-lg font-bold shadow-lg'})
    sub_btn.string = "선택 완료"
    btn_div.append(sub_btn)
    container.append(btn_div)

    main_body.append(container)

# 6. Save
with open('visit_schedule_v3.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))
print("Done.")
