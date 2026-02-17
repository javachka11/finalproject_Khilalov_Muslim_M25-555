import logging
import logging.handlers
import os

from valutatrade_hub.infra.settings import config


def run_logging() -> None:
    """
    Создать и настроить логгер.
    
    :return: Логгер
    :rtype: Logger
    """

    os.makedirs(config.get('log_path', 'logs/'), exist_ok=True)
    
    logfmt = '%(levelname)s %(asctime)s %(message)s'
    datefmt = '%Y-%m-%dT%H:%M:%S'
    
    logger = logging.getLogger('base')
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(config.get('log_path', 'logs/'), 'actions.log'),
        maxBytes=10*1024*1024,
        backupCount=3,
        encoding='utf-8'
    )
    
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(logfmt, datefmt=datefmt)
    handler.setFormatter(formatter)
    logger.addHandler(handler)