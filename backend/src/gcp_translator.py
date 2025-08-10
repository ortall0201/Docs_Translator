# GCP Vertex AI Translation Integration
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import json

class GCPTranslator:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID")
        self.location = os.getenv("GCP_LOCATION", "us-central1")  # Default to us-central1
        self.model_name = "gemini-1.5-pro"  # Using Gemini Pro model
        
        # Initialize Vertex AI
        if self.project_id:
            vertexai.init(project=self.project_id, location=self.location)
    
    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text using GCP Vertex AI Gemini model"""
        try:
            print("[DEBUG] DEBUG: Starting GCP Vertex AI translation...")
            
            # Language mapping
            language_map = {
                "pl": "Polish",
                "he": "Hebrew", 
                "en": "English",
                "uk": "Ukrainian",
                "ru": "Russian",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "it": "Italian"
            }
            
            target_lang_name = language_map.get(target_language, target_language)
            
            # Create the translation prompt
            prompt = f"""You are a professional document translator. Please translate the following text to {target_lang_name}.

IMPORTANT INSTRUCTIONS:
1. Maintain the original formatting and structure
2. For bureaucratic or technical terms, provide clear translations but preserve important official terminology
3. If you encounter forms or official documents, translate field labels and instructions accurately
4. Keep any numbers, dates, or proper names unchanged unless they need cultural adaptation
5. Return ONLY the translated text, no explanations or additional comments

TEXT TO TRANSLATE:
{text}

TRANSLATION:"""

            print(f"[DEBUG] DEBUG: Using GCP Project: {self.project_id}")
            print(f"[DEBUG] DEBUG: Using location: {self.location}")
            print(f"[DEBUG] DEBUG: Target language: {target_lang_name}")
            
            # Initialize the Gemini model
            model = GenerativeModel(self.model_name)
            
            print("[DEBUG] DEBUG: Sending request to Vertex AI...")
            
            # Generate the translation
            response = model.generate_content(prompt)
            
            if response and response.text:
                translated_text = response.text.strip()
                print(f"[DEBUG] DEBUG: GCP translation completed, length: {len(translated_text)}")
                return translated_text
            else:
                raise Exception("No response from Vertex AI model")
                
        except Exception as e:
            print(f"[ERROR] DEBUG: GCP translation failed: {str(e)}")
            # Fallback to simple indication
            return f"[GCP Translation to {target_lang_name}]\\n\\n{text}\\n\\n[Note: GCP Vertex AI translation failed - {str(e)}]"

# Create global translator instance
gcp_translator = GCPTranslator()