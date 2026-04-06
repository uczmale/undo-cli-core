# Origin - https://stackoverflow.com/a/67962816
# Posted by furas, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-01, License - CC BY-SA 4.0
import os, sys, logging, re, json, base64
import importlib
# add trace logger level
logger = logging.getLogger()
logging.TRACE = logging.DEBUG - 5
logging.addLevelName(logging.DEBUG - 5, 'TRACE')
logger.setLevel(logging.getLevelName(os.environ.get("LOG_LEVEL", "ERROR")))
logging.basicConfig(level=logging.getLevelName(os.environ.get("LOG_LEVEL", "ERROR")))

import http.server
import socketserver
import jwt
import urllib

from easiutils import request
from handler import handler

class UnHandler(http.server.SimpleHTTPRequestHandler):
    @classmethod
    def define_paths(cls, args):
        # define the path set up front eh? probs should be in the class but in a sec
        # assumes the second argument is the port (the first is the file, obvs)
        path_set = []
        for arg in args:
            path_key = arg.strip("/")
            # create a mask to absolutely match this route in future
            path_mask = re.sub("{[^/]+}", "([^/]+)", path_key)

            # get each part of the path and if it's a placeholder, grab it
            # (without the braces)
            path_parts = path_key.split("/")
            path_params = []
            for part in path_parts:
                if part.startswith("{") and part.endswith("}"):
                    path_params.append(part[1:-1])

            path_set.append({
                "key": "/" + path_key,
                "mask": re.compile("^/" + path_mask + "$"),
                "params": path_params
            })
        cls.path_set = path_set

        return cls.path_set


    @staticmethod
    def extract_path_params(path_set, raw_path):
        # using the path_keys defined in the initial args to start the proxy
        # see if this path matches any of them
        # (if not, i guess, pass it through anyway it should just error out in handler.py)
        path_key = raw_path
        path_params = {}
        
        # for each route_key (e.g. /entity or /entity/{identifier})
        # check if this route (e.g. /entity/123-value) matches the regex mask
        # if it does, capture that key
        # then loop through all the {mask}s (f there are any) to extract the 123-values
        # and map them to their {identifier} param names
        for path_item in path_set:
            if path_item["mask"].match(raw_path):
                path_key = path_item["key"]
                if path_item["params"]:
                    # findall returns list of tuples if there are multiple capture groups
                    # so force that down to just a single list first
                    path_values = path_item["mask"].findall(raw_path)
                    if len(path_item["params"]) > 1:
                        path_values = list(path_values[0])
                    for idx, path_value in enumerate(path_values):
                        path_params[path_item["params"][idx]] = path_value

        return path_key, path_params


    @staticmethod
    def extract_query_params(query_string):
        # now also extract the much easier query params
        # which should be empty for no query params
        if not query_string:
            return None

        query_params = {}
        for param in query_string.split("&"):
            query_parts = param.split("=") 
            query_parts = query_parts + [""] * (2 - len(query_parts)) # always two parts
            query_params[query_parts[0]] = urllib.parse.unquote(query_parts[1])

        return query_params


    @staticmethod
    def extract_authorisation(auth_header):
        if not auth_header:
            return None

        auth_element = auth_header.split()
        auth_type = auth_element[0]
        auth_string = auth_element[1]
        
        # for basic auth
        # return as AWS would for basic auth, which is done via a Lambda
        # (albeit without the department.. will need a way to mock that i guess?)
        if auth_type.lower() == "basic":
            decoded_auth = base64.standard_b64decode(auth_string.strip()).decode("utf-8")
            auth_block = {
                "lambda": {
                    "full_name": decoded_auth.split(":")[0]
                }
            }
            return auth_block

        # else assume jwt if it's got the basic structure eh?
        elif auth_type.lower() == "bearer" and "." in auth_string:
            decoded_jwt = jwt.decode(auth_string,
                                    key=None, options={"verify_signature": False})
                                
            auth_block = {
                "jwt": {
                    "claims": decoded_jwt,
                    "scopes": None
                }
            }
            return auth_block

        # otherwise, i guess, good luck?
        return None


    def process_request(self):
        logger.debug("--------------------------------------")
        logger.info("START UnHandler event")

        # extract the request
        headers = {}
        for header in self.headers.keys():
            headers[header] = self.headers.get(header)

        content_length = self.headers['Content-Length']
        if content_length:
            body = self.rfile.read(int(content_length)).decode("utf-8")
        else:
            body = None

        path_parts = self.path.split("?")
        raw_path = path_parts[0]
        query_string = path_parts[1] if len(path_parts) > 1 else ""

        path_key, path_params = self.extract_path_params(self.path_set, raw_path)
        query_params = self.extract_query_params(query_string)
        auth_block = self.extract_authorisation(headers.get("Authorization", None))

        # the AWS event for an API
        event = {
            "version": "2.0",
            "routeKey": f"{self.incoming_method} {path_key}",
            "rawPath": raw_path,
            "rawQueryString": query_string,
            "headers": headers,
            "queryStringParameters": query_params,
            "requestContext": {
                "accountId": "1515717`14362",
                "apiId": "ou1hycoh17",
                "authorizer": auth_block,
                "domainName": "aais.integration-dev.ucl.ac.uk",
                "domainPrefix": "aais",
                "http": {
                    "method": self.incoming_method,
                    "path": raw_path,
                    "protocol": "HTTP/1.1",
                    "sourceIp": "149.34.173.132",
                    "userAgent": "curl/7.68.0"
                },
                "requestId": "TD-ZAh44LPEEMOg=",
                "routeKey": f"{self.incoming_method} {path_key}",
                "stage": "$default",
                "time": "26/Oct/2025:15:54:33 +0000",
                "timeEpoch": 1761494073215
            },
            "isBase64Encoded": False
        }

        if not query_params:
            del(event["queryStringParameters"])

        if not auth_block:
            del(event["requestContext"]["authorizer"])

        if path_params:
            event["pathParameters"] = path_params

        if body:
            event["body"] = body
        # print(event)

        # extract the details from the AWS request
        convert = False if os.environ.get("EASIKIT_EVENT_CONVERT") == "False" else True
        evt = request.extract_request(event, convert=convert)
        event["easikit"] = { "request": evt, "event": evt }
        logger.log(logging.TRACE, "Handler event: " + str(event))

        for name in list(sys.modules.keys()):
            if name.startswith("handler."):
                importlib.reload(sys.modules[name])

        resp = handler.handler(event)
        # print(resp)

        # return the response to the request as EASIKit would've wanted it 
        self.send_response(resp["statusCode"])
        for header_name, header_value in resp["headers"].items():
            self.send_header(header_name, header_value)
        
        # add the localhost specific headers to allow frontend testing
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "close")
        self.end_headers()

        self.wfile.write(resp["body"].encode("utf-8"))
        logger.info("END UnHandler event")
        logger.debug("--------------------------------------")


    def do_GET(self):
        self.incoming_method = "GET"
        self.process_request()

    def do_POST(self):
        self.incoming_method = "POST"
        self.process_request()

    def do_PUT(self):
        self.incoming_method = "PUT"
        self.process_request()

    def do_PATCH(self):
        self.incoming_method = "PATCH"
        self.process_request()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "Authorization, *")
        self.send_header("Access-Control-Max-Age", "0")
        self.end_headers()


