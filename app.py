#Automation – 'File Organiser'

import os
import shutil
import sys
import platform
from pathlib import Path
from collections import defaultdict

# GUI imports
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("Warning: tkinter not available. Using command line interface.")

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


def detect_system():
    """Detect the operating system and return system info."""
    system = platform.system()
    version = platform.version()
    print(f"Detected system: {system} {version}")
    return system


def select_folder_gui():
    """Open a GUI dialog to select the folder to organize."""
    if not GUI_AVAILABLE:
        return select_folder_cli()
    
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Set window to appear on top
    root.attributes('-topmost', True)
    
    folder_path = filedialog.askdirectory(
        title="Select folder to organize files",
        initialdir=Path.home()
    )
    
    root.destroy()
    
    if folder_path:
        return Path(folder_path)
    else:
        print("No folder selected.")
        return None


def select_folder_cli():
    """Command line interface for folder selection."""
    print("\n=== File Organizer ===")
    print("Available options:")
    print("1. Use current directory")
    print("2. Enter custom path")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            return Path.cwd()
        elif choice == "2":
            path_input = input("Enter the folder path: ").strip()
            if path_input:
                path = Path(path_input)
                if path.exists() and path.is_dir():
                    return path
                else:
                    print("Invalid path or directory doesn't exist.")
            else:
                print("No path entered.")
        elif choice == "3":
            print("Exiting...")
            return None
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


def get_file_category(file_path):
    """Determine the category of a file based on its extension."""
    extension = file_path.suffix.lower()
    return extension_to_category.get(extension, "Other")


def organize_files(target_folder):
    """Organize files into category folders."""
    if not target_folder or not target_folder.exists():
        print("Invalid target folder.")
        return
    
    # Performance optimization: Get files list only when needed
    files = [f for f in target_folder.iterdir() if f.is_file()]
    
    if not files:
        print("No files found to organize.")
        return
    
    print(f"Found {len(files)} files to organize...")
    
    # Performance optimization: Group files by category first
    files_by_category = defaultdict(list)
    for file_path in files:
        category = get_file_category(file_path)
        files_by_category[category].append(file_path)
    
    # Performance optimization: Process files by category for better I/O patterns
    total_moved = 0
    total_skipped = 0
    folders_created = []
    
    for category, file_list in files_by_category.items():
        if not file_list:  # Skip categories with no files
            continue
            
        print(f"\nProcessing {len(file_list)} files for category: {category}")
        
        # Only create folder if there are files to put in it
        destination_folder = target_folder / category
        if not destination_folder.exists():
            destination_folder.mkdir(exist_ok=True)
            folders_created.append(category)
            print(f"Created folder: {destination_folder}")
        
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
    print(f"Folders created: {len(folders_created)}")
    if folders_created:
        print(f"Created folders: {', '.join(folders_created)}")
    print(f"Files moved: {total_moved}")
    print(f"Files skipped: {total_skipped}")
    
    # Show completion message in GUI if available
    if GUI_AVAILABLE and total_moved > 0:
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(
            "File Organization Complete",
            f"Successfully organized {total_moved} files!\nFolders created: {len(folders_created)}\nFiles moved: {total_moved}\nFiles skipped: {total_skipped}"
        )
        root.destroy()


def main():
    """Main function to run the file organizer."""
    print("Starting File Organizer...")
    
    # Detect system
    system = detect_system()
    
    # Select folder to organize
    target_folder = select_folder_gui()
    
    if target_folder:
        print(f"Selected folder: {target_folder}")
        organize_files(target_folder)
    else:
        print("No folder selected. Exiting...")


if __name__ == "__main__":
    main()
