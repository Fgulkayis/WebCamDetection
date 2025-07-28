from django.shortcuts import render

def index(request):
    return render(request, 'camera_app/index.html')
