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
    show_rates,
    update_rates,
)
from valutatrade_hub.logging_config import run_logging


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

    run_logging()
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
                    result = buy(logged_username, currency, float(amount))
                    if result is not None:
                        info = f"Покупка выполнена: {float(amount):.8f} {currency} "\
                               f"по курсу {result['rate']:.8f} "\
                               f"{currency} -> USD\n"\
                               f"Изменения в портфеле:\n"\
                               f"- {currency}: было {result['before']:.8f} → "\
                               f"стало {result['now']:.8f}\n"\
                               f"Оценочная стоимость покупки: "\
                               f"{result['rate']*float(amount):.8f} USD"
                        print(info)
                case ['sell', '--currency', currency, '--amount', amount]:
                    result = sell(logged_username, currency, float(amount))
                    if result is not None:
                        info = f"Продажа выполнена: {float(amount):.8f} {currency} "\
                               f"по курсу {result['rate']:.8f} "\
                               f"{currency} -> USD\n"\
                               f"Изменения в портфеле:\n"\
                               f"- {currency}: было {result['before']:.8f} → "\
                               f"стало {result['now']:.8f}\n"\
                               f"Оценочная выручка: "\
                               f"{result['rate']*float(amount):.8f} USD"
                        print(info)
                case ['get-rate', '--from', from_currency, '--to', to_currency]:
                    get_rate(from_currency, to_currency, None, True)
                case ['update-rates', 'crypto']:
                    update_rates('crypto')
                case ['update-rates', 'fiat']:
                    update_rates('fiat')
                case ['update-rates']:
                    update_rates()
                case ['show-rates', '--currency', currency,
                                    '--top', top,
                                    '--base', base]:
                    show_rates(currency=currency,
                               top=int(top),
                               base=base)
                case ['show-rates', '--currency', currency,
                                    '--top', top]:
                    show_rates(currency=currency,
                               top=int(top))
                case ['show-rates', '--currency', currency,
                                    '--base', base]:
                    show_rates(currency=currency,
                               base=base)
                case ['show-rates', '--top', top,
                                    '--base', base]:
                    show_rates(top=int(top),
                               base=base)
                case ['show-rates', '--currency', currency]:
                    show_rates(currency=currency)
                case ['show-rates', '--top', top]:
                    show_rates(top=int(top))
                case ['show-rates', '--base', base]:
                    show_rates(base=base)
                case ['show-rates']:
                    show_rates()
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