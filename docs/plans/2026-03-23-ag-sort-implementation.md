# ag-sort Upgrade Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Upgrade the existing script to securely sort files by EXIF/OS metadata into `MM-YYYY` folders with 100% data integrity, cryptographic handshake deduplication, and detailed logging/reporting.

**Architecture:** Modifies `main.py` to extract correct `DateTimeOriginal` and OS `st_ctime` attributes. Updates `engine.py` to securely copy files, perform a SHA-256 integrity check ("Handshake"), handle file collisions by appending sequence numbers, and handle duplicate files by moving them into a `duplicates` subfolder. Finally, updates the interface to print a summary of all operations.

**Tech Stack:** Python 3, `hashlib`, `shutil`, `exifread` (or `PIL.Image.Exif`), `datetime`

---

### Task 1: Add dependencies and test structure for Metadata Extraction

**Files:**
- Create: `requirements.txt`
- Create: `tests/test_main.py`
- Modify: `main.py`

**Step 1: Write the failing test**

```python
import pytest
from pathlib import Path
from datetime import datetime

# A mock function mapping from main
def test_metadata_extraction(tmp_path):
    # Setup mock file structure and test correct 'MM-YYYY' extraction
    pass # Will implement detailed test in test_main.py
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`
Expected: FAIL due to unimplemented functions.

**Step 3: Write minimal implementation**

Modify `main.py` to include `pip install` required libraries in the plan documentation, and update the metadata extraction loop for `MM-YYYY`. 

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_main.py main.py
git commit -m "feat: EXIF metadata extraction and MM-YYYY sorting logic"
```

### Task 2: Implement the 100% Integrity Handshake and SHA-256 Engine

**Files:**
- Create: `tests/test_engine.py`
- Modify: `engine.py`

**Step 1: Write the failing test**

```python
def test_engine_process_files(tmp_path):
    # Mock source file, call process_files, check if safely copied and original deleted if hash matched
    assert False, "To be implemented"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_engine.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Rewrite `engine.get_hash()` to use SHA-256. 
Rewrite `engine.process_files()` to:
1. Copy using `shutil.copy2()`.
2. Check `get_hash(src) == get_hash(dst)`.
3. If matches, `unlink(src)`.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_engine.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/test_engine.py engine.py
git commit -m "feat: 100% integrity handshake with SHA-256"
```

### Task 3: Implement Deduplication, Collisions, and Summary Reporting

**Files:**
- Modify: `engine.py`

**Step 1: Write the failing test**

Update `test_engine.py` to include tests for exact hash matches (true duplicates going to `MM-YYYY/duplicates/`) and same name collisions (appending _1, _2). Add test for text summary.

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_engine.py -v`
Expected: FAIL

**Step 3: Write minimal implementation**

Update `engine.process_files()` to:
1. Check destination dir for existing identical hashes.
2. If collision, handle names safely.
3. Write to `.log`.
4. Return a summary dictionary.
Update `main.py` to print this summary.

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_engine.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add engine.py main.py
git commit -m "feat: deduplication, name collisions, and console summary"
```
