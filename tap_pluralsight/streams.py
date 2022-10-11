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
    records_jsonpath = "$.data.courseCatalog.nodes[*]" # https://jsonpath.com Use requests response json to identify the json path 
    primary_keys = ["id"]
    replication_key = None
    #schema_filepath = SCHEMAS_DIR / "coursecatalog.json"  # Optional: use schema_filepath with .json inside schemas/ 

    # Optional: If using schema_filepath, remove the propertyList schema method below
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("idNum", th.NumberType),
        th.Property("title", th.StringType),
        th.Property("url", th.StringType),
        th.Property("authors", th.StringType),
        th.Property("__typename", th.StringType),
        th.Property("publishedDate", th.DateTimeType),
        th.Property("displayDate", th.DateTimeType),
        th.Property("releasedDate", th.DateTimeType),
        th.Property("image", th.StringType),
        th.Property("tags", th.ObjectType(
            th.Property("idNum", th.NumberType),
            th.Property("superDomain", th.StringType),
            th.Property("domain", th.StringType),
            th.Property("audience", th.StringType),
            )   
        ),
        th.Property("courseStatus", th.ObjectType(
            th.Property("name", th.StringType),
            th.Property("reason", th.StringType),
            th.Property("replacementCourseId", th.StringType),
            )
        ),
        th.Property("averageRating", th.NumberType),
        th.Property("level", th.StringType),
        th.Property("language", th.StringType),
        th.Property("slug", th.StringType),
        th.Property("courseSeconds", th.StringType),
    ).to_dict()

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Define request parameters to return"""

        # working graphyql
        request_data = {
            "query": ("{ courseCatalog(first:50) { nodes{ title, url, authors, __typename, publishedDate, image:url, displayDate, releasedDate, tags { idNum superDomain domain audience }, courseStatus { name reason replacementCourseId }, averageRating, level, language, slug, courseSeconds}}}"),
            "variables": {},
        }
        
        return  request_data
