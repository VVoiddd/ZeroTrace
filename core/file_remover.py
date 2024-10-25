# file_remover.py

import os
import shutil
import logging

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'file_remover_logs.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def check_permissions(path):
    """Checks if the path is writable."""
    writable = os.access(path, os.W_OK)
    logging.info(f"Checked permissions for {path}: {'Writable' if writable else 'Not Writable'}")
    return writable

def remove_program(program_path):
    """Removes the specified program or directory."""
    try:
        if not check_permissions(program_path):
            logging.error(f"Permission Denied for {program_path}")
            return

        if os.path.isdir(program_path):
            shutil.rmtree(program_path)
            logging.info(f"Successfully removed directory: {program_path}")
        elif os.path.isfile(program_path):
            os.remove(program_path)
            logging.info(f"Successfully removed file: {program_path}")
        else:
            logging.warning(f"Path is neither a file nor a directory: {program_path}")

    except Exception as e:
        logging.error(f"Error while removing program: {program_path}. Reason: {e}")

