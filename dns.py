'''
Update the DNS server to reflect the migration between hosts
Call change_ip()
'''

# To do
# Requesst timeouts, retries

import requests
import json
import configparser
import ipaddress

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
    # except requests.exceptions`.HTTPError as e:
    #     raise DNSUpdateError(f"{e}")
    except Exception as e:
        raise


def change_ip(passed_ip):
    '''
    Handles DNS update for service change

    Parameters
    ------
    passed_ip : str
        the ip address of the new host in dotted decimal form 'x.x.x.x' passed by driver

    Raises
    ------
    DNSUpdateError
        something went wrong updating the DNS server

    Returns
    ------
    '''

    try:
        ip = ipaddress.IPv4Address(passed_ip)
    except ipaddress.AddressValueError as e:
        # raise(DNSUpdateError(e))
        raise

    try:
        config = configparser.ConfigParser()
        config.read(__config_file__)
    except Exception as e:
        # raise(DNSUpdateError( e, f"Could not read configuration file {__config_file__}"))
        raise

    try:
        # Read data from config
        dns = config['dns']
        api_key, api_secret = dns['key'], dns['secret']
        domain = dns['domain']
    except Exception as e:
        # raise(DNSUpdateError(e, f'An error occured attempting to load configuration'))
        raise

    # Construct variables for requests
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/@'

    # dns_session = requests.Session()
    # dns_session.headers.update(headers)

    _update_ip(url, headers, ip.exploded)
    curr_dns_ip = _get_ip(url, headers)
    if (ip.exploded == curr_dns_ip):
        return
    else:
        # The IP has not updated
        raise DNSUpdateError('if(ip == current_ip)',
                             f'Change to {ip.exploded} requested but DNS is {curr_dns_ip}')


def gen_config():
    '''
    Creates a config.ini, if it already exists: truncates it
    '''
    while True:
        try:
            print("You are required to provide the following information")
            domain_in = input("Domain: ")
            key_in = input("API key: ")
            secret_in = input("API secret: ")
        except:
            print("Incorrect input")
            continue
        else:
            break
    config = configparser.ConfigParser()
    config['dns'] = {'domain': f'{domain_in}',
                     'key': f'{key_in}',
                     'secret': f'{secret_in}'}

    with open(f'{__config_file__}', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    # For testing
    # change_ip('1.1.1.8')
    gen_config()
