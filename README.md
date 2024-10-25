# ZeroTrace

ZeroTrace is an uninstaller that assists in removing unwanted programs from Windows PCs. It also offers an option to scan and clean up leftover files and directories from uninstalled programs, making it ideal for users who want a clean and organized system.

## Features

- Lists all installed programs on the system.
- Allows users to select and uninstall programs.
- Offers a scan for leftover files and directories after uninstallation.
- Detailed logging of all processes.
  
## Requirements

- Python 3.x
- Windows OS (for Winreg module and directory scanning)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/VVoiddd/ZeroTrace
```

2. Navigate to the project directory:

```bash
cd ZeroTrace
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Program

Simply run the `main.py` script:

```bash
python main.py
```

## Scanning and Cleaning Leftovers

After uninstalling a program, ZeroTrace will prompt if you'd like to scan the entire system for leftover files and directories related to the uninstalled program. If you opt to scan, it will search through common directories and offer to delete any found leftovers.

## Logs

All logs related to uninstallation and scanning will be saved in the `Logs` directory with a timestamped `.vdwr` extension for easier tracking.

## License

This project is licensed under the MIT License.
```