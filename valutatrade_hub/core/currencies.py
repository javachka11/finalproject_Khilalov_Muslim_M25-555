from abc import ABC, abstractmethod
from typing import Optional


class Currency(ABC):
    """
    Абстрактный класс для валюты.
    """

    def __init__(self, code: str, name: str) -> None:
        """
        Создать валюту.
        
        :param code: ISO-код или общепринятый тикер ("USD", "EUR", "BTC", "ETH")
        :type code: str
        :param name: Человекочитаемое имя (например, “US Dollar”, “Bitcoin”)
        :type name: str
        """

        if not code.isupper():
            raise ValueError('Код валюты должен состоять из заглавных букв!')
        if len(code) < 2 or len(code) > 5:
            raise ValueError('Код валюты должен состоять из 2-5 символов!')
        if ' ' in code:
            raise ValueError('Код валюты не может включать в себя пробелы!')
        
        
        if not name:
            raise ValueError('Название валюты не может быть пустым!')
        
        self._code = code
        self._name = name


    @property
    def code(self) -> str:
        """
        Геттер.
        
        :return: Код валюты
        :rtype: str
        """

        return self._code


    @property
    def name(self) -> str:
        """
        Геттер.
        
        :return: Название валюты
        :rtype: str
        """

        return self._name
    

    @abstractmethod
    def get_display_info(self) -> str:
        """
        Получить строковое представление для UI/логов.
        
        :return: Информация о валюте
        :rtype: str
        """

        pass


class FiatCurrency(Currency):
    """
    Фиатная валюта.
    """

    def __init__(self,
                 code: str,
                 name: str,
                 issuing_country: str) -> None:
        """
        Создать фиатную валюту.
        
        :param code: Код валюты
        :type code: str
        :param name: Название валюты
        :type name: str
        :param issuing_country: Страна/зона эмиссии
        :type issuing_country: str
        """

        super().__init__(code, name)
        self._issuing_country = issuing_country


    @property
    def issuing_country(self) -> str:
        """
        Геттер.
        
        :return: Страна/зона эмиссии
        :rtype: str
        """

        return self._issuing_country
    

    def get_display_info(self) -> str:
        """
        Получить строковое представление для UI/логов.
        
        :return: Информация о валюте
        :rtype: str
        """

        info = f"[FIAT] {self._code} — {self._name} "
        info += f"(Issuing: {self._issuing_country})"
        return info

   
class CryptoCurrency(Currency):
    """
    Криптовалюта.
    """

    def __init__(self,
                 code: str,
                 name: str,
                 algorithm: str,
                 market_cap: float) -> None:
        """
        Создать криптовалюту.
        
        :param code: Код валюты
        :type code: str
        :param name: Название валюты
        :type name: str
        :param algorithm: Алгоритм шифрования
        :type algorithm: str
        :param market_cap: Капитализация криптовалюты
        :type market_cap: float
        """

        super().__init__(code, name)
        if not isinstance(market_cap, (int, float)):
            raise ValueError('Капитализация криптовалюты должна быть вещественным числом')
        self._algorithm = algorithm
        self._market_cap = market_cap


    @property
    def algorithm(self) -> str:
        """
        Геттер.
        
        :return: Алгоритм шифрования
        :rtype: str
        """

        return self._algorithm
    

    @property
    def market_cap(self) -> float:
        """
        Геттер.
        
        :return: Капитализация
        :rtype: float
        """

        return self._market_cap
    

    def get_display_info(self) -> str:
        """
        Получить строковое представление для UI/логов.
        
        :return: Информация о валюте
        :rtype: str
        """
        
        info = f"[CRYPTO] {self._code} — {self._name} "
        info += f"(Algo: {self._algorithm}, MCAP: {self._market_cap:.2e})"
        return info
    
    

def get_currency(code: str) -> Optional[Currency]:
    if code == 'USD':
        return FiatCurrency('USD', 'Us Dollar', 'United States')
    elif code == 'EUR':
        return FiatCurrency('EUR', 'Euro', 'Eurozone')
    elif code == 'BTC':
        return CryptoCurrency('BTC', 'Bitcoin', 'SHA-256', 1159299359324.63)
    elif code == 'ETH':
        return CryptoCurrency('ETH', 'Ethereum', 'Ethash', 208687511047)
    else:
        print('Неверный код валюты!')
