# chatbot.py
# This module handles interactions with the Ollama API.

import os
import requests

# Get the Ollama API URL and default model from environment variables
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
OLLAMA_DEFAULT_MODEL = os.getenv('OLLAMA_DEFAULT_MODEL', 'llama3')

def get_ollama_response(user_message):
    """
    Sends a user message to the Ollama API and returns the AI's response.
    This version is memory-less.

    Args:
        user_message (str): The message from the user.

    Returns:
        tuple: A tuple containing (AI response string, HTTP status code, error_message).
               If successful, error_message is None.
               If an error occurs, AI response string is None.
    """
    if not user_message:
        return None, 400, "No message provided."

    try:
        # Prepare the payload for the Ollama API
        payload = {
            "model": OLLAMA_DEFAULT_MODEL,
            "prompt": user_message,
            "stream": False # We want a single response, not a stream
        }
        headers = {'Content-Type': 'application/json'}

        # Make the request to the Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON response
        ollama_response = response.json()
        ai_response_content = ollama_response.get('response', None)
        if not ai_response_content:
            return None, 500, "No response content from Ollama API."
        return ai_response_content, 200, None

    except requests.exceptions.ConnectionError:
        return None, 503, "Could not connect to Ollama server. Is it running?"
    except requests.exceptions.Timeout:
        return None, 504, "Ollama server timed out."
    except requests.exceptions.RequestException as e:
        return None, 500, f"Error communicating with Ollama server: {e}"
    except Exception as e:
        return None, 500, f"An unexpected error occurred: {e}"