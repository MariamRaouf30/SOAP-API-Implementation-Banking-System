import http.client
from xml.etree import ElementTree as ET

def send_soap_request(account):
    conn = http.client.HTTPConnection('localhost', 8080)
    request = f"""
    <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body><getBalance><account>{account}</account></getBalance></soap:Body>
    </soap:Envelope>
    """
    conn.request('POST', '/', request, headers={'Content-Type': 'text/xml'})
    response = ET.fromstring(conn.getresponse().read().decode())
    balance = response.find('.//balance').text
    print(f"Balance for account {account}: {balance}")
    conn.close()

if __name__ == '__main__':
    send_soap_request("123456")
