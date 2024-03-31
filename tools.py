"""Tool for the Udacity catalog search"""

from typing import Dict, List, Optional, Type, Union

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

from utilities import UdacityCatalogSearchAPIWrapper


class UdacityCatalogSearchInput(BaseModel):
    """Input for the Udacity catalog search tool."""
    query: str = Field(description="search query to look up")


class UdacityCatalogSearch(BaseTool):
    """Tool that queries the Udacity catalog gets back json."""

    name: str = "udacity_catalog_search"
    description: str = (
        "An Algolia-backed search engine for the Udacity catalog. "
        "Input should be a search query."
    )
    api_wrapper: UdacityCatalogSearchAPIWrapper = Field(default_factory=UdacityCatalogSearchAPIWrapper)
    max_results: int = 5
    args_schema: Type[BaseModel] = UdacityCatalogSearchInput

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> List[Dict]:
        """Use the tool."""
        try:
            return self.api_wrapper.run(
                query,
                self.max_results,
            )
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Union[List[Dict], str]:
        """Use the tool asynchronously."""
        try:
            return await self.api_wrapper.results_async(
                query,
                self.max_results,
            )
        except Exception as e:
            return repr(e)
