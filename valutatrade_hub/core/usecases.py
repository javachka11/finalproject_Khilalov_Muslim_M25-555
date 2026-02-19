import hashlib
import os
from datetime import datetime, timedelta
from typing import Optional

from valutatrade_hub.core.currencies import get_currency
from valutatrade_hub.core.exceptions import (
    InsufficientFundsError,
)
from valutatrade_hub.core.utils import (
    load_portfolios,
    load_users,
    save_portfolios,
    save_users,
)
from valutatrade_hub.decorators import log_action
from valutatrade_hub.infra.settings import config
from valutatrade_hub.parser_service.storage import RatesStorage
from valutatrade_hub.parser_service.updater import RatesUpdater


def register(username: str, password: str) -> None:
    """
    Создать нового пользователя.
    
    :param username: Имя пользователя
    :type username: str
    :param password: Пароль
    :type password: str
    """

    users = load_users(config.get('data_path', 'data/'))
    for user in users:
        if user['username'] == username:
            print(f"Имя пользователя '{username}' уже занято!")
            return None
        
    if len(password) < 4:
        raise ValueError('Пароль должен быть не короче 4 символов!')
    
    user_id = max([user['user_id'] for user in users], default=0) + 1
    
    salt = os.urandom(8).hex()
    hashed_password = (password + salt).encode('utf-8')
    hashed_password = hashlib.sha256(hashed_password).hexdigest()
    
    users.append({'user_id': user_id,
                  'username': username,
                  'hashed_password': hashed_password,
                  'salt': salt,
                  'registration_date': datetime.now().isoformat()})
    
    save_users(users, config.get('data_path', 'data/'))
    
    portfolios = load_portfolios(config.get('data_path', 'data/'))
    portfolios.append({'user_id': user_id,
                       'wallets': dict(USD=dict(currency_code='USD',
                                                balance=100))})
    save_portfolios(portfolios, config.get('data_path', 'data/'))
    
    hidden_password = '*'*len(password)
    
    print(f"Пользователь '{username}' зарегистрирован (id={user_id}). "
          f"Войдите: login --username {username} --password {hidden_password}")
    

def login(username: str, password: str) -> Optional[str]:
    """
    Залогиниться и зафиксировать текущую сессию.
    
    :param username: Имя пользователя
    :type username: str
    :param password: Пароль
    :type password: str
    :return: Имя залогированного пользователя (или None, если не найден)
    :rtype: int | None
    """

    users = load_users(config.get('data_path', 'data/'))
    for user in users:
        if user['username'] == username:
            verified = hashlib.sha256((password + user['salt']).encode('utf-8'))\
                .hexdigest() == user['hashed_password']

            if verified:
                print(f'Добро пожаловать, {username}!')
                return username
            else:
                print("Неверный пароль!")
                return None

    print(f"Пользователь '{username}' не найден!")
    return None


def show_portfolio(logged_name: Optional[str], base_currency: str = 'USD') -> None:
    """
    Показать все кошельки и итоговую стоимость в базовой валюте.
    
    :param logged_name: Имя пользователя
    :type logged_name: str
    :param base_currency: Базовая валюта
    :type base_currency: str
    """

    if logged_name is None:
        print('Сначала выполните login!')
        return None
    
    users = load_users(config.get('data_path', 'data/'))

    for user in users:
        if user['username'] == logged_name:
            user_id = user['user_id']
            break

    porfolios = load_portfolios(config.get('data_path', 'data/'))
    for portfolio in porfolios:
        if portfolio['user_id'] == user_id:
            if not portfolio['wallets']:
                print('Портфель пуст!')
                return None
            wallets = portfolio['wallets']
            break

    storage = RatesStorage()
    
    rates = storage.load_rates()
    total = 0
    info = f"Портфель пользователя '{logged_name}' (база: {base_currency}):\n"
    for cur in wallets.keys():
        exchange_rate = get_rate(cur, base_currency, rates)
        if exchange_rate is None:
            return None
        base_balance = exchange_rate*wallets[cur]['balance']
        info += f"- {cur}: {wallets[cur]['balance']:20.8f}  →  "
        info += f"{base_balance:20.8f} {base_currency}\n"
        total += base_balance
    info += "---------------------------------\n"
    info += f"ИТОГО: {total:.8f} {base_currency}"
    print(info)


