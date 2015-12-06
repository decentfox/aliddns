# aliddns

The DDNS tool for domains hosted on
[AliYun](http://wanwang.aliyun.com/domain/dns/). It keeps your domain pointing
to your changing local IP, by updating domain record value when local IP is
changed. Therefore, there will be a DELAY after IP change, when you should
expect some downtime. USE WITH CAUTION.

For now, aliddns supports only ppp on linux.

This is not an Alibaba product.

## Installation

Due to dependency, aliddns can only be used on Python 2.6 and above.
Using `pip install` in a virtualenv is the recommended way. For example:

```
source $VIRTUAL_ENV/bin/activate
pip install git+https://github.com/decentfox/aliddns
```

Then configure aliddns by editing
`$VIRTUAL_ENV/lib/python2.x/site-packages/aliddns/local_config.py`:

```
INTERFACES = ['ppp0']
RECORDS = [
    (u'@', u'example.com', u'A'),
    (u'www', u'example.com', u'A'),
]

ALIYUN_KEY_ID = 'xxx'
ALIYUN_KEY_SECRET = 'xxx'
```

This will result the values of A records of `example.com` and `www.example.com`
to always be the IP on local network interface `ppp0`.

### ppp

To enable aliddns on a ppp interface, you'll need to link the hook:

```
cd /etc/ppp/if-up.d
ln -s $VIRTUAL_ENV/bin/aliddns-ppp
```

## Debugging

Log file is by default located at `/var/log/aliddns.log`. And there're a few
more logging configurations in `aliddns/config.py` which you can override in
`local_config.py` specified above.
