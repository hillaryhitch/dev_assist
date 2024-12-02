# Dev Assist

A command-line AI assistant for software development that brings Claude 3 Sonnet's capabilities directly to your terminal.

## Installation

```bash
# Install from source
git clone https://github.com/hillaryhitch/dev_assist.git
cd dev-assist
pip install -e .

# Or install directly using pip (once published)
pip install dev-assist
```

## Claude API Setup

Dev Assist requires a running instance of the Claude API wrapper. You have two options:

### Option 1: Local Setup

1. Clone the Claude API wrapper repository
2. Install dependencies:
```bash
cd claude_api
pip install -r requirements.txt
```

3. Configure AWS credentials for Bedrock:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region  # e.g., us-east-1
```

4. Run the API server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 2: Docker Setup

1. Build and run the Docker container:
```bash
cd claude_api
docker build -t claude-api .
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_DEFAULT_REGION=your_region \
  claude-api
```

## Usage

After installation and setting up the Claude API, you can use Dev Assist directly from your terminal:

```bash
# First-time setup (will prompt for Claude API URL)
dev_assist configure

# Ask Dev Assist for help
dev_assist ask "Create a Python function to sort a list of dictionaries by a specific key"

# Show verbose output
dev_assist ask -v "How do I implement a binary search tree in Python?"

# Check version
dev_assist version
```

## Features

- Direct command-line interface for quick access to Claude 3 Sonnet's capabilities
- Rich terminal output with syntax highlighting and formatting
- Built-in tools for:
  - File operations (read/write)
  - Code search and analysis
  - System command execution
  - File listing and searching
  - Code definition analysis

## Configuration

On first use, Dev Assist will prompt you for your Claude API URL. This will be stored in `~/.dev_assist/.env`. You can reconfigure at any time using:

```bash
dev_assist configure
```

## Examples

1. Get help with code:
```bash
dev_assist ask "How do I read a JSON file in Python?"
```

2. Search for patterns in code:
```bash
dev_assist ask "Find all TODO comments in my project"
```

3. Get explanations:
```bash
dev_assist ask "Explain how this function works" < mycode.py
```

4. Create new files:
```bash
dev_assist ask "Create a Python script that downloads images from a URL"
```

## Environment Variables

- `CLAUDE_API_URL`: URL of your Claude API endpoint (default: http://localhost:8000)
- `DEV_ASSIST_DEBUG`: Set to "1" for debug output
- `DEV_ASSIST_CONFIG_DIR`: Override default config directory (default: ~/.dev_assist)

## Development

To contribute to Dev Assist:

1. Fork the repository from https://github.com/hillaryhitch/dev_assist
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Make your changes and submit a pull request

## Troubleshooting

1. If you see permission errors:
```bash
# Install for current user only
pip install --user dev-assist
```

2. If the command isn't found:
```bash
# Make sure your Python scripts directory is in PATH
# Usually one of:
# - Windows: %APPDATA%\Python\Scripts
# - Unix: ~/.local/bin
```

3. If you can't connect to Claude API:
- Verify the API server is running
- Check the URL configuration (dev_assist configure)
- Ensure AWS credentials are properly set up

## License

MIT License - feel free to use in your own projects.

## Credits

Created by Hillary Murefu (hillarywang2005@gmail.com)

## Repository

https://github.com/hillaryhitch/dev_assist
# dev_assist
