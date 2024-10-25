import os
import sys
import ctypes
import logging
import datetime
import requests
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

WEBHOOK_URL = "https://discord.com/api/webhooks/1299139384314036264/Gj3EatuHgxSFL22-wWaqznmvvZnlUD1U_rm2_FVPlWHCWIpVo0Wph929ZPVSZxQb_U13"

def send_log_to_webhook(log_file_path, error_message=None):
    """Send the log file or error message to a Discord webhook."""
    embed_content = {
        "content": "ZeroTrace Application Error",
        "embeds": [{
            "title": "Crash Report",
            "description": error_message if error_message else "Log file attached.",
            "fields": [
                {"name": "File:", "value": log_file_path},
                {"name": "Timestamp:", "value": str(datetime.datetime.now())}
            ]
        }]
    }

    try:
        with open(log_file_path, 'rb') as file:
            response = requests.post(WEBHOOK_URL, json=embed_content, files={'file': file})
            logging.info(f"Log file {log_file_path} sent to Discord webhook.")
            if response.status_code == 204:
                logging.info("Webhook upload successful.")
            else:
                logging.error(f"Webhook upload failed with status code: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending log to webhook: {str(e)}")

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
        interface.app.mainloop()
    except Exception as e:
        crash_log = os.path.join(log_dir, f"crash_log_{timestamp}.vdwr")
        logging.error(f"Unhandled exception in GUI: {str(e)}")
        send_log_to_webhook(crash_log, error_message=str(e))

if __name__ == "__main__":
    main()
