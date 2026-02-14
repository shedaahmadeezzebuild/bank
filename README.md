# HBDB Banking Bot 🏦

A Streamlit-based banking assistant powered by Mistral AI. This bot answers questions about HBDB banking services using a comprehensive FAQ database.

## Features

- ✅ Real-time streaming responses
- ✅ FAQ-based knowledge system  
- ✅ Professional banking support
- ✅ Easy to deploy on Streamlit Cloud
- ✅ Works locally with Python

## Local Development

### Prerequisites
- Python 3.8+
- Virtual Environment (venv)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/shedaahmadeezzebuild/bank.git
cd bank
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the app**
```bash
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

## Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository
Ensure these files are in your GitHub repository:
- `streamlit_app.py` - Main Streamlit app
- `banking_bot.py` - Bot logic
- `requirements.txt` - Python dependencies
- `hbdb_banking_faqs (2) (1).csv` - FAQ database
- `.streamlit/config.toml` - Streamlit configuration

### Step 2: Add Secrets on Streamlit Cloud (Web Dashboard)
1. Go to [Streamlit Cloud](https://share.streamlit.io/)
2. Login with your GitHub account
3. Click "New app"
4. Select your GitHub repository, branch, and `streamlit_app.py` as entry point
5. Click "Deploy"
6. Once deployed, click the **Settings** icon (gear) → **Secrets**
7. Add your API key:
```toml
MISTRAL_API_KEY = "your_actual_mistral_api_key_here"
```
8. The app will automatically rerun with the secret

### Important Notes
- ⚠️ **Never commit secrets.toml to GitHub**
- ✅ For local development: Create `.streamlit/secrets.toml` (in `.gitignore`)
- ✅ For cloud: Use the Streamlit Cloud web dashboard to add secrets
- The app will automatically use secrets from the dashboard when deployed

### Step 3: Verify Deployment
Once deployed:
1. The app will load automatically
2. You should see "🏦 HBDB Banking Bot" 
3. Try asking: "How do I open a savings account?"
4. Get instant responses powered by Mistral AI

## Local Setup with Secrets

For local development with secrets:

1. Create `.streamlit/secrets.toml`:
```toml
MISTRAL_API_KEY = "your_mistral_api_key_here"
```

2. Run locally:
```bash
streamlit run streamlit_app.py
```

The secrets file is in `.gitignore` and won't be committed.


## Usage

### Local Usage
1. Start the app: `streamlit run streamlit_app.py`
2. Ask questions in the chat interface
3. Get instant answers powered by Mistral AI

### Cloud Usage
1. Visit your Streamlit Cloud URL
2. Ask questions in the chat
3. Responses are streamed in real-time

## Example Questions

- "How do I open a savings account?"
- "What is HBDB Premier?"
- "How do I reset my password?"
- "How do I contact customer service?"
- "What are the mortgage rates?"

## Configuration

### Streamlit Config (`/.streamlit/config.toml`)
Customize colors and theme:
```toml
[theme]
primaryColor = "#1976d2"
backgroundColor = "#f5f5f5"
```

### Environment Variables
- `MISTRAL_API_KEY` - Your Mistral AI API key (required)

## File Structure

```
bank/
├── streamlit_app.py              # Main Streamlit application
├── banking_bot.py                # Bot logic and Mistral integration
├── requirements.txt              # Python dependencies
├── hbdb_banking_faqs (2) (1).csv # FAQ database
├── .streamlit/
│   ├── config.toml              # Streamlit configuration
│   └── secrets.toml             # Local secrets (not committed)
└── README.md                     # This file
```

## API Keys

Get your Mistral AI API key from [console.mistral.ai](https://console.mistral.ai)

## Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### API Key not working
- Verify your Mistral AI API key is correct
- On Streamlit Cloud, check that the secret is added properly
- Restart the app after adding secrets

### CSV file not found
Ensure `hbdb_banking_faqs (2) (1).csv` is in the root directory

## Support

For issues or questions, contact HBDB customer service or check the FAQ database.

## License

This project is provided as-is for HBDB banking services.
