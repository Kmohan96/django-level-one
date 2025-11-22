from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def basic(requset):
    return HttpResponse("hello world")