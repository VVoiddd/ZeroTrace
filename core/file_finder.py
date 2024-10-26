# file_finder.py

import os
import winreg
import datetime
import logging

# Set up logging for file finder
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

file_finder_log = os.path.join(log_dir, f'file_finder_logs_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.txt')

logging.basicConfig(
    filename=file_finder_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_installed_programs():
    """Returns a dictionary of installed programs with their paths."""
    installed_programs = {}
    core_windows_dirs = [
        os.path.expandvars("%SystemRoot%"),
        os.path.expandvars("%ProgramFiles%"),
        os.path.expandvars("%ProgramFiles(x86)%"),
    ]
    
    try:
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, sub_key) as program_key:
                        program_name = winreg.QueryValueEx(program_key, "DisplayName")[0]
                        program_path = winreg.QueryValueEx(program_key, "InstallLocation")[0] if winreg.QueryValueEx(program_key, "InstallLocation")[0] else "N/A"
                        
                        # Skip core Windows directories
                        if any(core_dir in program_path for core_dir in core_windows_dirs):
                            continue
                        
                        installed_programs[program_name] = program_path
                        logging.info(f"Program found: {program_name}, path: {program_path}")
                except EnvironmentError:
                    continue
    except Exception as e:
        logging.error(f"Error retrieving installed programs: {str(e)}")
    
    logging.info(f"Installed programs found: {installed_programs}")
    return installed_programs
