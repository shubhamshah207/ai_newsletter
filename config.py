import os

class Config:
    newsapi_key=os.getenv('newsapi_key')
    OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')
    GROQ_API_KEY=os.getenv('GROQ_API_KEY')
    OPENROUTER_API_KEY=os.getenv('OPENROUTER_API_KEY')
    GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY')
    CLIENT_ID=os.getenv('CLIENT_ID')
    CLIENT_SECRET=os.getenv('CLIENT_SECRET')
    OAUTH2_REDIRECT_URL=os.getenv('OAUTH2_REDIRECT_URL')
    lifecycleState=os.getenv('lifecycleState')
