from django.shortcuts import render
from django.http import HttpResponse
import datetime
from rest_framework_swagger import renderers
from rest_framework.decorators import api_view, renderer_classes


@api_view(['GET'])
@renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
