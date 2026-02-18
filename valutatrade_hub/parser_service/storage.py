import json
import os
from datetime import datetime
from typing import Any

from valutatrade_hub.parser_service.config import ParserConfig


class RatesStorage:
    """
    Хранилище для курсов валют.
    """
    
    def __init__(self) -> None:
        """
        Инициализировать хранилище.
        
        :param config: Конфиг
        :type config: ParserConfig
        """

        self.config = ParserConfig()


    def load_rates(self) -> dict:
        """
        Загрузить текущие курсы.
    
        :return: Словарь текущих курсов
        :rtype: dict[Any, Any]
        """
    
        os.makedirs(os.path.dirname(self.config.RATES_FILE_PATH), exist_ok=True)

        fp = None
        try:
            fp = open(self.config.RATES_FILE_PATH, 'r')
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            rates = dict()
        else:
            rates = json.load(fp)
        finally:
            if fp is not None:
                fp.close()
        return rates


    def load_exchange_rates(self) -> list[dict]:
        """
        Загрузить историю курсов.
    
        :return: Список истории курсов
        :rtype: list[dict]
        """
    
        os.makedirs(os.path.dirname(self.config.HISTORY_FILE_PATH), exist_ok=True)

        fp = None
        try:
            fp = open(self.config.HISTORY_FILE_PATH, 'r')
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            rates = list()
        else:
            rates = json.load(fp)
        finally:
            if fp is not None:
                fp.close()
        return rates
    
    
    def save_rates(self, rates: dict[str, Any]):
        """
        Сохранить текущие курсы валют в кэш.
        
        :param rates: Словарь курсов
        :type rates: dict[str, Any]
        """

        current_rates = self.load_rates()
        pairs = current_rates.get('pairs', {})
        n_updated = 0

        for rate_key, rate_value in rates.items():
            rate_record = {'rate': rate_value.get('rate', 0),
                           'updated_at': rate_value.get('timestamp', ''),
                           'source': rate_value.get('source', 'Unknown')}
            
            if (datetime.fromisoformat(pairs.get(rate_key, {})\
                                       .get('updated_at', '2000-01-01T00:00:00Z')\
                                       .replace('Z', '+00:00')) <
                datetime.fromisoformat(rate_value\
                                       .get('timestamp', '2000-01-01T00:00:01Z')\
                                       .replace('Z', '+00:00'))):
                pairs[rate_key] = rate_record
                n_updated += 1
        
        current_time = datetime.now().isoformat()
        data = {'pairs': pairs,
                'source': 'ParserService',
                'last_refresh': current_time}
   
        tmp_file = f"{os.path.dirname(self.config.RATES_FILE_PATH)}.tmp"

        with open(tmp_file, 'w') as fp:
            json.dump(data, fp, indent=4, ensure_ascii=False)
        os.replace(tmp_file, self.config.RATES_FILE_PATH)

        return n_updated

    
    def save_exchange_rates(self, rates: dict[str, Any]):
        """
        Сохранить текущие курсы валют в историю.
        
        :param rates: Словарь курсов
        :type rates: dict[str, Any]
        """

        history = self.load_exchange_rates()
        history_ids = [h['id'] for h in history]

        for rate_key, rate_value in rates.items():
            from_currency, to_currency = rate_key.split('_')
            timestamp = rate_value.get('timestamp', '')

            if from_currency and to_currency and timestamp:
                record_id = f"{from_currency}_{to_currency}_{timestamp}"
                
                history_record = {
                    'id': record_id,
                    'from_currency': from_currency,
                    'to_currency': to_currency,
                    'rate': rate_value.get('rate', 0),
                    'timestamp': timestamp,
                    'source': rate_value.get('source', 'Unknown'),
                    'meta': rate_value.get('meta', {})
                }

                if record_id not in history_ids:
                    history.append(history_record)
        
        with open(self.config.HISTORY_FILE_PATH, 'w') as fp:
            json.dump(history, fp, indent=4, ensure_ascii=False)
