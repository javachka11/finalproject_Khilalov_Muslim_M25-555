from datetime import datetime
from typing import Optional

from valutatrade_hub.core.exceptions import ApiRequestError
from valutatrade_hub.parser_service.api_clients import (
    CoinGeckoClient,
    ExchangeRateApiClient,
)
from valutatrade_hub.parser_service.config import ParserConfig
from valutatrade_hub.parser_service.storage import RatesStorage


class RatesUpdater:
    """
    Точка входа для обновления курса валют.
    """
    
    def __init__(self):
        """
        Инициализировать класс.
        """

        self.config = ParserConfig()
        
        self.coingecko = CoinGeckoClient(self.config)
        self.exchangerate = ExchangeRateApiClient(self.config)
    
        self.storage = RatesStorage()

    
    def run_update(self, source: Optional[str] = None) -> None:
        """
        Запустить обновление курсов валют.
        
        :param source: Клиент
        :type source: Optional[str]
        """

        print("INFO: Starting rates update...")
        
        all_rates = {}
        
        if source is None or source == 'coingecko':
            try:
                coingecko_rates = self.coingecko.fetch_rates()
                all_rates.update(coingecko_rates)
                    
                print(f"INFO: Fetching from CoinGecko... "
                      f"OK ({len(coingecko_rates)} rates)")
            except ApiRequestError as e:
                print(f"ERROR: Failed to fetch from CoinGecko: {e.reason}")
            
        if source is None or source == 'exchangerate':
            try:
                exchangerate_rates = self.exchangerate.fetch_rates()
                all_rates.update(exchangerate_rates)
 
                print(f"INFO: Fetching from ExchangeRate-API... "
                      f"OK ({len(exchangerate_rates)} rates)")
            except ApiRequestError as e:
                print(f"ERROR: Failed to fetch from ExchangeRate-API: {e.reason}")
                    
        if all_rates:
            print(f"INFO: Writing {len(all_rates)} rates to data/rates.json...")
            n_updated = self.storage.save_rates(all_rates)
            self.storage.save_exchange_rates(all_rates)
            now = datetime.now().isoformat()
            print(f"Update successful. Total rates updated: {n_updated}. "
                  f"Last refresh: {now}")
            
            return None
        else:
            print("Update completed with errors.")
            raise ApiRequestError("Курсы не были получены с клиентских API.")
