import pandas as pd
from mistralai import Mistral

class BankingBot:
    def __init__(self, api_key: str, csv_path: str):
        """
        Initialize the Banking Bot with Mistral AI API and FAQ data.
        
        Args:
            api_key: Mistral AI API key
            csv_path: Path to the FAQ CSV file
        """
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.faq_data = self._load_faqs(csv_path)
        self.system_prompt = self._create_system_prompt()
    
    def _load_faqs(self, csv_path: str) -> pd.DataFrame:
        """Load FAQ data from CSV file."""
        df = pd.read_csv(csv_path)
        return df
    
    def _create_system_prompt(self) -> str:
        """Create system prompt with FAQ context."""
        faq_text = "You are a helpful HBDB Banking Assistant. Here is the banking FAQ knowledge base:\n\n"
        
        for idx, row in self.faq_data.iterrows():
            faq_text += f"Q: {row['Question']}\nA: {row['Answer']}\n\n"
        
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
        
        try:
            # Use streaming for real-time response
            response = self.client.chat.stream(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            # Stream the response
            for chunk in response:
                if chunk.data.choices and len(chunk.data.choices) > 0:
                    if hasattr(chunk.data.choices[0], 'delta') and chunk.data.choices[0].delta.content:
                        yield chunk.data.choices[0].delta.content
        except Exception as e:
            # Fallback to non-streaming if streaming fails
            try:
                response = self.client.chat.complete(
                    model=self.model,
                    messages=messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                yield response.choices[0].message.content
            except Exception as fallback_error:
                yield f"Error: {str(fallback_error)}"

