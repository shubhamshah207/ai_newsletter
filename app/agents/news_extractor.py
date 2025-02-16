import os
from app.tools.news_extractor import extract_live_news
from agno.agent import Agent
from agno.models.google import Gemini


def get_news_extractor():
    """
    Creates and returns an instance of the News Extractor agent.

    This agent is responsible for extracting the top stories from news APIs using
    the 'extract_live_news' tool. It is configured with a Gemini model for processing,
    and equipped with telemetry, monitoring, and debugging features.

    Returns:
        Agent: The configured News Extractor agent instance.
    """

    # Retrieve the API key from environment variables (ensure it is set before running the app)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key is missing. Please set the GOOGLE_API_KEY environment variable."
        )

    # Initialize the Agent with necessary configurations
    news_extractor = Agent(
        name="News Extractor",  # Descriptive name for the agent
        role="Fetches top stories from news APIs",  # Brief description of the agent's function
        tools=[extract_live_news],  # Assigning the tool used by the agent
        model=Gemini(
            id="gemini-1.5-flash", api_key=api_key
        ),  # Assigning the AI model (Gemini) and API key
        system_message=""" 
        Always include the source URL when extracting news stories.
        Use the 'extract_live_news' tool for fetching the latest stories.
        """,  # System message guiding the agent's behavior
        ### ------ Optional Debug/Telemetry/Monitoring Settings --------- ###
        show_tool_calls=True,  # Show details of the tool calls for debugging purposes
        markdown=True,  # Enable markdown formatting in the output
        debug_mode=True,  # Enable debugging to capture detailed logs (useful during development)
        telemetry=True,  # Enable telemetry for tracking performance and usage
        monitoring=True,  # Enable monitoring for ensuring the agent team operates correctly
        ### ------ END --------- ###
    )

    return news_extractor
