"""
This module contains functions that are not related to anything specific but
are ought to be used throughout the project. 
"""

from typing import Dict, List
from urllib.parse import urljoin
from sqlalchemy.ext.declarative import DeclarativeMeta


def map_keys_to_url(url_mapper: Dict[str, str], data: Dict[str, str]) -> Dict[str, str]:
    """
    Maps keys to a url using a url mapper.

    Args:
        url_mapper: Dict[str, str] - A dictionary that maps keys to urls.
        data: Dict[str, str] - The data to map to urls.

    Returns:
        A dictionary with the keys mapped to the urls.
    """
    for key, value in data.items():
        if key in url_mapper:
            data[key] = urljoin(url_mapper[key], str(value))
    return data

def map_all_keys_to_url(url_mapper: Dict[str, str], data: List[Dict[str, str]]):
    """
    Maps all keys to a url using a url mapper.

    Args:
        url_mapper: Dict[str, str] - A dictionary that maps keys to urls.
        data: List[Dict[str, str]] - The data to map to urls.

    Returns:
        A list of dictionaries with the keys mapped to the urls.
    """
    print(data)
    return [map_keys_to_url(url_mapper, entry) for entry in data]

def model_to_dict(instance: DeclarativeMeta) -> Dict[str, str]:
    """
    Converts an sqlalchemy model to a dictionary.

    Args:
        instance: DeclarativeMeta - The instance of the model to convert to a dictionary.

    Returns:
        A dictionary with the keys and values of the model.
    """
    return {column.key: getattr(instance, column.key) for column in instance.__table__.columns}

def models_to_dict(instances: List[DeclarativeMeta]) -> List[Dict[str, str]]:
    """
    Converts a list of sqlalchemy models to a list of dictionaries.

    Args:
        instances: List[DeclarativeMeta] - The instances of the models to convert to dictionaries.

    Returns:
        A list of dictionaries with the keys and values of the models.
    """
    return [model_to_dict(instance) for instance in instances]
