"""
Configuration settings for the Desktop Application
"""
import os

# Base URL for the API
# To change this, set the API_BASE_URL environment variable or modify this string
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/api")
