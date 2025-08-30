#Automation – 'File Organiser'

import os
import shutil
from pathlib import Path
from collections import defaultdict


categories = {
    "Images": [".png", ".jpg", ".jpeg", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".xml", ".json"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov"],
    "Music": [".mp3", ".wav"]
}

# Performance optimization: Create reverse lookup dictionary for O(1) extension lookup
extension_to_category = {}
for category, extensions in categories.items():
    for ext in extensions:
        extension_to_category[ext.lower()] = category

# Performance optimization: Pre-compute all category folders
all_categories = list(categories.keys()) + ["Other"]
target_folder = Path("D:\\GitHub\\Curor Santander\\File Organiser\\target")


def get_file_category(file_path):
    """Determine the category of a file based on its extension."""
    extension = file_path.suffix.lower()
    return extension_to_category.get(extension, "Other")


def organize_files():
    """Organize files into category folders."""
    # Performance optimization: Get files list only when needed
    files = [f for f in target_folder.iterdir() if f.is_file()]
    
    if not files:
        print("No files found to organize.")
        return
    
    print(f"Found {len(files)} files to organize...")
    
    # Performance optimization: Create all folders at once
    category_folders = {}
    for category in all_categories:
        category_folder = target_folder / category
        category_folder.mkdir(exist_ok=True)
        category_folders[category] = category_folder
        print(f"Created/verified folder: {category_folder}")
    
    # Performance optimization: Group files by category first
    files_by_category = defaultdict(list)
    for file_path in files:
        category = get_file_category(file_path)
        files_by_category[category].append(file_path)
    
    # Performance optimization: Process files by category for better I/O patterns
    total_moved = 0
    total_skipped = 0
    
    for category, file_list in files_by_category.items():
        print(f"\nProcessing {len(file_list)} files for category: {category}")
        destination_folder = category_folders[category]
        
        for file_path in file_list:
            destination_path = destination_folder / file_path.name
            
            # Check if file already exists in destination
            if destination_path.exists():
                print(f"File {file_path.name} already exists in {category} folder. Skipping...")
                total_skipped += 1
                continue
            
            try:
                shutil.move(str(file_path), str(destination_path))
                print(f"Moved {file_path.name} to {category} folder")
                total_moved += 1
            except Exception as e:
                print(f"Error moving {file_path.name}: {e}")
    
    print(f"\nOrganization completed!")
    print(f"Files moved: {total_moved}")
    print(f"Files skipped: {total_skipped}")


if __name__ == "__main__":
    print("Starting file organization...")
    organize_files()
