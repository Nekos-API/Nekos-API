from django.conf import settings


def jsonapi_response(request, data, meta=None, links=None, included=None):
    """
    Returns a JSON:API formatted dict.
    """
    res = {
        "jsonapi": {"version": "1.1"},
        "data": data,
        "links": {"self": request.build_absolute_uri()},
        "meta": {"apiVersion": settings.API_VERSION},
    }

    if meta:
        res["meta"].update(meta)
    if links:
        res["links"].update(links)
    if included:
        res.update({"included": included})

    return res
