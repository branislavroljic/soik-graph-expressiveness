from django.http import HttpResponse
from django.apps.registry import apps
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the graph index.")
