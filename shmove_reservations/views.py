from django.shortcuts import render


# def home(request):
#     return render(request, template_name='index.html')


def afspraak_maken(request):
    return render(request, template_name='index.html')


def afspraak_bevestigen(request):
    return render(request, template_name='index.html')


def afspraak_geboekt(request):
    return render(request, template_name='index.html')


def dashboard(request):
    return render(request, template_name='index.html')
