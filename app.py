from flask import Flask, request, Response
from xml.etree import ElementTree as ET

app = Flask(__name__)

accounts = {"123456": 5000.0, "654321": 3000.0}

@app.route('/', methods=['GET'])
def health_check():
    return "OK", 200

@app.route('/', methods=['POST'])
def soap_handler():
    try:
        data = request.data
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
        return Response(response, content_type='text/xml')
    except Exception as e:
        return Response(f"<error>{str(e)}</error>", status=500, content_type="text/xml")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
