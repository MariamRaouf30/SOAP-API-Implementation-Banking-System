from flask import Flask, request, Response
from xml.etree import ElementTree as ET

app = Flask(__name__)

accounts = {"123456": 5000.0, "654321": 3000.0}

@app.route("/", methods=["POST"])
def soap_handler():
    try:
        root = ET.fromstring(request.data.decode("utf-8"))
        body = root.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
        method_elem = list(body)[0]
        method = method_elem.tag

        if method.endswith('getBalance'):
            acc_elem = method_elem.find('account')
            acc = acc_elem.text if acc_elem is not None else None
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
        else:
            response = """
            <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Body>
                    <soap:Fault>
                        <faultcode>Server</faultcode>
                        <faultstring>Method not found</faultstring>
                    </soap:Fault>
                </soap:Body>
            </soap:Envelope>
            """

        return Response(response.strip(), mimetype='text/xml')

    except Exception as e:
        error_response = f"""
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
            <soap:Body>
                <soap:Fault>
                    <faultcode>Server</faultcode>
                    <faultstring>Internal server error: {str(e)}</faultstring>
                </soap:Fault>
            </soap:Body>
        </soap:Envelope>
        """
        return Response(error_response.strip(), status=500, mimetype='text/xml')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
