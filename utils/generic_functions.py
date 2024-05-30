from functools import wraps


def check_none(func):
    @wraps(func)
    def wrapper(values):
        # VERIFICA SE HÁ ALGUM VALOR NÃO NONE NA LISTA
        if any(x is not None for x in values):
            return func(values)
        else:
            return None

    return wrapper
