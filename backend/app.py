"""
Hugging Face Space entrypoint for the AIDO TODO Application backend
"""
import os
import sys

# Add the current directory to the Python path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Import the app directly from the src directory
from src.main import app

# Make the app available
__all__ = ['app']