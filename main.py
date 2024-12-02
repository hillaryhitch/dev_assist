from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Union
import os
from dotenv import load_dotenv
from enum import Enum
import openai

# Load environment variables
load_dotenv()

app = FastAPI(title="Python Cline", description="A Python implementation of Cline's capabilities")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

class ToolType(str, Enum):
    EXECUTE_COMMAND = "execute_command"
    READ_FILE = "read_file"
    WRITE_FILE = "write_to_file"
    SEARCH_FILES = "search_files"
    LIST_FILES = "list_files"
    LIST_CODE_DEFINITIONS = "list_code_definition_names"
    BROWSER_ACTION = "browser_action"

class Tool(BaseModel):
    tool_type: ToolType
    parameters: Dict[str, str]

class Task(BaseModel):
    description: str
    tools_needed: Optional[List[Tool]] = None
    context: Optional[Dict[str, str]] = None

class Response(BaseModel):
    message: str
    actions_taken: List[str]
    next_steps: Optional[List[str]] = None

class ToolManager:
    @staticmethod
    async def execute_command(command: str) -> str:
        """Execute system commands with proper security measures."""
        # This would need proper security measures and sandboxing
        raise NotImplementedError("Command execution requires security implementation")

    @staticmethod
    async def read_file(path: str) -> str:
        """Read file contents safely."""
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"File not found: {path}")
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    @staticmethod
    async def write_file(path: str, content: str) -> bool:
        """Write content to file safely."""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error writing file: {str(e)}")

    @staticmethod
    async def search_files(path: str, pattern: str) -> List[str]:
        """Search files with pattern matching."""
        import re
        import glob

        results = []
        try:
            for filepath in glob.glob(f"{path}/**/*", recursive=True):
                if os.path.isfile(filepath):
                    with open(filepath, 'r') as f:
                        content = f.read()
                        matches = re.finditer(pattern, content)
                        for match in matches:
                            results.append({
                                'file': filepath,
                                'match': match.group(),
                                'line': content.count('\n', 0, match.start()) + 1
                            })
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching files: {str(e)}")

    @staticmethod
    async def list_files(path: str, recursive: bool = False) -> List[str]:
        """List files in directory."""
        try:
            if recursive:
                files = []
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        files.append(os.path.join(root, filename))
                return files
            else:
                return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

class LLMHandler:
    def __init__(self):
        self.model = "gpt-4"
        self.tool_manager = ToolManager()

    async def process_task(self, task: Task) -> Response:
        """Process a task using the LLM and execute necessary tools."""
        try:
            messages = self._prepare_messages(task)
            
            # Get response from OpenAI
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages
            )

            # Process and execute the LLM's plan
            return await self._execute_plan(response.choices[0].message.content, task)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing task: {str(e)}")

    def _prepare_messages(self, task: Task) -> List[Dict[str, str]]:
        """Prepare the conversation messages for the LLM."""
        system_message = """You are Cline, a software engineering assistant. 
        You have access to various tools for file operations, code analysis, and system commands. 
        Analyze tasks carefully and provide step-by-step solutions."""

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": self._format_task(task)}
        ]

    def _format_task(self, task: Task) -> str:
        """Format the task for LLM consumption."""
        return f"""
        Task Description: {task.description}
        
        Context: {task.context or {}}
        
        Available Tools:
        {[tool.tool_type.value for tool in (task.tools_needed or [])]}
        
        Please analyze this task and provide a detailed plan of execution.
        """

    async def _execute_plan(self, llm_response: str, task: Task) -> Response:
        """Execute the plan provided by the LLM."""
        # Parse the LLM's response and execute tools as needed
        # This would need proper implementation to safely execute the plan
        actions_taken = []
        next_steps = []
        
        return Response(
            message="Task processed successfully",
            actions_taken=actions_taken,
            next_steps=next_steps
        )

# API Endpoints
@app.post("/process-task", response_model=Response)
async def process_task(task: Task):
    """Process a task using Cline's capabilities."""
    llm_handler = LLMHandler()
    return await llm_handler.process_task(task)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
