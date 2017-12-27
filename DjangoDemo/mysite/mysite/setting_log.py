Mylog = {
    'version': 1,  # 日志版本
    'disable_existing_loggers': False,  # True：disable原有日志相关配置
    'formatters': {  # 日志格式
        'verbose': {  # 详细格式
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {  # 简单格式
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {  # 日志过滤器
        # 'special': {  # 特殊过滤器，替换foo成bar，可以自己配置
        #     '()': 'project.logging.SpecialFilter',
        #     'foo': 'bar',
        # },
        'require_debug_true': {  # 是否支持DEBUG级别日志过滤
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志handlers
        'file': {  # 文件handler
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': './django.log',
            'formatter': 'verbose',
        },
        'console': {  # 控制器handler，INFO级别以上的日志都要Simple格式输出到控制台
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {  # 邮件handler，ERROR级别以上的日志要特殊过滤后输出
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'filters': ['special']
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'myproject.custom': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
            # 'filters': ['special']
        }
    }
}
