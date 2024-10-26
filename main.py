import os
import sys
import ctypes
import logging
import datetime
from gui import interface

# Set up logging with timestamps and custom file extension
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f'main_logs_{timestamp}.vdwr')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_admin():
    """Check if the script is running with admin rights."""
    try:
        result = ctypes.windll.shell32.IsUserAnAdmin()
        logging.info(f"Admin check: {result}")
        return result
    except Exception as e:
        logging.error(f"Error checking admin status: {str(e)}")
        return False

def run_with_admin():
    """Run the current script with admin permissions."""
    try:
        if sys.argv[0]:
            logging.info("Attempting to run with admin permissions...")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            logging.info("Successfully initiated admin permissions request.")
    except Exception as e:
        logging.error(f"Error attempting to run as admin: {str(e)}")

def main():
    if not is_admin():
        run_with_admin()
        return

    logging.info("Launching ZeroTrace...")

    # Initialize the GUI (which will handle the program logic)
    try:
        interface.create_interface()  # Correct function to call
    except Exception as e:
        logging.error(f"Unhandled exception in GUI: {str(e)}")

if __name__ == "__main__":
    main()
