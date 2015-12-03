import logging

INTERFACES = ['ppp0']
TYPE = u'A'
DOMAIN_NAME = u'example.com'
RRS = [u'@', u'www']

ALIYUN_KEY_ID = ''
ALIYUN_KEY_SECRET = ''

LOG_FILE = '/var/log/aliddns.log'
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
LOG_LEVEL = logging.INFO

try:
    from .local_config import *
except ImportError:
    pass
