import json
import os

DATA_DIR = 'data/'

def load_users(data_path: str) -> list[dict]:
    """
    Загрузить пользователей из системы.
    
    :param data_path: Путь к данным
    :type data_path: str
    :return: Список словарей пользователей
    :rtype: list[dict[Any, Any]]
    """
    
    filepath = os.path.join(data_path, 'users.json')
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


def save_users(data: list[dict], data_path: str) -> None:
    """
    Сохранить пользователей в систему.
    
    :param data: Данные
    :type data: list[dict]
    :param data_path: Путь к данным
    :type data_path: str
    """

    filepath = os.path.join(data_path, 'users.json')
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)


def load_portfolios(data_path: str) -> list[dict]:
    """
    Загрузить портфели из системы.
    
    :param data_path: Путь к данным
    :type data_path: str
    :return: Список словарей портфелей
    :rtype: list[dict[Any, Any]]
    """

    filepath = os.path.join(data_path, 'portfolios.json')
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


def save_portfolios(data: list[dict], data_path: str) -> None:
    """
    Сохранить портфели в систему.
    
    :param data: Данные
    :type data: list[dict]
    :param data_path: Путь к данным
    :type data_path: str
    """

    filepath = os.path.join(data_path, 'portfolios.json')
    with open(filepath, 'w') as fp:
        json.dump(data, fp, indent=4)


def load_rates(data_path: str) -> dict:
    """
    Загрузить текущие курсы.
    
    :param data_path: Путь к данным
    :type data_path: str
    :return: Словарь курсов
    :rtype: dict[Any, Any]
    """
    
    filepath = os.path.join(data_path, 'rates.json')
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    fp = None
    try:
        fp = open(filepath, 'r')
    except FileNotFoundError:
        rates = dict()
    else:
        rates = json.load(fp)
    finally:
        if fp is not None:
            fp.close()
    return rates

