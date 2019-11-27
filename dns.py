import requests


def main(domain, service, api_key='', api_secret=''):
    """Updates domain name servers to point at new cloud service

    """
    nameserver_dict = {'AWS': ['ns1.aws.com', 'ns2.aws.com'],
                       'GCP': ['ns1.gcp.com', 'ns2.gcp.com'],
                       'Azure': ['ns1.azure.com', 'ns2.azure.com']}

    # curl -X PUT -H"Authorization: sso-key [API_KEY]:[API_SECRET]""https://api.godaddy.com/v1/domains/{domain}/records"

    url = f"https://api.godaddy.com/v1/domains/{domain}/records"
    _SSO_KEY_TEMPLATE = f'sso-key {api_key}:{api_secret}'
    payload = "requestjson"
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    r = requests.put()


main('glaros.uk', 'AWS')
