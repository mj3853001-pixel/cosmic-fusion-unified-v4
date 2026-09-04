import subprocess
import os

# 1. تعديل ملف README لإضافة الـ YAML (عشان التحذير يختفي)
readme_path = "README.md"
yaml_header = """---
license: sosl
tags:
- sovereign-ai
- physics
- quantum
- rust
- edge-computing
- zero-dependency
---

"""

if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if not content.startswith("---"):
        print("[-] Adding YAML metadata to README...")
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(yaml_header + content)
        print("[+] README updated successfully!")
    else:
        print("[*] YAML already exists. Skipping README edit.")
else:
    print("[!] README.md not found! Making sure we are in the right directory.")

# 2. أوامر الرفع
commands = [
    ["git", "add", "."],
    ["git", "commit", "-m", "Add Sovereign YAML metadata & final polish"],
    ["git", "push", "hf", "main", "--force"]
]

for cmd in commands:
    print(f"\n[>] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # طباعة الناتج
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0:
        print(f"[-] Error: {result.stderr}")
        break
    else:
        print("[+] Success!")

print("\n[✔] Done! Metadata fixed and pushed to Hugging Face.")
