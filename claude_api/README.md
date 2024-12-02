# Claude API Wrapper for Dev Assist

A FastAPI service that wraps AWS Bedrock's Claude 3 Sonnet model, providing a simple REST API interface for the Dev Assist CLI tool.

Part of the [Dev Assist](https://github.com/hillaryhitch/dev_assist) project by Hillary Murefu.

## Prerequisites

1. AWS Account with Bedrock access
2. AWS credentials configured with appropriate permissions
3. Python 3.8+

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure AWS credentials:
Either set up your AWS credentials file (`~/.aws/credentials`) or set environment variables:
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_region  # e.g., us-east-1
```

3. Run the server:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

### POST /v1/chat/completions

Create a chat completion using Claude 3 Sonnet.

Request body:
```json
{
    "messages": [
        {
            "role": "user",
            "content": "Hello, how are you?"
        }
    ],
    "max_tokens": 2048,
    "temperature": 0.7,
    "system_prompt": "Optional system prompt"
}
```

Response:
```json
{
    "response": "Claude's response text",
    "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579
    }
}
```

### GET /health

Health check endpoint.

Response:
```json
{
    "status": "healthy"
}
```

## Docker Deployment

Build and run using Docker:

```bash
docker build -t claude-api .
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  -e AWS_DEFAULT_REGION=your_region \
  claude-api
```

## Security Considerations

1. Add authentication (e.g., API keys)
2. Implement rate limiting
3. Use HTTPS in production
4. Restrict CORS settings
5. Monitor usage and costs

## Environment Variables

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_DEFAULT_REGION`: AWS region (default: us-east-1)

## Author

Hillary Murefu (hillarywang2005@gmail.com)

## Repository

This is part of the [Dev Assist](https://github.com/hillaryhitch/dev_assist) project.
