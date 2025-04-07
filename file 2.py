import google.generativeai as genai
import random
from datetime import datetime

class MentalHealthCompanion:
    def _init_(self):
        self.session_start = datetime.now()
        self.disclaimer_shown = False
        # Configure Gemini API
        genai.configure(api_key='AIzaSyC64qZXYY5FqmP5f1-9r4RmYFvQkqdVTT4')
        
        # Safety settings for the model
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        # Initialize the model with safety settings
        self.model = genai.GenerativeModel('gemini-pro', safety_settings=safety_settings)
        
        # Add crisis resources
        self.crisis_resources = {
            "National Crisis Hotline": "988",
            "Crisis Text Line": "Text HOME to 741741",
            "Emergency": "911",
            "Suicide Prevention Lifeline": "1-800-273-8255"
        }
        self.greeting_messages = [
            "Hello! I'm here to help you with your mood today. How are you feeling?",
            "Welcome! I'm your supportive companion. Tell me about your emotions.",
            "Hi! This is a safe space. How's your mood right now?"
        ]
        
        self.mood_improvement_techniques = {
            "sad": [
                "Practice deep breathing exercises",
                "Listen to uplifting music",
                "Call a friend or family member",
                "Take a walk in nature",
                "Write down three things you're grateful for"
            ],
            # ... rest of the mood techniques remain the same ...
        }

    def get_ai_response(self, user_input):
        try:
            # Create prompt for Gemini
            prompt = f"""As a supportive and empathetic AI companion specialized in mood improvement:
            1. Acknowledge and validate the user's feelings
            2. Identify their emotional state
            3. Provide specific, actionable suggestions for mood improvement
            4. Encourage positive thinking while remaining realistic
            5. If serious concerns arise, gently suggest professional help
            
            User message: {user_input}"""

            # Get response from Gemini
            response = self.model.generate_content(prompt)
            ai_response = response.text
            
            # Add mood-specific suggestions
            for mood in self.mood_improvement_techniques.keys():
                if mood in user_input.lower():
                    techniques = random.sample(self.mood_improvement_techniques[mood], 2)
                    ai_response += f"\n\nHere are some techniques that might help you feel better:\n• {techniques[0]}\n• {techniques[1]}"
            
            return ai_response
            
        except Exception as e:
            print(f"Gemini API Error: {str(e)}")  # Print error for debugging
            return f"I notice you're feeling {user_input}. I want to help, but I'm having trouble connecting. Could you try sharing more about your feelings?"

    def show_disclaimer(self):
        disclaimer = """
        IMPORTANT: I am an AI companion designed to provide support and mood improvement suggestions.
        I am NOT a replacement for professional mental health services.
        If you're experiencing a Crisis or need professional help,
        please contact a licensed mental health professional or emergency services.
        """
        return disclaimer

if __name__ == "__main__":
    companion = MentalHealthCompanion()
    print(companion.show_disclaimer())
    print("\nHow are you feeling today?")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Take care! Remember, help is always available if you need it.")
            break
        response = companion.get_ai_response(user_input)
        print("\nAI: " + response)