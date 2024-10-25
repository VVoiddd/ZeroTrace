# file_finder.py

import os
import winreg
import datetime
import logging

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f'file_finder_logs_{timestamp}.txt')
app_data_log = os.path.join(log_dir, 'applicationdata.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def find_installed_programs():
    """Returns a dictionary of installed programs with their paths."""
    installed_programs = {}
    try:
        uninstall_key = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, uninstall_key) as key:
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                try:
                    sub_key = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, sub_key) as program_key:
                        program_name = winreg.QueryValueEx(program_key, "DisplayName")[0]
                        program_path = winreg.QueryValueEx(program_key, "InstallLocation")[0] if winreg.QueryValueEx(program_key, "InstallLocation")[0] else "N/A"
                        installed_programs[program_name] = program_path
                except EnvironmentError:
                    continue
    except Exception as e:
        logging.error(f"Error retrieving installed programs: {str(e)}")
    
    with open(app_data_log, 'a') as f:
        f.write(f"Installed programs found: {installed_programs}\n")

    logging.info(f"Installed programs found: {installed_programs}")
    return installed_programs
