from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Flight,
    Order,
    Route,
    Ticket,
)
from airport.serializers import RouteSerializer, TicketSerializer
from airport.views import OrderViewSet, TicketViewSet


class RouteSerializerTests(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(
            name="Kyiv Airport",
            closest_big_city="Kyiv",
        )

    def test_source_and_destination_cannot_be_the_same(self):
        data = {
            "source": self.airport.id,
            "destination": self.airport.id,
            "distance": 100,
        }

        serializer = RouteSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)


class TicketSerializerTests(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(
            name="Kyiv Airport",
            closest_big_city="Kyiv",
        )

        self.destination = Airport.objects.create(
            name="Lviv Airport",
            closest_big_city="Lviv",
        )

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737-800",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.route = Route.objects.create(
            source=self.airport,
            destination=self.destination,
            distance=500,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-08-10T10:00:00Z",
            arrival_time="2026-08-10T12:00:00Z",
        )

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.order = Order.objects.create(
            user=self.user,
        )

    def test_row_cannot_exceed_airplane_capacity(self):
        data = {
            "row": 11,
            "seat": 1,
            "flight": self.flight.id,
            "order": self.order.id,
        }

        serializer = TicketSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_seat_cannot_exceed_airplane_capacity(self):
        data = {
            "row": 1,
            "seat": 7,
            "flight": self.flight.id,
            "order": self.order.id,
        }

        serializer = TicketSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_valid_ticket(self):
        data = {
            "row": 1,
            "seat": 1,
            "flight": self.flight.id,
            "order": self.order.id,
        }

        serializer = TicketSerializer(data=data)

        self.assertTrue(serializer.is_valid())


class OrderViewSetTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="user1",
            password="password1",
        )

        self.other_user = user_model.objects.create_user(
            username="user2",
            password="password2",
        )

        self.user_order = Order.objects.create(
            user=self.user,
        )

        self.other_order = Order.objects.create(
            user=self.other_user,
        )

        self.factory = APIRequestFactory()

    def test_user_can_see_only_own_orders(self):
        request = self.factory.get("/orders/")
        request.user = self.user

        view = OrderViewSet()
        view.request = request

        queryset = view.get_queryset()

        self.assertIn(self.user_order, queryset)
        self.assertNotIn(self.other_order, queryset)


class TicketViewSetTests(TestCase):
    def setUp(self):
        user_model = get_user_model()

        self.user = user_model.objects.create_user(
            username="user1",
            password="password1",
        )

        self.other_user = user_model.objects.create_user(
            username="user2",
            password="password2",
        )

        self.user_order = Order.objects.create(
            user=self.user,
        )

        self.other_order = Order.objects.create(
            user=self.other_user,
        )

        self.airport = Airport.objects.create(
            name="Kyiv Airport",
            closest_big_city="Kyiv",
        )

        self.destination = Airport.objects.create(
            name="Lviv Airport",
            closest_big_city="Lviv",
        )

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737-800",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.route = Route.objects.create(
            source=self.airport,
            destination=self.destination,
            distance=500,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-08-10T10:00:00Z",
            arrival_time="2026-08-10T12:00:00Z",
        )

        self.user_ticket = Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.user_order,
        )

        self.other_ticket = Ticket.objects.create(
            row=1,
            seat=2,
            flight=self.flight,
            order=self.other_order,
        )

        self.factory = APIRequestFactory()

    def test_user_can_see_only_own_tickets(self):
        request = self.factory.get("/tickets/")
        request.user = self.user

        view = TicketViewSet()
        view.request = request

        queryset = view.get_queryset()

        self.assertIn(self.user_ticket, queryset)
        self.assertNotIn(self.other_ticket, queryset)


class TicketConstraintTests(TestCase):
    def setUp(self):
        self.airport = Airport.objects.create(
            name="Kyiv Airport",
            closest_big_city="Kyiv",
        )

        self.destination = Airport.objects.create(
            name="Lviv Airport",
            closest_big_city="Lviv",
        )

        self.airplane_type = AirplaneType.objects.create(
            name="Boeing 737",
        )

        self.airplane = Airplane.objects.create(
            name="Boeing 737-800",
            rows=10,
            seats_in_row=6,
            airplane_type=self.airplane_type,
        )

        self.route = Route.objects.create(
            source=self.airport,
            destination=self.destination,
            distance=500,
        )

        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time="2026-08-10T10:00:00Z",
            arrival_time="2026-08-10T12:00:00Z",
        )

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="testuser",
            password="testpassword",
        )

        self.order = Order.objects.create(
            user=self.user,
        )

    def test_same_seat_cannot_be_booked_twice_on_same_flight(self):
        Ticket.objects.create(
            row=1,
            seat=1,
            flight=self.flight,
            order=self.order,
        )

        with self.assertRaises(IntegrityError):
            Ticket.objects.create(
                row=1,
                seat=1,
                flight=self.flight,
                order=self.order,
            )
