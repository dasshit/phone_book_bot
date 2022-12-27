from loguru import logger


# logger.remove()
logger.add(
    "logs/{time:YYYY-MM-DD}/bot-{time:HH}.log",
    rotation="08:00",
    retention="1 day",
    level="DEBUG",
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{function: <40}</cyan>:<cyan>{line: <4}</cyan> - <level>{message}</level>",
    colorize=True,
    compression="zip"
)
