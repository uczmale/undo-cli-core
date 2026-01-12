import logging
logger = logging.getLogger()

# easikit imports
from easiutils import response, exceptions as er

# project specific imports 
from handler import service as sv


# the handler's only job is to route traffic from the outside work (a user api
# request, an sns event) to the appropriate service, which will then decide
# where it needs to go next
# the handler generally does not maniplate, process or forward data

# throughout this template, please delete code you don't need and rename
# code so it matches your particular interface

def handler(event, context={}):
    req = event["easikit"]["request"]

    if req["route_method"] == "GET":
        resp = sv.get_note(params=req["params"])

    else:
        resp = er.RequestError(type=er.REQ_UNHANDLED_ROUTE, log=req)

    return response.response(**resp, req=req)
