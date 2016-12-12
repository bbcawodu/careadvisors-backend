"""
Defines view for the home page
"""
from django.http import HttpResponse


def index(request):
    return HttpResponse("PIC Backend Home")