from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree import ElementTree as ET

accounts = {"123456": 5000.0, "654321": 3000.0}

class SOAPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        data = self.rfile.read(length)
        root = ET.fromstring(data)
        method = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')[0].tag

        if method.endswith('getBalance'):
            acc = root.find('.//account').text
            balance = accounts.get(acc, "Account not found")
            response = f"""
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body><getBalanceResponse><balance>{balance}</balance></getBalanceResponse></soap:Body>
            </soap:Envelope>
            """
        else:
            response = """
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body><soap:Fault><faultcode>Server</faultcode><faultstring>Method not found</faultstring></soap:Fault></soap:Body>
            </soap:Envelope>
            """

        self.send_response(200)
        self.send_header('Content-type', 'text/xml')
        self.end_headers()
        self.wfile.write(response.encode())

def run(port=8081):
    server = HTTPServer(('', port), SOAPRequestHandler)
    print(f"SOAP server running on port {port}...")
    server.serve_forever()

if __name__ == '__main__':
    run()
