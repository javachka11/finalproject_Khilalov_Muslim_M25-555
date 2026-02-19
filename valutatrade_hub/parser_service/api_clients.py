from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict

import requests

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.config import ParserConfig


class BaseApiClient(ABC):
    """
    Абстрактный базовый класс клиентского API.
    """
    
    def __init__(self, config: ParserConfig) -> None:
        """
        Создать клиентский API.

        :param config: Конфигурация парсера
        :type config: ParserConfig
        """

        if not config.EXCHANGERATE_API_KEY:
            raise ValueError('Добавьте API-ключ в переменную окружения.')
        self.config = config
    

    @abstractmethod
    def fetch_rates(self) -> Dict[str, Any]:
        """
        Получить курс валют.
        
        :return: Словарь с курсом валют
        :rtype: Dict[str, Any]
        """
        pass


class CoinGeckoClient(BaseApiClient):
    def fetch_rates(self) -> Dict[str, Any]:
        """
        Получить курс валют с CoinGecko API.
        
        :return: Словарь с курсом валют
        :rtype: Dict[str, Any]
        """
        
        url = f"{self.config.COINGECKO_URL}"
        params = {
            'ids': ','.join([self.config.CRYPTO_ID_MAP[code]
                             for code in self.config.CRYPTO_CURRENCIES]),
            'vs_currencies': self.config.BASE_CURRENCY
        }
        
        try:
            response = requests.get(
                url, 
                params=params, 
                timeout=self.config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(f"CoinGecko API error: {e}")
            
        rates = dict()
        now = datetime.now().isoformat() + 'Z'
        
        for code in self.config.CRYPTO_CURRENCIES:
            valuta = self.config.CRYPTO_ID_MAP[code]
            if (valuta in data and
                self.config.BASE_CURRENCY.lower() in data[valuta]):
                rates[f'{code}_{self.config.BASE_CURRENCY}'] = {
                    'rate': float(data[valuta][self.config.BASE_CURRENCY.lower()]),
                    'timestamp': now,
                    'source': 'CoinGecko',
                    'meta': {
                        'raw_id': valuta,
                        'request_ms': int(response.elapsed.total_seconds() * 1000),
                        'status_code': response.status_code,
                        'etag': response.headers.get('ETag', '')
                    }
                }
        
        return rates


class ExchangeRateApiClient(BaseApiClient):
    def fetch_rates(self) -> Dict[str, Any]:
        """
        Получить курс валют с ExchangeRate-API.
        
        :return: Словарь с курсом валют
        :rtype: Dict[str, Any]
        """

        url = f"{self.config.EXCHANGERATE_API_URL}/"\
              f"{self.config.EXCHANGERATE_API_KEY}/latest/{self.config.BASE_CURRENCY}"
        
        try:
            response = requests.get(url,
                                    timeout=self.config.REQUEST_TIMEOUT)
            response.raise_for_status()
            
            data = response.json()
        except requests.exceptions.RequestException as e:
            raise ApiRequestError(f"ExchangeRate-API: {e}")
        
        if data.get('result') != 'success':
            raise ApiRequestError("ExchangeRate-API: Попробуйте ещё раз.")
            
        rates = dict()
        last_update = data.get('time_last_update_utc', '')
        try:
            dt = datetime.strptime(last_update, "%a, %d %b %Y %H:%M:%S %z")
            last_update = dt.isoformat().replace('+00:00', 'Z')
        except (ValueError, TypeError):
            last_update = datetime.now().isoformat() + "Z"
            
        conversion_rates = data.get('conversion_rates', {})
            
        for fiat_currency in self.config.FIAT_CURRENCIES:
            if fiat_currency in conversion_rates:
                rates[f"{fiat_currency}_{self.config.BASE_CURRENCY}"] = {
                    'rate': 1 / float(conversion_rates[fiat_currency]),
                    'timestamp': last_update,
                    'source': 'ExchangeRate-API',
                    'meta': {
                        'raw_id': fiat_currency,
                        'request_ms': int(response.elapsed.total_seconds() * 1000),
                        'status_code': response.status_code,
                        'etag': response.headers.get('ETag', '')
                    }
                }
            
        return rates