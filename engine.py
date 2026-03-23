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
def process_files(plan, tgt, log_path, prefix="", suffix="", custom=""):
    audit = []
    details = []
    total = sum(len(v) for v in plan.values())
    count = 0
    summary_counts = {}
    summary_txt = log_path.with_name(log_path.stem + ".log")
    with open(summary_txt, "w") as sf:
        sf.write("ag-sort Transfer Summary\n========================\n")

    for folder, files in plan.items():
        if tgt.name == folder:
            dest_dir = tgt
        else:
            dest_dir = tgt / folder
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Performance fix for Cloud/Network drives: 
        # Collect dest files by size first (fast), only hash if size matches source.
        dest_files_by_size = {}
        for df in dest_dir.glob("*"):
            if df.is_file() and df.parent != dest_dir / "duplicates":
                size = df.stat().st_size
                if size not in dest_files_by_size: dest_files_by_size[size] = []
                dest_files_by_size[size].append(df)
        
        dest_hashes = {} # Cache for lazy hashing of target files
                
        for f in files:
            try:
                pre_h = get_hash(f)
                update_bar(count, total, f"Sorting {f.name[:10]}")
                
                # Check for existing duplicate in destination
                is_duplicate = pre_h in dest_hashes
                if not is_duplicate:
                    src_size = f.stat().st_size
                    candidates = dest_files_by_size.get(src_size, [])
                    for cand in candidates:
                        # Lazy hash only if we haven't hashed this candidate yet
                        cand_h = get_hash(cand)
                        dest_hashes[cand_h] = cand
                        if cand_h == pre_h:
                            is_duplicate = True
                            break
                
                if is_duplicate:
                    dup_dir = dest_dir / "duplicates"
                    dup_dir.mkdir(exist_ok=True)
                    target = dup_dir / f"{f.name}"
                elif custom:
                    target = dest_dir / f"{custom}{f.suffix}"
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
                    ext_key = f.suffix.lower()
                    summary_counts[ext_key] = summary_counts.get(ext_key, 0) + 1
                    details.append(f"Moved {f.name} -> {target.name}")
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
    
    # Finalize logs as Read-Only for high-integrity audit trail
    try:
        os.chmod(log_path, 0o444)
        os.chmod(summary_txt, 0o444)
    except: pass
    
    return summary_counts, details
