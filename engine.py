import hashlib, shutil, json, sys
def get_hash(path):
    h = hashlib.sha256()
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
                shutil.copy2(str(f), str(target))
                post_h = get_hash(target)
                if pre_h == post_h:
                    f.unlink()
                    status = "VERIFIED"
                else:
                    target.unlink()
                    status = "FAIL"
                audit.append({"name": target.name, "old": str(f.absolute()), "new": str(target.absolute()), "hash": pre_h, "status": status})
            except Exception as e: audit.append({"name": f.name, "status": str(e)})
            count += 1
            with open(log_path, "w") as lf: json.dump(audit, lf, indent=4)
    print("\n[COMPLETE]")
