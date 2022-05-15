from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import logging
def base(request):
    return HttpResponse('Hello')