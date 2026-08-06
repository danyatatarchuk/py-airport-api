from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
)

router = DefaultRouter()

router.register("airports", AirportViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = router.urls
