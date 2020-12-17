from rest_framework import routers
from barber.views import AppointmentsView  # example of rest api view import


router = routers.DefaultRouter()
router.register('appointments', AppointmentsView)
