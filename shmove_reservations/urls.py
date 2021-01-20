"""shmove_reservations URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib import admin
from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from .router import router
from shmove_reservations import views
from django.conf.urls import url
from django.views.generic import TemplateView
from dashboard import views as dash_view

urlpatterns = [

    path('admin/', admin.site.urls),  # load admin urls
    path('api/', include(router.urls)),  # api base route
    path('api/signin/', dash_view.signin),
    # embeded static frontend files
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    # frontend urls
    # path('/', views.home, name='home'),
    path('afspraak-maken/', views.afspraak_maken, name='afspraak-maken'),
    path('afspraak-bevestigen/', views.afspraak_bevestigen,
         name='afspraak-bevestigen/'),
    path('afspraak-geboekt/', views.afspraak_geboekt, name='afspraak-geboekt'),
    path('dashboard/', views.dashboard, name='dashboard'),

] + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT,
)
