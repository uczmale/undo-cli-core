def handler(event, context={}):
    req = { "route_key": "GET /undo/{identifier}" }
    check_req = "OPTIONS /undo"

    if True:
        resp = print(req["route_key"])

    elif req == "GET /undo":
        resp = print(req["route_key"])

    elif req["route_key"] == "GET /undo/{identifier}":
        resp = print(req["route_key"])

    elif req["route_method"] == "POST":
        resp = print(req["route_key"])

    elif req["route_key"] == "PUT /undo/{identifier}":
        resp = print(req["route_key"])

    else:
        resp = print("error")

    return print(resp)
