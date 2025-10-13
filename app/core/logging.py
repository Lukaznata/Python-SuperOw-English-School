import logging
import os
from datetime import datetime
from functools import wraps
from typing import Callable
import traceback

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"

# Formato mais detalhado com linha do arquivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),  # Salva logs em arquivo com UTF-8
        logging.StreamHandler()                            # Mostra logs no console
    ]
)

logger = logging.getLogger(__name__)


def log_function_call(func: Callable) -> Callable:
    """
    Decorator para logar chamadas de funções com parâmetros e resultados.
    """
    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        logger.info(f"Chamando função: {func_name}")
        logger.debug(f"Parâmetros: args={args}, kwargs={kwargs}")
        
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Função {func_name} executada com sucesso")
            return result
        except Exception as e:
            logger.error(f"Erro na função {func_name}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        func_name = f"{func.__module__}.{func.__name__}"
        logger.info(f"Chamando função: {func_name}")
        logger.debug(f"Parâmetros: args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            logger.info(f"Função {func_name} executada com sucesso")
            return result
        except Exception as e:
            logger.error(f"Erro na função {func_name}: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
    
    # Detecta se a função é assíncrona ou síncrona
    import asyncio
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
