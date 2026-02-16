import requests
import re
import os
from bs4 import BeautifulSoup

# =================================================================================
# [스크립트 설명: PPT Page 213 구현 (이동 위치 선택)]
# 파일명: page213_move_location.html
# 주요 내용:
# 1. 헤더: "서비스 안내" (좌측 홈 아이콘)
# 2. 본문: "이동할 위치를 선택해 주세요."
# 3. 선택 옵션: "같은 방 내에서 이동", "다른 방으로 이동" (2열 그리드)
# 4. 안내 사항: 배선 공사 관련 주의사항 텍스트
# 5. 버튼: "신청하기" (visit_schedule_modal.html 로 이동)
# =================================================================================

BASE_DIR = 'completed'
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

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
    new_text = "이동할 위치를 선택해 주세요."
    html_content = re.sub(r'const\s+textToType\s*=\s*".*?";', f'const textToType = "{new_text}";', html_content)
except Exception as e:
    print(f"Regex failed: {e}")

soup = BeautifulSoup(html_content, 'html.parser')

# 3. 헤더 수정
header = soup.find('header')
if header:
    # 홈 아이콘
    left_btn = header.find('button')
    if left_btn:
        left_btn.clear()
        home_svg = soup.new_tag('svg', **{
            'xmlns': "http://www.w3.org/2000/svg",
            'width': "24",
            'height': "24",
            'viewBox': "0 0 24 24",
            'fill': "none",
            'stroke': "currentColor",
            'stroke-width': "2",
            'stroke-linecap': "round",
            'stroke-linejoin': "round",
            'class': "lucide lucide-home"
        })
        path1 = soup.new_tag('path', d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z")
        path2 = soup.new_tag('polyline', points="9 22 9 12 15 12 15 22")
        home_svg.append(path1)
        home_svg.append(path2)
        left_btn.append(home_svg)

    h1 = header.find('h1')
    if h1: h1.string = "서비스 안내"

# 4. 메인 컨텐츠 구성
main_body = soup.find(id='main-content-body')
target_anchor = soup.find(id='target-anchor')

if main_body and target_anchor:
    print("UI 구성 중 (Page 213 Location Selection)...")
    
    # 타이틀
    h2 = target_anchor.find('h2')
    if h2:
        h2.clear()
        span = soup.new_tag('span', **{'class': 'text-black font-bold'})
        span.string = "이동할 위치를"
        h2.append(span)
        h2.append(soup.new_tag('br'))
        h2.append("선택해 주세요.")

    target_anchor_extracted = target_anchor.extract()
    main_body.clear()
    
    wrapper = soup.new_tag('div', **{'class': 'flex flex-col h-full bg-white px-1'}) 
    wrapper.append(target_anchor_extracted)
    
    # [4-3] 위치 선택 영역 (가이드 준수 콤팩트 그리드)
    option_grid = soup.new_tag('div', **{'class': 'mt-6 mb-4 grid grid-cols-2 gap-3'})
    
    card_cls = 'location-option relative flex flex-col items-center justify-center p-4 aspect-square rounded-2xl border border-gray-100 bg-gray-50 cursor-pointer transition-all active:scale-95'
    
    # 옵션 1: 같은 방
    opt1 = soup.new_tag('div', **{'class': card_cls, 'onclick': "selectLocation(this, 'same_room')"})
    icon1 = soup.new_tag('div', **{'class': 'w-10 h-10 rounded-full bg-white flex items-center justify-center text-xl mb-2 shadow-sm'})
    icon1.string = "🏠"
    opt1.append(icon1)
    text1 = soup.new_tag('span', **{'class': 'text-[14px] font-bold text-gray-800 text-center leading-tight'})
    text1.string = "같은 방 내에서\n이동"
    # replace newline with br for proper rendering
    text1.clear()
    text1.append("같은 방 내에서")
    text1.append(soup.new_tag('br'))
    text1.append("이동")
    opt1.append(text1)
    
    chk1 = soup.new_tag('div', **{'class': 'absolute top-3 right-3 text-[#5031E5] opacity-0 check-mark'})
    svg1 = soup.new_tag('svg', **{'xmlns':"http://www.w3.org/2000/svg", 'width':"18", 'height':"18", 'viewBox':"0 0 24 24", 'fill':"none", 'stroke':"currentColor", 'stroke-width':"3", 'stroke-linecap':"round", 'stroke-linejoin':"round"})
    svg1.append(soup.new_tag('polyline', points="20 6 9 17 4 12"))
    chk1.append(svg1)
    opt1.append(chk1)
    option_grid.append(opt1)

    # 옵션 2: 다른 방
    opt2 = soup.new_tag('div', **{'class': card_cls, 'onclick': "selectLocation(this, 'diff_room')"})
    icon2 = soup.new_tag('div', **{'class': 'w-10 h-10 rounded-full bg-white flex items-center justify-center text-xl mb-2 shadow-sm'})
    icon2.string = "🚪"
    opt2.append(icon2)
    text2 = soup.new_tag('span', **{'class': 'text-[14px] font-bold text-gray-800 text-center leading-tight'})
    text2.clear()
    text2.append("다른 방으로")
    text2.append(soup.new_tag('br'))
    text2.append("이동")
    opt2.append(text2)
    
    chk2 = soup.new_tag('div', **{'class': 'absolute top-3 right-3 text-[#5031E5] opacity-0 check-mark'})
    svg2 = soup.new_tag('svg', **{'xmlns':"http://www.w3.org/2000/svg", 'width':"18", 'height':"18", 'viewBox':"0 0 24 24", 'fill':"none", 'stroke':"currentColor", 'stroke-width':"3", 'stroke-linecap':"round", 'stroke-linejoin':"round"})
    svg2.append(soup.new_tag('polyline', points="20 6 9 17 4 12"))
    chk2.append(svg2)
    opt2.append(chk2)
    option_grid.append(opt2)
    
    wrapper.append(option_grid)

    # [4-4] 주의 사항 (Page 213 텍스트 반영)
    info_box = soup.new_tag('div', **{'class': 'bg-[#F1F3F5] rounded-xl p-4 mb-4'})
    info_flex = soup.new_tag('div', **{'class': 'flex gap-2'})
    info_icon = soup.new_tag('div', **{'class': 'w-5 h-5 rounded-full bg-[#868E96] text-white flex items-center justify-center text-[11px] flex-shrink-0 font-bold'})
    info_icon.string = "i"
    info_flex.append(info_icon)
    
    info_txt = soup.new_tag('p', **{'class': 'text-[12px] text-[#495057] leading-relaxed'})
    info_txt.string = "단, 배선 공사가 필요하거나 외부로 노출되지 않고 안내 장치 설치를 하는 등은 추가 비용이 발생할 수 있습니다."
    info_flex.append(info_txt)
    info_box.append(info_flex)
    wrapper.append(info_box)

    # [4-5] 하단 버튼
    btn_div = soup.new_tag('div', **{'class': 'mt-auto pt-2 pb-4'})
    sub_btn = soup.new_tag('button', **{
        'id': 'apply-btn', 
        'class': 'w-full bg-[#E9ECEF] text-[#ADB5BD] py-4 rounded-xl text-[18px] font-bold transition-all cursor-not-allowed',
        'disabled': 'disabled',
        'onclick': "goToSchedule()"
    })
    sub_btn.string = "신청하기"
    btn_div.append(sub_btn)
    wrapper.append(btn_div)
    
    main_body.append(wrapper)

    # JS
    js_content = """
    <script>
    let selectedLoc = null;

    function selectLocation(el, loc) {
        document.querySelectorAll('.location-option').forEach(opt => {
            opt.classList.remove('border-[#5031E5]', 'bg-[#eff6ff]', 'ring-2', 'ring-[#5031E5]/20');
            opt.classList.add('border-gray-100', 'bg-gray-50');
            opt.querySelector('.check-mark').classList.add('opacity-0');
        });

        el.classList.remove('border-gray-100', 'bg-gray-50');
        el.classList.add('border-[#5031E5]', 'bg-[#eff6ff]', 'ring-2', 'ring-[#5031E5]/20');
        el.querySelector('.check-mark').classList.remove('opacity-0');
        
        selectedLoc = loc;
        
        const btn = document.getElementById('apply-btn');
        btn.disabled = false;
        btn.onclick = () => location.href = 'visit_schedule_modal.html';
        btn.classList.remove('bg-[#E9ECEF]', 'text-[#ADB5BD]', 'cursor-not-allowed');
        btn.classList.add('bg-[#5031E5]', 'text-white', 'shadow-lg');
    }
    </script>
    """
    soup.body.append(BeautifulSoup(js_content, 'html.parser'))
    # soup.body.contents[-1].replace_with(BeautifulSoup(js_content, 'html.parser'))

# 5. 저장
output_filename = os.path.join(BASE_DIR, 'page213_move_location.html')
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(str(soup))
print(f"HTML 생성 완료: {output_filename}")
