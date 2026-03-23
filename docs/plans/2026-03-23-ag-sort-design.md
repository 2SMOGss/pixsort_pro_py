# ag-sort Upgrade Design Document

## Architecture & Goals
Upgrade the existing `ag_sort` Python tool to securely sort images/videos into `MM-YYYY` folders while strictly ensuring zero data loss through cryptographic hashing and file verification.

## Core Features

1. **Metadata Extraction (`main.py`)**: 
   - Parse EXIF `DateTimeOriginal` for images.
   - Fallback to OS `st_ctime` (creation date) for videos or files lacking EXIF.
   - Group files into a `MM-YYYY` directory plan (e.g., `03-2024`).

2. **The 100% Integrity Handshake (`engine.py`)**:
   - Calculate source SHA-256 hash.
   - Copy file to destination preserving metadata (e.g., `shutil.copy2`).
   - Calculate destination SHA-256 hash.
   - ONLY delete the original source file if the sequence is completed and both hashes perfectly match.

3. **Deduplication & Collision Handling (`engine.py`)**:
   - Compare new file hashes against existing files in the specific `MM-YYYY` folder.
   - **True Duplicates:** If a file has the exact same SHA-256 hash as an existing file in that month's folder, move it to a `MM-YYYY/duplicates/` subfolder.
   - **Name Collisions:** If two different files (different hashes) have the same name, append a sequence number (e.g., `IMG_0001_1.jpg`) to avoid overwrites.

4. **Logging & Printed Summary (`engine.py` / `interface.py`)**:
   - Maintain the JSON audit log for the `UNDO` feature.
   - Write a human-readable `.log` file detailing all moves, duplicates, and collisions.
   - **Console Summary:** Upon completion, print a clear text summary to the console detailing every file that was moved (showing the `source -> destination` paths) and pointing to the log file.
