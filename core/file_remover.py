# file_remover.py

import os
import shutil
import logging

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

app_data_log = os.path.join(log_dir, 'applicationdata.txt')

logging.basicConfig(
    filename=os.path.join(log_dir, 'file_remover_logs.txt'),
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

def check_permissions(path):
    """Checks if the path is writable."""
    writable = os.access(path, os.W_OK)
    logging.info(f"Checked permissions for {path}: {'Writable' if writable else 'Not Writable'}")
    return writable

def is_core_windows_file(path):
    """Checks if the path is a core Windows file or directory."""
    return any(path.startswith(core_path) for core_path in CORE_WINDOWS_PATHS)

def remove_program(program_path):
    """Removes the specified program or directory."""
    try:
        if not check_permissions(program_path):
            logging.error(f"Permission Denied for {program_path}")
            return

        if is_core_windows_file(program_path):
            logging.warning(f"Skipped core Windows file or directory: {program_path}")
            with open(app_data_log, 'a') as f:
                f.write(f"Skipped core Windows file or directory: {program_path}\n")
            return

        if os.path.isdir(program_path):
            shutil.rmtree(program_path)
            logging.info(f"Successfully removed directory: {program_path}")
            with open(app_data_log, 'a') as f:
                f.write(f"Successfully removed directory: {program_path}\n")
        elif os.path.isfile(program_path):
            os.remove(program_path)
            logging.info(f"Successfully removed file: {program_path}")
            with open(app_data_log, 'a') as f:
                f.write(f"Successfully removed file: {program_path}\n")
        else:
            logging.warning(f"Path is neither a file nor a directory: {program_path}")

    except Exception as e:
        logging.error(f"Error while removing program: {program_path}. Reason: {e}")
        with open(app_data_log, 'a') as f:
            f.write(f"Error while removing program: {program_path}. Reason: {e}\n")
