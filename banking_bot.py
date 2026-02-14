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
        self.api_key = api_key
        self.csv_path = csv_path
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.faq_data = self._load_faqs(csv_path)
        self.system_prompt = self._create_system_prompt()
    
    def _load_faqs(self, csv_path: str) -> pd.DataFrame:
        """Load FAQ data from CSV file."""
        # Handle both relative and absolute paths
        if not os.path.exists(csv_path):
            # Try relative path
            csv_path = csv_path.replace("(2) (1)", "(2) (1)").replace(" ", " ")
        
        df = pd.read_csv(csv_path)
        return df
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with FAQ context."""
        faq_text = "You are a helpful HBDB Banking Assistant. Here is the banking FAQ knowledge base:\n\n"
        
        for idx, row in self.faq_data.iterrows():
            question = str(row.get('Question', '')).strip()
            answer = str(row.get('Answer', '')).strip()
            if question and answer:
                faq_text += f"Q: {question}\nA: {answer}\n\n"
        
        faq_text += """
Instructions:
1. Answer banking questions based on the provided FAQ knowledge base
2. If the question is not covered in the FAQs, provide general banking guidance
3. Always be professional and helpful
4. For specific account details or urgent issues, direct users to contact customer service
5. Keep responses concise and clear
"""
        return faq_text
    
    def get_response(self, user_message: str):
        """
        Get a streaming response from the bot.
        
        Args:
            user_message: User's question or message
            
        Yields:
            Text chunks of the response
        """
        try:
            messages = [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
            
            # Use streaming for real-time response
            response = self.client.chat.stream(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            # Stream the response
            for chunk in response:
                try:
                    if hasattr(chunk, 'data') and chunk.data and hasattr(chunk.data, 'choices'):
                        if chunk.data.choices and len(chunk.data.choices) > 0:
                            choice = chunk.data.choices[0]
                            if hasattr(choice, 'delta') and choice.delta:
                                if hasattr(choice.delta, 'content') and choice.delta.content:
                                    yield choice.delta.content
                except (AttributeError, IndexError):
                    continue
                    
        except Exception as e:
            # Fallback to non-streaming if streaming fails
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                if response and hasattr(response, 'choices') and response.choices:
                    yield response.choices[0].message.content
            except Exception as fallback_error:
                error_msg = f"I apologize, but I encountered an error processing your request. Please try again in a moment."
                yield error_msg


