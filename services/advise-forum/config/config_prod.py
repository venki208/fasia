import logging

# MongoDB
MONGODB_SETTINGS = {
    'db':'fasiadb',
    'host':'localhost',
    'port':27017,
    'username':'faadmin',
    'password':'nri(texas)#78',
}
    
# Logger
LOGGING_FORMAT = '[filename:%(module)s - function name:%(funcName)s - line no:%(lineno)d] -%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOGGING_LOCATION = 'fasiaadvise.log'
LOGGING_LEVEL = logging.DEBUG
