import logging
import sys

from .config import *


def main():
    import aliyun.api

    interface = sys.argv[1]
    if interface not in INTERFACES:
        return

    ip = sys.argv[4].decode('utf-8')

    logging.info('Detected %s IP change: %s', interface, ip)

    aliyun.setDefaultAppInfo(ALIYUN_KEY_ID, ALIYUN_KEY_SECRET)

    req = aliyun.api.dns.DnsDescribeDomainRecordsRequest()
    req.DomainName = DOMAIN_NAME
    req.TypeKeyWord = TYPE

    for rr in RRS:
        req.RRKeyWord = rr
        records = req.getResponse()['DomainRecords']['Record']
        if records:
            record = records[0]
            if record['Value'] == ip:
                logging.debug('%s.%s is already %s', rr, DOMAIN_NAME, ip)
            else:
                logging.info('Updating %s.%s from %s to %s', rr, DOMAIN_NAME,
                             record['Value'], ip)
                update = aliyun.api.dns.DnsUpdateDomainRecordRequest()
                update.RecordId = record['RecordId']
                update.RR = rr
                update.Type = TYPE
                update.Value = ip
                update.getResponse()
        else:
            logging.warning('No such record %s.%s, skipping for now.', rr,
                            DOMAIN_NAME)

    logging.info('Finished DDNS process.')


def main_wrapper():
    logging.basicConfig(filename='/var/log/aliyun-ddns.log',
                        level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s')
    try:
        main()
    except Exception:
        logging.exception('Failed due to exception!')


if __name__ == '__main__':
    main()
