import re
import json
import httpx
from typing import Optional, Dict
from django.conf import settings

def fetch_obj_tool_data() -> Optional[Dict]:
    """
    Fetches the 'toolData' variable from the target website and converts it into a dictionary.

    Returns:
        Optional[Dict]: A dictionary representation of the 'toolData' JSON, or None if not found or an error occurs.
    """
    url = settings.URL_INFOMONEY_ALTAS_BAIXAS
    assert url, "URL_INFOMONEY_ALTAS_BAIXAS is not set in settings.py"

    try:
        # Make a GET request
        with httpx.Client() as client:
            response: httpx.Response = client.get(url, headers={"User-Agent": "Mozilla/5.0"})
            response.raise_for_status()  # Raise exception for error HTTP codes

            # Read the HTML content
            html_content: str = response.text

            # Extract tool_data_dict using the helper function
            return extract_tool_data(html_content)

    except httpx.RequestError as e:
        print(f"Erro ao acessar o site: {e}")
        return None

def extract_tool_data(html_content: str) -> Optional[Dict]:
    """
    Extracts the 'toolData' variable from the HTML content and converts it into a dictionary.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        Optional[Dict]: A dictionary representation of the 'toolData' JSON, or None if not found or an error occurs.
    """
    pattern: str = r"var\s+toolData\s*=\s*(\{.*?\});"  # Captures JSON from the toolData variable
    tool_data_match: Optional[re.Match] = re.search(pattern, html_content, re.DOTALL)

    if tool_data_match:
        # Extract JSON as string
        tool_data_json: str = tool_data_match.group(1)
        # Convert JSON string to dictionary
        try:
            tool_data_dict: Dict = json.loads(tool_data_json)
        except json.JSONDecodeError as e:
            print(f"Error converting toolData to dictionary: {e}")
            return None
        return tool_data_dict

    return None