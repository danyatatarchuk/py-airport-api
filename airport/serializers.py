from rest_framework import serializers

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Crew,
    Flight,
    Order,
    Route,
    Ticket,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    route_info = serializers.SerializerMethodField()
    airplane_info = serializers.SerializerMethodField()
    crew_info = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = [
            "id",
            "route",
            "route_info",
            "airplane",
            "airplane_info",
            "crew",
            "crew_info",
            "departure_time",
            "arrival_time",
        ]

    def get_route_info(self, obj):
        return {
            "id": obj.route.id,
            "source": obj.route.source.name,
            "destination": obj.route.destination.name,
            "distance": obj.route.distance,
        }

    def get_airplane_info(self, obj):
        return {
            "id": obj.airplane.id,
            "name": obj.airplane.name,
            "rows": obj.airplane.rows,
            "seats_in_row": obj.airplane.seats_in_row,
            "airplane_type": obj.airplane.airplane_type.name,
        }

    def get_crew_info(self, obj):
        return [
            {
                "id": crew.id,
                "first_name": crew.first_name,
                "last_name": crew.last_name,
            }
            for crew in obj.crew.all()
        ]

    def validate(self, attrs):
        departure_time = attrs.get(
            "departure_time",
            getattr(self.instance, "departure_time", None),
        )
        arrival_time = attrs.get(
            "arrival_time",
            getattr(self.instance, "arrival_time", None),
        )

        if departure_time and arrival_time:
            if arrival_time <= departure_time:
                raise serializers.ValidationError(
                    "Arrival time must be later than departure time."
                )

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs):
        flight = attrs.get(
            "flight",
            getattr(self.instance, "flight", None),
        )
        row = attrs.get(
            "row",
            getattr(self.instance, "row", None),
        )
        seat = attrs.get(
            "seat",
            getattr(self.instance, "seat", None),
        )

        if flight and row is not None and seat is not None:
            if row < 1 or row > flight.airplane.rows:
                raise serializers.ValidationError(
                    f"Row must be between 1 and {flight.airplane.rows}."
                )

            if seat < 1 or seat > flight.airplane.seats_in_row:
                raise serializers.ValidationError(
                    f"Seat must be between 1 and {flight.airplane.seats_in_row}."
                )

            tickets = Ticket.objects.filter(
                flight=flight,
                row=row,
                seat=seat,
            )

            if self.instance:
                tickets = tickets.exclude(pk=self.instance.pk)

            if tickets.exists():
                raise serializers.ValidationError(
                    "This seat is already booked for this flight."
                )

        return attrs
