from google import genai
import os
import sys
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv

# Add parent directory to Python path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.prompt import system_prompt

load_dotenv()

class res_model(BaseModel):
    Central_Idea : str
    Tone_of_author : str
    Paragraph_wise_summary : list[str]
    Vocabulary_builder : list[str]
    critical_thinking : str
    takeaway: str


class Gemini:
    def __init__(self,api_key=os.getenv("GEMINI_API_KEY")):
        try:
            self.client = genai.Client(
                api_key=api_key,
                vertexai=False
            )
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            raise
    
    def gemini_response(self,user_prompt:str,model="gemini-2.5-flash"):
        try:
            response = self.client.models.generate_content(
                model=model,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt(),
                    response_mime_type="application/json",
                    response_schema=res_model
                ),
                contents=[user_prompt]
            )
            return response.text
        except Exception as e:
            print(e)

if __name__ == "__main__":
    client = Gemini()
    res = client.gemini_response()

    print(res)