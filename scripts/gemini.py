from google import genai
import os
import sys
import json
from google.genai import types
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Annotated
from enum import Enum
from dotenv import load_dotenv

# Add parent directory to Python path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.prompt_updated import system_prompt

load_dotenv()

class AuthorTone(str, Enum):
    """Enumeration of possible author tones"""
    CRITICAL = "critical"
    ANALYTICAL = "analytical"
    PERSUASIVE = "persuasive"
    SARCASTIC = "sarcastic"
    OBJECTIVE = "objective"
    REFLECTIVE = "reflective"
    OPTIMISTIC = "optimistic"
    PESSIMISTIC = "pessimistic"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"

class VocabularyWord(BaseModel):
    """Model for vocabulary builder words"""
    word: str = Field(description="The difficult or advanced word from the text")
    meaning: str = Field(description="Simple English meaning of the word")
    example_usage: str = Field(description="Short sentence demonstrating usage")

class CriticalThinkingQuestion(BaseModel):
    """Model for critical thinking questions"""
    question: str = Field(description="Question to test understanding or inference")
    question_type: str = Field(description="Type: 'main_idea', 'assumptions', or 'inference'")

class EditorialAnalysis(BaseModel):
    """Comprehensive model for editorial analysis"""
    model_config = ConfigDict(
        title="Editorial Analysis Schema",
        description="Comprehensive analysis of newspaper editorials for CAT VARC preparation"
    )
    
    central_idea: str = Field(
        description="2-3 lines summarizing the main argument or message",
        min_length=30,
        max_length=500
    )
    tone_of_author: AuthorTone = Field(
        description="The predominant tone of the author"
    )
    paragraph_wise_summary: Annotated[List[str], Field(
        description="1-2 sentences per paragraph explaining content and connection to main idea",
        min_length=1
    )]
    vocabulary_builder: Annotated[List[VocabularyWord], Field(
        description="5-7 difficult or advanced words with meanings and examples",
        min_length=4,
        max_length=8
    )]
    critical_thinking_questions: Annotated[List[CriticalThinkingQuestion], Field(
        description="2-3 questions testing understanding, assumptions, and inference",
        min_length=2,
        max_length=4
    )]
    takeaway: str = Field(
        description="Short advice on what to notice while reading such articles",
        min_length=15,
        max_length=200
    )


class Gemini:
    def __init__(self, api_key=os.getenv("GEMINI_API_KEY")):
        try:
            self.client = genai.Client(
                api_key=api_key,
                vertexai=False
            )
        except Exception as e:
            print(f"Error initializing Gemini client: {e}")
            raise
    
    def gemini_response(self, user_prompt: str, model="gemini-2.5-flash"):
        """
        Generate structured editorial analysis using the latest Gemini API features
        
        Args:
            user_prompt: The editorial text to analyze
            model: The Gemini model to use
            
        Returns:
            dict: Parsed JSON response conforming to EditorialAnalysis schema
        """
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt(),
                    response_mime_type="application/json",
                    response_schema=EditorialAnalysis,
                    temperature=0.3,  # Lower temperature for more consistent output
                    max_output_tokens=3000,  # Increased for comprehensive analysis
                ),
            )
            
            # Parse the response to ensure it's valid JSON
            parsed_response = json.loads(response.text)
            
            # Try to validate with the Pydantic model, but return raw data if validation fails
            try:
                validated_analysis = EditorialAnalysis.model_validate(parsed_response)
                return validated_analysis.model_dump()
            except Exception as validation_error:
                print(f"Validation warning: {validation_error}")
                print("Returning raw response data...")
                return parsed_response
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            print(f"Raw response: {response.text}")
            return None
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def get_available_models(self):
        """List available models for reference"""
        try:
            models = []
            for model in self.client.models.list():
                # Handle different model object structures
                if hasattr(model, 'name'):
                    models.append(model.name)
                elif hasattr(model, 'model'):
                    models.append(model.model)
                else:
                    models.append(str(model))
            return models
        except Exception as e:
            print(f"Error listing models: {e}")
            return []

if __name__ == "__main__":
    # Example usage
    client = Gemini()
    
    # Test with a sample editorial
    sample_editorial = """
    The recent surge in renewable energy adoption marks a significant shift in global energy policy. 
    Governments worldwide are recognizing the urgent need to transition away from fossil fuels to 
    combat climate change. This transition, however, presents both opportunities and challenges.
    
    The economic implications are profound. While renewable energy promises long-term cost savings 
    and energy independence, the initial investment required is substantial. Countries must balance 
    immediate financial constraints with long-term environmental goals.
    
    Furthermore, the technological infrastructure needed to support renewable energy requires 
    careful planning and implementation. Grid modernization, energy storage solutions, and skilled 
    workforce development are critical components of this transition.
    
    The path forward demands both political will and public support. Only through coordinated 
    efforts can nations successfully navigate this energy transformation and secure a sustainable 
    future for coming generations.
    """
    
    print("Testing Gemini API with sample editorial...")
    result = client.gemini_response(sample_editorial)
    
    if result:
        print("\n" + "="*50)
        print("STRUCTURED EDITORIAL ANALYSIS")
        print("="*50)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Failed to generate analysis")
    
    print(f"\nAvailable models: {client.get_available_models()[:5]}")  # Show first 5 models