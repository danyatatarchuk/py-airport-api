# Airport API

A RESTful API for managing airports, airplane types, airplanes, routes, crews, flights, orders, and tickets.

The project is built with Django REST Framework and provides JWT authentication, CRUD operations, filtering, searching, pagination, Swagger documentation, and custom validation logic.

## Features

- JWT authentication
- Authenticated API access
- CRUD operations for airports
- CRUD operations for airplane types
- CRUD operations for airplanes
- CRUD operations for routes
- CRUD operations for crews
- CRUD operations for flights
- CRUD operations for orders
- CRUD operations for tickets
- Airport filtering
- Airport searching
- API pagination
- Detailed flight information
- Flight departure and arrival time validation
- Ticket seat availability validation
- Swagger API documentation
- Django Admin interface

## Technologies

- Python 3.11
- Django
- Django REST Framework
- Django Filter
- djangorestframework-simplejwt
- drf-spectacular
- SQLite
- Git
- GitHub

## Project Structure

    py-airport-api/
    │
    ├── airport/
    │   ├── migrations/
    │   ├── admin.py
    │   ├── apps.py
    │   ├── models.py
    │   ├── serializers.py
    │   ├── urls.py
    │   └── views.py
    │
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    │
    ├── db.sqlite3
    ├── manage.py
    ├── requirements.txt
    └── README.md

## Installation

### 1. Clone the repository

    git clone https://github.com/danyatatarchuk/py-airport-api.git
    cd py-airport-api

### 2. Create a virtual environment

    python3 -m venv venv

### 3. Activate the virtual environment

For macOS/Linux:

    source venv/bin/activate

For Windows:

    venv\Scripts\activate

### 4. Install dependencies

    pip install -r requirements.txt

### 5. Apply migrations

    python manage.py migrate

### 6. Create a superuser

    python manage.py createsuperuser

### 7. Run the development server

    python manage.py runserver

The API will be available at:

    http://127.0.0.1:8000/

## Authentication

The API uses JWT authentication with djangorestframework-simplejwt.

All API endpoints require authentication.

### Obtain JWT Token

Send a POST request to:

    /api/token/

with your username and password:

    {
        "username": "your_username",
        "password": "your_password"
    }

The response contains access and refresh tokens:

    {
        "refresh": "your_refresh_token",
        "access": "your_access_token"
    }

Use the access token in authenticated requests:

    Authorization: Bearer <access_token>

### Refresh Token

Send a POST request to:

    /api/token/refresh/

with:

    {
        "refresh": "your_refresh_token"
    }

## API Documentation

The project uses drf-spectacular for OpenAPI documentation.

### Swagger UI

Open:

    http://127.0.0.1:8000/api/doc/swagger/

To authorize requests:

1. Obtain an access token.
2. Open Swagger UI.
3. Click Authorize.
4. Enter:

       Bearer <access_token>

5. Click Authorize.

After authorization, authenticated endpoints can be tested directly from Swagger UI.

### OpenAPI Schema

The OpenAPI schema is available at:

    http://127.0.0.1:8000/api/schema/

## API Endpoints

All main API endpoints are available under:

    /api/airport/

### Airports

    GET     /api/airport/airports/
    POST    /api/airport/airports/
    GET     /api/airport/airports/{id}/
    PUT     /api/airport/airports/{id}/
    PATCH   /api/airport/airports/{id}/
    DELETE  /api/airport/airports/{id}/

### Airplane Types

    GET     /api/airport/airplane-types/
    POST    /api/airport/airplane-types/
    GET     /api/airport/airplane-types/{id}/
    PUT     /api/airport/airplane-types/{id}/
    PATCH   /api/airport/airplane-types/{id}/
    DELETE  /api/airport/airplane-types/{id}/

### Airplanes

    GET     /api/airport/airplanes/
    POST    /api/airport/airplanes/
    GET     /api/airport/airplanes/{id}/
    PUT     /api/airport/airplanes/{id}/
    PATCH   /api/airport/airplanes/{id}/
    DELETE  /api/airport/airplanes/{id}/

### Routes

    GET     /api/airport/routes/
    POST    /api/airport/routes/
    GET     /api/airport/routes/{id}/
    PUT     /api/airport/routes/{id}/
    PATCH   /api/airport/routes/{id}/
    DELETE  /api/airport/routes/{id}/

### Crews

    GET     /api/airport/crews/
    POST    /api/airport/crews/
    GET     /api/airport/crews/{id}/
    PUT     /api/airport/crews/{id}/
    PATCH   /api/airport/crews/{id}/
    DELETE  /api/airport/crews/{id}/

### Flights

    GET     /api/airport/flights/
    POST    /api/airport/flights/
    GET     /api/airport/flights/{id}/
    PUT     /api/airport/flights/{id}/
    PATCH   /api/airport/flights/{id}/
    DELETE  /api/airport/flights/{id}/

### Orders

    GET     /api/airport/orders/
    POST    /api/airport/orders/
    GET     /api/airport/orders/{id}/
    PUT     /api/airport/orders/{id}/
    PATCH   /api/airport/orders/{id}/
    DELETE  /api/airport/orders/{id}/

### Tickets

    GET     /api/airport/tickets/
    POST    /api/airport/tickets/
    GET     /api/airport/tickets/{id}/
    PUT     /api/airport/tickets/{id}/
    PATCH   /api/airport/tickets/{id}/
    DELETE  /api/airport/tickets/{id}/

## Filtering

Airport filtering is available by airport name and closest big city.

Example:

    GET /api/airport/airports/?name=Kyiv

or:

    GET /api/airport/airports/?closest_big_city=Kyiv

## Searching

Airport search is available by:

- airport name
- closest big city

Example:

    GET /api/airport/airports/?search=Kyiv

## Pagination

The API uses page-number pagination.

The default page size is 10 objects per page.

Example:

    GET /api/airport/airports/

A paginated response contains:

    {
        "count": 25,
        "next": "http://127.0.0.1:8000/api/airport/airports/?page=2",
        "previous": null,
        "results": []
    }

To request another page:

    GET /api/airport/airports/?page=2

## Custom Logic

### Flight Validation

The FlightSerializer contains custom validation for departure and arrival times.

The arrival time must be later than the departure time.

If:

    arrival_time <= departure_time

the API returns a validation error.

### Detailed Flight Information

The Flight serializer provides additional information about related objects.

It includes:

- route information
- source airport
- destination airport
- route distance
- airplane information
- airplane type
- crew members

### Ticket Seat Validation

The API prevents booking the same seat twice for the same flight.

A ticket is identified by:

- flight
- row
- seat

If a seat is already booked for a specific flight, creating another ticket for the same seat returns a validation error.

Example:

    {
        "non_field_errors": [
            "This seat is already booked for this flight."
        ]
    }

## Permissions

The default permission class is:

    IsAuthenticated

Therefore, users must provide a valid JWT access token to access the API endpoints.

## Admin Panel

The Django Admin interface is available at:

    http://127.0.0.1:8000/admin/

Create an administrator account using:

    python manage.py createsuperuser

## Database

The project uses SQLite.

The database file is:

    db.sqlite3

Main entities:

- Airport
- AirplaneType
- Airplane
- Route
- Crew
- Flight
- Order
- Ticket

## Project Check

Run:

    python manage.py check

Expected result:

    System check identified no issues (0 silenced).

## API Usage Workflow

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies.
4. Apply migrations.
5. Create a superuser.
6. Start the development server.
7. Obtain a JWT access token.
8. Open Swagger UI.
9. Authorize using the access token.
10. Use the API endpoints.
11. Use filtering, searching, and pagination when working with collections.
