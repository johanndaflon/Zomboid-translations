# Project Zomboid Translation Tools

This repository contains two Python scripts designed to help convert and maintain translation files for Project Zomboid mods.

## Scripts Overview

### 1. Zomboid_txt_to_json.py
Converts `.txt` translation files (Lua-style format) into structured `.json` files.

### 2. Zomboid_sync_translation_files.py
Synchronizes translation JSON files across multiple languages using English (`EN`) as the reference.

---

## Installation

### Requirements
- Python 3.8+
- No external dependencies

---

## Script 1: TXT → JSON Conversion

### Purpose
Converts `.txt` files into `.json` format.

### Features
- Detects encoding automatically
- Removes prefixes like `ItemName_` and `Recipe_`
- Cleans filenames
- Processes folders recursively

### Usage
```bash
python Zomboid_txt_to_json.py <folder_path>
```

---

## Script 2: JSON Synchronization

### Purpose
Ensures all translation files match the English (`EN`) structure.

### Usage
```bash
python Zomboid_sync_translation_files.py <root_folder>
```

---

## Recommended Workflow

1. Convert TXT to JSON
2. Organize language folders
3. Run synchronization

---

## Notes
- This script overwrites files
- Keep backups before running
