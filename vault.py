import json, os, shutil
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
        
        # Make the log writeable to allow cleanup after successful undo
        try: os.chmod(logs[int(c)-1], 0o666)
        except: pass
        
        logs[int(c)-1].unlink()
        print("Undo successful.")
    except Exception as e: print(f"Error: {e}")
