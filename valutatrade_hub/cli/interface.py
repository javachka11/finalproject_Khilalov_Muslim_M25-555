import shlex
from valutatrade_hub.core.usecases import register

def run():
    while True:
        command = input('> ')

        sh = shlex.shlex(command, punctuation_chars='=()')
        args = list(sh)

        match args:
            case ['register', '--username', username, '--password', password]:
                register(username, password)
            case ['quit']:
                return None
            case _:
                print('Некорректная команда!')