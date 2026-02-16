import os
import glob

def fix_files():
    print("Checking and fixing null bytes in .py files...")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    exts = ['*.py']
    
    files = []
    for ext in exts:
        files.extend(glob.glob(os.path.join(root_dir, '**', ext), recursive=True))
    
    for file_path in files:
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            if b'\x00' in content:
                print(f"[FIXING] Null bytes found in: {file_path}")
                
                filename = os.path.basename(file_path)
                
                # Only auto-fix __init__.py for now as they are empty/simple
                if filename == "__init__.py":
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("# package initialized")
                    print(f"  -> Recreated clean {filename}")
                else:
                    print(f"  -> [WARNING] Critical file corrupted: {file_path}. Ask agent to restore.")

        except Exception as e:
            print(f"[ERROR] Could not process {file_path}: {e}")

if __name__ == "__main__":
    fix_files()
