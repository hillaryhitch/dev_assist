# Dev Assist Project

A comprehensive software development assistant powered by Claude 3 Sonnet, consisting of two main components:

1. **Dev Assist CLI** - A command-line interface for interacting with the AI assistant
2. **Claude API Wrapper** - A FastAPI service that wraps AWS Bedrock's Claude 3 Sonnet model

## Project Structure

```
.
├── dev_assist/         # CLI tool package
│   ├── dev_assist/    # Source code
│   ├── setup.py       # Package configuration
│   └── README.md      # CLI documentation
│
└── claude_api/        # API wrapper service
    ├── main.py       # FastAPI application
    ├── Dockerfile    # Container configuration
    └── README.md     # API documentation
```

## Quick Start

1. First, set up the Claude API wrapper:
```bash
cd claude_api
pip install -r requirements.txt

# Configure AWS credentials
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region

# Start the API server
uvicorn main:app --host 0.0.0.0 --port 8000
```

2. Then, install and configure the CLI tool:
```bash
cd dev_assist
pip install -e .

# Configure the CLI
dev_assist configure
```

3. Start using Dev Assist:
```bash
dev_assist ask "How do I implement a binary search tree in Python?"
```

## Detailed Documentation

- [Dev Assist CLI Documentation](dev_assist/README2.md)
- [Claude API Wrapper Documentation](claude_api/README.md)

## Development

This project is open source and welcomes contributions. Please feel free to submit issues and pull requests.

## Author

Hillary Murefu (hillarywang2005@gmail.com)

## Repository

https://github.com/hillaryhitch/dev_assist

## License

MIT License - See individual component READMEs for details.
