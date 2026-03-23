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
    process_files(plan, tgt_dir, log_path, prefix="", suffix="")
    
    # Check that file was moved into the correct folder
    target_file = tgt_dir / "03-2024" / "photo.jpg"
    assert target_file.exists(), "Target file was not copied correctly"
    
    # Check that the original file was strictly DELETED (because the hashes should match)
    assert not f.exists(), "Source file was not unlinked after successful integrity handshake"
    
    # Check log for VERIFIED
    with open(log_path, "r") as lf:
        audit = json.load(lf)
        assert audit[0]["status"] == "VERIFIED", "Status should be VERIFIED"
