import requests
import json

api_key = ''
api_secret = ''

# To do
# Improve modularity
# IO for keys


def get(domain):
    """retrieve domain records
    """
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    r = requests.get(
        f'https://api.godaddy.com/v1/domains/{domain}/records', headers=headers)
    print(r.json())


def put(domain):
    """Update domain records
    """
    headers = {'Authorization': f'sso-key {api_key}:{api_secret}'}
    url = f'https://api.godaddy.com/v1/domains/{domain}/records/NS'

    payload = json.dumps(
        [
            {
                "data": "ns2.digitalocean.com.",
                "name": "@",
                "port": 80,
                "priority": 10,
                "protocol": "string",
                "service": "string",
                "ttl": 600,
                "weight": 10
            },
            {
                "data": "ns1.digitalocean.com.",
                "name": "@",
                "port": 80,
                "priority": 10,
                "protocol": "string",
                "service": "string",
                "ttl": 600,
                "weight": 10
            },
            {
                "data": "ns3.digitalocean.com.",
                "name": "@",
                "port": 80,
                "priority": 10,
                "protocol": "string",
                "service": "string",
                "ttl": 600,
                "weight": 10
            }
        ]
    )

    headers = {'Authorization': f'sso-key {api_key}:{api_secret}',
               'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    r = requests.put(url, data=payload, headers=headers)
    print(r)


def main(domain, service):
    """Updates domain name servers to point at new cloud service

    """
    nameserver_dict = {'AWS': ['ns1.aws.com', 'ns2.aws.com'],
                       'GCP': ['ns1.gcp.com', 'ns2.gcp.com'],
                       'Azure': ['ns1.azure.com', 'ns2.azure.com']}

    # curl -X PUT -H"Authorization: sso-key [API_KEY]:[API_SECRET]""https://api.godaddy.com/v1/domains/{domain}/records"

    get(domain)
    put(domain)


main('GLAROS.UK', 'AWS')
