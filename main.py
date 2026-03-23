from pathlib import Path
from datetime import datetime
from collections import defaultdict
import exifread
import security, vault, engine, interface
VERSION = "13.0"
EXT = {".jpg", ".png", ".mp4", ".mov", ".heic", ".jpeg"}
VAULT_DIR = Path("./.pixsort_vault"); VAULT_DIR.mkdir(exist_ok=True)
guard = security.VaultSecurity(VAULT_DIR)

def get_file_metadata(filepath: Path) -> str:
    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False, stop_tag='EXIF DateTimeOriginal')
            if 'EXIF DateTimeOriginal' in tags:
                date_str = str(tags['EXIF DateTimeOriginal'])
                date_obj = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                return date_obj.strftime("%m-%Y")
    except Exception:
        pass
    return datetime.fromtimestamp(filepath.stat().st_ctime).strftime("%m-%Y")

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
            for f in files: plan[get_file_metadata(f)].append(f)
            print(f"\nPlan: {len(files)} files.")
            print("Renaming options:")
            print(" [n] None  [c] Custom Name  [p] Prefix  [s] Suffix")
            choice = input("Select: ").lower()
            
            custom = ""; prefix = ""; suffix = ""
            if choice == "c": custom = input("Custom Name: ").strip()
            elif choice == "p": prefix = input("Prefix: ").strip()
            elif choice == "s": suffix = input("Suffix: ").strip()
            
            if input("Approve? [y/n]: ").lower() == "y":
                log = VAULT_DIR / f"audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                summary_counts, details = engine.process_files(plan, tgt, log, prefix, suffix, custom)
                
                print("\n" + "="*40)
                print("TRANSFER SUMMARY")
                print("="*40)
                for entry in details:
                    print(entry)
                print("-" * 40)
                for ext, count in summary_counts.items():
                    print(f"Moved {count} {ext} files.")
                print("="*40)
            input("\nPress Enter...")
        elif c == "2" and guard.verify(): vault.search(VAULT_DIR); input("\nPress Enter...")
        elif c == "3" and guard.verify(): vault.undo(VAULT_DIR); input("\nPress Enter...")
        elif c == "q": break
if __name__ == "__main__": start()
