import pandas as pd
import os
from mistralai import Mistral

class BankingBot:
    def __init__(self, api_key: str, csv_path: str):
        """Initialize the Banking Bot with Mistral AI API and FAQ data."""
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.csv_path = csv_path
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.faq_data = self._load_faqs(csv_path)
        self.system_prompt = self._create_system_prompt()
    
    def _load_faqs(self, csv_path: str) -> pd.DataFrame:
        """Load FAQ data from CSV file."""
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        
        df = pd.read_csv(csv_path)
        return df
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with FAQ context."""
        faq_text = "You are a helpful HBDB Banking Assistant. Here is the banking FAQ knowledge base:\n\n"
        
        # Use all FAQs but make it concise
        for idx, row in self.faq_data.iterrows():
            question = str(row.get('Question', '')).strip()
            answer = str(row.get('Answer', '')).strip()
            if question and answer:
                # Shorten answers for system prompt
                answer = answer[:100] if len(answer) > 100 else answer
                faq_text += f"Q: {question}\nA: {answer}\n"
        
        faq_text += "\nBe concise, professional, and helpful. Answer based on the FAQ knowledge base."
        return faq_text
    
    def get_response(self, user_message: str):
        """Get a response from the bot with proper error handling."""
        
        messages = [
            {
                "role": "user",
                "content": f"{self.system_prompt}\n\nUser question: {user_message}"
            }
        ]
        
        try:
            # Call the API
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=512,
                temperature=0.5
            )
            
            # Extract content
            if response and hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content
                if content:
                    # Yield words to simulate streaming
                    for word in content.split():
                        yield word + " "
                    return
            
            # Fallback if no content
            yield "I apologize, I could not generate a response."
                
        except Exception as e:
            # Detailed error message for debugging
            import traceback
            error_details = f"Error: {str(e)}"
            yield error_details
