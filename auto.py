import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from pathlib import Path

from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

# Defining my directories path
source_dir = str(Path.home() / "Downloads")
sorted_files_dir = str(Path.home() / "Documents/Sorted Files")

# Hashmap file extensions and their directories
dest_dirs = {
    'Apps': ('.exe', '.dmg'),
    'Docs': ('.doc', '.docx'),
    'Images': ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.jfif'),
    'PDF': ('.pdf',),
    'PPT': ('.ppt', '.pptx'),
    'RAR': ('.zip', '.rar', '.7z', '.tar'),
    'Sheets': ('.xls', '.xlsx', '.ods', '.csv'),
    'Txt': ('.txt',)
}

# Create destination directories if they don't exist
for dir_name in dest_dirs.keys():
    os.makedirs(os.path.join(sorted_files_dir, dir_name), exist_ok=True)

def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

def move_file(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_unique(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)

class MyEventHandler(LoggingEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                if entry.is_file():
                    file_extension = os.path.splitext(entry.name)[1].lower()
                    dest_dir = None

                    if file_extension in dest_dirs['Apps']:
                        dest_dir = os.path.join(sorted_files_dir, 'Apps')
                    elif file_extension in dest_dirs['Docs']:
                        dest_dir = os.path.join(sorted_files_dir, 'Docs')
                    elif file_extension in dest_dirs['Images']:
                        dest_dir = os.path.join(sorted_files_dir, 'Images')
                    elif file_extension in dest_dirs['PDF']:
                        dest_dir = os.path.join(sorted_files_dir, 'PDF')
                    elif file_extension in dest_dirs['PPT']:
                        dest_dir = os.path.join(sorted_files_dir, 'PPT')
                    elif file_extension in dest_dirs['RAR']:
                        dest_dir = os.path.join(sorted_files_dir, 'RAR')
                    elif file_extension in dest_dirs['Sheets']:
                        dest_dir = os.path.join(sorted_files_dir, 'Sheets')
                    elif file_extension in dest_dirs['Txt']:
                        dest_dir = os.path.join(sorted_files_dir, 'Txt')

                    if dest_dir:
                        move_file(dest_dir, os.path.join(source_dir, entry.name), entry.name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()