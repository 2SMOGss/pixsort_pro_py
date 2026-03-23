# Custom Upgrades Design Document

## Architecture & Goals
Remove any renaming prompts, prevent nested dating folders, and add a detailed file-type summary upon completion.

## Core Features

1. **Remove Renaming Logic (`main.py`)**: 
   - Remove the `Rename? [n/p/s]` prompt completely.
   - Do not pass prefix or suffix variables to the engine. All files will retain their original physical filenames. 
   - *Note: Sequence numbers for name collisions (e.g., `_1`, `_2`) will remain strictly to prevent overwriting different files with the exact same name, as agreed regarding 100% integrity.*

2. **Smart Directory Nesting (`main.py` & `engine.py`)**:
   - If the user provides a Target path that already ends in the designated `MM-YYYY` folder string (e.g., Target: `G:\Pictures\11-2021` and the plan resolves to `11-2021`), the engine will place the files directly into that Target path without appending a redundant `11-2021` subfolder.

3. **Enhanced Summary Reporting (`engine.py` & `main.py`)**:
   - The engine will aggregate the successfully moved files by their file extensions (e.g., `.jpg`, `.mp4`).
   - The CLI will print a final status message summarizing the counts exactly as requested: "Moved 36 .jpg files and 3 .mp4 files from [Source] to [Target]".
