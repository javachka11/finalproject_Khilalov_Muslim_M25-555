import hashlib
import os
from datetime import datetime
from typing import Optional

from valutatrade_hub.core.exceptions import (
    InsufficientFundsError,
)
from valutatrade_hub.core.utils import (
    load_portfolios,
    load_rates,
    load_users,
    save_portfolios,
    save_users,
)


def register(username: str, password: str) -> None:
    """
    Создать нового пользователя.
    
    :param username: Имя пользователя
    :type username: str
    :param password: Пароль
    :type password: str
    """

    users = load_users()
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
    
    save_users(users)
    
    portfolios = load_portfolios()
    portfolios.append({'user_id': user_id,
                       'wallets': dict(USD=dict(currency_code='USD',
                                                balance=100))})
    save_portfolios(portfolios)
    
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

    users = load_users()
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


def show_portfolio(logged_name: str, base_currency: str = 'USD') -> None:
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
    
    users = load_users()

    for user in users:
        if user['username'] == logged_name:
            user_id = user['user_id']
            break

    porfolios = load_portfolios()
    for portfolio in porfolios:
        if portfolio['user_id'] == user_id:
            if not portfolio['wallets']:
                print('Портфель пуст!')
                return None
            wallets = portfolio['wallets']
            break
    
    rates = load_rates()
    total = 0
    info = f"Портфель пользователя '{logged_name}' (база: {base_currency}):\n"
    for cur in wallets.keys():
        exchange_rate = get_rate(cur, base_currency, rates)
        if exchange_rate is None:
            return None
        base_balance = exchange_rate*wallets[cur]['balance']
        info += f"- {cur}: {wallets[cur]['balance']:12.8f}  →  "
        info += f"{base_balance:12.8f} {base_currency}\n"
        total += base_balance
    info += "---------------------------------\n"
    info += f"ИТОГО: {total:.8f} {base_currency}"
    print(info)


def buy(logged_name: str, currency: str, amount: float) -> None:
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
    
    if not currency:
        raise ValueError('Код валюты пуст!')

    if not currency.isupper():
        raise ValueError('Код валюты должен состоять из заглавных букв!')
    
    amount = float(amount)
    if amount <= 0:
        raise ValueError('Количество валюты должно быть положительным числом!')
    
    users = load_users()

    for user in users:
        if user['username'] == logged_name:
            user_obj = user
            break

    porfolios = load_portfolios()
    for portfolio in porfolios:
        if portfolio['user_id'] == user_obj['user_id']:
            portfolio_obj = portfolio
            break
    
    exchange_rate = get_rate(currency, 'USD')
    if exchange_rate is None:
        return None
    
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

    info = f"Покупка выполнена: {amount:.8f} {currency} по курсу {exchange_rate:.8f} "
    info += f"{currency} -> USD\n"
    info += "Изменения в портфеле:\n"
    info += f"- {currency}: было {prev_balance:.8f} → "
    info += f"стало {portfolio_obj['wallets'][currency]['balance']:.8f}\n"
    info += f"Оценочная стоимость покупки: {exchange_rate*amount:.8f} USD"
    print(info)

    save_portfolios(porfolios)


def sell(logged_name: str, currency: str, amount: float) -> None:
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
    
    if not currency:
        raise ValueError('Код валюты пуст!')

    if not currency.isupper():
        raise ValueError('Код валюты должен состоять из заглавных букв!')
    
    amount = float(amount)
    
    if amount <= 0:
        raise ValueError('Количество валюты должно быть положительным числом!')
    
    users = load_users()

    for user in users:
        if user['username'] == logged_name:
            user_obj = user
            break

    porfolios = load_portfolios()
    for portfolio in porfolios:
        if portfolio['user_id'] == user_obj['user_id']:
            portfolio_obj = portfolio
            break
    
    exchange_rate = get_rate(currency, 'USD')
    if exchange_rate is None:
        return None

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

    info = f"Продажа выполнена: {amount:.8f} {currency} по курсу {exchange_rate:.8f} "
    info += f"{currency} -> USD\n"
    info += "Изменения в портфеле:\n"
    info += f"- {currency}: было {prev_balance:.8f} → "
    info += f"стало {portfolio_obj['wallets'][currency]['balance']:.8f}\n"
    info += f"Оценочная выручка: {exchange_rate*amount:.8f} USD"
    print(info)
    
    save_portfolios(porfolios)
    


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

    if rates is None:
        rates = load_rates()
    
    exchange = rates.get(f'{from_currency}_{to_currency}')
    if exchange is None:
        print(f"Курс {from_currency}→{to_currency} недоступен. "
              "Повторите попытку позже.")
        return None
    
    if display:
        info = f"Курс {from_currency}→{to_currency}: {exchange['rate']:.8f} "
        info += f"(обновлено: {datetime.fromisoformat(exchange['updated_at'])})\n"
        info += f"Обратный курс {to_currency}→{from_currency}: {1/exchange['rate']:.8f}"
        print(info)

    return exchange['rate']
    