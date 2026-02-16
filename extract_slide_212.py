from utils.file_reader import read_file_content
import os

def extract_slide_212():
    filename = "SKB_AICC_콜봇_멀티모달_화면기획서_v1.73_250211.pptx"
    # Assuming the file is in 'inputs' relative to project root
    # script is in root (MultiAgentDev)
    file_path = f"inputs/{filename}"
    
    print(f"Reading {file_path}...")
    content = read_file_content(file_path)
    
    if "[Error]" in content:
        print(content)
        return

    # Find Slide 212
    start_marker = "--- Slide 212 ---"
    end_marker = "--- Slide 213 ---"
    
    start_idx = content.find(start_marker)
    if start_idx == -1:
        print(f"Could not find {start_marker}")
        return
        
    end_idx = content.find(end_marker)
    
    if end_idx == -1:
        # Last slide maybe?
        slide_content = content[start_idx:]
    else:
        slide_content = content[start_idx:end_idx]
        
    print("="*50)
    print(slide_content)
    print("="*50)

if __name__ == "__main__":
    extract_slide_212()
