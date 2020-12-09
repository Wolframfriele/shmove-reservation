from rest_framework import routers
from barber.views import TestView, Appointments  # example of rest api view import


router = routers.DefaultRouter()
router.register('test', TestView)  # example of how to register a function as api route
router.register('appointments', Appointments)
