from openai import OpenAI
import json
import os
import sys

class Assistant():
    def __init__(self, keys_file, skill_objects):
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
        self.known_skills = self.reload_skills(skill_objects)

    def get_skill_metadata(self):
        skills_metadata = []
        for skill in self.known_skills.values():
            skills_metadata.append(skill.metadata)

        return skills_metadata

    def reload_skills(self, skill_objects):
        known_skills = {}
        for skill in skill_objects:
            known_skills[skill.name] = skill

        return known_skills

    def add_msg_to_transcript(self, role, content):
        msg_dict = {"role": role, "content": content}
        self.conversation_transcript.append(msg_dict)

    def get_openai_api_call(self):
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.conversation_transcript,
            functions=self.get_skill_metadata(),
            function_call="auto"
        )
        return response

    def get_response(self, prompt):

        self.add_msg_to_transcript("user", prompt)
        while True:
            response = self.get_openai_api_call()

            assistant_msg = response.choices[0].message
            msg_contents = assistant_msg.content

            if not assistant_msg.function_call:
                self.add_msg_to_transcript("assistant", msg_contents)
                return msg_contents

            skill_name = assistant_msg.function_call.name
            skill = self.known_skills.get(skill_name)

            if not skill:
                return f"{skill_name} Does not Exist"

            skill_parameters = json.loads(assistant_msg.function_call.arguments)

            result = skill.perform(**skill_parameters)

            self.conversation_transcript.append(
                {
                    "role": "function",
                    "name": skill_name,
                    "content": result
                }
            )

            print(f"Performed {skill_name} and got the following result: {result}")