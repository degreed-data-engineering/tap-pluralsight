"""pluralsight tap class."""

from pathlib import Path
from typing import List
import logging
import click
from singer_sdk import Tap, Stream
from singer_sdk import typing as th

from tap_pluralsight.streams import (
    Pluralsight_ContentCatalog,
)

PLUGIN_NAME = "tap-pluralsight"

STREAM_TYPES = [ 
    Pluralsight_ContentCatalog,
]

class TapPluralsight(Tap):
    """pluralsight tap class."""

    name = "tap-pluralsight"
    config_jsonschema = th.PropertiesList(

        th.Property("api_token", th.StringType, required=True, description="api token for Basic auth"),

    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        streams =  [stream_class(tap=self) for stream_class in STREAM_TYPES]

        return streams


# CLI Execution:
cli = TapPluralsight.cli