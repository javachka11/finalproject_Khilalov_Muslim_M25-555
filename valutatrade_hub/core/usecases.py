import os
import hashlib
from datetime import datetime
from valutatrade_hub.core.utils import load_users, save_users, load_portfolios, save_portfolios


def register(username: str, password: str) -> None:
    users = load_users()
    for user in users:
        if user['username'] == username:
            print(f"Имя пользователя '{username}' уже занято!")
            return None
        
    if len(password) < 4:
        print('Пароль должен быть не короче 4 символов!')
        return None
    
    user_id = max([user['user_id'] for user in users], default=0) + 1
    
    salt = os.urandom(8)
    hashed_password = password.encode('utf-8') + salt
    hashed_password = hashlib.sha256(hashed_password).hexdigest()
    
    users.append({'user_id': user_id,
                  'username': username,
                  'hashed_password': hashed_password,
                  'salt': salt.hex(),
                  'registration_date': datetime.now().isoformat()})
    
    save_users(users)
    
    portfolios = load_portfolios()
    portfolios.append({'user_id': user_id,
                       'wallets': dict()})
    save_portfolios(portfolios)
    
    hidden_password = '*'*len(password)
    
    print(f"Пользователь '{username}' зарегистрирован (id={user_id}). "
          f"Войдите: login --username {username} --password {hidden_password}")
    