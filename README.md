[中文](README.CN.md)

# FastGithub Introduction

FastGithub is a graphical Github accelerator tool developed based on PyQt5. It solves the problem of slow or inaccessible access to Github by automatically updating the local hosts file. The tool features a concise and intuitive interface, simple operation, and supports multiple platforms including Windows, macOS, and Linux. All operation results are prompted via pop-up windows, and detailed operation logs are provided .

### ✨ Core Features

- 🚀 Update Github-related hosts entries with one click, automatically obtaining the latest IP addresses
- 🔄 Restore the local hosts file to its default state with one click (remove Github-related entries)
- 📝 Real-time log recording with timestamps displaying all operation processes
- 🎨 Simple graphical interface mimicking mainstream accelerators, with real-time status display
- 🚨 Pop-up prompts for operation results (success/failure), with clear error messages
- ⚡ Background thread processing to avoid interface lag
- 💻 Cross-platform support (Windows/macOS/Linux)

### 📋 Requirements

- Python 3.6 or higher
- Windows/macOS/Linux operating system
- Administrator/root privileges (required for modifying the hosts file)

### 🚀 Installation Steps

### 1. Clone the Project

```
git clone https://github.com/YuxuanBai1/FastGithub.git
cd FastGithub
```

### 2. Install Dependencies

```
pip install requests PyQt5
```

### 📖 Usage Guide

### 1. Run the Program

#### Windows System

- **Must run as administrator**: Right-click on Command Prompt/Terminal, select "Run as administrator", then execute:

  ```
  python main.py
  ```

#### macOS/Linux Systems

- Run with root privileges:

  ```
  sudo python main.py
  ```

### 2. Operation Instructions

| Button          | Function Description                                         |
| --------------- | ------------------------------------------------------------ |
| Update Hosts    | Automatically obtains the latest Github hosts information and updates the local hosts file |
| Restore Default | Removes Github-related entries from the hosts file, restoring it to its original state |

### 3. Interface Description

- **Status Display**: Shows the current operation status in real-time (Not started/Updating/Update successful/Update failed/Restored to default)
- **Operation Log**: Records the time and detailed information of all operations for troubleshooting
- **Bottom Prompt**: Reminds the user to run the program with administrator/root privileges

### 📁 Project Directory Structure

```
FastGithub/
├── main.py          # Project entry file (core logic implementation)
├── app.ico          # Program icon (optional)
└── LICENSE # License
```

### 🔧 Common Issue Resolution

- Q: Program prompts "Insufficient permissions"? A: This tool needs to modify the system-level hosts file and must be run with **administrator (Windows)** or **root (macOS/Linux)** privileges.
- Q: No icon appears after starting the program? A: Ensure the `app.ico`file is placed in the project root directory, or simply delete the line `self.setWindowIcon(QIcon("app.ico"))`in the code.

### ⚠️ Important Notes

1. Ensure the network can access `https://raw.hellogithub.com/hosts.json`(this interface provides the latest Github hosts information)
2. Before modifying the hosts file, the tool automatically backs up the original content, only replacing/adding Github-related entries
3. If using a proxy tool, it is recommended to turn off the proxy before using this tool
4. This tool is for learning and personal use only; do not use it for commercial purposes

### 📄 License

This project adopts the MIT open source license, allowing free modification, distribution, and commercial use. For details, please refer to the LICENSE file.