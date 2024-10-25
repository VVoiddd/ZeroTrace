# leftovers_cleaner.py

import os
import datetime
import shutil
import logging

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f'leftovers_cleaner_logs_{timestamp}.txt')
app_data_log = os.path.join(log_dir, 'applicationdata.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# List of core Windows paths to skip
CORE_WINDOWS_PATHS = [
    os.environ['SYSTEMROOT'],
    os.environ['WINDIR'],
    os.path.expanduser("~\\AppData\\Local"),
    os.path.expanduser("~\\AppData\\Roaming"),
]

def is_core_windows_file(path):
    """Checks if the path is a core Windows file or directory."""
    return any(path.startswith(core_path) for core_path in CORE_WINDOWS_PATHS)

def find_leftovers(program_name):
    """Finds leftover files and directories associated with the specified program."""
    leftovers = []
    common_dirs = [
        os.path.expanduser("~\\AppData\\Local"),
        os.path.expanduser("~\\AppData\\Roaming"),
        os.path.expanduser("~\\AppData\\LocalLow"),
        os.path.expanduser("~\\Temp"),
    ]
    
    for directory in common_dirs:
        if not os.path.exists(directory):
            logging.warning(f"Directory does not exist: {directory}")
            continue

        for root, dirs, files in os.walk(directory):
            if program_name.lower() in root.lower() and not is_core_windows_file(root):
                leftovers.append(root)
            for file in files:
                if program_name.lower() in file.lower() and not is_core_windows_file(os.path.join(root, file)):
                    leftovers.append(os.path.join(root, file))
    
    logging.info(f"Found leftovers for {program_name}: {leftovers}")
    with open(app_data_log, 'a') as f:
        f.write(f"Found leftovers for {program_name}: {leftovers}\n")
    return leftovers

def clean_leftovers(leftovers):
    """Cleans up leftover files and directories."""
    for leftover in leftovers:
        try:
            if os.path.isdir(leftover):
                shutil.rmtree(leftover)
                logging.info(f"Removed leftover directory: {leftover}")
                with open(app_data_log, 'a') as f:
                    f.write(f"Removed leftover directory: {leftover}\n")
            elif os.path.isfile(leftover):
                os.remove(leftover)
                logging.info(f"Removed leftover file: {leftover}")
                with open(app_data_log, 'a') as f:
                    f.write(f"Removed leftover file: {leftover}\n")
        except Exception as e:
            logging.error(f"Error removing {leftover}: {str(e)}")
            with open(app_data_log, 'a') as f:
                f.write(f"Error removing {leftover}: {str(e)}\n")

def clean_up(program_name):
    """Initiates cleanup for a specific program's leftovers."""
    logging.info(f"Cleaning up leftovers for: {program_name}")
    leftovers = find_leftovers(program_name)
    clean_leftovers(leftovers)
    logging.info(f"Cleanup complete for {program_name}")
    with open(app_data_log, 'a') as f:
        f.write(f"Cleanup complete for {program_name}\n")
