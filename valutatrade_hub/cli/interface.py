import shlex
from valutatrade_hub.core.usecases import register, login, show_portfolio, buy, get_rate

def run():
    logged_username = None
    while True:
        if logged_username is None:
            command = input('\n> ')
        else:
            command = input(f'\n{logged_username}> ')


        sh = shlex.shlex(command)
        sh.wordchars += '-'
        args = list(sh)

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
            case ['get-rate', '--from', from_currency, '--to', to_currency]:
                get_rate(from_currency, to_currency, None, True)
            case ['quit'|'exit']:
                return None
            case _:
                print('Некорректная команда!')