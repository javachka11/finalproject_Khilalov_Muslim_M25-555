import os
import hashlib
from datetime import datetime
from valutatrade_hub.core.utils import load_users, save_users, load_portfolios, save_portfolios, load_rates
from typing import Optional


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
        print('Пароль должен быть не короче 4 символов!')
        return None
    
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
        print('Ошибка валидации: код валюты пуст!')
        return None

    if not currency.isupper():
        print('Ошибка валидации: код валюты должен состоять из заглавных букв!')
        return None
    
    try:
        amount = float(amount)
    except ValueError:
        print('Ошибка валидации: количество валюты должно быть вещественным числом!')
        return None
    
    if amount <= 0:
        print('Ошибка валидации: количество валюты должно быть положительным числом!')
        return None
    
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
        print("На кошельке 'USD' не хватает средств, для покупки валюты!")
        return None

    if currency not in portfolio_obj['wallets'].keys():
        portfolio_obj['wallets'][currency] = dict(currency_code=currency,
                                              balance=amount)
    else:
        portfolio_obj['wallets'][currency]['balance'] += amount
    
    portfolio_obj['wallets']['USD']['balance'] -= exchange_rate*amount

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
        print('Ошибка валидации: код валюты пуст!')
        return None

    if not from_currency.isupper() or not to_currency.isupper():
        print('Ошибка валидации: код валюты должен состоять из заглавных букв!')
        return None
    
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
    