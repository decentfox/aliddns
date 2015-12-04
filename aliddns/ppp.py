import logging
import socket
import sys
import time

import StringIO

from . import config


def main():
    """
    This script is called with the following arguments:
       Arg  Name                          Example
       $1   Interface name                ppp0
       $2   The tty                       ttyS1
       $3   The link speed                38400
       $4   Local IP number               12.34.56.78
       $5   Peer  IP number               12.34.56.99
       $6   Optional ``ipparam'' value    foo
    """
    # noinspection PyPackageRequirements
    import aliyun.api

    if not sys.stdin.encoding:
        sys.stdin = StringIO.StringIO()
        sys.stdin.encoding = sys.getdefaultencoding()

    interface = sys.argv[1]
    if interface not in config.INTERFACES:
        return

    ip = sys.argv[4].decode('utf-8')

    logging.info('Detected %s IP change: %s', interface, ip)

    # noinspection PyUnresolvedReferences
    aliyun.setDefaultAppInfo(config.ALIYUN_KEY_ID, config.ALIYUN_KEY_SECRET)

    req = aliyun.api.dns.DnsDescribeDomainRecordsRequest()
    req.DomainName = config.DOMAIN_NAME
    req.TypeKeyWord = config.TYPE

    tries = 0
    while True:
        try:
            tries += 1
            for rr in config.RRS:
                req.RRKeyWord = rr
                records = req.getResponse()['DomainRecords']['Record']
                if records:
                    record = records[0]
                    if record['Value'] == ip:
                        logging.debug('%s.%s is already %s',
                                      rr, config.DOMAIN_NAME, ip)
                    else:
                        logging.info('Updating %s.%s from %s to %s',
                                     rr, config.DOMAIN_NAME, record['Value'],
                                     ip)
                        update = aliyun.api.dns.DnsUpdateDomainRecordRequest()
                        update.RecordId = record['RecordId']
                        update.RR = rr
                        update.Type = config.TYPE
                        update.Value = ip
                        update.getResponse()
                else:
                    logging.warning('No such record %s.%s, skipping for now.',
                                    rr, config.DOMAIN_NAME)
            break
        except socket.error:
            if tries < 3:
                logging.warning(
                    'Network issue, try again in %s second(s).',
                    tries ** 2, exc_info=True)
                time.sleep(tries ** 2)
            else:
                logging.critical(
                    'Still no network, please set DNS manually.',
                    exc_info=True)
                break

    logging.info('Finished DDNS process.')


def main_wrapper():
    logging.basicConfig(filename=config.LOG_FILE, level=config.LOG_LEVEL,
                        format=config.LOG_FORMAT)
    # noinspection PyBroadException
    try:
        main()
    except Exception:
        logging.exception('Failed due to exception!')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(levelname)s: %(message)s')
    main()
