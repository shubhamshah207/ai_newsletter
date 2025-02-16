import os
import sys
from typing import Dict, Optional
from flask import Flask, redirect, request, render_template
from dotenv import load_dotenv, find_dotenv
from linkedin_api.clients.auth.client import AuthClient
from linkedin_api.clients.restli.client import RestliClient
from app.agents.newsletter_generator import get_newsletter_generator
from agno.agent import RunResponse
import markdown
from bs4 import BeautifulSoup
from flask import Blueprint


bp = Blueprint("linkedin", __name__)

# Add the parent directory to the Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Load environment variables from .env file
load_dotenv(find_dotenv())
TEMPLATE = "index.html"
# Constants for LinkedIn API and post configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH2_REDIRECT_URL = os.getenv("OAUTH2_REDIRECT_URL")
LIFECYCLE_STATE = os.getenv("lifecycleState")
UGC_POSTS_RESOURCE = "/ugcPosts"
MAX_POST_LENGTH = 2500


# Global variables for LinkedIn access and user information
access_token: Optional[str] = None
entity: Optional[Dict] = None

# Author information for rendering in templates
author = {
    "name": "Shubham Shah",
    "linkedin": "https://www.linkedin.com/in/shubhamshah207",
    "github": "https://github.com/shubhamshah207",
}

# Initialize LinkedIn API clients
auth_client = AuthClient(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_url=OAUTH2_REDIRECT_URL
)
restli_client = RestliClient()


def bold_text(text: str) -> str:
    """
    Convert a given text to bold using Unicode bold characters.

    Args:
        text (str): The input text to be converted.

    Returns:
        str: The text converted to bold using Unicode characters.
    """
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    bold = "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗝𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
    bold_mapping = str.maketrans(normal, bold)
    return text.translate(bold_mapping)


def parse_html(html: str) -> str:
    """
    Parse HTML content and extract text while preserving structure.
    Text inside header tags (h1-h4) will be bolded.

    Args:
        html (str): The HTML content to be parsed.

    Returns:
        str: The parsed and formatted text with bold headers.
    """
    soup = BeautifulSoup(html, features="html.parser")
    text = []
    prev_element = None

    for element in soup.descendants:
        if isinstance(element, str):
            stripped_text = element.strip()
            if stripped_text:
                # Apply bold_text to text inside <strong>, <h1>, <h2>, <h3>, <h4>
                if prev_element in ["h1", "h2", "h3", "h4", "strong"]:  # Bold headers
                    text.append(bold_text(stripped_text))
                else:
                    text.append(stripped_text)
        elif element.name in ["br", "p", "h1", "h2", "h3", "h4"]:
            if prev_element not in ["br", "p", "h1", "h2", "h3", "h4"]:
                text.append("\n\n")
        elif element.name == "li":
            depth = len(element.find_parents("ul")) + len(element.find_parents("ol"))
            text.append("\n" + "  " * (depth - 1) + "- ")
        elif element.name in ["tr"]:
            text.append("\n")
        elif element.name in ["th", "td"]:
            text.append("\t")

        prev_element = element.name

    return "".join(text).strip()


@bp.route("/linkedin_access", methods=["GET"])
def linkedin_access():
    """
    Handle LinkedIn access and authentication. Redirects to LinkedIn authentication if
    access token is not available, else retrieves user information and renders the dashboard.
    """
    global access_token, entity
    if access_token is None:
        return redirect(
            auth_client.generate_member_auth_url(
                scopes=["w_member_social", "openid", "profile"]
            )
        )
    else:
        entity = restli_client.get(
            resource_path="/userinfo", access_token=access_token
        ).entity
        return render_template(TEMPLATE, entity=entity, author=author)


@bp.route("/linkedin_post", methods=["POST"])
def linkedin_post():
    """
    Create a LinkedIn post with the provided content.
    """
    global entity, access_token
    if entity is None or access_token is None:
        return redirect("/linkedin_access")

    post_content = request.form["post"]
    text = parse_html(post_content)
    print(text)

    # Prepare the LinkedIn post
    ugc_post = {
        "author": f"urn:li:person:{entity['sub']}",
        "lifecycleState": LIFECYCLE_STATE,
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": text[:MAX_POST_LENGTH]},
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"},
    }

    # Send the post creation request
    ugc_posts_create_response = restli_client.create(
        resource_path=UGC_POSTS_RESOURCE,
        entity=ugc_post,
        access_token=access_token,
    )

    # Redirect to the new post URL
    return redirect(
        f"https://www.linkedin.com/feed/update/{ugc_posts_create_response.entity_id}/"
    )


@bp.route("/newsletter", methods=["POST"])
def newsletter():
    """
    Generate a newsletter based on user input and return the HTML content.
    """
    command = request.form["text"]
    agent = get_newsletter_generator()

    # Run the newsletter generation agent
    response: RunResponse = agent.run(command, markdown=True)
    html_content = markdown.markdown(response.content)
    result = {
        "response": html_content,
        "input": command,
    }
    return render_template(TEMPLATE, result=result, author=author)


@bp.route("/oauth", methods=["GET"])
def oauth():
    """
    Handle OAuth callback and token exchange.
    """
    global access_token

    auth_code = request.args.get("code")

    if auth_code:
        token_response = auth_client.exchange_auth_code_for_access_token(auth_code)
        access_token = token_response.access_token
        print(f"Access token: {access_token[:10]}...")
        return redirect("/linkedin_access")


@bp.route("/", methods=["GET"])
def index():
    """
    Render the main page.
    """
    return render_template(TEMPLATE, result=None, author=author)
