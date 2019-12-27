'''
Update the DNS server to reflect the migration between hosts
Call change_service()
'''

# To do
# Error handling for configparser
# Requesst timeouts, retries

import requests
import json
import configparser


__config_file__ = 'config.ini'


class Error(Exception):
    '''
    Base class for exceptions
    '''
    pass


class DNSUpdateError(Error):
    '''
    Exception raised for errors in the input.

    Attributes
    ------
        expression -- input expression in which the error occurred
        message -- explanation of the error
    '''

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


def _get_ip(url, headers):
    '''
    Retrieves the currently set IP address in the DNS A-Record 

    Parameters
    ------
    url : str
        the url for the api call

    headers : str
        headers to send for api authentication

    Raises
    ------
    Exception

    Returns
    -------
    ip
        the IPv4 address of the A-record in dotted decimal form 'x.x.x.x'
    '''

    try:
        response = requests.get(url, headers=headers)
        ip = response.json()[0]['data']
        response.raise_for_status()
        return ip
    except Exception as e:
        raise


def _update_ip(url, headers, ip):
    '''
    Updates the DNS server records to reflect the new IP

    Parameters
    ------
    url : str
        the url for the api call

    headers : str
        headers to send for api authentication

    ip : str
        the ip address of the new host in dotted decimal form 'x.x.x.x'

    Raises
    ------
    Exception
    '''

    payload = json.dumps(
        [{'data': f'{ip}', 'ttl': 600}])
    try:
        response = requests.put(url, data=payload, headers=headers)
        response.raise_for_status()
    # except requests.exceptions.RequestException as e:
    #     raise DNSUpdateError(f"{e}, {response.json()['fields']}")
    # except requests.exceptions.HTTPError as e:
    #     raise DNSUpdateError(f"{e}")
    except Exception as e:
        raise


def change_service(service):
    '''
    Handles DNS update for service change

    Parameters
    ------
    service : str
        aws, azure or gcp
        this string will be used to take relevant IP address from config file

    Raises
    ------
    DNSUpdateError
        something went wrong updating the DNS server
    '''

    try:
        config = configparser.ConfigParser()
        config.read(__config_file__)
    except Exception as e:
        raise(DNSUpdateError(f"Could not read {__config_file__}"))

    # Read in data from config
    dns = config['dns']
    api_key, api_secret = dns['key'], dns['secret']
    domain = dns['domain']
    ip = config[f'{service.lower()}']['ip']

    # Construct variables for requests
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/@'

    # dns_session = requests.Session()
    # dns_session.headers.update(headers)

    current_ip = _get_ip(url, headers)
    _update_ip(url, headers, ip)
    print(f"DNS server A-record IP changed from {current_ip} to {ip}")


if __name__ == "__main__":
    change_service('msft')
