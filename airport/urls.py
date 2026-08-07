from rest_framework.routers import DefaultRouter

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    RouteViewSet,
)

router = DefaultRouter()

router.register("airports", AirportViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("routes", RouteViewSet)

urlpatterns = router.urls
