from typing import Dict, List
from urllib.parse import urljoin

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

def model_to_dict(instance):
    return {column.key: getattr(instance, column.key) for column in instance.__table__.columns}

def models_to_dict(instances):
    return [model_to_dict(instance) for instance in instances]