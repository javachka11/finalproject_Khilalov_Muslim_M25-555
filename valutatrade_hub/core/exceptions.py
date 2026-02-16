class InsufficientFundsError(Exception):
    """
    Исключение о недостатке средств на балансе.
    """

    def __init__(self,
                 available: float,
                 required: float,
                 code: str) -> None:
        """
        Сгенерировать исключение.
        
        :param available: Доступно, средств
        :type available: float
        :param required: Требуется, средств
        :type required: float
        :param code: Код валюты
        :type code: str
        """

        info = f"Недостаточно средств: доступно {available:.8f} {code}, "
        info += f"требуется {required:.8f} {code}"
        super().__init__(info)

        self.available = available
        self.required = required
        self.code = code


class CurrencyNotFoundError(Exception):
    """
    Исключение о неизвестной для системы валюте.
    """

    def __init__(self, code: str) -> None:
        info = f"Неизвестная валюта '{code}'"
        super().__init__(info)

        self.code = code


class ApiRequestError(Exception):
    """
    Исключение об ошибке при обращении к внешнему API.
    """

    def __init__(self, reason: str) -> None:
        info = f"Ошибка при обращении к внешнему API: {reason}"
        super().__init__(info)

        self.reason = reason

