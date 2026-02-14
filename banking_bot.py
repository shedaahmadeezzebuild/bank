import pandas as pd
import os
from mistralai import Mistral

class BankingBot:
    def __init__(self, api_key: str, csv_path: str):
        """
        Initialize the Banking Bot with Mistral AI API and FAQ data.
        
        Args:
            api_key: Mistral AI API key
            csv_path: Path to the FAQ CSV file
        """
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
        # Shorter system prompt to reduce token usage
        faq_text = "You are a helpful HBDB Banking Assistant. Answer banking questions based on this FAQ knowledge base:\n\n"
        
        # Limit to first 30 FAQs to reduce token size
        for idx, row in self.faq_data.head(30).iterrows():
            question = str(row.get('Question', '')).strip()
            answer = str(row.get('Answer', '')).strip()
            if question and answer:
                faq_text += f"{question}: {answer}\n"
        
        faq_text += "\nBe concise, professional, and helpful."
        return faq_text
    
    def get_response(self, user_message: str):
        """
        Get a response from the bot.
        
        Args:
            user_message: User's question or message
            
        Yields:
            Text chunks of the response
        """
        messages = [
            {
                "role": "user",
                "content": f"{self.system_prompt}\n\nQuestion: {user_message}"
            }
        ]
        
        try:
            # Use the simple complete method
            response = self.client.chat.complete(
                model=self.model,
                messages=messages,
                max_tokens=512,
                temperature=0.5
            )
            
            # Extract and yield the response
            if response and hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content
                # Yield in chunks for streaming effect
                words = content.split()
                for word in words:
                    yield word + " "
            else:
                yield "I apologize, I could not generate a response."
                
        except Exception as e:
            error_msg = f"I apologize, but I'm unable to process your request at the moment. Please try again later."
            yield error_msg
