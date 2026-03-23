import os

# Define the project structure
files = {
    "security.py": r'''import hashlib, getpass, secrets, string
class VaultSecurity:
    def __init__(self, vault_dir):
        self.pwd_file = vault_dir / ".vault_key"
        self.recovery_file = vault_dir / ".recovery_key"
    def setup(self):
        if not self.pwd_file.exists():
            print("\n[FIRST-TIME SETUP] Security Initialization...")
            pwd = getpass.getpass("Create Master Vault Password: ")
            recovery = "".join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            with open(self.pwd_file, "w") as f: f.write(hashlib.sha256(pwd.encode()).hexdigest())
            with open(self.recovery_file, "w") as f: f.write(hashlib.sha256(recovery.encode()).hexdigest())
            print(f"\n[IMPORTANT] RECOVERY KEY: {recovery}\nSave this now!")
            input("Press Enter to proceed...")
    def verify(self):
        attempt = getpass.getpass("\n[SECURITY] Vault Access Required: ")
        hashed_attempt = hashlib.sha256(attempt.encode()).hexdigest()
        with open(self.pwd_file, "r") as f: return hashed_attempt == f.read().strip()
''',
    "vault.py": r'''import json, os, shutil
def search(vault_dir):
    query = input("\n[SEARCH] Enter filename keyword: ").lower()
    found = False
    for log in vault_dir.glob("*.json"):
        with open(log, "r") as f:
            for e in json.load(f):
                if query in e.get("name", "").lower():
                    print(f"\nFound: {e['name']}\nDest: {e['new']}")
                    found = True
    if not found: print("No records.")
def undo(vault_dir):
    logs = sorted(list(vault_dir.glob("*.json")), reverse=True)[:5]
    if not logs: return print("No history.")
    for i, l in enumerate(logs, 1): print(f" [{i}] {l.name}")
    c = input("\nSelect session to UNDO: ")
    try:
        with open(logs[int(c)-1], "r") as f:
            for e in json.load(f):
                if os.path.exists(e["new"]):
                    os.makedirs(os.path.dirname(e["old"]), exist_ok=True)
                    shutil.move(e["new"], e["old"])
        logs[int(c)-1].unlink()
        print("Undo successful.")
    except Exception as e: print(f"Error: {e}")
''',
    "engine.py": r'''import hashlib, shutil, json, sys
def get_hash(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""): h.update(chunk)
    return h.hexdigest()
def update_bar(count, total, task):
    percent = 100 * (count / total)
    bar = "█" * int(30 * count // total) + "-" * (30 - int(30 * count // total))
    sys.stdout.write(f"\rProgress: |{bar}| {percent:.1f}% [{task}]")
    sys.stdout.flush()
def process_files(plan, tgt, log_path, prefix, suffix):
    audit = []
    total = sum(len(v) for v in plan.values())
    count = 0
    for folder, files in plan.items():
        dest_dir = tgt / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        for f in files:
            target = dest_dir / f"{prefix}{f.stem}{suffix}{f.suffix}"
            try:
                pre_h = get_hash(f)
                update_bar(count, total, f"Moving {f.name[:10]}")
                shutil.move(str(f), str(target))
                post_h = get_hash(target)
                audit.append({"name": target.name, "old": str(f.absolute()), "new": str(target.absolute()), "hash": pre_h, "status": "VERIFIED" if pre_h == post_h else "FAIL"})
            except Exception as e: audit.append({"name": f.name, "status": str(e)})
            count += 1
            with open(log_path, "w") as lf: json.dump(audit, lf, indent=4)
    print("\n[COMPLETE]")
''',
    "interface.py": r'''import os
def logo(v):
    os.system("cls" if os.name == "nt" else "clear")
    print(rf"""
  _____ _      _____  ____  _____ _______ 
 |  __ (_)    / ____|/ __ \|  __ \__   __|
 | |__) |__ _| (___ | |  | | |__) | | |   
 |  ___/ \ \ / \___ \| |  | |  _  /  | |   
 | |   | |>  < ____) | |__| | | \ \  | |   
 |_|   |_/_/\_\_____/ \____/|_|  \_\ |_|   
        MODULAR ENGINE v{v} | LOCKED CORE
    """)
''',
    "main.py": r'''from pathlib import Path
from datetime import datetime
from collections import defaultdict
import security, vault, engine, interface
VERSION = "13.0"
EXT = {".jpg", ".png", ".mp4", ".mov", ".heic", ".jpeg"}
VAULT_DIR = Path("./.pixsort_vault"); VAULT_DIR.mkdir(exist_ok=True)
guard = security.VaultSecurity(VAULT_DIR)
def start():
    guard.setup()
    while True:
        interface.logo(VERSION)
        print("\n [1] Sort  [2] Search  [3] Undo  [Q] Quit")
        c = input("\nSelect: ").lower()
        if c == "1":
            src, tgt = Path(input("Source: ").strip()), Path(input("Target: ").strip())
            files = [f for f in src.rglob("*") if f.is_file() and f.suffix.lower() in EXT]
            plan = defaultdict(list)
            for f in files: plan[datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m")].append(f)
            print(f"\nPlan: {len(files)} files."); ren = input("Rename? [n/p/s]: ").lower()
            pre = input("Prefix: ") if ren == "p" else ""; sfx = input("Suffix: ") if ren == "s" else ""
            if input("Approve? [y/n]: ").lower() == "y":
                log = VAULT_DIR / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                engine.process_files(plan, tgt, log, pre, sfx)
            input("\nPress Enter...")
        elif c == "2" and guard.verify(): vault.search(VAULT_DIR); input("\nPress Enter...")
        elif c == "3" and guard.verify(): vault.undo(VAULT_DIR); input("\nPress Enter...")
        elif c == "q": break
if __name__ == "__main__": start()
'''
}

# Create the files
for filename, content in files.items():
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {filename}")

print("\nSuccess! Run 'python main.py' to start PixSort Pro.")