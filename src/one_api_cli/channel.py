import requests
from .constant import base_url, headers, default_channel_data
from loguru import logger

channel_url = f"{base_url}/api/channel"

class Channel():
    """
    A class to represent a channel.
    """

    def __init__(self, id:int):
        data = self.fetch_channel_data(id)
        if not data:
            raise ValueError(f"Channel with ID {id} not found.")
        self.__dict__.update(data)
    
    def dumps(self):
        return self.__dict__.copy()
    
    @classmethod
    def fetch_channel_data(cls, id:int) -> dict:
        """
        Fetch the data of a channel.

        Args:
            id (int): The ID of the channel.

        Returns:
            dict: The data of the channel.
        """
        channel_id_url = f"{channel_url}/{id}"
        response = cls._make_request('get', channel_id_url)
        if not response['success']:
            logger.error(response['message'])
            raise ValueError(f"Channel with ID {id} not found.")
        return response['data']

    @staticmethod
    def get_channels(page=None):
        """
        Retrieve a list of channels.

        Returns:
            list: A list of channel dictionaries.
        """
        if page is not None:
            suffix = f"/?p={page}"
            channel_data = Channel._make_request('get', channel_url + suffix)['data']
        else:
            i = 0
            channel_data = []
            while True:
                suffix = f"?p={i}"
                response = Channel._make_request('get', channel_url + suffix)
                new_data = response['data']
                if not new_data:
                    break
                channel_data.extend(new_data)
                i += 1
        return [Channel.from_data(**data) for data in channel_data]
    
    @staticmethod
    def from_data(**data:dict):
        """
        Create a channel object from data.

        Args:
            **data: The data of the channel.
        
        Returns:
            Channel: A channel object.
        """
        channel = Channel.__new__(Channel)
        channel.__dict__.update(data)
        return channel

    def update(self, **channel_data):
        """Update the channel data."""
        data = self.__dict__.copy()
        data.update(channel_data)
        response = self._make_request('put', channel_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        self.__dict__.update(channel_data)
        return True
    
    def delete(self, confim:bool=True):
        """Delete the channel."""
        if confim:
            logger.warning(f"Deleting channel {self.name} with ID {self.id}")
            c = input("Are you sure? (y/n): ")
            if c.lower() != 'y': return False
        channel_id_url = f"{channel_url}/{self.id}"
        msg = self._make_request('delete', channel_id_url)
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    
    @staticmethod
    def create(**channel_data):
        """Create a new channel.
        
        Args:
            name (str): The name of the channel.
            key (str): The api key of the channel.
            base_url (str): The base URL of the channel.
            models (list): The models of the channel.
        """
        data = default_channel_data.copy()
        data.update(channel_data)
        assert None not in data.values(), "Missing required fields"
        response = Channel._make_request('post', channel_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        return True
    
    @staticmethod
    def _make_request(method:str, url:str, **kwargs):
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error making request: {e}")
            return {}

    def __repr__(self) -> str:
        return f"Channel({self.__dict__})"
    
    def __str__(self) -> str:
        return f"Channel({self.__dict__})"
