from rest_framework import routers

from barber.views import AppointmentsView, DashboardAppointmentView  # example of rest api view import


router = routers.DefaultRouter()
router.register('appointments', AppointmentsView)
