"""Update the A-record of the DNS server to point to a new vm

Call change_service
"""

# To do
# Improve modularity, extendability
# Error handling for configparser
# Better docstrings

import requests
import json
import configparser


__config_file = 'config.ini'


class Error(Exception):
    """Base class for exceptions"""
    pass


class DNSUpdateError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def _get_ip(url, headers):
    """Retrieve domain records
    Returns current IP address
    """

    try:
        response = requests.get(url, headers=headers)
        ip = response.json()[0]['data']
        response.raise_for_status()
        return ip
    except Exception as e:
        raise Exception(f"{e}")


def _update_ip(ip, headers, url):
    """Update domain records
    """

    payload = json.dumps(
        [{'data': f'{ip}', 'ttl': 600}])
    try:
        response = requests.put(url, data=payload, headers=headers)
        print(response)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # This shouldn't happen
        raise Exception(f"{e}, {response.json()['fields']}")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"{e}")


def change_service(service):
    """Updates domain name servers to point at new cloud service
    Will throw DNSUpdateError if update failed

    """

    try:
        config = configparser.ConfigParser()
        config.read(__config_file)
    except Exception as e:
        print(f"Could not read {__config_file}")
        raise(DNSUpdateError)

    # Read in data from config
    dns = config['dns']
    api_key, api_secret = dns['key'], dns['secret']
    domain = dns['domain']
    ip = config[f'{service.lower()}']['ip']

    # Construct variables for requests
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/@'

    try:
        current_ip = _get_ip(url, headers)
        if(current_ip == ip):
            pass
        _update_ip(ip, headers, url)
    except Exception as e:
        raise(DNSUpdateError(e, ""))
    else:
        print("Changed IP")


if __name__ == "__main__":
    change_service('aws')
