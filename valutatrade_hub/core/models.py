from datetime import datetime
import os
import hashlib
from typing import Optional


class User:
    """
    Пользователь системы.
    """

    def __init__(self,
                 user_id: int,
                 username: str,
                 hashed_password: str,
                 salt: str,
                 registration_date: datetime) -> None:
        """
        Зарегистрировать пользователя в системе.
        
        :param user_id: ID
        :type user_id: int
        :param username: Имя
        :type username: str
        :param hashed_password: Пароль (в хэш-форме)
        :type hashed_password: str
        :param salt: Соль
        :type salt: str
        :param registration_date: Дата регистрации
        :type registration_date: datetime
        """

        self._user_id = user_id
        self._username = username
        self._hashed_password = hashed_password
        self._salt = salt
        self._registration_date = registration_date


    def get_user_info(self) -> str:
        """
        Получить информацию о пользователе.
        
        :return: Строка с ID, именем и датой регистрации пользователя
        :rtype: str
        """

        info = f"ID: {self._user_id}\n"
        info += f"Имя: {self._username}\n"
        info += f"Дата регистрации: {self._registration_date}\n"
        return info


    def change_password(self, new_password: str) -> None:
        """
        Сменить пароль.
        
        :param new_password: Новый пароль
        :type new_password: str
        """

        if not isinstance(new_password, str):
            raise TypeError('Некорректный тип данных для пароля!')
        
        if len(new_password) < 4:
            raise ValueError('Пароль не должен быть короче 4 символов!')
        
        new_salt = os.urandom(8)
        new_hashed_password = new_password.encode('utf-8') + new_salt

        self._hashed_password = hashlib.sha256(new_hashed_password).hexdigest()
        self._salt = new_salt.hex()


    def verify_password(self, password: str) -> bool:
        """
        Проверить введённый пароль на совпадение.
        
        :param password: Введённый пароль
        :type password: str
        :return: Флаг верификации пароля
        :rtype: bool
        """

        verified = hashlib.sha256((password + self._salt).encode('utf-8'))\
            .hexdigest() == self._hashed_password
        return verified
    

    @property
    def user_id(self) -> int:
        """
        Геттер.
        
        :return: ID
        :rtype: int
        """

        return self._user_id
    

    @property
    def username(self) -> str:
        """
        Геттер.
        
        :return: Имя
        :rtype: str
        """

        return self._username
    

    @username.setter
    def username(self, new_name: str) -> None:
        """
        Сеттер для имени.
        
        :param new_name: Новое имя
        :type new_name: str
        """

        if not isinstance(new_name, str):
            raise TypeError('Некорректный тип данных для имени пользователя!')
        
        if not new_name:
            raise ValueError('Имя пользователя не может быть пустым!')
        
        self._username = new_name


    @property
    def registration_date(self) -> datetime:
        """
        Геттер.
        
        :return: Дата регистрации
        :rtype: datetime
        """

        return self._registration_date
    

class Wallet:
    """
    Кошелёк пользователя для одной конкретной валюты.
    """

    def __init__(self,
                 currency_code: str,
                 balance: float = 0.0) -> None:
        """
        Создать кошелёк.
        
        :param currency_code: Код валюты
        :type currency_code: str
        :param balance: Баланс в данной валюте
        :type balance: float
        """

        self.currency_code = currency_code
        self._balance = balance


    def deposit(self, amount: float) -> None:
        """
        Пополнить баланс.
        
        :param amount: Сумма пополнения
        :type amount: float
        """

        if not isinstance(amount, (int, float)):
            raise TypeError('Некорректный тип данных для суммы пополнения баланса!')
        
        if amount <= 0:
            raise ValueError('Сумма пополнения баланса должна быть больше нуля!')
        
        self._balance += amount


    def get_balance_info(self) -> str:
        """
        Получить информацию о текущем балансе.
        
        :return: Строка с текущим балансом и кодом его валюты
        :rtype: str
        """

        info = f"Текущий баланс: {self._balance:.2f} {self.currency_code}"
        return info
        

    @property
    def balance(self) -> float:
        """
        Геттер.
        
        :return: Текущий баланс
        :rtype: float
        """

        return self._balance
    

    @balance.setter
    def balance(self, new_balance: float) -> None:
        """
        Сеттер для баланса.
        
        :param new_balance: Новый баланс
        :type new_balance: float
        """

        if not isinstance(new_balance, (int, float)):
            raise TypeError('Некорректный тип данных для баланса!')
        
        if new_balance < 0:
            raise ValueError('Баланс не может быть отрицательным!')
        
        self._balance = new_balance


    def withdraw(self, amount: float) -> None:
        """
        Снять средства с баланса (если он позволяет).
        
        :param amount: Сумма снятия
        :type amount: float
        """

        if not isinstance(amount, (int, float)):
            raise TypeError('Некорректный тип данных для суммы снятия баланса!')
        
        if amount <= 0:
            raise ValueError('Сумма снятия баланса должна быть больше нуля!')
        
        if amount > self._balance:
            raise ValueError('На балансе недостаточно средств!')
        
        self._balance -= amount

    
class Portfolio:
    """
    Портфель для управления всеми кошельками одного пользователя.
    """

    def __init__(self,
                 user_id: int,
                 wallets: dict[str, Wallet]) -> None:
        """
        Создать портфель.
        
        :param user_id: ID пользователя
        :type user_id: int
        :param wallets: Словарь кошельков (ключ - код валюты)
        :type wallets: dict[str, Wallet]
        """

        self._user_id = user_id
        self._wallets = wallets

    
    def add_currency(self, currency_code: str) -> None:
        """
        Добавить новый кошелёк (если его ещё нет).
        
        :param currency_code: Код валюты
        :type currency_code: str
        """

        if currency_code not in self._wallets.keys():
            self._wallets[currency_code] = Wallet(currency_code)
        else:
            print(f'Кошелёк с валютой {currency_code} уже существует в портфеле'
                  f'пользователя {self._user_id}!')
    
    
    def get_total_value(self, base_currency: str = 'USD') -> float:
        """
        Возвращает общую стоимость всех валют пользователя
        в указанной базовой валюте.

        :param base_currency: Код базовой валюты
        :type base_currency: str
        :return: Общая стоимость
        :rtype: float
        """

        exchange_rates = {'USD': 1,
                          'EUR': 0.84,
                          'RUB': 77.18,
                          'BTC': 0.000014}
        
        total = sum((exchange_rates[base_currency] / exchange_rates[cur])*
                         self._wallets[cur].balance for cur in self._wallets.keys())
        
        return total


    @property
    def user_id(self) -> int:
        """
        Геттер.
        
        :return: ID пользователя
        :rtype: int
        """

        return self._user_id
    
    @property
    def wallets(self) -> dict[str, Wallet]:
        """
        Геттер.
        
        :return: Копия словаря кошельков
        :rtype: dict[str, Wallet]
        """

        return self._wallets.copy()
    
    
    def get_wallet(self, currency_code: str) -> Optional[Wallet]:
        """
        Получить кошелёк по коду валюты.
        
        :param currency_code: Код валюты
        :type currency_code: str
        :return: Кошелёк (или None при его отсутствии)
        :rtype: Wallet | None
        """

        return self._wallets.get(currency_code)
    

    