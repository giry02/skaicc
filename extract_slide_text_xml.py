import re
import os

def extract_text_from_xml(slide_number):
    file_path = f"temp_ppt/ppt/slides/slide{slide_number}.xml"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract text between <a:t> and </a:t>
    # Note: Sometimes text is split, but this usually gives enough context
    matches = re.findall(r'<a:t>(.*?)</a:t>', content)
    
    print(f"--- Content of Slide {slide_number} ---")
    for text in matches:
        print(text)
    print("-------------------------------------")

if __name__ == "__main__":
    extract_text_from_xml(214)
