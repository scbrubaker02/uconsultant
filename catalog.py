import requests
from langchain.tools import tool
from langchain_core.tools import ToolException

@tool
def search(query: str) -> dict:
    """Query the Udacity Catalog for a course based on the provided query."""

    # The URL for the API endpoint
    url = "https://api.udacity.com/api/unified-catalog/search"
    
    # The data payload for the POST request, inserting the query parameter
    payload = {
        "searchText": query,
        "sortBy": "relevance",
        "page": 0,
        "pageSize": 6,
        "semanticTypes": ["Part"]
    }
    
    # Attempting the POST request
    try:
        response = requests.post(url, json=payload)
        
        # Ensure the response status is 200 (OK)
        response.raise_for_status()

        # If successful, return the JSON response
        r = response.json()
        hits = [
            {
                "title": hit['title'],
                "key": hit['key'],
                "summary": hit['summary'],
                "skills": hit['skill_names'],
                "slug": hit['slug']
            }
            for hit in r['searchResult']['hits']
        ]

        return {"hits": hits }

    except requests.exceptions.HTTPError as e:
        # If the request failed, raise a ToolException with the status code
        raise ToolException(f"HTTP error occurred: {e.response.status_code} {e.response.reason}")
    except requests.exceptions.RequestException as e:
        # For other requests-related issues, raise a ToolException with the error description
        raise ToolException(f"Error making request to Udacity catalog: {str(e)}")
