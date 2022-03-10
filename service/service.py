import requests
from flask import Flask, Response, request
import os
import logging
import cherrypy
import ujson
from certificate_handler import CertificateHandler

app = Flask(__name__)

logger = logging.getLogger("basic-auth-proxy-service")
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

url = os.environ.get("base_url")
username = os.environ.get("username")
pw = os.environ.get("password")
log_response_data = os.environ.get("log_response_data", "false").lower() == "true"
headers = ujson.loads('{"Content-Type": "application/json"}')
stream_data = os.environ.get("stream_data", "false").lower() == "true"

ca_cert = os.environ.get("ca_cert", None)
ca_cert_file = os.environ.get("ca_cert_file", "/usr/local/share/ca-certificates/ca.crt")
ca_cert_path = os.environ.get("ca_cert_path", "/etc/ssl/certs")

# install CA certificate inside container
if ca_cert:
    ca = CertificateHandler(ca_cert, ca_cert_file)
    logger.debug(ca)
    ca.write()
    os.system("update-ca-certificates")


def stream_json(clean):
    data = ujson.loads(clean)
    first = True
    yield '['
    for i, row in enumerate(data):
        if not first:
            yield ','
        else:
            first = False
        yield ujson.dumps(row)
    yield ']'


class BasicUrlSystem:
    def __init__(self, config):
        self._config = config

    def make_session(self):
        session = requests.Session()
        session.headers = self._config["headers"]
        session.verify = ca_cert_path
        return session


session_factory = BasicUrlSystem({"headers": headers})


@app.route("/<path:path>", methods=["GET"])
def get(path):
    request_url = "{0}{1}".format(url, path)
    if request.query_string:
        request_url = "{0}?{1}".format(request_url, request.query_string.decode("utf-8"))

    logger.info("Request url: %s", request_url)

    try:
        with session_factory.make_session() as s:
            request_data = s.request("GET", request_url, auth=(username, pw), headers=headers)
            if log_response_data:
                logger.info("Data received: '%s'", request_data.text)
    except Exception as e:
        logger.warning("Exception occurred when download data from '%s': '%s'", request_url, e)
        raise

    if stream_data:
        return Response(stream_json(request_data.text), mimetype='application/json')

    return Response(request_data, mimetype='application/json')


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5002,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
