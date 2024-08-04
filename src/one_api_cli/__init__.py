"""Top-level package for one-api-cli."""

__author__ = """Rex Wang"""
__email__ = '1073853456@qq.com'
__version__ = '0.2.0'

from .account import get_users, update_user, get_user, create_user, delete_user
from .channel import get_channels, update_channel, delete_channel, create_channel, get_channel