import requests
from .constant import base_url, headers
from loguru import logger
from typing import List, Union

def get_users() -> List[dict]:
    """
    Retrieve a list of users.
    
    Returns:
        list: A list of user dictionaries.
    """
    user_url = f"{base_url}/api/user"
    try:
        response = requests.get(user_url, headers=headers)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return {}
        return msg['data']
    except requests.RequestException as e:
        logger.error(f"Error fetching users: {e}")
        return []

def get_user(ind:int) -> dict:
    """
    Retrieve the data of a user.
    
    Returns:
        dict: A user dictionary.
    """
    user_url = f"{base_url}/api/user/{ind}"
    try:
        response = requests.get(user_url, headers=headers)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return {}
        return msg['data']
    except requests.RequestException as e:
        logger.error(f"Error fetching user: {e}")
        return {}

def create_user(
        username:str,
        display_name:str,
        password:str,
        group:str='default',
        quota:int=0,
        is_edit:bool=False
    ) -> bool:
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
        bool: Whether the user was created successfully.
    """
    user_url = f"{base_url}/api/user"
    user_data = {
        'username': username,
        'display_name': display_name,
        'password': password,
        'group': group,
        'quota': quota,
        'is_edit': is_edit
    }
    try:
        response = requests.post(user_url, headers=headers, json=user_data)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error creating user: {e}")
        return False

def update_user(user_id:int, **options) -> bool:
    """
    Update a user's data.
    
    Args:
        user_id (int): The ID of the user.
        **options: The data to update.
    
    Returns:
        bool: Whether the user was updated successfully.
    """
    user_url = f"{base_url}/api/user"
    user_data = get_user(user_id)
    if not user_data:
        logger.error(f"User with ID {user_id} not found.")
        return False
    
    user_data.update(options)
    try:
        response = requests.put(user_url, headers=headers, json=user_data)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error updating user: {e}")
        return False

def delete_user(user:Union[int, str]) -> bool:
    """
    Delete a user.
    
    Args:
        user (int, str): The ID or username of the user.
    
    Returns:
        str: The response message.
    """
    delete_url = f"{base_url}/api/user/manage"
    try:
        username = get_user(user)['username'] if isinstance(user, int) else user
        data = {"username":username, "action":"delete"}
        response = requests.post(delete_url, headers=headers, json=data)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error deleting user: {e}")
        return False