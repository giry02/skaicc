import sys
import os

print("Debugging import...")
try:
    from workflow.orchestrator import Orchestrator
    print("Import SUCCESS!")
except Exception as e:
    print(f"Import FAILED: {e}")
except SyntaxError as e:
    print(f"SyntaxError: {e}")

print("Checking workflow/orchestrator.py...")
with open("workflow/orchestrator.py", "rb") as f:
    content = f.read()
    if b'\x00' in content:
        print("FAIL: workflow/orchestrator.py contains NULL bytes")
    else:
        print("OK: workflow/orchestrator.py is clean")

print("Checking workflow/__init__.py...")
with open("workflow/__init__.py", "rb") as f:
    content = f.read()
    if b'\x00' in content:
        print("FAIL: workflow/__init__.py contains NULL bytes")
    else:
        print("OK: workflow/__init__.py is clean")
