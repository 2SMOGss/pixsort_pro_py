from pathlib import Path
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
