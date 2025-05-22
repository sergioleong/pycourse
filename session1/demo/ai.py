import requests
import json

try:
    data = {
        "prompt": "What is the capital of Spain?",
        "model": "llama3"
    }
    #Start Ollama on host listening to any IP with:
    # $env:OLLAMA_HOST='0.0.0.0:11434'
    # ollama serve
    host = '192.168.0.25'
    response = requests.post('http://' + host+ ':11434/api/generate', json=data, stream=True)
    response.raise_for_status()  # Raise an exception for bad status codes

    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            try:
                json_data = json.loads(decoded_line)
                if 'response' in json_data:
                    print(json_data['response'], end='', flush=True)
                if json_data.get('done'):
                    print()
                    break
            except json.JSONDecodeError:
                print(f"Error decoding JSON: {decoded_line}")

except requests.exceptions.RequestException as e:
    print(f"Error querying Ollama: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")