#!/usr/bin/env python3

import yaml
import socket
import requests
import sys

with open('./vars/main.yaml') as f:

    domains = yaml.load(f, Loader=yaml.FullLoader)

    output = dict()
    output['apache_remove_default_vhost'] = True
    output['apache_ssl_protocol'] = '-all +TLSv1.3 +TLSv1.2'
    output['apache_ssl_cipher_suite'] = 'HIGH:!aNULL:!MD5'
    output['apache_vhosts'] = [] 
    output['apache_vhosts_ssl'] = [] 
    for domain in domains:
        try:
            ipaddress = socket.gethostbyname(domain['domain'])
        except:
            sys.stderr.write(f"Cannot resolve ip for domain {domain['domain']}. Skipping...\n")
            continue
        if ipaddress != '77.87.50.10':
            sys.stderr.write(f"Domain {domain['domain']} doesn't point to our redirects server, but {ipaddress}. Skipping...\n")
            continue
        try:
            r = requests.head(domain['target'], timeout=10)
        except:
            sys.stderr.write(f"Exception when trying to reach target {domain['target']} for domain {domain['domain']}. Skipping...\n")
            continue
        if r.status_code >= 400:
            sys.stderr.write(f"Target {domain['target']} gives status {r.status_code} for domain {domain['domain']}. FIY...\n")
        vhost = dict()
        vhost['servername'] = domain['domain']
        vhost['redirect_to_https'] = True
        vhost_ssl = dict()
        vhost_ssl['servername'] = domain['domain']
        vhost_ssl['certificate_file'] =  f"/etc/letsencrypt/live/{domain['domain']}/fullchain.pem"
        vhost_ssl['certificate_key_file'] = f"/etc/letsencrypt/live/{domain['domain']}/privkey.pem"
        conditions = dict()
        conditions['test_string'] = "%{HTTP_HOST}"
        conditions['pattern'] = domain['pattern']
        conditions['flags'] = "[NC]"
        pattern = dict()
        pattern['pattern'] = "^(.*)$"
        pattern['substitution'] = domain['target']
        pattern['flags'] = "[R,L]"
        pattern['conditions'] = []
        pattern['conditions'].append(conditions)
        vhost_ssl['custom_rewrites'] = []
        vhost_ssl['custom_rewrites'].append(pattern)
        output['apache_vhosts'].append(vhost)
        output['apache_vhosts_ssl'].append(vhost_ssl)

fallbackVhost = dict()
fallbackVhost['servername'] = "www.freifunk.net"
fallbackVhost['serveralias'] = []
fallbackVhost['serveralias'].append("*.freifunk.net")
fallbackVhost['custom_rewrites'] = []
fallbackCondition = dict()
fallbackCondition['test_string'] = "%{HTTP_HOST}"
fallbackCondition['pattern'] = "!^freifunk\\.net"
fallbackCondition['flags'] = "[NC]"
fallbackPattern = dict()
fallbackPattern['conditions'] = []
fallbackPattern['conditions'].append(fallbackCondition)
fallbackPattern['substitution'] = "-"
fallbackPattern['flags'] = "[G]"
fallbackPattern['pattern'] = "^.*$"
fallbackVhost['custom_rewrites'].append(fallbackPattern)
output['apache_vhosts'].append(fallbackVhost)

print(yaml.dump(output))
