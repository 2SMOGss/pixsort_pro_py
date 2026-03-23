# Custom Upgrades Implementation Plan

> **For Antigravity:** REQUIRED WORKFLOW: Use `.agent/workflows/execute-plan.md` to execute this plan in single-flow mode.

**Goal:** Clean up the CLI by removing renaming, fix nested path creation, and add a file-typified transfer summary to the console output.

**Architecture:** Modifies `main.py` and `engine.py` to streamline the user experience based on the second design document.

---

### Task 1: Remove CLI Renaming and Pass Original Names

**Files:**
- Modify: `main.py`
- Modify: `engine.py`
- Modify: `tests/test_engine.py`
- Modify: `tests/test_main.py`

**Step 1: Write the failing test**

Update tests to remove `prefix` and `suffix` arguments.

**Step 2: Write minimal implementation**

Remove the renaming prompts from `main.py`. Remove `prefix` and `suffix` arguments from `engine.process_files(...)`. 

**Step 3: Run test to verify it passes**

Run: `pytest tests/`
Expected: PASS

**Step 4: Commit**

```bash
git add .
git commit -m "feat: removed all renaming prompts"
```

### Task 2: Fix Nested Directory Pathing

**Files:**
- Modify: `engine.py`
- Modify: `tests/test_engine.py`

**Step 1: Write the failing test**

Add a test where the `tgt` path ends with exactly the same string as the `folder` key (e.g., tgt: `temp/03-2024`, folder: `03-2024`), asserting it doesn't create `temp/03-2024/03-2024`.

**Step 2: Write minimal implementation**

Update `engine.process_files`:
```python
if tgt.name == folder:
    dest_dir = tgt
else:
    dest_dir = tgt / folder
```

**Step 3: Run test to verify it passes**

Run: `pytest tests/test_engine.py`
Expected: PASS

**Step 4: Commit**

```bash
git add .
git commit -m "fix: smart nested directory pathing"
```

### Task 3: Implement Detailed File-Type Output Summary

**Files:**
- Modify: `engine.py`
- Modify: `main.py`

**Step 1: Write the failing test**

Update `test_engine.py` to assert that `process_files` returns a dictionary of counts.

**Step 2: Write minimal implementation**

Add `summary_counts = defaultdict(int)` to `engine.py`. During the loop, if VERIFIED, `summary_counts[target.suffix.lower()] += 1`. Return `summary_counts`.
Update `main.py` to format and print this dictionary after `process_files()` runs.

**Step 3: Run tests to verify they pass**

Run: `pytest tests/`
Expected: PASS

**Step 4: Commit**

```bash
git add .
git commit -m "feat: detailed file type console summary"
```
