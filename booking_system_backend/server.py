from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from sqlalchemy.orm import Session
from typing import Union, Optional
from dotenv import load_dotenv
import os
import httpx
from .db import SessionLocal, init_db, get_db
from .seed import seed
from .services import flight, user, booking
from .schemas import FlightOut, BookingOut, UserOut, ErrorResponse, BookingRequest, UserRegistration

# Load environment variables from .env file
load_dotenv()


# ==================== MCP SERVER (for AI agents) ====================
# NOTE: MCP server must be created before FastAPI app to properly combine lifespans

mcp = FastMCP("Galaxium Booking System")


@mcp.tool()
def list_flights() -> list[FlightOut]:
    """List all available flights.
    Returns a list of flights with origin, destination, times, price, and seats available."""
    db = SessionLocal()
    try:
        return flight.list_flights(db)
    finally:
        db.close()


@mcp.tool()
def book_flight(user_id: int, name: str, flight_id: int, seat_class: str = "economy") -> BookingOut:
    """Book a seat on a specific flight for a user in the specified seat class.
    Requires user_id, name, and flight_id.
    Optional seat_class: 'economy' (default), 'business', or 'galaxium'.
    Decrements available seats for the selected class if successful.
    Returns booking details or raises an error if booking is not possible."""
    db = SessionLocal()
    try:
        result = booking.book_flight(db, user_id, name, flight_id, seat_class)
        if isinstance(result, ErrorResponse):
            raise Exception(result.details or result.error)
        return result
    finally:
        db.close()


@mcp.tool()
def get_bookings(user_id: int) -> list[BookingOut]:
    """Retrieve all bookings for a specific user by user_id.
    Returns a list of booking details for the user."""
    db = SessionLocal()
    try:
        return booking.get_bookings(db, user_id)
    finally:
        db.close()


@mcp.tool()
def cancel_booking(booking_id: int) -> BookingOut:
    """Cancel an existing booking by its booking_id.
    Increments available seats for the flight if successful.
    Returns updated booking details or raises an error if already cancelled or not found."""
    db = SessionLocal()
    try:
        result = booking.cancel_booking(db, booking_id)
        if isinstance(result, ErrorResponse):
            raise Exception(result.details or result.error)
        return result
    finally:
        db.close()


@mcp.tool()
def register_user(name: str, email: str) -> UserOut:
    """Register a new user with a name and unique email.
    Returns the created user's details or raises an error if the email is already registered."""
    db = SessionLocal()
    try:
        result = user.register_user(db, name, email)
        if isinstance(result, ErrorResponse):
            raise Exception(result.details or result.error)
        return result
    finally:
        db.close()


@mcp.tool()
def get_user_id(name: str, email: str) -> UserOut:
    """Retrieve a user's information, including user_id, by providing both name and email.
    Returns user details or raises an error if not found."""
    db = SessionLocal()
    try:
        result = user.get_user(db, name, email)
        if isinstance(result, ErrorResponse):
            raise Exception(result.details or result.error)
        return result
    finally:
        db.close()


# Create the MCP HTTP app for mounting
mcp_app = mcp.http_app()


# ==================== LIFESPAN ====================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()

    should_seed = os.getenv("SEED_DEMO_DATA", "true").lower() in {"1", "true", "yes", "on"}
    if should_seed:
        seed()

    yield
    # Shutdown (nothing to do)


# ==================== FASTAPI APP (REST + Swagger UI) ====================

app = FastAPI(
    title="Galaxium Booking System",
    description="API for booking interplanetary flights. Swagger UI available at /docs",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/api"  # Add this for ALB routing
)

# Get allowed origins from environment
allowed_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "OK"}


