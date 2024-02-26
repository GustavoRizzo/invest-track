import datetime

from django.http import HttpResponse


def current_datetime(request):
    now = datetime.datetime.now()
    html = """<html><title>Current Time</title><body>It is now %s.</body><style>body {background-color: #637ed6;}</style></html>""" % now
    return HttpResponse(html)
