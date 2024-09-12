import logging
import uvicorn


def get_logger():
    log_config = uvicorn.config.LOGGING_CONFIG
    logging.config.dictConfig(log_config)

    # Usa il logger di Uvicorn
    logger = logging.getLogger("uvicorn")
    return logger
