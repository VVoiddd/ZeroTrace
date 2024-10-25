import os
import winreg
import logging
import datetime

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f'file_finder_logs_{timestamp}.txt')

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
                    subkey_name = winreg.EnumKey(key, i)
                    with winreg.OpenKey(key, subkey_name) as subkey:
                        program_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0] if winreg.QueryValueEx(subkey, "InstallLocation") else ""
                        installed_programs[program_name] = install_location
                        logging.info(f"Found installed program: {program_name} at {install_location}")
                except OSError:
                    continue
    except Exception as e:
        logging.error(f"Error finding installed programs: {str(e)}")

    return installed_programs
