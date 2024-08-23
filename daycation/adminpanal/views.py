from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.
def adminindex(request):
    return render(request, 'adminindex.html')