from rest_framework import routers
from barber.views import AppointmentsView  # example of rest api view import
from dashboard.views import DashboardView


router = routers.DefaultRouter()
router.register('appointments', AppointmentsView)
router.register('dashboard', DashboardView)
