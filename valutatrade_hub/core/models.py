from datetime import datetime
import os
import hashlib

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
        Регистрирует пользователя в системе.
        
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

        info = "Информация о пользователе:\n"
        info += f"ID: {self._user_id}\n"
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
            raise TypeError('Пароль должен быть строкой!')
        
        if len(new_password) < 4:
            raise ValueError('Пароль не должен быть короче 4 символов!')
        
        new_salt = os.urandom(8)
        new_hashed_password = new_password.encode('utf-8') + new_salt

        self._hashed_password = hashlib.sha256(new_hashed_password).hexdigest()
        self._salt = new_salt.hex()
    

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
        Сеттер, вызывается при смене имени.
        
        :param new_name: Новое имя
        :type new_name: str
        """

        if not isinstance(new_name, str):
            raise TypeError('Имя пользователя должно быть строкой!')
        
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
    
    