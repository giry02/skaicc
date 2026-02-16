import os
import re

root_dir = r"e:\AI_Project\MultiAgentDev\completed"
target_link = "'../index.html'"
index_link = "'./index.html'"

def update_home_link(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        modified = False
        
        rel_path = os.path.relpath(file_path, root_dir)
        is_root = os.path.dirname(rel_path) == ''
        correct_link = index_link if is_root else target_link

        for i, line in enumerate(lines):
            if 'data-lucide="home"' in line:
                # Search backwards for the <button start
                button_start_idx = -1
                for j in range(i, max(-1, i-10), -1):
                    if '<button' in lines[j]:
                        button_start_idx = j
                        break
                
                if button_start_idx != -1:
                    # Now search from button_start_idx to i (inclusive) for onclick
                    for k in range(button_start_idx, i + 1):
                        if 'onclick=' in lines[k]:
                            # Found the onclick line
                            # Check if it already has the correct link
                            if f"location.href={correct_link}" in lines[k]:
                                break
                            
                            pattern = r"location\.href\s*=\s*(['\"])(.*?)\1"
                            match = re.search(pattern, lines[k])
                            
                            if match:
                                current_url = match.group(2)
                                new_line = re.sub(pattern, f"location.href={correct_link}", lines[k])
                                lines[k] = new_line
                                modified = True
                                print(f"[UPDATED] {rel_path}: {current_url} -> {correct_link}")
                            # Stop searching for onclick for this button
                            break
                            
        if modified:
             with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(lines))

    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")

print("Starting link update...")
for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".html"):
            update_home_link(os.path.join(subdir, file))
print("Completed.")
