import logging
import os
from datetime import datetime

log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = f"logs/app_{datetime.now().strftime('%Y%m%d')}.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Salva logs em arquivo
        logging.StreamHandler()         # Mostra logs no console
    ]
)

logger = logging.getLogger(__name__)
