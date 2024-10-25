# leftovers_cleaner.py

import os
import datetime
import shutil
import logging

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

application_log = os.path.join(log_dir, 'applicationdata.txt')

logging.basicConfig(
    filename=application_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_leftovers(program_name, scan_level="medium"):
    """Finds leftover files and directories associated with the specified program.
       Supports light, medium, and aggressive scan levels.
    """
    leftovers = []
    common_dirs = [
        os.path.expanduser("~\\AppData\\Local"),
        os.path.expanduser("~\\AppData\\Roaming"),
        os.path.expanduser("~\\AppData\\LocalLow"),
        os.path.expanduser("~\\Temp"),
    ]
    
    # Aggressive scan will include more directories
    if scan_level == "aggressive":
        common_dirs += [
            "C:\\ProgramData",
            os.path.expanduser("~\\Documents"),
        ]

    for directory in common_dirs:
        if not os.path.exists(directory):
            logging.warning(f"Directory does not exist: {directory}")
            continue

        for root, dirs, files in os.walk(directory):
            if program_name.lower() in root.lower():
                leftovers.append(root)
            for file in files:
                if program_name.lower() in file.lower():
                    leftovers.append(os.path.join(root, file))
    
    logging.info(f"Found leftovers for {program_name} in scan level {scan_level}: {leftovers}")
    return leftovers

def clean_leftovers(leftovers):
    """Cleans up leftover files and directories."""
    for leftover in leftovers:
        try:
            if os.path.isdir(leftover):
                shutil.rmtree(leftover)
                logging.info(f"Removed leftover directory: {leftover}")
            elif os.path.isfile(leftover):
                os.remove(leftover)
                logging.info(f"Removed leftover file: {leftover}")
        except Exception as e:
            logging.error(f"Error removing {leftover}: {str(e)}")

def clean_up(program_name, scan_level="medium"):
    """Initiates cleanup for a specific program's leftovers."""
    logging.info(f"Cleaning up leftovers for: {program_name} using {scan_level} scan")
    leftovers = find_leftovers(program_name, scan_level)
    clean_leftovers(leftovers)
    logging.info(f"Cleanup complete for {program_name} at {scan_level} scan")
