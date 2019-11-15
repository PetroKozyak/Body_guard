from rest_framework import routers
from .views import UserView, JobViewSet, GuardFirmViewSet, FirmFeedbackViewSet, OrderViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r"users", UserView, basename="users")
router.register(r"jobs", JobViewSet, basename="jobs")
router.register(r"guard_firm", GuardFirmViewSet, basename="guard")
router.register(r"feed_back", FirmFeedbackViewSet, basename="feed_back")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path(r'', include(router.urls))
]