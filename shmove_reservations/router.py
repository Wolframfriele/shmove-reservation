from rest_framework import routers
# example of rest api view import
from barber.views import TestView, AppointmentsView
from dashboard.views import DashboardView

router = routers.DefaultRouter()
# example of how to register a function as api route
router.register('test', TestView)
router.register('appointments', AppointmentsView)
router.register('dashboard', DashboardView)
