import json
from typing import (
    Any,
    Optional,
)


class SettingsLoader:
    """Единая точка конфигурации (Singleton)"""
    
    _instance: Optional['SettingsLoader'] = None
    _initialized: bool = False
    _config: Optional[dict[str, Any]] = None
    
    def __new__(cls) -> 'SettingsLoader':
        """
        Выбран способ через __new__ из-за его простоты относительно метаклассов.
        
        :param cls: Класс
        :return: Экземпляр класса
        :rtype: SettingsLoader
        """

        if cls._instance is None:
            cls._instance = super(SettingsLoader, cls).__new__(cls)
        return cls._instance
    

    def __init__(self) -> None:
        """
        Загрузить конфигурацию системы.
        """

        if self._initialized:
            return None
        
        config_path = 'config.json'
        
        fp = None
        try:
            fp = open(config_path, 'r')
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self._config = {'data_path': 'data/',
                            'rates_ttl_seconds': 300,
                            'log_path': 'logs/'}
            
        else:
            self._config = json.load(fp)
        finally:
            if fp is not None:
                fp.close()
        
        self._initialized = True
    

    def get(self, key: str, default: Any = None) -> Any:
        """
        Получить конфиг по ключу.
        
        :param key: Ключ
        :type key: str
        :param default: Значение по умолчанию
        :type default: Any
        :return: Значение конфига
        :rtype: Any
        """

        if self._config is not None:
            return self._config.get(key, default)


config = SettingsLoader()