import logging , datetime
import logging.handlers
from time import sleep

log = logging.getLogger('log_custom')
log.setLevel(logging.DEBUG)
log.propagate = True
formatter = logging.Formatter("%(asctime)s;[%(levelname)s];%(message)s",
                              "%Y-%m-%d %H:%M:%S")
## 그냥 처리
#fileHandler = logging.FileHandler('./log.txt' ,mode = "w")
streamHandler = logging.StreamHandler()
log_max_size = 10 * 512
log_file_count = 5
## 용량별 처리
### log.txt에는 용량만큼 쌓고
### backupCount 수만큼 쌓는 것을 저장함.
# fileHandler = logging.handlers.RotatingFileHandler(filename='./log.txt', 
#                                                    maxBytes=log_max_size,
#                                                    backupCount=log_file_count,
#                                                    mode = "w", 
#                                                   )
## 시간별 처리
### log.txt에는 when 시간 동안 쌓이고
### backupCount에서 그 형식의 이름으로 저장
fileHandler = logging.handlers.TimedRotatingFileHandler(
    filename='./log.txt', 
    when = "M" ,  # W0
    backupCount= 4 , 
    atTime=datetime.time(0, 0, 0)
    )
fileHandler.setLevel(logging.DEBUG)
streamHandler.setLevel(logging.DEBUG)

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)
log.addHandler(fileHandler)
log.addHandler(streamHandler)

log.info('fdsafasf')
log.info('fdsafasf')
log.info('fdsafasf')
log.info('fdsafasf')
log.info('fdsafasf')
log.info('fdsafasf')
log.info('fdsafasf')
log.debug('asdsdaf')
log.debug('asdsdaf')
log.debug('asdsdaf')
