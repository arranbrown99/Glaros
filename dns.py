"""Update the A-record of the DNS server to point to a new vm

Call change_service
"""

# To do
# Improve modularity, extendability
# Custom error exceptions
# Better docstrings

import requests
import json
import configparser


__config_file = 'config.ini'


def _get(domain):
    """Retrieve domain records
    """
    r = requests.get(
        f'https://api.godaddy.com/v1/domains/{domain}/records/A/@', headers=headers)
    return(r.json())


def _update_ip(ip, headers, url):
    """Update domain records
    """

    payload = json.dumps(
        [{'data': f'{ip}', 'ttl': 600}])
    try:
        response = requests.put(url, data=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"{e}, {response.json()['fields']}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"{e}")


def change_service(service):
    """Updates domain name servers to point at new cloud service

    """

    try:
        config = configparser.ConfigParser()
        config.read(__config_file)
    except Exception as e:
        print(f"Could not read {__config_file}")

    dns = config['dns']
    api_key, api_secret = dns['key'], dns['secret']
    domain = config['DEFAULT']['domain']
    ip = config[f'{service.lower()}']['ip']

    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/@'

    try:
        _update_ip(ip, headers, url)
    except Exception as e:
        print(f"{e}")
    else:
        print("Changed IP")


if __name__ == "__main__":
    change_service('aws')
