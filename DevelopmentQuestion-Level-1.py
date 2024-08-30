import openai
import os
import json

os.environ["OPENAI_API_KEY"] = "" #Add your api key here

def read_input_file(file_path):
    """Reads a file and returns a list of lines."""
    absolute_path = os.path.abspath(file_path)

    with open(absolute_path, 'r') as file:
        inputs = file.readlines()
    return [line.strip() for line in inputs]

def send_request(params):
    """Sends a request to the OpenAI API and returns the response."""
    try:
        print("Requesting completion from OpenAI API...")
        response = openai.ChatCompletion.create(**params)
        return response
    except Exception as e:
        print(f"Error during API call: {e}")
        return None
    
def set_system_message(sysmsg):
    """Sets the system message for the chat."""
    return [{
        "role": "system",
        "content": sysmsg
    }]

def set_user_message(user_msg_str, question, tiled=True):
    """Sets the user message for the chat."""
    if tiled:
        content = user_msg_str + question
        return [{"role": "user", "content": content}]
    else:
        return [{
            "role": "user",
            "content": user_msg_str
        }]

def main():
    prompt = '''As an expert in computer science, answer this question in one line'''

    questions = read_input_file('input.txt')

    result = []

    for i, question in enumerate(questions):
        entries = {'Prompt': None, 'Message': None}
        system_msg = ""
        system = set_system_message(system_msg)
        user = set_user_message(prompt, question)

        params = {
            "model": "gpt-4o-mini",
            "messages": system + user,
            "max_tokens": 256,
        }

        response = send_request(params)

        if response:
            entries['Prompt'] = question
            entries['Message'] = response['choices'][0]['message']['content']
            result.append(entries)

    with open("data.json", "w") as json_file:
        json.dump(result, json_file, indent=4)

if __name__ == "__main__":
    main()
