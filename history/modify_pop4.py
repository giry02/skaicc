import requests
from bs4 import BeautifulSoup

# 1. Fetch pop4.html
url = 'https://giry02.dothome.co.kr/pop4.html'
response = requests.get(url)
response.encoding = 'utf-8' # Ensure correct encoding
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

# 2. Modify Header Title (if exists, usually first h1 or header text)
# pop4.html has <title> and maybe a visible header. Let's find common header patterns.
header = soup.find('header')
if header:
    # Assuming h1 inside header or just text
    h1 = header.find('h1')
    if h1:
        h1.string = "방문일정 등록"
    else:
        # If text is directly in header
        header.string = "방문일정 등록"
        # Restore close button if it was there (often absolute positioned span/button)
        # We might have wiped it. Let's check children first.
        # Actually safer to find the specific text node or element if possible.
        # But for now, let's assume simple replacement or append close button.
        close_btn = soup.new_tag('span', **{'class': 'absolute right-4 top-4 cursor-pointer text-xl'})
        close_btn.string = '✕'
        header.append(close_btn)

# 3. Locate Main Content Body
main_body = soup.find(id='main-content-body')
if main_body:
    # Clear existing content (The "Info cards" and "Typing text bubbles")
    main_body.clear()

    # 4. Create New Content (Visit Schedule Form)
    # Container for form
    container = soup.new_tag('div', **{'class': 'px-5 py-6 bg-white rounded-t-3xl min-h-[500px]'}) # White background container
    
    # Title Section
    title_div = soup.new_tag('div', **{'class': 'mb-6'})
    h2 = soup.new_tag('h2', **{'class': 'text-xl font-bold text-gray-900 mb-2'})
    h2.string = "가정 내 PC/TV 이동"
    p = soup.new_tag('p', **{'class': 'text-sm text-gray-600'})
    span = soup.new_tag('span', **{'class': 'text-blue-600 font-bold'})
    span.string = "{다른 방으로 이동}"
    p.append(span)
    p.append("에 대한 방문 일정이에요.")
    title_div.append(h2)
    title_div.append(p)
    container.append(title_div)

    # Blue Banner
    banner = soup.new_tag('div', **{'class': 'bg-[#4a86e8] text-white p-4 -mx-5 mb-6 text-lg font-medium leading-snug'})
    banner.string = "원하시는 날짜와 시간을 선택해 주세요." # Use decode if needed for korean characters? bs4 handles it.
    # Actually need <br> for break.
    banner.clear()
    banner.append("원하시는 날짜와 시간을 선택해")
    banner.append(soup.new_tag('br'))
    banner.append("주세요.")
    container.append(banner)

    # Calendar Section
    cal_div = soup.new_tag('div', **{'class': 'mb-8'})
    cal_header = soup.new_tag('div', **{'class': 'text-sm font-bold text-gray-900 mb-3'})
    cal_header.string = "2025년 7월"
    cal_div.append(cal_header)

    # Grid
    grid = soup.new_tag('div', **{'class': 'grid grid-cols-7 gap-1 text-center'})
    days = ['오늘', '수', '목', '금', '토', '일', '월']
    for d in days:
        th = soup.new_tag('div', **{'class': 'text-xs text-gray-400 mb-2'})
        th.string = d
        grid.append(th)
    
    # Dates (Example 25th selected)
    dates = [
        ('25', True), ('26', False), ('27', False), ('28', False), 
        ('29', False), ('30', False, True), ('1', False, True)
    ]
    for d_text, is_selected, *is_disabled in dates:
        classes = 'py-2 rounded-lg text-sm cursor-pointer transition-colors duration-200 '
        if is_selected:
            classes += 'bg-white border-2 border-[#6c5ce7] text-[#6c5ce7] font-bold shadow-sm'
        elif is_disabled:
            classes += 'text-gray-300 cursor-default'
        else:
            classes += 'text-gray-900 hover:bg-gray-100'
        
        btn = soup.new_tag('div', **{'class': classes})
        btn.string = d_text
        grid.append(btn)
    
    cal_div.append(grid)
    container.append(cal_div)

    # Time Slots Section
    time_div = soup.new_tag('div', **{'class': 'mb-24'}) # Margin bottom for fixed button space
    time_header = soup.new_tag('div', **{'class': 'text-sm font-bold text-gray-900 mb-3'})
    time_header.string = "원하는 시간을 선택해주세요"
    time_div.append(time_header)

    time_grid = soup.new_tag('div', **{'class': 'grid grid-cols-4 gap-2'})
    times = [
        ('10-11시', False), ('11-12시', False), ('점심', False, True),
        ('13-14시', False), ('14-15시', False), ('15-16시', False),
        ('16-17시', False), ('17-18시', True) # Selected
    ]
    for t_text, is_selected, *is_disabled in times:
        classes = 'py-3 rounded-md text-xs font-medium text-center transition-all duration-200 border '
        if is_selected:
            classes += 'bg-blue-50 border-blue-600 text-blue-600 font-bold'
        elif is_disabled:
            classes += 'bg-gray-200 text-gray-400 border-transparent cursor-not-allowed'
        else:
            classes += 'bg-gray-100 text-gray-600 border-transparent hover:bg-gray-200 cursor-pointer'
        
        btn = soup.new_tag('div', **{'class': classes})
        btn.string = t_text
        time_grid.append(btn)
    
    time_div.append(time_grid)
    container.append(time_div)

    # Append container to main body
    main_body.append(container)


# 5. Modify Bottom Button (if exists) or Add Fixed Button
# Check for existing bottom bar or create new one
# Usually pop4 might have a button area. If not, we add one.
# Looking at pop4 source snippet (from previous step), it mentions `showBottomElements`.
# We'll add a fixed bottom button container.
bottom_bar = soup.new_tag('div', **{'class': 'fixed bottom-0 left-0 right-0 p-5 bg-white border-t border-gray-100 max-w-md mx-auto'})
submit_btn = soup.new_tag('button', **{'class': 'w-full py-4 bg-[#003366] text-white rounded-xl text-lg font-bold shadow-lg active:scale-[0.98] transition-transform'})
submit_btn.string = "선택 완료"
bottom_bar.append(submit_btn)
soup.body.append(bottom_bar)

# 6. Save modified HTML
with open('visit_schedule_v2.html', 'w', encoding='utf-8') as f:
    f.write(str(soup))

print("Successfully created visit_schedule_v2.html")
