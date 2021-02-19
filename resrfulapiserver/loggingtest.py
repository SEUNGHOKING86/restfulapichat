import logging
#from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)


streamHandler = logging.StreamHandler()
fileHandler = logging.FileHandler('.django.log')

fileHandler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)s] >> %(message)s'))



#logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

logger.setLevel(level=logging.DEBUG)
logger.debug('my DEBUG log')
logger.info('my INFO log')
logger.warning('my WARNING log')
logger.error('my ERROR log')
logger.critical('my CRITICAL log')