@app.get("/flights", response_model=list[FlightOut], tags=["Flights"])
def get_flights(
    # Basic filters from main branch
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    departure_date_from: Optional[str] = None,
    departure_date_to: Optional[str] = None,
    min_price: Optional[int] = None,
    max_price: Optional[int] = None,
    has_economy: Optional[bool] = None,
    has_business: Optional[bool] = None,
    has_galaxium: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = 'asc',
    # Phase 1: Core Filters from feature branch
    sort_by: Optional[str] = None,
    sort_order: Optional[str] = None,
    seat_class: Optional[str] = None,
    # Phase 2: Additional Filters from feature branch
    departure_time_period: Optional[str] = None,
    min_duration: Optional[int] = None,
    max_duration: Optional[int] = None,
    min_seats_available: Optional[int] = None,
    # Phase 3: Popular Routes from feature branch
    route_category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List all available flights with optional filtering and sorting.
    
    All query parameters are optional for backward compatibility.
    
    **Basic Filters:**
    - origin: Filter by origin (case-insensitive partial match)
    - destination: Filter by destination (case-insensitive partial match)
    - departure_date_from: Filter flights departing on or after this date (ISO format)
    - departure_date_to: Filter flights departing on or before this date (ISO format)
    - min_price: Minimum price (checks economy price)
    - max_price: Maximum price (checks economy price)
    - has_economy: Only flights with economy seats available
    - has_business: Only flights with business seats available
    - has_galaxium: Only flights with galaxium seats available
    - sort: Sort by 'price', 'departure_time', or 'duration'
    - order: Sort order 'asc' or 'desc' (default: asc)
    
    **Phase 1 - Core Filters:**
    - sort_by: Field to sort by (departure_time, base_price, duration, seats_available)
    - sort_order: Sort direction (asc, desc)
    - seat_class: Filter by seat class availability (economy, business, galaxium)
    
    **Phase 2 - Additional Filters:**
    - departure_time_period: Time of day (morning, afternoon, evening, night)
    - min_duration: Minimum flight duration in hours
    - max_duration: Maximum flight duration in hours
    - min_seats_available: Minimum total seats available
    
    **Phase 3 - Popular Routes:**
    - route_category: Route category (inner_planets, outer_planets, moons)
    """
    return flight.list_flights(
        db=db,
        origin=origin,
        destination=destination,
        departure_date_from=departure_date_from,
        departure_date_to=departure_date_to,
        min_price=min_price,
        max_price=max_price,
        has_economy=has_economy,
        has_business=has_business,
        has_galaxium=has_galaxium,
        sort=sort,
        order=order,
        sort_by=sort_by,
        sort_order=sort_order,
        seat_class=seat_class,
        departure_time_period=departure_time_period,
        min_duration=min_duration,
        max_duration=max_duration,
        min_seats_available=min_seats_available,
        route_category=route_category
    )


@app.post("/book", response_model=Union[BookingOut, ErrorResponse], tags=["Bookings"])
def book_flight_endpoint(request: BookingRequest, db: Session = Depends(get_db)):
    """Book a seat on a specific flight for a user in the specified seat class.

    Requires user_id, name, and flight_id.
    Optional seat_class: 'economy' (default), 'business', or 'galaxium'.
    Decrements available seats for the selected class if successful.
    """
    return booking.book_flight(db, request.user_id, request.name, request.flight_id, request.seat_class)


@app.get("/bookings/{user_id}", response_model=list[BookingOut], tags=["Bookings"])
def get_user_bookings(user_id: int, db: Session = Depends(get_db)):
    """Retrieve all bookings for a specific user by user_id."""
    return booking.get_bookings(db, user_id)


@app.post("/cancel/{booking_id}", response_model=Union[BookingOut, ErrorResponse], tags=["Bookings"])
def cancel_booking_endpoint(booking_id: int, db: Session = Depends(get_db)):
    """Cancel an existing booking by its booking_id.

    Increments available seats for the flight if successful.
    """
    return booking.cancel_booking(db, booking_id)


@app.post("/register", response_model=Union[UserOut, ErrorResponse], tags=["Users"])
def register_user_endpoint(request: UserRegistration, db: Session = Depends(get_db)):
    """Register a new user with a name and unique email."""
    return user.register_user(db, request.name, request.email)


@app.get("/user", response_model=Union[UserOut, ErrorResponse], tags=["Users"])
def get_user_endpoint(name: str, email: str, db: Session = Depends(get_db)):
    """Get user by name and email."""
    return user.get_user(db, name, email)


# ==================== JAVA SERVICE INTEGRATION ====================

JAVA_SERVICE_URL = os.getenv("JAVA_SERVICE_URL", "http://localhost:8080")


@app.post("/internal/bookings/from-hold", response_model=BookingOut, tags=["Internal"])
def create_booking_from_hold(hold_data: dict, db: Session = Depends(get_db)):
    """Internal endpoint for Java hold service to create bookings.

    This endpoint is called by the Java inventory hold service when confirming a hold.
    Returns HTTP 400 on booking failure so the Java service can detect and propagate the error.
    """
    result = booking.book_flight(
        db,
        user_id=hold_data["travelerId"],
        name=hold_data["travelerName"],
        flight_id=hold_data["flightId"],
        seat_class=hold_data["seatClass"]
    )
    if isinstance(result, ErrorResponse):
        raise HTTPException(status_code=400, detail=result.model_dump())
    return result


# ==================== JAVA SERVICE PROXY ENDPOINTS ====================

@app.post("/quotes", tags=["Quotes"])
async def create_quote(quote_data: dict, db: Session = Depends(get_db)):
    """Proxy endpoint to create a hold in the Java hold service.
    
    Note: The Java service doesn't have a separate 'quote' concept.
    This endpoint directly creates a hold and returns it as a quote.
    """
    # Get flight to calculate price first
    from .models import Flight
    from .services.booking import SEAT_CLASS_MULTIPLIERS
    
    flight_id = quote_data.get("flightId")
    seat_class = quote_data.get("seatClass", "economy")
    quantity = quote_data.get("quantity", 1)
    
    flight = db.query(Flight).filter(Flight.flight_id == flight_id).first()
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")
    
    # Calculate prices
    multiplier = SEAT_CLASS_MULTIPLIERS.get(seat_class, 1.0)
    price_per_seat = flight.base_price * multiplier
    total_price = price_per_seat * quantity
    
    # Transform frontend camelCase to Java snake_case and include price data
    hold_request = {
        "flight_id": quote_data.get("flightId"),
        "seat_class": quote_data.get("seatClass"),
        "quantity": quote_data.get("quantity", 1),
        "duration_minutes": quote_data.get("durationMinutes", 15),
        "price_per_seat": price_per_seat,
        "total_price": total_price
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{JAVA_SERVICE_URL}/api/v1/holds", json=hold_request)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())
        
        # Enrich response with price data and transform to Quote format
        hold_data = response.json()
        quote_response = {
            "quoteId": str(hold_data.get("holdId")),  # Java serializes as "holdId" not "id"
            "flightId": hold_data.get("flightId"),
            "seatClass": hold_data.get("seatClass"),
            "quantity": hold_data.get("quantity"),
            "pricePerSeat": price_per_seat,
            "totalPrice": total_price,
            "expiresAt": hold_data.get("expiresAt"),
            "createdAt": hold_data.get("createdAt"),
            "status": "CREATED"
        }
        return quote_response


@app.get("/quotes/{quote_id}", tags=["Quotes"])
async def get_quote(quote_id: str, db: Session = Depends(get_db)):
    """Proxy endpoint to get a hold from the Java hold service (returned as a quote)."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JAVA_SERVICE_URL}/api/v1/holds/{quote_id}",
                timeout=30.0
            )
            response.raise_for_status()
            hold_data = response.json()
            
            # Get flight to calculate price
            from .models import Flight
            from .services.booking import SEAT_CLASS_MULTIPLIERS
            
            flight_id = hold_data.get("flightId")
            seat_class = hold_data.get("seatClass", "economy")
            quantity = hold_data.get("quantity", 1)
            
            flight = db.query(Flight).filter(Flight.flight_id == flight_id).first()
            if not flight:
                return {"error": "Flight not found"}
            
            # Calculate prices
            multiplier = SEAT_CLASS_MULTIPLIERS.get(seat_class, 1.0)
            price_per_seat = flight.base_price * multiplier
            total_price = price_per_seat * quantity
            
            # Transform to Quote format
            quote_response = {
                "quoteId": str(hold_data.get("holdId")),  # Java serializes as "holdId" not "id"
                "flightId": hold_data.get("flightId"),
                "seatClass": hold_data.get("seatClass"),
                "quantity": hold_data.get("quantity"),
                "pricePerSeat": price_per_seat,
                "totalPrice": total_price,
                "expiresAt": hold_data.get("expiresAt"),
                "createdAt": hold_data.get("createdAt"),
                "status": "CREATED"
            }
            return quote_response
        except httpx.HTTPError as e:
            return {"error": f"Failed to get quote: {str(e)}"}


