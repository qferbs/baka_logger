from baka_logger import logger_setup, print
import logging

logger_setup(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    character='Taiga from Toradora',
    file='log.out',
    logger=True,
    excepthook=True
)

logging.warning("The program has crashed")

print('Testing print statement', [0, 1, 2])

raise Exception("The programmer is a baka")
