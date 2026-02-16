import os

ROOT_DIR = r"e:\AI_Project\MultiAgentDev\completed"
target_files = []

# Walk manually or just use the list I found
for root, dirs, files in os.walk(ROOT_DIR):
    for file in files:
        if file.endswith(".html"):
            target_files.append(os.path.join(root, file))

START_MARKER_HINT = 'id="swipe-area"'
END_MARKER_HINT = 'id="fail-modal"'

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if START_MARKER_HINT not in content:
        print(f"Skipping {file_path}: No swipe-area found.")
        return

    # Find the start of the block
    # We look for the comment <!-- [컴포넌트 주입 영역] --> or just the div
    start_idx = content.find('<!-- [컴포넌트 주입 영역] -->')
    if start_idx == -1:
        # Try finding the div directly
        # <div ... id="swipe-area">
        # We need to find the opening tag of the div that contains id="swipe-area"
        # This is strictly relying on the formatting provided by the user in previous examples
        # Let's try to be a bit robust.
        # Find the line containing id="swipe-area" and go back to the start of that tag.
        pass
    
    # Actually, the user's code block usually starts with <!-- [컴포넌트 주입 영역] -->
    # and ends with the closing div of fail-modal.
    
    # Robust approach:
    # 1. Provide the exact string of the block is hard.
    # 2. We can use string slicing if we locate markers.
    
    # Locate Start: <!-- [컴포넌트 주입 영역] -->
    # If not present, look for <div ... id="swipe-area">
    
    start_marker = '<!-- [컴포넌트 주입 영역] -->'
    start_pos = content.find(start_marker)
    
    if start_pos == -1:
         # Fallback: Look for the div line
         # <div class="w-full ... ... id="swipe-area">
         swipe_area_pos = content.find('id="swipe-area"')
         if swipe_area_pos == -1: return
         # Search backwards for <div
         start_pos = content.rfind('<div', 0, swipe_area_pos)
    
    # Locate End: Closing div of fail-modal
    # Structure: <div ... id="fail-modal"> ... </div>
    fail_modal_pos = content.find('id="fail-modal"')
    if fail_modal_pos == -1:
        print(f"Skipping {file_path}: Found swipe-area but no fail-modal.")
        return
        
    # We need to find the closing div of this modal.
    # Since it's nested: 
    # <div id="fail-modal">
    #    <div class="absolute inset-0 ..."></div>
    #    <div class="absolute bottom-0 ...">
    #       ...
    #    </div>
    # </div>
    # Counting divs is risky without a parser.
    # However, in the user's snippet, the next sibling is usually <script src="js/common_ui.js"></script>
    # So we can look for the script tag.
    
    script_pos = content.find('src="js/common_ui.js"', fail_modal_pos)
    if script_pos == -1:
        script_pos = content.find('src="../js/common_ui.js"', fail_modal_pos)
    
    if script_pos == -1:
         print(f"Skipping {file_path}: Could not find common_ui.js script tag.")
         return

    # Find the tag start "<script" before that src
    end_pos = content.rfind('<script', 0, script_pos)
    
    # Now we have the range [start_pos : end_pos] to replace.
    # Double check that we aren't cutting off too much.
    
    # Determine the replacement path
    # relative to e:\AI_Project\MultiAgentDev\completed
    rel_path = os.path.relpath(file_path, ROOT_DIR)
    depth = rel_path.count(os.sep)
    
    if depth == 0:
        js_path = "js/agent_overlay.js"
    else:
        js_path = "../" * depth + "js/agent_overlay.js"
        
    new_script_tag = f'<script src="{js_path}"></script>\n    '
    
    # Check if we already have it
    if js_path in content:
        print(f"Skipping {file_path}: Already has agent_overlay.js")
        return

    # Construct new content
    new_content = content[:start_pos] + new_script_tag + content[end_pos:]
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated {file_path}")

# Run
for f in target_files:
    # Skip the template file itself or files we don't want to touch
    if "agent_overlay.js" in f: continue
    if "agent_overlay.html" in f: continue
    try:
        process_file(f)
    except Exception as e:
        print(f"Error processing {f}: {e}")
