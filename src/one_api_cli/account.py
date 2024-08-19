import requests
from loguru import logger
from typing import List, Union
import one_api_cli
from .auth import OneAPI


class User():

    def __init__(self, user:Union[int, str], auth:Union[OneAPI, None]=None):
        """
        Initialize a user.

        Args:
            user (int, str): The ID or username of the user.
            auth (OneAPI): The authentication object.
        """
        self.auth = auth or OneAPI(one_api_url=one_api_cli.one_api_url, access_token=one_api_cli.access_token)
        user_id = self.auth.get_id_from_username(user) if isinstance(user, str) else user
        self.user_id = user_id
        self.user_url = self.auth.user_url
        self.data = self._fetch_user_data()
        self.__dict__.update(self.data)

    def _fetch_user_data(self) -> dict:
        """
        Fetch the data of a user.
        
        Returns:
            dict: The data of the user.
        """
        user_id_url = f"{self.user_url}/{self.user_id}"
        response = self.auth._make_request('get', user_id_url)
        if not response['success']:
            logger.error(response['message'])
            raise ValueError(f"User with ID {self.user_id} not found.")
        return response['data']
    
    def update(self, **user_data):
        """Update the user and push the changes to the server."""
        data = self.data.copy()
        data.update(user_data)
        response = self.auth._make_request('put', self.user_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        self.data = data
        self.__dict__.update(data)
        return True
    
    def delete(self, confim:bool=False) -> bool:
        """Delete the user."""
        if confim:
            logger.warning("User deletion is irreversible.")
            c = input("Are you sure you want to delete this user? (y/n): ")
            if c.lower() != 'y':
                return False
        delete_url = f"{self.user_url}/manage"
        data = {"username":self.username, "action":"delete"}
        response = self.auth._make_request('post', delete_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        return True

    @staticmethod
    def from_data(auth:str, data:dict):
        """
        Create a user object from data.

        Args:
            data: The data of the user.
        
        Returns:
            User: A user object.
        """
        user = User.__new__(User)
        user.auth, user.user_url = auth, auth.user_url
        user.data = data
        user.__dict__.update(data)
        return user
    
    def __str__(self):
        return f"User({self.id}, {self.username})"

    def __repr__(self):
        return f"User({self.id}, {self.username})"