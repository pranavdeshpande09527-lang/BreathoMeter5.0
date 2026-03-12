import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.gemini_api_key)

class AIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_explanation(self, topic: str, user_data: dict) -> str:
        """
        Generates explanation using Gemini based on topic and user context.
        Topics can be: 'lung_health_score', 'aqi_impact', 'breathing_improvement'
        """
        prompt = f"As a respiratory health AI assistant for Breathometer 4.0, explain this topic to the user:\nTopic: {topic}\nUser Context Data: {user_data}\nKeep the explanation concise, medically safe, and easy to understand for a layperson. Provide actionable advice."
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Unable to generate explanation at this time. Error: {str(e)}"

ai_service = AIService()
