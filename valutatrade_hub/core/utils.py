import json
import os
from typing import Optional


DATA_DIR = 'data/'

def load_users() -> list[dict]:
    """
    Загрузить пользователей из системы.
    
    :return: Список словарей пользователей
    :rtype: list[dict[Any, Any]]
    """
    
    filepath = os.path.join(DATA_DIR, 'users.json')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fp = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        users = []
    else:
        users = json.load(fp)
    finally:
        if fp is not None:
            fp.close()
    return users


def save_users(data):
    filepath = os.path.join(DATA_DIR, 'users.json')
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)


def load_portfolios() -> list[dict]:
    """
    Загрузить портфели из системы.
    
    :return: Список словарей портфелей
    :rtype: list[dict[Any, Any]]
    """

    filepath = os.path.join(DATA_DIR, 'portfolios.json')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    fp = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        portfolios = []
    else:
        portfolios = json.load(fp)
    finally:
        if fp is not None:
            fp.close()
    return portfolios


def save_portfolios(data):
    filepath = os.path.join(DATA_DIR, 'portfolios.json')
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)