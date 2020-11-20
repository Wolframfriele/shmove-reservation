from django.shortcuts import render


def home(request):
    return render(request, template_name='index.html')

def appointment(request):
    return render(request, template_name='index.html')

def confirmation(request):
    return render(request, template_name='index.html')

def book_appointment(request):
    return render(request, template_name='index.html')

def dashboard(request):
    return render(request, template_name='index.html')