# turn it into a threaded server so Firefox stops giving me grief
# https://obinexus.medium.com/python-is-a-great-language-for-building-servers-especially-for-quick-projects-and-prototyping-71e0769bf738
class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True # Ensures threads exit when the server shuts down


def main():
    PORT = (int(sys.argv[1])
            if len(sys.argv) > 1 and isinstance(sys.argv[1], str) else 8000)

    UnHandler.define_paths(sys.argv[2:])
    Handler = UnHandler

    print(f"\n\033[0;32mStarting http://0.0.0.0:{PORT}\033[0m")
    if UnHandler.path_set:
        print("Mapping routes for following path masks (for all methods):")
        for path in UnHandler.path_set:
            print(f"\t- {path['key']}")
    else:
        print ("\033[90m[NOTE: No routes mapped, "
                + "so /path/{params} won't be handled.]\033[0m")

    httpd = None
    try:
        with ThreadedHTTPServer(("", PORT), Handler) as httpd:
            print(f"\nRunning...")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nStopping by Ctrl+C, may take a sec to free up entirely..")
    finally:
        # to resolve problem `OSError: [Errno 98] Address already in use` 
        # but it still takes a bit of time so, like, chill
        if httpd:
            httpd.server_close()
        print("Server stopped!\n")

if __name__ == "__main__":
    main()