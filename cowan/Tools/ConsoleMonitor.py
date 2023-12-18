import logging.config

# 日志配置字典
LOGGING_DIC = {
    'version': 1.0,
    'disable_existing_loggers': False,
    # 日志格式 -----------------------------------------------------------------
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)8s: %(message)s',
            'datefmt': '%H:%M:%S',
        },
        'default_with_thread_process': {
            'format': '[%(asctime)s] | %(processName)s - %(threadName)s | %(levelname)8s: %(message)s',
            'datefmt': '%H:%M:%S',
        },
        'less_info': {
            'format': '%(levelname)8s: %(message)s',
        },
        'more_info': {
            'format': '[%(asctime)s] '
                      '[%(pathname)s:%(lineno)d] '
                      '[%(threadName)s:%(thread)d] '
                      '[%(processName)s:%(process)d] '
                      ' %(levelname)8s: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'filters': {},
    # 日志处理器 -----------------------------------------------------------------
    'handlers': {
        'console_debug_handler': {
            'level': 'DEBUG',  # 日志处理的级别限制
            'class': 'logging.StreamHandler',  # 输出到终端
            'formatter': 'default'  # 日志格式
        },
        # 'file_info_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件,日志轮转
        #     'filename': 'abc.log',
        #     'maxBytes': 800,  # 日志大小 10M
        #     'backupCount': 3,  # 日志文件保存数量限制
        #     'encoding': 'utf-8',
        #     'formatter': 'standard',
        # },
        # 'file_debug_handler': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',  # 保存到文件
        #     'filename': 'test.log',  # 日志存放的路径
        #     'encoding': 'utf-8',  # 日志文件的编码
        #     'formatter': 'test',
        # },
        # 'file_deal_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',  # 保存到文件
        #     'filename': 'deal.log',  # 日志存放的路径
        #     'encoding': 'utf-8',  # 日志文件的编码
        #     'formatter': 'standard',
        # },
        # 'file_operate_handler': {
        #     'level': 'INFO',
        #     'class': 'logging.FileHandler',  # 保存到文件
        #     'filename': 'operate.log',  # 日志存放的路径
        #     'encoding': 'utf-8',  # 日志文件的编码
        #     'formatter': 'standard',
        # },
    },
    # 日志记录器 -----------------------------------------------------------------
    'loggers': {
        # 模板如下
        # '<logger_name>': {
        #     'handlers': ['<handler_name>', '<...>', ...],
        #     'level': '<level_name>',
        #     'propagate': [bool],
        # },
        # 注释如下
        # <logger_name>    导入时logging.getLogger时使用的app_name
        # <handler_name>   日志处理器的名称
        # <level_name>     日志记录的级别限制
        # [bool]           默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递

        'logger_to_console': {  # 导入时logging.getLogger时使用的app_name
            'handlers': ['console_debug_handler'],  # 日志分配到哪个handlers中
            'level': 'DEBUG',  # 日志记录的级别限制
            'propagate': False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
    }
}

logging.config.dictConfig(LOGGING_DIC)
console_logger = logging.getLogger('logger_to_console')
