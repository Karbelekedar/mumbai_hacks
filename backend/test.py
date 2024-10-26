import requests
import json
import re

def extract_json_from_line(line):
    """
    Extracts the JSON string from a line prefixed with 'data: '.

    Args:
        line (str): A single line from the response.

    Returns:
        dict or None: The parsed JSON object if extraction and parsing are successful; otherwise, None.
    """
    prefix = "data: "
    if line.startswith(prefix):
        json_str = line[len(prefix):].strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON in line: {line}\nError: {e}")
    return None

def execute_task(command):
    """
    Sends a POST request to the specified URL with the given command and processes the streamed response.

    Args:
        command (str): The command to execute.

    Returns:
        dict or None: The parsed JSON response of type 'answer', or None if not found or an error occurs.
    """
    url = "http://127.0.0.1:8000/execute_task"
    payload = {
        "command": command
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request with stream=True to handle streamed responses
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Iterate over each line in the streamed response
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    print(f"Raw Line: {line}")  # For debugging purposes
                    json_obj = extract_json_from_line(line)
                    if json_obj:
                        # Process the JSON object based on its 'type'
                        msg_type = json_obj.get("type")
                        if msg_type == "answer":
                            return json_obj  # Return the first 'answer' type message
                        # You can process other types if needed
        print("No 'answer' type message found in the response.")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None

def main():
    command = "Find the price of rtx 3060ti"
    result = execute_task(command)

    if result is not None:
        print("\nParsed JSON Response (Type 'answer'):")
        print(json.dumps(result, indent=4, ensure_ascii=False))
    else:
        print("No valid JSON response of type 'answer' received.")

if __name__ == "__main__":
    main()
