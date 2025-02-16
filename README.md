# LinkedIn Newsletter Generator

A powerful Flask application that integrates AI-driven news extraction and content generation with seamless LinkedIn posting. This tool utilizes Google's Gemini model, NewsAPI, and intelligent agents to craft engaging newsletters ready for LinkedIn publication.

---

## 🌟 Features

### 🔍 Advanced News Extraction
- **Dual News Fetching**:
  - Live news articles with custom queries
  - Top headlines by category
- **Customization Options**:
  - Adjustable date ranges
  - Multi-language support
  - Category-based filtering
  - Source attribution
  - Popularity-based sorting

### 🤖 AI-Powered Content Generation
- **Leveraging Google's Gemini 1.5 Flash model**:
  - Intelligent content summarization
  - Automated formatting & structure
  - Source preservation with citations

### 🔗 LinkedIn Integration
- **Effortless Posting**:
  - Direct LinkedIn publishing
  - OAuth authentication for security [Follow these steps to setup](https://www.cozmoslabs.com/docs/profile-builder/add-ons/social-connect/create-linkedin-app-social-connect/)
  - Character limit handling
  - Rich text formatting for readability

---

## 🏗️ Architecture

### 🚀 Tools

#### 1️⃣ Live News Extraction
```python
    def extract_live_news(
        q="Artificial Intelligence OR Data Science",
        from_param="2024-02-09",
        to="2024-02-16",
        language="en",
        sort_by="popularity",
        page_size=1
    )
```

#### 2️⃣ Top Stories Extraction
```python
    def extract_top_stories(
        category="technology",
        language="en",
        country="us",
        page_size=1
    )
```

### 📦 API Response Format

A typical news article contains:
```json
{
    "source": { "id": "source-id", "name": "Source Name" },
    "author": "Author Name",
    "title": "Article Title",
    "description": "Article Description",
    "url": "Article URL",
    "urlToImage": "Image URL",
    "publishedAt": "2024-02-16T12:00:00Z",
    "content": "Article Content"
}
```

### 🛠️ AI Agents

#### 📰 News Extractor Agent
```python
    news_extractor = Agent(
        name="News Extractor",
        role="Fetches top stories from news APIs",
        tools=[extract_live_news],
        model=Gemini(id="gemini-1.5-flash", api_key=api_key),
        system_message="""
        Always include the source URL when extracting news stories.
        Use the 'extract_live_news' tool for fetching the latest stories.
        """
    )
```

#### ✍️ Newsletter Generator Team
```python
    agents_team = Agent(
        name="Newsletter Team",  
        model=Gemini(id="gemini-1.5-flash", api_key=api_key),
        team=[get_news_extractor()],
        instructions=[
            "Use the News Extractor agent to fetch relevant articles.",
            "Summarize content in an engaging format.",
            "Retain the article title as a clickable source link."
        ]
    )
```

---

## 🛠️ Prerequisites

- Python 3.7+
- LinkedIn Developer Account
- LinkedIn API Credentials
- Google API Key for Gemini model
- NewsAPI Key
- Required Python Packages:
  ```bash
  pip install -r requirements.txt
  ```

---

## ⚙️ Environment Setup

Create a `.env` file with:
```env
# LinkedIn Credentials
CLIENT_ID=your_linkedin_client_id
CLIENT_SECRET=your_linkedin_client_secret
OAUTH2_REDIRECT_URL=your_oauth_redirect_url
lifecycleState=PUBLISHED

# API Keys
GOOGLE_API_KEY=your_google_api_key
newsapi_key=your_newsapi_key
```

### 🚀 Starting the Application
```bash
python run.py
```
The app will be available at `http://localhost:3000`

---

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main application page |
| `/linkedin_access` | GET | LinkedIn authentication flow |
| `/oauth` | GET | OAuth callback & token handling |
| `/newsletter` | POST | Generate AI-powered newsletter |
| `/linkedin_post` | POST | Publish newsletter to LinkedIn |

---

## 🤝 Contributing

1. **Fork** the repository
2. **Create** a feature branch
3. **Write tests** for new functionality
4. **Ensure API keys** are securely managed
5. **Submit** a pull request 🚀

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

Created by [Shubham Shah](https://www.linkedin.com/in/shubhamshah207)

- **GitHub**: [@shubhamshah207](https://github.com/shubhamshah207)
- **LinkedIn**: [Shubham Shah](https://www.linkedin.com/in/shubhamshah207)

