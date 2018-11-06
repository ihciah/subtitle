import requests
import random
import re
import time
import logging
from urllib3.util import connection


class HTTPDNSBase(object):
    _instance = None

    def __init__(self):
        self.session = requests.session()
        self.whiteList = []
        self.cache = {}

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(HTTPDNSBase, cls).__new__(cls, *args, **kw)
            cls._instance._initialized = False
        return cls._instance

    def cacheLookup(self, domain):
        standard_domain = self.toStandardDomain(domain)
        if standard_domain not in self.cache:
            return []
        ips, expire = self.cache[standard_domain]
        if time.time() < expire:
            return ips
        return []

    def cacheUpdate(self, domain, ips):
        if not ips:
            return
        standard_domain = self.toStandardDomain(domain)
        self.cache[standard_domain] = (ips, time.time() + 300)

    def toStandardDomain(self, domain):
        domain = domain if domain.endswith('.') else domain + '.'
        return domain

    def resolve(self, domain):
        standard_domain = self.toStandardDomain(domain)
        if re.match(r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$', domain):
            return [domain]
        if standard_domain in self.whiteList:
            return [standard_domain]
        return self.cacheLookup(domain)


class HTTPDNSCloudflare(HTTPDNSBase):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        super(HTTPDNSCloudflare, self).__init__()
        self.whiteList = ["cloudflare-dns.com."]

    def resolve(self, domain):
        ret = super(HTTPDNSCloudflare, self).resolve(domain)
        if ret:
            return ret
        domain = self.toStandardDomain(domain)
        url = 'https://cloudflare-dns.com/dns-query?name={}&type=A'
        headers = {'accept': 'application/dns-json'}
        cnames = []
        try:
            res = self.session.get(url.format(domain), headers=headers)
            json_data = res.json()
            for answer in json_data['Answer']:
                if answer['name'] == domain and answer['type'] == 1:
                    ret.append(answer['data'])
                if answer['name'] == domain and answer['type'] == 5:
                    cnames.append(answer['data'])
        except:
            pass
        if ret:
            self.cacheUpdate(domain, ret)
            return ret
        for cname in cnames:
            ret += self.resolve(cname)
        self.cacheUpdate(domain, ret)
        return ret


class HTTPDNSDnspod(HTTPDNSBase):
    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        super(HTTPDNSDnspod, self).__init__()
        self.whiteList = ["119.29.29.29."]

    def resolve(self, domain):
        ret = super(HTTPDNSDnspod, self).resolve(domain)
        if ret:
            return ret
        url = 'http://119.29.29.29/d?dn={}'
        try:
            res = self.session.get(url.format(domain)).text
            ips = res.split(';')
            ret += ips
        except:
            pass
        self.cacheUpdate(domain, ret)
        return ret


def dns_hijack(http_dns=None):
    httpDNS = HTTPDNSBase
    if http_dns == 'dnspod':
        httpDNS = HTTPDNSDnspod
    elif http_dns in ['cf', 'cloudflare']:
        httpDNS = HTTPDNSCloudflare

    _orig_create_connection = connection.create_connection

    def patched_create_connection(address, *args, **kwargs):
        """Wrap urllib3's create_connection to resolve the name elsewhere"""
        # resolve hostname to an ip address; use your own
        # resolver here, as otherwise the system resolver will be used.
        host, port = address
        hostnames = httpDNS().resolve(host)
        logging.debug("Resolve {}: Got {} results.".format(host, len(hostnames)))
        if hostnames:
            host = random.choice(hostnames)
        return _orig_create_connection((host, port), *args, **kwargs)
    connection.create_connection = patched_create_connection
