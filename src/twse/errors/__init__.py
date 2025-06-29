"""Module for TWSE error classes."""

__all__ = [
    "TWSEAPIError",
    "TWSEDataError",
]

from .api_error import TWSEAPIError
from .data_error import TWSEDataError
