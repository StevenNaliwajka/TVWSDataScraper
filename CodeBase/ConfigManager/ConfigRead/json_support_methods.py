import json
import sys
import time

def validate_json_file(file_path):
    try:
        # Open and read the file contents
        with open(file_path, 'r') as file:
            # Parse the JSON from the file
            data = json.load(file)
        # If successful, return the parsed JSON object
        return data
    except json.JSONDecodeError as e:
        # JSON is invalid; print the error and return None
        time.sleep(.0005)
        sys.exit(f"Invalid JSON format: {e}")
    except FileNotFoundError:
        # Handle case if the file is not found
        time.sleep(.0005)
        sys.exit(f"File not found: {file_path}")
