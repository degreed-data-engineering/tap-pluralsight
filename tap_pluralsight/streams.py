"""Stream class for tap-pluralsight."""

import base64
import json
from typing import Dict, Optional, Any, Iterable
from pathlib import Path
from singer_sdk import typing
from functools import cached_property
from singer_sdk import typing as th
from singer_sdk.streams import RESTStream
from singer_sdk.authenticators import SimpleAuthenticator
import requests

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class TapPluralsightStream(RESTStream):
    """Pluralsight stream class."""
    
    _LOG_REQUEST_METRIC_URLS: bool = True
    @property
    def url_base(self) -> str:
        """Base URL of source"""
        return f"https://paas-api.pluralsight.com"

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["Content-Type"] = "application/json"
        return headers

    @property
    def authenticator(self):
        http_headers = {}

        http_headers["Authorization"] = "Bearer " + self.config.get("api_token")

        return SimpleAuthenticator(stream=self, auth_headers=http_headers)

class CourseCatalog(TapPluralsightStream):
    rest_method = "POST"
    name = "coursecatalog" # Stream name 
    path = "/graphql" # API endpoint after base_url 
    records_jsonpath = "$.data.contentCatalog.nodes[*]" # https://jsonpath.com Use requests response json to identify the json path 
    next_page_token_jsonpath = "$.data.contentCatalog.pageInfo.endCursor"
    primary_keys = ["contentId"]
    replication_key = None
    #schema_filepath = SCHEMAS_DIR / "coursecatalog.json"  # Optional: use schema_filepath with .json inside schemas/ 

    # Optional: If using schema_filepath, remove the propertyList schema method below
    schema = th.PropertiesList(
        th.Property("contentId", th.StringType),
        th.Property("contentType", th.StringType),
        th.Property("title", th.StringType),
        th.Property("status", th.StringType),
        th.Property("pathName", th.StringType),
        th.Property("datePublished", th.DateTimeType),
        th.Property("dateModified", th.DateTimeType),
        th.Property("description", th.StringType),
        th.Property("duration", th.NumberType),
        th.Property("imageUrl", th.StringType),
        th.Property("tags", th.ObjectType(
            th.Property("superDomain", th.StringType),
            th.Property("domain", th.StringType),
            th.Property("audience", th.StringType),
            th.Property("primaryAtomic", th.ObjectType(
                th.Property("name", th.StringType),
                th.Property("alternativeNames", th.StringType),
                ),
            ),
        ),
    )
    ).to_dict()

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Define request parameters to return"""

        # working graphyql
        request_data = {
            "query": (f'{{ contentCatalog(first: 100 after: "{next_page_token}") {{ totalCount pageInfo {{ endCursor hasNextPage }} nodes {{ contentId contentType title status pathName datePublished dateModified description duration imageUrl tags {{ superDomain domain audience primaryAtomic {{ name alternativeNames }} }} }} }} }}'),
            "variables": {},
        }
        
        return  request_data


