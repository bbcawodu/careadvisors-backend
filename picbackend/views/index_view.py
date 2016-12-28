"""
Defines view for the home page
"""
from django.http import HttpResponse


# Defines view for the index of the Patient Innovation Center Backend
def index(request):
    return HttpResponse("PIC Backend Home")