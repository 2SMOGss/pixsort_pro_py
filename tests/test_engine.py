import pytest
from pathlib import Path
import os
import hashlib
from engine import get_hash, process_files
import json

def test_sha256_hash(tmp_path):
    # Test that get_hash returns a valid SHA-256 hash instead of MD5
    f = tmp_path / "hash_test.txt"
    content = b"handshake_test_data"
    f.write_bytes(content)
    
    expected_hash = hashlib.sha256(content).hexdigest()
    actual_hash = get_hash(f)
    
    assert actual_hash == expected_hash, "Hashing must strictly use SHA-256"

def test_100_percent_integrity_handshake(tmp_path):
    # Test that files are copied using handshake, verified, and only deleted if correct
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    tgt_dir = tmp_path / "tgt"
    tgt_dir.mkdir()
    
    f = src_dir / "photo.jpg"
    f.write_text("photo data")
    
    plan = {"03-2024": [f]}
    log_path = tmp_path / "audit.json"
    
    # Process files
    process_files(plan, tgt_dir, log_path)
    
    # Check that file was moved into the correct folder
    target_file = tgt_dir / "03-2024" / "photo.jpg"
    assert target_file.exists(), "Target file was not copied correctly"
    
    # Check that the original file was strictly DELETED (because the hashes should match)
    assert not f.exists(), "Source file was not unlinked after successful integrity handshake"
    
    # Check log for VERIFIED
    with open(log_path, "r") as lf:
        audit = json.load(lf)
        assert audit[0]["status"] == "VERIFIED", "Status should be VERIFIED"

def test_collision_handling(tmp_path):
    # Test collision: same name, different hash
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    tgt_dir = tmp_path / "tgt"
    tgt_dir.mkdir()
    
    # Pre-existing file in target
    dest_dir = tgt_dir / "04-2024"
    dest_dir.mkdir(parents=True)
    existing_file = dest_dir / "img.jpg"
    existing_file.write_text("old data")
    
    # New file in source
    f = src_dir / "img.jpg"
    f.write_text("new data")
    
    plan = {"04-2024": [f]}
    log_path = tmp_path / "audit.json"
    process_files(plan, tgt_dir, log_path)
    
    # Check that it got renamed
    assert (dest_dir / "img_1.jpg").exists(), "Collision not handled with sequence number"

def test_deduplication(tmp_path):
    # Test duplication: same hash
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    tgt_dir = tmp_path / "tgt"
    tgt_dir.mkdir()
    
    dest_dir = tgt_dir / "05-2024"
    dest_dir.mkdir(parents=True)
    existing_file = dest_dir / "img.jpg"
    existing_file.write_text("duplicate data")
    
    f = src_dir / "img2.jpg"
    f.write_text("duplicate data")
    
    plan = {"05-2024": [f]}
    log_path = tmp_path / "audit.json"
    process_files(plan, tgt_dir, log_path)
    
    # Check that it went into duplicates folder
    dup_dir = dest_dir / "duplicates"
    assert (dup_dir / "img2.jpg").exists(), "Duplicate not moved to duplicates directory"

def test_smart_nested_pathing(tmp_path):
    src_dir = tmp_path / "src2"
    src_dir.mkdir()
    tgt_dir = tmp_path / "11-2021"
    tgt_dir.mkdir()
    
    f = src_dir / "photo.jpg"
    f.write_text("data")
    
    plan = {"11-2021": [f]}
    log_path = tmp_path / "audit.json"
    process_files(plan, tgt_dir, log_path)
    
    assert (tgt_dir / "photo.jpg").exists(), "Smart pathing failed, file not in root."
    assert not (tgt_dir / "11-2021").exists(), "Double nested directory was erroneously created"
