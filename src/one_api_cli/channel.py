from typing import Union
from loguru import logger
import one_api_cli
from .auth import OneAPI

class Channel():
    """
    A class to represent a channel.
    """

    def __init__(self, id:int, auth:Union[OneAPI, None]=None):
        """
        Initialize a channel.

        Args:
            id (int): The ID of the channel.
            auth (OneAPI): The authentication object.
        """
        self.auth = auth or OneAPI(one_api_url=one_api_cli.one_api_url, access_token=one_api_cli.access_token)
        self.channel_url, self.id = self.auth.channel_url, id
        # fetch the channel data
        data = self._fetch_channel_data()
        if not data:
            raise ValueError(f"Channel with ID {id} not found.")
        self.data = data
        self.__dict__.update(data)

    def _fetch_channel_data(self) -> dict:
        """
        Fetch the data of a channel.

        Returns:
            dict: The data of the channel.
        """
        channel_id_url = f"{self.channel_url}/{self.id}"
        response = self.auth._make_request('get', channel_id_url)
        if not response['success']:
            logger.error(response['message'])
            raise ValueError(f"Channel with ID {self.id} not found.")
        return response['data']
        
    @staticmethod
    def from_data(auth:str, data:dict):
        """
        Create a channel object from data.

        Args:
            data: The data of the channel.
        
        Returns:
            Channel: A channel object.
        """
        channel = Channel.__new__(Channel)
        channel.auth, channel.channel_url = auth, auth.channel_url
        channel.data = data
        channel.__dict__.update(data)
        return channel

    def update(self, **channel_data):
        """Update the channel and push the changes to the server."""
        data = self.data.copy()
        data.update(channel_data)
        response = self.auth._make_request('put', self.channel_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        self.data = data
        self.__dict__.update(data)
        return True
    
    def delete(self, confim:bool=True):
        """Delete the channel."""
        if confim:
            logger.warning(f"Deleting channel {self.name} with ID {self.id}")
            c = input("Are you sure? (y/n): ")
            if c.lower() != 'y': return False
        channel_id_url = f"{self.channel_url}/{self.id}"
        msg = self.auth._make_request('delete', channel_id_url)
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    
    def __repr__(self) -> str:
        return f"Channel({self.id}, {self.name})"
    
    def __str__(self) -> str:
        return self.__repr__()