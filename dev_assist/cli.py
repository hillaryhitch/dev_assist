import os
import typer
import httpx
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from pathlib import Path
from typing import Optional, List, Dict
from dotenv import load_dotenv
import asyncio
from .tools import ToolManager

# Initialize typer app and rich console
app = typer.Typer(help="Dev Assist - Your command-line AI assistant for software development")
console = Console()
tool_manager = ToolManager()

# Load environment variables
load_dotenv()

CLAUDE_API_URL = os.getenv("CLAUDE_API_URL", "http://localhost:8000")

def setup_api_config():
    """Setup API configuration."""
    if not os.getenv("CLAUDE_API_URL"):
        console.print("[yellow]Claude API URL not found in environment variables.[/yellow]")
        api_url = Prompt.ask("Please enter your Claude API URL", default="http://localhost:8000")
        
        # Save to .env file
        env_path = Path.home() / ".dev_assist" / ".env"
        env_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(env_path, "w") as f:
            f.write(f"CLAUDE_API_URL={api_url}")
        
        os.environ["CLAUDE_API_URL"] = api_url

async def process_task(task: str) -> str:
    """Process a task using Claude API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CLAUDE_API_URL}/v1/chat/completions",
                json={
                    "messages": [
                        {
                            "role": "user",
                            "content": task
                        }
                    ],
                    "system_prompt": "You are Dev Assist, a software engineering assistant. "
                                   "You have access to various tools for file operations, "
                                   "code analysis, and system commands.",
                    "max_tokens": 2048,
                    "temperature": 0.7
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")
            
            data = response.json()
            return data["response"]
            
    except Exception as e:
        console.print(f"[red]Error processing task: {str(e)}[/red]")
        return None

@app.command()
def ask(
    task: str = typer.Argument(..., help="The task or question you want help with"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output")
):
    """Ask Dev Assist for help with a development task."""
    try:
        # Setup API config if needed
        setup_api_config()
        
        # Show thinking indicator
        with console.status("[bold green]Thinking...") as status:
            # Run the async task
            response = asyncio.run(process_task(task))
            
            if response:
                # Display the response in a nice panel
                console.print(Panel(
                    Markdown(response),
                    title="Dev Assist's Response",
                    border_style="green"
                ))
                
                # If verbose, show additional debug info
                if verbose:
                    console.print("\n[dim]Debug Information:[/dim]")
                    console.print(f"[dim]Current Directory: {os.getcwd()}[/dim]")
                    console.print(f"[dim]Available Tools: {tool_manager.list_tools()}[/dim]")
    
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

@app.command()
def configure():
    """Configure Dev Assist settings."""
    setup_api_config()
    console.print("[green]Configuration completed successfully![/green]")

@app.command()
def version():
    """Show the version of Dev Assist."""
    from . import __version__
    console.print(f"Dev Assist version: {__version__}")

def main():
    """Main entry point for the CLI."""
    app()

if __name__ == "__main__":
    main()
