import functools
import logging
from typing import Any, Callable


def log_action(action: str, verbose: bool = False) -> Callable:
    """
    Фабрика декораторов для логирования.

    :param action: Выполняемое действие
    :type action: str
    :param verbose: Подробный вывод
    :type verbose: bool
    :return: Декоратор
    :rtype: Callable
    """
    
    def decorator(func: Callable) -> Callable:
        """
        Декоратор для логирования.
        
        :param func: Функция
        :type func: Callable
        :return: Обёртка над функцией
        :rtype: Callable
        """
        
        @functools.wraps(func)
        def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
            """
            Обёртка над функцией.
            
            :param args: Позиционные аргументы
            :type args: list[Any]
            :param kwargs: Именованные аргументы
            :type kwargs: dict[str, Any]
            :return: Результат выполнения функции
            :rtype: Any
            """

            logger = logging.getLogger('base')
            logs = dict()
            
            if action not in ['BUY', 'SELL']:
                return func(*args, **kwargs)

            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logs['type'] = f"'{e.__class__.__name__}'"
                logs['msg'] = f"'{str(e)}'"
                logs['result'] = 'ERROR'
                
                logger.error(action + ' ' +
                            ' '.join([key+'='+val for key, val in logs.items()]))
                raise
            
            if result is None:
                return result
                
            logs['user'] = f"'{args[0]}'"
            logs['currency'] = f"'{args[1]}'"
            logs['amount'] = f"{args[2]:.4f}"
            logs['rate'] = f"{result['rate']:.2f}"
            logs['base'] = "'USD'"
                
            if verbose:
                logs['before'] = f"{result['before']:.4f}"
                logs['now'] = f"{result['now']:.3f}"
            logs['result'] = 'OK'
                
            logger.info(action + ' ' +
                        ' '.join([key+'='+val for key, val in logs.items()]))
                
            return result
        
        return wrapper
    
    return decorator

