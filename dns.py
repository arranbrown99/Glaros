import requests
import json
import configparser

# To do
# Improve modularity
# IO for keys


def get(domain):
    """Retrieve domain records
    """
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    r = requests.get(
        f'https://api.godaddy.com/v1/domains/{domain}/records/A/@', headers=headers)
    print(r.json())


def put(domain, ip, headers, url):
    """Update domain records
    """

    payload = json.dumps(
        [{'data': f'{ip}', 'ttl': 600}])
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    r = requests.put(url, data=payload, headers=headers)
    print(r)


def main(domain):
    """Updates domain name servers to point at new cloud service

    """

    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = config['KEYS']['api_key']
    api_secret = config['KEYS']['api_secret']

    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/A/@'
    put(domain, '1.1.1.1', headers, url)


main('GLAROS.UK')
