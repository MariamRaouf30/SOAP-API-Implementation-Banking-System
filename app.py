from flask import Flask, request, Response
from xml.etree import ElementTree as ET

app = Flask(__name__)

accounts = {"123456": 5000.0, "654321": 3000.0}

@app.route("/", methods=["POST"])
def soap_handler():
    try:
        xml_data = request.data.decode("utf-8")
        root = ET.fromstring(xml_data)
        ns = {'soap': 'http://schemas.xmlsoap.org/soap/envelope/'}

        body = root.find('soap:Body', ns)
        if body is None:
            raise ValueError("Missing SOAP Body")

        method_elem = list(body)[0]
        if method_elem.tag.endswith('getBalance'):
            acc_elem = method_elem.find('account')
            if acc_elem is None:
                raise ValueError("Missing account element")

            acc = acc_elem.text.strip()
            balance = accounts.get(acc, "Account not found")

            response = f"""
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <getBalanceResponse>
                        <balance>{balance}</balance>
                    </getBalanceResponse>
                </soap:Body>
            </soap:Envelope>
            """
            return Response(response.strip(), mimetype='text/xml')
        else:
            raise ValueError("Unknown method")

    except Exception as e:
        print("ERROR:", str(e))
        error_response = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <soap:Fault>
                    <faultcode>Server</faultcode>
                    <faultstring>{str(e)}</faultstring>
                </soap:Fault>
            </soap:Body>
        </soap:Envelope>
        """
        return Response(error_response.strip(), status=500, mimetype='text/xml')

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
