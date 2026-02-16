import shlex

from valutatrade_hub.core.exceptions import (
    ApiRequestError,
    CurrencyNotFoundError,
    InsufficientFundsError,
)
from valutatrade_hub.core.usecases import (
    buy,
    get_rate,
    login,
    register,
    sell,
    show_portfolio,
)


def show_info():
    info = "***Интерфейс платформы:***\n"
    info += "<command> register --username <имя> --password "
    info += "<пароль> - зарегистрировать пользователя\n"
    info += "<command> login --username <имя> --password "
    info += "<пароль> - залогиниться под конкретным пользователем\n"
    info += "<command> show-portfolio - "
    info += "отобразить портфель пользователя (в долларах)\n"
    info += "<command> show-portfolio --base <код_валюты> - "
    info += "отобразить портфель пользователя (в базовой валюте)\n"
    info += "<command> buy --currency <код_валюты> --amount "
    info += "<количество_валюты> - купить валюту\n"
    info += "<command> sell --currency <код_валюты> --amount "
    info += "<количество_валюты> - продать валюту\n"
    info += "<command> get-rate --from <исх_валюта> --to "
    info += "<цел_валюта> - получить текущий курс валюты\n"
    info += "<command> help|info - отобразить справку\n"
    info += "<command> quit|exit - выйти из программы"
    print(info)


def run():
    logged_username = None
    while True:
        if logged_username is None:
            command = input('\n> ')
        else:
            command = input(f'\n{logged_username}> ')


        sh = shlex.shlex(command)
        sh.wordchars += '-.'
        args = list(sh)

        try:
            match args:
                case ['register', '--username', username, '--password', password]:
                    register(username, password)
                case ['login', '--username', username, '--password', password]:
                    logged_username = login(username, password)
                case ['show-portfolio', '--base', currency]:
                    show_portfolio(logged_username, currency)
                case ['show-portfolio']:
                    show_portfolio(logged_username)
                case ['buy', '--currency', currency, '--amount', amount]:
                    buy(logged_username, currency, amount)
                case ['sell', '--currency', currency, '--amount', amount]:
                    sell(logged_username, currency, amount)
                case ['get-rate', '--from', from_currency, '--to', to_currency]:
                    get_rate(from_currency, to_currency, None, True)
                case ['help'|'info']:
                    show_info()
                case ['quit'|'exit']:
                    return None
                case _:
                    print('Некорректная команда!')
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
        except InsufficientFundsError as e:
            print(e)
        except CurrencyNotFoundError as e:
            print(f'{e} Введите help get-rate.')
        except ApiRequestError as e:
            print(f'{e} Проверьте сеть или повторите позже.')
        except Exception as e:
            print(f'Непредвиденная ошибка: {e}')