@app.post("/quotes/{quote_id}/holds", tags=["Holds"])
async def create_hold(quote_id: str):
    """Proxy endpoint - in the Java service, quotes and holds are the same.
    
    This endpoint returns the existing hold (quote) without creating a new one.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JAVA_SERVICE_URL}/api/v1/holds/{quote_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to create hold: {str(e)}"}


@app.get("/holds/{hold_id}", tags=["Holds"])
async def get_hold(hold_id: str):
    """Proxy endpoint to get a hold from the Java hold service."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{JAVA_SERVICE_URL}/api/v1/holds/{hold_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to get hold: {str(e)}"}


@app.post("/holds/{hold_id}/confirm", tags=["Holds"])
async def confirm_hold(hold_id: str):
    """Proxy endpoint to confirm a hold in the Java hold service."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{JAVA_SERVICE_URL}/api/v1/holds/{hold_id}/confirm",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to confirm hold: {str(e)}"}


@app.post("/holds/{hold_id}/release", tags=["Holds"])
async def release_hold(hold_id: str):
    """Proxy endpoint to release a hold in the Java hold service."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                f"{JAVA_SERVICE_URL}/api/v1/holds/{hold_id}",
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": f"Failed to release hold: {str(e)}"}

    """Retrieve a user's information by providing both name and email."""
    return user.get_user(db, name, email)


# ==================== MOUNT MCP INTO FASTAPI ====================

app.mount("/mcp", mcp_app)


# ==================== MAIN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
