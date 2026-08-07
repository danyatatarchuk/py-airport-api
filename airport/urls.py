from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    CrewViewSet,
    FlightViewSet,
    RouteViewSet,
)

router = DefaultRouter()

router.register("airports", AirportViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)

urlpatterns = router.urls
