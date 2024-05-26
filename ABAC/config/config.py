import os

# Cấu hình cơ sở dữ liệu
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Tai@6410'
DB_NAME = 'abacdb'

# Cấu hình logging
LOGGING_CONFIG = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/app.log',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