@log_action("BUY", True)
def buy(logged_name: Optional[str],
        currency: str,
        amount: float) -> Optional[dict[str, float]]:
    """
    Купить валюту.
    
    :param logged_name: Имя пользователя
    :type logged_name: str
    :param currency: Код валюты
    :type currency: str
    :param amount: Количество валюты
    :type amount: float
    """

    if logged_name is None:
        print('Сначала выполните login!')
        return None
    
    exchange_rate = get_rate(currency, 'USD')
    if exchange_rate is None:
        return None
    
    if amount <= 0:
        raise ValueError('Количество валюты должно быть положительным числом!')
    
    users = load_users(config.get('data_path', 'data/'))

    for user in users:
        if user['username'] == logged_name:
            user_obj = user
            break

    porfolios = load_portfolios(config.get('data_path', 'data/'))
    for portfolio in porfolios:
        if portfolio['user_id'] == user_obj['user_id']:
            portfolio_obj = portfolio
            break
    
    if exchange_rate*amount > portfolio_obj['wallets']['USD']['balance']:
        raise InsufficientFundsError(portfolio_obj['wallets']['USD']['balance'],
                                     exchange_rate*amount,
                                     'USD')

    if currency not in portfolio_obj['wallets'].keys():
        prev_balance = 0
        portfolio_obj['wallets'][currency] = dict(currency_code=currency,
                                                  balance=amount)
    else:
        prev_balance = portfolio_obj['wallets'][currency]['balance']
        portfolio_obj['wallets'][currency]['balance'] += amount

    
    portfolio_obj['wallets']['USD']['balance'] -= exchange_rate*amount

    save_portfolios(porfolios, config.get('data_path', 'data/'))
    transaction = {'before': prev_balance,
                   'now': portfolio_obj['wallets'][currency]['balance'],
                   'rate': exchange_rate}
    return transaction


@log_action("SELL", True)
def sell(logged_name: Optional[str],
         currency: str,
         amount: float) -> Optional[dict[str, float]]:
    """
    Продать валюту.
    
    :param logged_name: Имя пользователя
    :type logged_name: str
    :param currency: Код валюты
    :type currency: str
    :param amount: Количество валюты
    :type amount: float
    """

    if logged_name is None:
        print('Сначала выполните login!')
        return None
    
    exchange_rate = get_rate(currency, 'USD')
    if exchange_rate is None:
        return None
    
    if amount <= 0:
        raise ValueError('Количество валюты должно быть положительным числом!')
    
    users = load_users(config.get('data_path', 'data/'))

    for user in users:
        if user['username'] == logged_name:
            user_obj = user
            break

    porfolios = load_portfolios(config.get('data_path', 'data/'))
    for portfolio in porfolios:
        if portfolio['user_id'] == user_obj['user_id']:
            portfolio_obj = portfolio
            break

    if currency not in portfolio_obj['wallets'].keys():
        print(f"У вас нет кошелька '{currency}'. Добавьте валюту: "
              "она создаётся автоматически при первой покупке.")
        return None
    
    if amount > portfolio_obj['wallets'][currency]['balance']:
        raise InsufficientFundsError(portfolio_obj['wallets'][currency]['balance'],
                                     amount,
                                     currency)
    
    prev_balance = portfolio_obj['wallets'][currency]['balance']
    portfolio_obj['wallets'][currency]['balance'] -= amount
    portfolio_obj['wallets']['USD']['balance'] += exchange_rate*amount
    
    save_portfolios(porfolios, config.get('data_path', 'data/'))
    transaction = {'before': prev_balance,
                   'now': portfolio_obj['wallets'][currency]['balance'],
                   'rate': exchange_rate}
    return transaction


