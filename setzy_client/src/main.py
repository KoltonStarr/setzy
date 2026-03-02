import json
import mimetypes
from datetime import datetime
from pathlib import Path

import httpx
import typer

app = typer.Typer()

AGENT_URL = "http://localhost:8081"
UPLOADER_URL = "http://localhost:8080"
THREADS_FILE = Path.home() / ".setzy" / "threads.json"


def save_thread(thread_id: str, context: str):
    THREADS_FILE.parent.mkdir(parents=True, exist_ok=True)
    threads = json.loads(THREADS_FILE.read_text()) if THREADS_FILE.exists() else []
    threads.append({
        "thread_id": thread_id,
        "saved_at": datetime.now().isoformat(),
        "context": context[:120],
    })
    THREADS_FILE.write_text(json.dumps(threads, indent=2))


@app.command()
def upload(file: Path = typer.Argument(..., help="Path to the audio file to upload")):
    """Upload an audio file to the Setzy uploader service."""
    if not file.exists():
        typer.echo(f"Error: file '{file}' not found.", err=True)
        raise typer.Exit(1)

    content_type, _ = mimetypes.guess_type(file)
    if not content_type:
        content_type = "application/octet-stream"

    typer.echo(f"Uploading {file.name}...")
    with open(file, "rb") as f:
        response = httpx.post(
            f"{UPLOADER_URL}/upload",
            files={"file": (file.name, f, content_type)},
            timeout=60.0,
        )

    if response.status_code == 201:
        typer.echo("Upload successful.")
    else:
        typer.echo(f"Upload failed: {response.json().get('detail', 'unknown error')}", err=True)
        raise typer.Exit(1)


@app.command()
def chat(
    thread_id: str = typer.Option(None, "--thread-id", "-t", help="Resume an existing conversation by thread ID"),
):
    """Start an interactive chat session with the Setzy agent.

    Commands during chat:
      /new   - Save current thread and start a fresh conversation
      /quit  - Exit
    """
    current_thread_id = thread_id
    first_message: str | None = None

    if current_thread_id:
        typer.echo(f"Resuming conversation (thread: {current_thread_id})")
    else:
        typer.echo("New conversation started. Type /new to start fresh or /quit to exit.")

    while True:
        try:
            user_input = typer.prompt("\nYou")
        except (KeyboardInterrupt, EOFError):
            break

        cmd = user_input.strip().lower()

        if cmd == "/quit":
            break

        if cmd == "/new":
            if current_thread_id:
                save_thread(current_thread_id, first_message or "")
                typer.echo(f"Thread saved to {THREADS_FILE} (id: {current_thread_id})")
            current_thread_id = None
            first_message = None
            typer.echo("New conversation started.")
            continue

        try:
            response = httpx.post(
                f"{AGENT_URL}/chat",
                json={"message": user_input, "thread_id": current_thread_id},
                timeout=300.0,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            typer.echo(f"Error: {e}", err=True)
            continue

        current_thread_id = data["thread_id"]
        if first_message is None:
            first_message = user_input

        typer.echo(f"\nAgent: {data['message']}")


if __name__ == "__main__":
    app()
