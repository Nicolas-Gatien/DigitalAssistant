from skills.basic_skill import BasicSkill

class LearnNewSkillSkill(BasicSkill):
    def __init__(self):
        self.name = "LearnNewSkill"
        self.metadata = {
            "name": self.name,
            "description": "Creates a New Python File For a Specified Skill and Allows The GPT Model to Perform That Skill",
            "parameters": {
                "type": "object",
                "properties": {
                    "skill_name": {
                        "type": "string",
                        "description": "The Name of the New Skill"
                    },
                    "python_implementation": {
                        "type": "string",
                        "description": """The Python Code That is Behind The New Skill. The code should follow the following template:
[[[
from skills.basic_skill import BasicSkill
{import any other libraries}
class {name of the new skill}Skill (BasicSkill):
   def __init__(self):
      self.name = {skill name}
      self.metatada = {
         \"name\": self.name,
         \"description\": \"{a description of the skill that describes when it should be used and what it does}\",
         \"parameters\": {
            \"type\": \"object\",
            \"properties\": {
               \"{parameter 1 name}\": {
                  \"type\": \"{parameter type, i.e: string}\",
                  \"description\": \"{description of what the parameter is used for}\"              
               },
               \"{parameter 2 name}\": {
                  \"type\": \"{parameter type, i.e: string}\",
                  \"description\": \"{description of what the parameter is used for}\"
               },
            },
            \"required\": [\"{name of required parameter}\", \"{name of required parameter}\"]
         }
      }
      super().__init__(name=self.name, metadata=self.metadata)

   def perform(self, {parameters}):
      {skill functionality}
      return {string that describes the result of the function}
]]]
"""
                    }
                },
                "required": ["skill_name", "python_implementation"]
            }
        }
        super().__init__(name=self.name, metadata=self.metadata)

    def perform(self, skill_name, python_implementation):
        file_name = f"{skill_name}.py"
        try:
            with open(file_name, 'w') as file:
                file.write(python_implementation)
                return f"Successfully Created {file_name}"
        except:
            return f"Could not create {file_name}"