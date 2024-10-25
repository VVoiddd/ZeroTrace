import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from core import file_finder, leftovers_cleaner

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

application_log = os.path.join(log_dir, 'applicationdata.txt')

logging.basicConfig(
    filename=application_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Custom dialog to ask for scan level
def get_scan_level():
    """Custom pop-up to select scan level."""
    scan_level = None

    # Create a custom popup dialog for scan selection
    def select_scan_level(level):
        nonlocal scan_level
        scan_level = level
        dialog.destroy()  # Close the popup once a selection is made

    dialog = tk.Toplevel()
    dialog.title("Select Scan Level")
    dialog.geometry("300x150")
    dialog.config(bg="#2C2C2C")

    label = ttk.Label(dialog, text="Choose Scan Level", background="#2C2C2C", foreground="white", font=("Arial", 14))
    label.pack(pady=10)

    # Create buttons for the scan level
    ttk.Button(dialog, text="Light", command=lambda: select_scan_level("light")).pack(pady=5)
    ttk.Button(dialog, text="Medium", command=lambda: select_scan_level("medium")).pack(pady=5)
    ttk.Button(dialog, text="Aggressive", command=lambda: select_scan_level("aggressive")).pack(pady=5)

    dialog.grab_set()  # Makes the popup modal
    dialog.wait_window()  # Wait until the popup is closed

    return scan_level

def on_program_select(program_listbox, installed_programs):
    """Handles program selection for deletion."""
    try:
        selected_program = program_listbox.get(program_listbox.curselection())
        program_path = installed_programs[selected_program]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {selected_program}?")
        logging.info(f"User confirmed deletion of: {selected_program}")

        if confirm:
            # Ask if user wants a Windows backup
            backup_confirm = messagebox.askyesno("Backup", "Would you like to create a Windows Backup before proceeding? (Recommended)")
            if backup_confirm:
                logging.info(f"User chose to create a backup for {selected_program}")

            # Get scan level from the user
            scan_level = get_scan_level()
            if scan_level is None:
                messagebox.showwarning("Scan Level Not Chosen", "You must choose a scan level to continue.")
                logging.warning("Scan level selection was canceled by the user.")
                return

            leftovers_cleaner.clean_up(selected_program, scan_level)

            messagebox.showinfo("Success", f"{selected_program} has been removed with a {scan_level} scan!")
            logging.info(f"Cleanup complete for {selected_program} at {scan_level} scan level.")
        else:
            logging.info("User cancelled program deletion.")
    except Exception as e:
        logging.error(f"Error during program selection: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Modern UI with Dark Mode
def create_interface():
    """Creates the main GUI window."""
    app = tk.Tk()
    app.title("ZeroTrace Uninstaller")
    app.geometry("700x500")
    app.config(bg="#2C2C2C")

    # Style for modern look
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", background="#3C3C3C", foreground="white", font=("Arial", 14))
    style.configure("TLabel", background="#2C2C2C", foreground="white", font=("Arial", 16))

    title_label = ttk.Label(app, text="ZeroTrace - Uninstaller", style="TLabel")
    title_label.pack(pady=20)

    # Program Listbox
    scrollbar = tk.Scrollbar(app)
    program_listbox = tk.Listbox(app, height=15, width=50, yscrollcommand=scrollbar.set, bg="#3C3C3C", fg="white", font=("Arial", 12))
    scrollbar.config(command=program_listbox.yview)
    scrollbar.pack(side="right", fill="y")
    program_listbox.pack(pady=20)

    # Load installed programs
    installed_programs = file_finder.find_installed_programs()
    for program in installed_programs.keys():
        program_listbox.insert(tk.END, program)

    # Remove Program Button
    remove_button = ttk.Button(app, text="Remove Program", command=lambda: on_program_select(program_listbox, installed_programs))
    remove_button.pack(pady=10)

    app.mainloop()

if __name__ == "__main__":
    create_interface()
