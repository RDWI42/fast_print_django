from django.shortcuts import render

def index(request):
    context = {
        'heading': 'home'
    }

    return render(request, 'index.html',context)