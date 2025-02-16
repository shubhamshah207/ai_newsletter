from datetime import datetime, timedelta
from newsapi import (
    NewsApiClient,
)  # Ensure you have the newsapi-python package installed
import os
import json

newsapi_key = os.getenv("newsapi_key")


def extract_live_news(
    q: str = "Artificial Intelligence OR Data Science",
    from_param: str = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d"),
    to: str = datetime.utcnow().strftime("%Y-%m-%d"),
    language: str = "en",
    sort_by: str = "popularity",
    page_size: int = 1,
):
    """
    Extracts live news articles from the past week (or a specified date range) based on the provided query parameters.

    This function connects to the News API using the provided API key and retrieves news articles
    that match the search criteria. It is primarily designed to fetch articles on topics such as
    "Artificial Intelligence" and "Data Science" by default, but you can customize the parameters
    to search for any subject matter. The results are returned as a list of dictionaries, each
    containing details about a news article.

    Parameters:
        q (str, optional):
            The query string used for searching news articles. It supports logical operators
            (e.g., OR, AND) for more complex searches.
            Default is "Artificial Intelligence OR Data Science".
            Example: "Climate Change AND Renewable Energy"

        from_param (str, optional):
            The start date for the news search, formatted as "YYYY-MM-DD". By default, it is set to 7 days
            before the current UTC date.
            Example: "2025-01-26"

        to (str, optional):
            The end date for the news search, formatted as "YYYY-MM-DD". By default, it is set to the
            current UTC date.
            Example: "2025-02-02"

        language (str, optional):
            The language of the news articles to retrieve. Default is "en" for English.
            Example: "es" for Spanish

        sort_by (str, optional):
            The order in which the news articles are sorted. Valid values include:
              - "popularity": Articles sorted by popularity.
              - "relevancy": Articles sorted by relevance to the query.
              - "publishedAt": Articles sorted by publication date.
            Default is "popularity".
            Example: "publishedAt"

        page_size (int, optional):
            The number of articles to retrieve per request. This is useful if you need to fetch multiple articles.
            Default is 1. Adjust based on your API plan and requirements.
            Example: 10

    Returns:
        List[dict]:
            A list of dictionaries where each dictionary represents a news article. Each article typically contains:
              - source: Information about the source of the article.
              - author: The author of the article.
              - title: The title of the article.
              - description: A brief description or summary.
              - url: The URL to the full article.
              - urlToImage: The URL to the article's image.
              - publishedAt: The publication date and time.
              - content: The main content of the article.

    Usage Examples:
        Example 1: Default usage to extract AI and Data Science articles from the past week:
            >>> articles = extract_live_news()
            >>> for article in articles:
            ...     print(article['title'])

        Example 2: Extracting articles on Climate Change from the past 3 days, sorted by publication date:
            >>> custom_from = (datetime.utcnow() - timedelta(days=3)).strftime("%Y-%m-%d")
            >>> custom_to = datetime.utcnow().strftime("%Y-%m-%d")
            >>> articles = extract_live_news(
            ...     q="Climate Change",
            ...     from_param=custom_from,
            ...     to=custom_to,
            ...     sort_by="publishedAt",
            ...     page_size=5
            ... )
            >>> for article in articles:
            ...     print(article['title'])

    Note:
        - Ensure you have a valid News API key and have installed the 'newsapi-python' package.
        - Date parameters use UTC time by default.
        - Customize the parameters as needed to suit your news retrieval needs.
    """
    # Initialize the NewsApiClient with your API key.
    newsapi = NewsApiClient(api_key=newsapi_key)

    # Query for news articles based on the specified parameters.
    response = newsapi.get_everything(
        q=q,
        from_param=from_param,
        to=to,
        language=language,
        sort_by=sort_by,  # Options: 'popularity', 'relevancy', 'publishedAt'
        page_size=page_size,  # Number of articles to retrieve per request
    )

    # Extract and return the list of articles.
    articles = response.get("articles", [])
    return json.dumps(articles)


def extract_top_stories(
    category: str = "technology",
    language: str = "en",
    country: str = "us",
    page_size: int = 1,
) -> str:
    """
    Extracts top news stories from NewsAPI based on category, language, and country.

    This function queries the NewsAPI service to retrieve top headlines for a specific
    category and country in the desired language. It returns the results as a
    JSON-formatted string containing article details.

    Prerequisites:
        - NewsAPI API key must be configured as newsapi_key
        - newsapi-python package must be installed: pip install newsapi-python

    Args:
        category (str, optional): News category to fetch articles from.
            Valid categories: business, entertainment, general, health, science,
            sports, technology
            Default: "technology"
        language (str, optional): Two-letter ISO 639-1 language code.
            Default: "en" (English)
        country (str, optional): Two-letter ISO 3166-1 country code.
            Default: "us" (United States)
        page_size (int, optional): Number of articles to retrieve per request (1-100).
            Default: 1

    Returns:
        str: JSON-formatted string containing list of articles. Each article includes:
            - source: Dictionary with 'id' and 'name' of the news source
            - author: String with article author's name
            - title: String with article headline
            - description: String with article description/summary
            - url: String with link to full article
            - urlToImage: String with link to article's featured image
            - publishedAt: String with ISO 8601 publication date/time
            - content: String with article content snippet

    Raises:
        NewsAPIException: If there's an error with the API request
        ValueError: If page_size is not between 1 and 100
        ValueError: If category is not one of the valid options
        ValueError: If country code is not supported

    Example:
        >>> # Get 3 top health stories from Germany in English
        >>> articles = extract_top_stories(
        ...     category="health",
        ...     language="en",
        ...     country="de",
        ...     page_size=3
        ... )
        >>> # Parse the returned JSON string
        >>> import json
        >>> news_items = json.loads(articles)
        >>> for item in news_items:
        ...     print(f"Title: {item['title']}")
        ...     print(f"Source: {item['source']['name']}")
        ...     print(f"URL: {item['url']}\n")

    Notes:
        - The function requires a valid NewsAPI API key
        - Rate limits apply based on your NewsAPI subscription
        - Some articles may have missing fields (None values)
        - Not all combinations of language and country are available
        - Categories are fixed and must match NewsAPI's predefined categories
        - The API might return fewer articles than requested if not enough
          are available for the specified criteria
    """
    # Initialize the NewsApiClient with your API key.
    newsapi = NewsApiClient(api_key=newsapi_key)

    # Query for news articles based on the specified parameters.
    response = newsapi.get_top_headlines(
        language=language,
        category=category,
        country=country,
        page_size=page_size,  # Number of articles to retrieve per request
    )

    # Extract and return the list of articles.
    articles = response.get("articles", [])
    return json.dumps(articles)
