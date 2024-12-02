import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import json
from typing import List, Optional, Dict, Any
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Claude API Wrapper")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AWS Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Change to your region
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    max_tokens: Optional[int] = 2048
    temperature: Optional[float] = 0.7
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    usage: Dict[str, Any]

def format_messages_for_claude(messages: List[Message], system_prompt: Optional[str] = None) -> str:
    formatted_messages = ""
    
    if system_prompt:
        formatted_messages += f"System: {system_prompt}\n\n"
    
    for message in messages:
        role_prefix = "Human" if message.role == "user" else "Assistant"
        formatted_messages += f"{role_prefix}: {message.content}\n\n"
    
    return formatted_messages.strip()

@app.post("/v1/chat/completions", response_model=ChatResponse)
async def create_chat_completion(request: ChatRequest):
    try:
        formatted_prompt = format_messages_for_claude(
            request.messages,
            request.system_prompt
        )

        body = {
            "prompt": formatted_prompt,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "anthropic_version": "bedrock-2023-05-31"
        }

        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',  # Use the appropriate model ID
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        # Extract the response text
        completion = response_body['completion']
        
        # Calculate token usage (approximate)
        input_tokens = len(formatted_prompt.split())
        output_tokens = len(completion.split())
        
        return ChatResponse(
            response=completion,
            usage={
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
