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
    summary_txt = log_path.with_name(log_path.stem + ".log")
    with open(summary_txt, "w") as sf:
        sf.write("ag-sort Transfer Summary\n========================\n")

    for folder, files in plan.items():
        dest_dir = tgt / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        dest_hashes = {}
        for df in dest_dir.rglob("*"):
            if df.is_file() and df.parent != dest_dir / "duplicates":
                dest_hashes[get_hash(df)] = df
                
        for f in files:
            try:
                pre_h = get_hash(f)
                update_bar(count, total, f"Moving {f.name[:10]}")
                
                if pre_h in dest_hashes:
                    dup_dir = dest_dir / "duplicates"
                    dup_dir.mkdir(exist_ok=True)
                    target = dup_dir / f"{prefix}{f.stem}{suffix}{f.suffix}"
                else:
                    target = dest_dir / f"{prefix}{f.stem}{suffix}{f.suffix}"
                    
                base_name = target.stem
                ext = target.suffix
                seq = 1
                while target.exists():
                    target = target.with_name(f"{base_name}_{seq}{ext}")
                    seq += 1
                    
                shutil.copy2(str(f), str(target))
                post_h = get_hash(target)
                if pre_h == post_h:
                    f.unlink()
                    status = "VERIFIED"
                    dest_hashes[pre_h] = target
                else:
                    target.unlink()
                    status = "FAIL"
                
                entry = {"name": target.name, "old": str(f.absolute()), "new": str(target.absolute()), "hash": pre_h, "status": status}
                audit.append(entry)
                
                with open(summary_txt, "a") as sf:
                    sf.write(f"[{status}] {entry['old']} -> {entry['new']}\n")
                    
            except Exception as e: audit.append({"name": f.name, "status": str(e)})
            count += 1
            with open(log_path, "w") as lf: json.dump(audit, lf, indent=4)
            
    print(f"\n[COMPLETE] Summary saved to {str(summary_txt)}")
