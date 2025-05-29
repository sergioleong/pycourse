# chatbot.py
# This module handles interactions with the Ollama API.

import os
import requests

# Get the Ollama API URL and default model from environment variables
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/chat')

def get_ollama_response(messages, model_name):
    """
    Sends a list of messages to the Ollama API and returns the AI's response.
    This function now supports conversational memory by sending the full history.

    Args:
        messages (list): A list of message dictionaries, where each dictionary
                         has 'role' (e.g., 'user', 'assistant') and 'content' keys.
                         Example: [{'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi there!'}]

    Returns:
        tuple: A tuple containing (AI response string, HTTP status code, error_message).
               If successful, error_message is None.
               If an error occurs, AI response string is None.
    """
    if not messages:
        return None, 400, "No messages provided for AI interaction."


    try:
        # Prepare the payload for the Ollama API
        payload = {
            "model": model_name,
            "messages": messages,
            "stream": False # We want a single response, not a stream
        }
        headers = {'Content-Type': 'application/json'}

        # Make the request to the Ollama API
        response = requests.post(OLLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)

        # Parse the JSON response
        ollama_response = response.json()
        print(payload)
        print(ollama_response)
        ai_response_content = ollama_response.get('message', {}).get('content', None)
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