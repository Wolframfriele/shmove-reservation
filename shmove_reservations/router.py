from rest_framework import routers
# example of rest api view import
from barber.views import AppointmentsView, DashboardAppointmentView
from dashboard.views import DashboardView


router = routers.DefaultRouter()
router.register('appointments', AppointmentsView)
router.register('dash_appointments', DashboardAppointmentView)
router.register('dashboard', DashboardView)
