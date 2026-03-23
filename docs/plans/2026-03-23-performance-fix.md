# performance-fix Implementation Plan

**Goal**: Optimize `engine.py` to prevent "freezing" when sorting into cloud-mounted drives (like Google Drive).

**Architecture**: Implement lazy hashing for destination files using file size as a pre-filter.

---

### Task 1: Optimize Destination Deduplication Scanning

**Files**:
- Modify: `engine.py`

**Steps**:
1. Scan for file sizes in the target directory first (fast even on cloud drives).
2. For each source file, only hash matching-sized destination files.
3. Maintain a cache of destination hashes to avoid re-hashing.

**Verify**:
- Run tests: `pytest tests/`
- All tests should still pass (ensures deduplication still works).

---

### Task 2: Re-run the Sort with the Fix

**Step**:
1. Re-run `main.py` and notify the user to try again.
