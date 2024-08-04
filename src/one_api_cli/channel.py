import requests
from .constant import base_url, headers
from loguru import logger

channel_url = f"{base_url}/api/channel"

def get_channels():
    """
    Retrieve a list of channels.
    
    Returns:
        list: A list of channel dictionaries.
    """
    try:
        response = requests.get(channel_url, headers=headers)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return {}
        return msg['data']
    except requests.RequestException as e:
        logger.error(f"Error fetching channels: {e}")
        return []
    
def get_channel(channel_id:int)->dict:
    """
    Retrieve the data of a channel.
    
    Returns:
        dict: A channel dictionary.
    """
    channel_id_url = f"{channel_url}/{channel_id}"
    try:
        response = requests.get(channel_id_url, headers=headers)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return {}
        return msg['data']
    except requests.RequestException as e:
        logger.error(f"Error fetching channel: {e}")
        return {}

def update_channel(channel_id, **options) -> bool:
    """
    Update a channel's data.
    
    Args:
        channel_id (int): The ID of the channel.
        **options: The data to update.
    
    Returns:
        bool: True if the channel is updated successfully, False otherwise.
    """
    
    try:
        channel_data = get_channel(channel_id)
        if not channel_data:
            logger.error(f"Channel with ID {channel_id} not found.")
            return False
        channel_data.update(options)
        response = requests.put(channel_url, headers=headers, json=channel_data)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error updating channel: {e}")
        return False

def delete_channel(channel_id) -> bool:
    """
    Delete a channel.
    
    Args:
        channel_id (int): The ID of the channel.
    
    Returns:
        bool: True if the channel is deleted successfully, False otherwise.
    """
    channel_id_url = f"{channel_url}/{channel_id}"
    try:
        response = requests.delete(channel_id_url, headers=headers)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error deleting channel: {e}")
        return False

def create_channel(
        name, key, base_url, models,
        type: int = 1,
        other: str = '',
        model_mapping: str = '',
        groups: list = ['default'],
        config: str = '{}',
        is_edit: bool = False,
        group: str = 'default'
) -> bool:
    """
    Create a new channel.
    
    Args:
        name (str): The name of the channel.
        key (str): The key of the channel.
        base_url (str): The base URL of the channel.
        models (list): The models of the channel.
        type (int): The type of the channel. Default to OpenAI.
        other (str): Other information of the channel.
        model_mapping (str): The model mapping of the channel.
        groups (list): The groups of the channel.
        config (str): The config of the channel.
        is_edit (bool): Whether the channel can be edited.
        group (str): The group of the channel.

    Returns:
        bool: True if the channel is created successfully, False otherwise.
    """
    
    data = {
        'name': name,
        'key': key,
        'base_url': base_url,
        'models': models,
        'type': type,
        'other': other,
        'model_mapping': model_mapping,
        'groups': groups,
        'config': config,
        'is_edit': is_edit,
        'group': group
    }
    try:
        response = requests.post(channel_url, headers=headers, json=data)
        response.raise_for_status()
        msg = response.json()
        if not msg['success']:
            logger.error(msg['message'])
            return False
        return True
    except requests.RequestException as e:
        logger.error(f"Error creating channel: {e}")
        return False