# MCP Config Manager

*Read this in [Korean](README.ko.md)*

MCP Config Manager is a tool for managing MCP (Model Context Protocol) server settings for Claude Desktop.

## Features

- Automatic crawling of MCP server list from GitHub
- Management of installed MCP servers
- Configuration file backup and restore
- Cross-platform support (Windows, macOS, Linux)
- Direct specification of Claude Desktop configuration file path

## Installation

### Pre-built Packages

#### Windows

1. Download the `MCP_Config_Manager_Setup.exe` file.
2. Run the installer and follow the instructions.

#### macOS

1. Download the `MCP_Config_Manager.dmg` file.
2. Open the DMG file and drag the application to the Applications folder.
3. Note: If you see an "unidentified developer" warning, right-click the app and select "Open".

#### Linux

1. Download the `MCP_Config_Manager.AppImage` file.
2. Grant execution permissions: `chmod +x MCP_Config_Manager.AppImage`
3. Run the application: `./MCP_Config_Manager.AppImage`

### Running from Source Code

1. Clone the repository:
   ```bash
   git clone https://github.com/darkdarkcocoa/mcp-manager.git
   cd mcp-manager
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # Activate on Windows
   venv\Scripts\activate
   
   # Activate on macOS/Linux
   source venv/bin/activate
   ```

3. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

### Setting the Configuration File Path

If the Claude Desktop configuration file path cannot be found on first run, you can specify the Claude Desktop installation folder directly.
* Windows: `%APPDATA%/Claude`
* macOS: `~/Library/Application Support/Claude`
* Linux: `~/.config/Claude`

You can also change the configuration file path later via the "Change Path" button in the "My MCP" tab.

### Managing MCP Servers

1. Run the MCP Config Manager.
2. Select the desired MCP server from the "Available MCPs" tab.
3. Enter the required settings and click the "Apply" button.
4. Manage installed MCP servers in the "My MCP" tab.
5. When you save changes, Claude Desktop will restart.

## Developer Information

- Development language: Python
- Libraries used: PyQt6, Requests, BeautifulSoup4, Markdown

## Development Setup

### Dependencies

Packages required for project development:
```
PyQt6>=6.0.0
requests>=2.25.0
beautifulsoup4>=4.9.0
markdown>=3.3.0
```

### Development and Contributing

1. Submit issues and feature requests through GitHub Issues.
2. Submit code contributions through Pull Requests.
3. Follow the PEP 8 style guide when writing code.

## License

MIT License
