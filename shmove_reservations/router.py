from rest_framework import routers
<<<<<<< HEAD
# from works.views import Works_view # example of rest api view import


router = routers.DefaultRouter()
# router.register('works', Works_view) # example of how to register a function as api route
=======
from barber.views import TestView, NewAppointments, GetAppointments  # example of rest api view import


router = routers.DefaultRouter()
router.register('test', TestView)  # example of how to register a function as api route
router.register('appointments', GetAppointments)
>>>>>>> 6d2b6ad... frontend merged
