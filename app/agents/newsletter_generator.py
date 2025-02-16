import os
from agno.agent import Agent
from agno.models.google import Gemini
from app.agents.news_extractor import get_news_extractor


def get_newsletter_generator():
    """
    Creates and returns an instance of the Newsletter Generator agent team.

    This agent team combines the News Extractor agent with a Gemini model to extract news
    and generate a newsletter with thoughtful and engaging summaries. The instructions
    guide the agent to provide news for a given date range and present each article
    with its title linked to the source URL.

    Returns:
        Agent: The configured Newsletter Generator agent team instance.
    """

    # Retrieve the Google API key from environment variables (ensure it is set before running the app)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError(
            "Google API key is missing. Please set the GOOGLE_API_KEY environment variable."
        )

    # Initialize the team of agents with their respective tasks
    agents_team = Agent(
        name="Newsletter Team",  # Descriptive name for the agent team
        model=Gemini(
            id="gemini-1.5-flash", api_key=api_key
        ),  # Assign the Gemini model and API key
        team=[get_news_extractor()],  # Add the News Extractor agent to the team
        instructions=[  # Detailed instructions to guide the team's behavior
            "First, use the News Extractor agent to get news for the provided date range.",
            "Next, provide thoughtful and engaging details of each article's content.",
            "Retain the article title.",
            "Make the title a clickable link to the source URL.",
        ],
        ### ------ Optional Debug/Telemetry/Monitoring Settings --------- ###
        show_tool_calls=True,  # Show details of the tool calls for debugging purposes
        markdown=True,  # Enable markdown formatting in the output
        debug_mode=True,  # Enable debugging to capture detailed logs (useful during development)
        telemetry=True,  # Enable telemetry for tracking performance and usage
        monitoring=True,  # Enable monitoring for ensuring the agent team operates correctly
        ### ------ END --------- ###
    )

    return agents_team
