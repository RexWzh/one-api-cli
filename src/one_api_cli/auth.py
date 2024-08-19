import one_api_cli
import requests
from loguru import logger
from typing import Union

class OneAPI():
    """Authentication class."""

    def __init__(self, one_api_url:str="", access_token:str=""):
        """
        Initialize the authentication class.

        Args:
            one_api_url (str): The base URL of the One API site.
            access_token (str): The access token of One API site. You can find it at {one_api_url}/panel/profile
        """
        self.access_token = access_token or one_api_cli.access_token
        assert self.access_token, "Access token is required."
        self.one_api_url = one_api_url or one_api_cli.one_api_url
        assert self.one_api_url, "One API URL is required."
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Authorization": f"Bearer {self.access_token}",
        }
        # set urls
        self.channel_url = f"{self.one_api_url}/api/channel"
        self.status_url = f"{self.one_api_url}/api/status"
        self.user_url = f"{self.one_api_url}/api/user"
    
    def _make_request(self, method:str, url:str, **kwargs):
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error making request: {e}")
            return {}

    def status(self) -> dict:
        """
        Retrieve the status of the One API site.

        Returns:
            dict: The status of the One API site.
        """
        return self._make_request('get', self.status_url)

    def is_valid(self)->bool:
        """
        Check if the authentication is valid.

        Returns:
            bool: True if the authentication is valid, False otherwise.
        """
        return self.status()['success']

    def get_channels(self, page:int=None):
        """
        Retrieve a list of channels.

        Args:
            page (int): The page number of the channels.

        Returns:
            list: A list of channel dictionaries.
        """
        if page is not None:
            suffix = f"/?p={page}"
            channel_data = self._make_request('get', self.channel_url + suffix)['data']
        else:
            i, channel_data = 0, []
            while True:
                suffix = f"?p={i}"
                new_data = self._make_request('get', self.channel_url + suffix)['data']
                if not new_data:
                    break
                channel_data.extend(new_data)
                i += 1
        return [
            one_api_cli.Channel.from_data(self, data) for data in channel_data]
    
    def latest_channel(self):
        """Retrieve the latest channel."""

        channel_data = self.get_channels(page=0)
        if not channel_data:
            logger.warning("No channels found.")
            return None
        return channel_data[0]
    
    def create_channel(self, **channel_data):
        """Create a new channel.
        
        Args:
            name (str): The name of the channel.
            key (str): The api key of the channel.
            base_url (str): The base URL of the channel.
            models (list): The models of the channel.
        """
        data = one_api_cli.default_channel_data.copy()
        data.update(channel_data)
        assert None not in data.values(), "Missing required fields"
        response = self._make_request('post', self.channel_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        return self.latest_channel()

    def get_users(self) -> list:
        """
        Retrieve a list of users.
        
        Returns:
            list: A list of user dictionaries.
        """
        user_data = self._make_request('get', self.user_url)['data']
        return [
            one_api_cli.User.from_data(self, data) for data in user_data]
    
    def get_id_from_username(self, username:str) -> int:
        """
        Retrieve the ID of a user by username.

        Args:
            username (str): The username of the user.

        Returns:
            int: The ID of the user.
        """
        users = self.get_users()
        for user in users:
            if user.username == username:
                return user.id
        return None
    
    def create_user(self,
            username:str,
            display_name:str,
            password:str,
            group:str='default',
            quota:int=0,
            is_edit:bool=False
        ):
        """
        Create a new user.

        Args:
            username (str): The username of the user.
            display_name (str): The display name of the user.
            password (str): The password of the user.
            group (str): The group of the user.
            quota (int): The quota of the user.
            is_edit (bool): Whether the user can edit.

        Returns:
            User: The user object.
        """
        user_data = {
            'username': username,
            'display_name': display_name,
            'password': password,
            'group': group,
            'quota': quota,
            'is_edit': is_edit
        }
        response = self._make_request('post', self.user_url, json=user_data)
        if not response['success']:
            logger.error(response['message'])
            return None
        return one_api_cli.User(user=username, auth=self)

    def delete_user(self, user:Union[str, int], confim:bool=False) -> bool:
        """
        Delete a user.

        Args:
            user (str, int): The username or ID of the user.
            confim (bool): Whether to confirm the deletion.

        Returns:
            bool: True if the user is deleted, False otherwise.
        """
        if confim:
            logger.warning("User deletion is irreversible.")
            c = input("Are you sure you want to delete this user? (y/n): ")
            if c.lower() != 'y':
                return False
        if isinstance(user, int):
            user = one_api_cli.User(user, auth=self).username
        delete_url = f"{self.user_url}/manage"
        data = {"username":user, "action":"delete"}
        response = self._make_request('post', delete_url, json=data)
        if not response['success']:
            logger.error(response['message'])
            return False
        return True