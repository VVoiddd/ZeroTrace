import os
import logging
import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from core import file_finder, leftovers_cleaner

# Set up logging
log_dir = "Logs"
os.makedirs(log_dir, exist_ok=True)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = os.path.join(log_dir, f'interface_logs_{timestamp}.vdwr')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def on_program_select():
    """Handles program selection for deletion."""
    try:
        selected_program = program_listbox.get(program_listbox.curselection())
        program_path = installed_programs[selected_program]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {selected_program}?")
        logging.info(f"User confirmed deletion of: {selected_program}")

        if confirm:
            # Remove the program
            leftovers_cleaner.clean_up(selected_program)
            messagebox.showinfo("Success", f"{selected_program} has been removed!")

            # Ask the user if they want to scan for leftovers
            scan_leftovers = messagebox.askyesno("Scan for Leftovers", "Do you want to scan the entire Windows PC for leftovers related to this program?")
            if scan_leftovers:
                # Find and clean leftovers
                leftovers = leftovers_cleaner.find_leftovers(selected_program)
                leftovers_cleaner.clean_leftovers(leftovers)
                messagebox.showinfo("Scan Complete", "Leftover files and directories have been cleaned!")
            else:
                messagebox.showinfo("No Scan", "No leftovers will be scanned.")

    except Exception as e:
        logging.error(f"Error during program selection: {str(e)}")
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def load_programs():
    """Loads installed programs into the listbox."""
    try:
        program_listbox.delete(0, tk.END)  # Clear the listbox
        logging.info("Loading installed programs...")

        global installed_programs
        installed_programs = file_finder.find_installed_programs()

        for program in installed_programs.keys():
            program_listbox.insert(tk.END, program)

        logging.info("Installed programs loaded successfully.")

    except Exception as e:
        logging.error(f"Error loading programs: {str(e)}")
        messagebox.showerror("Error", f"An error occurred while loading programs: {str(e)}")

# Create the main window
app = tk.Tk()
app.title("ZeroTrace Uninstaller")
app.geometry("600x400")
app.config(bg="#1E1E1E")

# Style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", background="#333333", foreground="white", font=("Arial", 12))
style.configure("TLabel", background="#1E1E1E", foreground="white", font=("Arial", 12))

# Title Label
title_label = ttk.Label(app, text="ZeroTrace - Uninstaller", style="TLabel")
title_label.pack(pady=10)

# Create a scrollbar
scrollbar = tk.Scrollbar(app)

# Listbox for programs
program_listbox = tk.Listbox(app, bg="#2E2E2E", fg="white", selectbackground="#444444", font=("Arial", 10), yscrollcommand=scrollbar.set)
scrollbar.config(command=program_listbox.yview)

# Pack the scrollbar and listbox
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
program_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Remove button
remove_button = ttk.Button(app, text="Remove Program", command=on_program_select)
remove_button.pack(pady=10)

# Load installed programs
load_programs()

# Start the GUI loop
try:
    app.mainloop()
except Exception as e:
    crash_log = os.path.join(log_dir, f"crash_log_{timestamp}.vdwr")
    logging.error(f"Unhandled exception in GUI: {str(e)}")
    send_log_to_webhook(crash_log, error_message=str(e))
    raise
