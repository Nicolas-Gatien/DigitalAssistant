import pywhatkit
from skills.basic_skill import BasicSkill

class PlayYoutubeVideoSkill(BasicSkill):
    def __init__(self):
        self.name = "PlayYoutubeVideo"
        self.metadata = {
            "name": self.name,
            "description": "Plays a Video on Youtube Based on Its Title",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_title": {
                        "type": "string",
                        "description": "The Name of the Youtube Video"
                    }
                },
                "required": ["video_title"]
            }
        }
        super().__init__(self.name, self.metadata)

    def perform(self, video_title):
        try:
            pywhatkit.playonyt(video_title)
            return f"{video_title} Is Now Playing On Youtube, Let the User Know"
        except:
            return f"Could not play {video_title}"