def get_rate(from_currency: str,
             to_currency: str,
             rates: Optional[dict] = None,
             display: bool = False) -> Optional[float]:
    """
    Получить текущий курс одной валюты к другой.
    
    :param from_currency: Исходная валюта
    :type from_currency: str
    :param to_currency: Целевая валюта
    :type to_currency: str
    :param rates: Словарь курсов (чтобы не подгружать каждый раз)
    :type rates: Optional[dict]
    :param display: Выводить ли информацию в консоль
    :type display: bool
    :return: Текущий курс
    :rtype: float | None
    """

    if not from_currency or not to_currency:
        raise ValueError('Код валюты пуст!')

    if not from_currency.isupper() or not to_currency.isupper():
        raise ValueError('Код валюты должен состоять из заглавных букв!')
    
    if from_currency == to_currency:
        return 1

    storage = RatesStorage()

    if rates is None:
        rates = storage.load_rates()

    from_valuta = get_currency(from_currency)
    to_valuta = get_currency(to_currency)
    
    exchange = rates.get('pairs', {}).get(f'{from_valuta.code}_{to_valuta.code}')
    if exchange is None:
        print(f"Курс {from_currency}→{to_currency} недоступен. "
              "Повторите попытку позже.")
        return None
    
    now_timestamp = datetime.now()
    if (datetime.fromisoformat(rates.get('last_refresh', '2000-01-01T00:00:00Z')\
                               .replace('Z', '')) < 
        (now_timestamp - timedelta(seconds=config.get('rates_ttl_seconds', 300)))):
        print('Курсы валют устарели! Обновите курсы с помощью команды update-rates.')
        return None
    
    now_rate = exchange['rate']
    
    if display:
        info = f"Курс {from_currency} → {to_currency}: {exchange['rate']:.8f} "
        info += "(обновлено: "
        info += f"{datetime.fromisoformat(exchange['updated_at'].replace('Z', ''))})\n"
        info += f"Обратный курс {to_currency} → {from_currency}: "
        info += f"{1/exchange['rate']:.8f}"
        print(info)

    return now_rate
    

def update_rates(source: Optional[str] = None) -> None:
    """
    Обновить текущий курс валют.
    
    :param source: Тип валют для обновления (crypto или fiat)
    :type source: Optional[str]
    """

    updater = RatesUpdater()
    updater.run_update(source)


def show_rates(currency: Optional[str] = None,
               top: Optional[int] = None,
               base: str = 'USD') -> None:
    """
    Отобразить текущий курс валют.
    
    :param currency: Код валюты
    :type currency: Optional[str]
    :param top: Топ курсов
    :type top: Optional[int]
    :param base: Код базовый валюты
    :type base: str
    """
    
    if currency is not None and len(currency) == 0:
        raise ValueError("Параметр '--currency' пуст!")
    
    if not base:
        raise ValueError("Параметр '--base' пуст!")

    if currency is not None and not currency.isupper():
        raise ValueError("Параметр '--currency' должен состоять из заглавных букв!")
    
    if not base.isupper():
        raise ValueError("Параметр '--base' должен состоять из заглавных букв!")
    
    if currency is not None:
        valuta = get_currency(currency)
    else:
        valuta = None
    base_valuta = get_currency(base)
    
    if top is not None and top <= 0:
        raise ValueError("Параметр '--top' не может быть отрицательным!")
    
    
    storage = RatesStorage()
    rates = storage.load_rates()
    pairs = rates.get('pairs', {})

    if not pairs:
        raise ValueError("Локальный кэш курсов пуст. "\
                         "Выполните 'update-rates', чтобы загрузить данные.")
    
    result = []
    now_timestamp = datetime.now()

    for rate_key, rate_value in pairs.items():
        from_currency, to_currency = rate_key.split('_')
        if to_currency == base_valuta.code:
            if (datetime.fromisoformat(rates\
                                       .get('last_refresh', '2000-01-01T00:00:00Z')\
                                       .replace('Z', '')) < 
               (now_timestamp - timedelta(seconds=config\
                                          .get('rates_ttl_seconds', 300)))):
                print("Курсы валют устарели! "\
                      "Обновите курсы с помощью команды update-rates.")
                return None
            result.append((from_currency, to_currency, rate_value['rate']))
    
    result = sorted(result, key=lambda x: x[2], reverse=True)

    if valuta is not None:
        result = [rate for rate in result if rate[0] == valuta.code]
        if not result:
            raise ValueError(f"Курс для '{valuta.code}' не найден в кеше.")

    if top is not None:
        result = result[:top]

    info = f"Rates from cache (updated at {rates.get('last_refresh', '<unknown>')}):\n"
    info += '\n'.join([f"- {rate[0]}_{rate[1]}: {rate[2]:.8f}" for rate in result])
    print(info)
