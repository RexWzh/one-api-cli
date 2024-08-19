"""Top-level package for one-api-cli."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '1.0.0'

from .account import User
from .channel import Channel
from .auth import OneAPI
import os

one_api_url = os.getenv("ONE_API_URL")
access_token = os.getenv("ONE_API_ACCESS_TOKEN")

default_channel_data =  {
    "name": None,
    "key": None,
    "base_url": None,
    "models": None,
    "type": 1,
    "other": "",
    "model_mapping": "",
    "groups": ["default"],
    "config": "{}",
    "is_edit": False,
    "group": "default"
}
