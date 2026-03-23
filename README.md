# ag_sort
**High-Integrity Chronological File Sorter & Deduplicator**

A specialized, security-first CLI engine designed for organizing large photo and video archives into a standardized, tamper-proof structure.

## 🚀 Top Features
- **100% Data Integrity Handshake**: Uses SHA-256 cryptographic verification before unlinking source files. If the copy fails, the source remains safe.
- **Precision Metadata Sorting**: Organizes files into `MM-YYYY` directory structures using EXIF `DateTimeOriginal` or OS creation fallback.
- **Smart Cloud Optimization**: Lazy hashing specifically tuned for Google Drive and network mounts—only downloads candidate files if the byte-size matches.
- **Immutable Audit Trail**: Generates read-only, tamper-proof session logs and transfer summaries for legal/personal records.
- **Intelligent Deduplication**: Automatically detects true duplicates and isolates them in dedicated subfolders; resolves filename collisions with a sequencer.
- **Premium Interface**: Features a High-Performance Matrix-style boot animation with a signature magenta pulse.

## 🛠️ Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the engine:
   ```bash
   python main.py
   ```
3. Use **Search** to find photo locations by name across all audit logs or **Undo** to instantly reverse a session.

## ⚖️ Security
Includes a built-in Master Password vault and recovery keys to protect your audit logs and search history.
