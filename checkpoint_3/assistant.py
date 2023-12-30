from openai import OpenAI
import json

class Assistant():
    def __init__(self, keys_file):
        self.conversation_transcript = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

        api_keys = ""
        with open(keys_file) as file:
            api_keys = json.load(file)

        self.client = OpenAI(api_key=api_keys["openai"])


    def add_msg_to_transcript(self, role, content):
        msg_dict = {"role": role, "content": content}
        self.conversation_transcript.append(msg_dict)

    def get_openai_api_call(self):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.conversation_transcript
        )
        return response

    def get_response(self, prompt):
        self.add_msg_to_transcript("user", prompt)
        response = self.get_openai_api_call()

        assistant_msg = response.choices[0].message
        msg_contents = assistant_msg.content

        self.add_msg_to_transcript("assistant", msg_contents)

        return  msg_contents