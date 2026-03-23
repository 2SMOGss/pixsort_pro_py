import pytest
from pathlib import Path
from datetime import datetime
import os
from main import get_file_metadata

def test_metadata_extraction_fallback(tmp_path):
    # Test OS ctime fallback (no EXIF data)
    test_file = tmp_path / "test_no_exif.txt"
    test_file.write_text("dummy")
    
    # Extract
    extracted_date = get_file_metadata(test_file)
    
    # Should be the ctime (creation time) string in MM-YYYY format
    expected_date = datetime.fromtimestamp(test_file.stat().st_ctime).strftime("%m-%Y")
    
    assert extracted_date == expected_date
