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


def show_info(key='all'):
    info = dict()

    info['register'] = "<command> register --username <имя> --password "\
                       "<пароль> - зарегистрировать пользователя"

    info['login'] = "<command> login --username <имя> --password "\
                    "<пароль> - залогиниться под конкретным пользователем"
    
    info['show-portfolio'] = "<command> show-portfolio - "\
                             "отобразить портфель пользователя (в долларах)\n"\
                             "<command> show-portfolio --base <код_валюты> - "\
                             "отобразить портфель пользователя (в базовой валюте)"
    
    info['buy'] = "<command> buy --currency <код_валюты> --amount "\
                  "<количество_валюты> - купить валюту"
    
    info['sell'] = "<command> sell --currency <код_валюты> --amount "\
                   "<количество_валюты> - продать валюту"
    
    info['get-rate'] = "<command> get-rate --from <исх_валюта> --to "\
                       "<цел_валюта> - получить текущий курс валюты"
    
    info['info'] = "<command> info - отобразить справку"
    info['help'] = "<command> help <команда> - отобразить справку для команды"
    info['quit'] = "<command> quit - выйти из программы"

    info['all'] = '\n'.join(info.values())

    guide = info.get(key)
    if guide is None:
        print(f'Для команды {key} справка не найдена.')
    else:
        print(info[key])


def run():
    print('Введите info для отображения интерфейса, quit - для выхода из программы.')
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
                    buy(logged_username, currency, float(amount))
                case ['sell', '--currency', currency, '--amount', amount]:
                    sell(logged_username, currency, float(amount))
                case ['get-rate', '--from', from_currency, '--to', to_currency]:
                    get_rate(from_currency, to_currency, None, True)
                case ['info']:
                    show_info()
                case ['help', command]:
                    show_info(command)
                case ['quit']:
                    print('Выход из программы.')
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