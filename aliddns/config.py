INTERFACES = ['ppp0']
TYPE = u'A'
DOMAIN_NAME = u'example.com'
RRS = [u'@', u'www']
ALIYUN_KEY_ID = ''
ALIYUN_KEY_SECRET = ''

try:
    from .local_config import *
except ImportError:
    pass
