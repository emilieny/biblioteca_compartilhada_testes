# PADRAO DECORATOR

import time
from functools import wraps

def timing_decorator(func):
    """
    Um decorador que mede e imprime o tempo de execução de uma função.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Função '{func.__name__}' executada em {end_time - start_time:.4f} segundos.")
        return result
    return wrapper