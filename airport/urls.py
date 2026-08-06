from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
)

router = DefaultRouter()

router.register(
    "airports",
    AirportViewSet,
)

router.register(
    "airplane-types",
    AirplaneTypeViewSet,
)

urlpatterns = router.urls
