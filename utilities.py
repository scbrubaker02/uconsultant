"""Wrapper for the Udacity Catalog API"""

from typing import Any, Dict, List
from langchain_core.pydantic_v1 import BaseModel, root_validator
from langchain_core.utils import get_from_dict_or_env

class UdacityCatalogSearchAPIWrapper(BaseModel):
    """Wrapper for the Udacity Catalog API

    Example:
        .. code-block:: python

            from utilities import UdacityCatalogSearchAPIWrapper
            ucatalog_search = UdacityCatalogSearchAPIWrapper(results_limit=6)
    """

    udacity_catalog_url: str = "https://api.udacity.com/api/unified-catalog/search"
    udacity_session: Any

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Checks that requests module is present and that catalog_url is valid.
        """

        # Get the Udacity Catalog URL from the environment or the provided value
        udacity_catalog_url = get_from_dict_or_env(
            values, "udacity_catalog_url", "UDACITY_CATALOG_URL"
        )
        values["udacity_catalog_url"] = udacity_catalog_url

        # Check if the requests module is present
        try:
            import requests
        except ImportError:
            raise ImportError(
                "requests package not found, please install it with pip install requests"
            )

        # Create a session for the Udacity Catalog API
        udacity_session = requests.Session()
        udacity_session.headers.update({"Content-Type": "application/json"})
        values["udacity_session"] = udacity_session

        return values

    def run(
        self, query: str,
        results_limit: int = 6,
    ) -> List[Dict]:
        """Search the Udacity Catalog for a course based on the provided query."""
        # The data payload for the POST request, inserting the query parameter
        payload = {
            "searchText": query,
            "sortBy": "relevance",
            "page": 0,
            "pageSize": results_limit,
            "semanticTypes": ["Part"]
        }
    
        # Attempting the POST request
        response = self.udacity_session.post(self.udacity_catalog_url, json=payload)
        
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


if __name__ == "__main__":
    ucatalog_search = UdacityCatalogSearchAPIWrapper()
    print(ucatalog_search.run("python"))