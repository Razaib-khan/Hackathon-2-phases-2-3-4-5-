#!/usr/bin/env python3
"""
Script to push the backend code to Hugging Face Space
"""
import os
import shutil
import subprocess
from pathlib import Path

def copy_backend_to_temp():
    """Copy backend files to a temporary directory for Hugging Face Space deployment"""
    backend_dir = Path("../backend")
    hf_space_dir = Path("hf_space_backend")

    # Remove existing temp directory
    if hf_space_dir.exists():
        shutil.rmtree(hf_space_dir)

    # Create new directory
    hf_space_dir.mkdir(exist_ok=True)

    # Create the Hugging Face Space directory with proper structure
    # Copy essential files directly to the root of the space directory
    files_to_copy = [
        "Dockerfile",  # This is already configured for direct approach
        "requirements.txt",
        "README.md",
        ".env.example",
        "src/",
        "database/",
        "models/",
        "api/",
        "middleware/",
        "config/",
        "services/",
        "utils/",
        "Makefile",
        "pyproject.toml",
        "pytest.ini"
    ]

    for item in files_to_copy:
        source = backend_dir / item
        dest = hf_space_dir / item

        if (backend_dir / item).is_file():
            shutil.copy2(source, dest)
        elif (backend_dir / item).is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(source, dest, dirs_exist_ok=True)

    # Don't copy app.py since we're using direct approach - remove if it exists
    app_py_path = hf_space_dir / "app.py"
    if app_py_path.exists():
        app_py_path.unlink()

    print(f"Copied backend files to {hf_space_dir}")

def push_to_hf_space():
    """Push the backend code to Hugging Face Space"""
    hf_space_dir = Path("hf_space_backend")

    if not hf_space_dir.exists():
        print(f"Directory {hf_space_dir} does not exist. Run copy_backend_to_temp first.")
        return

    # Change to the temp directory
    original_cwd = os.getcwd()
    os.chdir(hf_space_dir)

    try:
        # Initialize git repo if not already initialized
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "remote", "remove", "origin"], stderr=subprocess.DEVNULL)
        subprocess.run(["git", "remote", "add", "origin", "https://huggingface.co/spaces/Razaib123/todo-backend"], check=True)

        # Add all files
        subprocess.run(["git", "add", "."], check=True)

        # Commit changes
        subprocess.run(["git", "commit", "-m", "Initial commit for AIDO TODO Backend"], check=True)

        # Push to Hugging Face Space
        result = subprocess.run(["git", "push", "-u", "origin", "main", "--force"],
                              capture_output=True, text=True)

        if result.returncode == 0:
            print("Successfully pushed to Hugging Face Space!")
            print("Your backend should be available at: https://razaib123-hf-space-todo-backend.hf.space")
        else:
            print(f"Error pushing to Hugging Face Space: {result.stderr}")

    except subprocess.CalledProcessError as e:
        print(f"Error during git operations: {e}")
    finally:
        os.chdir(original_cwd)

if __name__ == "__main__":
    print("Preparing backend for Hugging Face Space deployment...")
    copy_backend_to_temp()
    print("\nPushing to Hugging Face Space...")
    push_to_hf_space()