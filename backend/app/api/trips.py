from fastapi import APIRouter

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("/")
def get_all_trips():
    """
    Response:
    [
        {
            "id": 1,
            "vehicle_id": 2,
            "driver_id": 5,
            "source": "Nagpur",
            "destination": "Pune",
            "status": "Draft"
        }
    ]
    """
    pass


@router.post("/")
def create_trip():
    """
    Request:
    {
        "vehicle_id": 2,
        "driver_id": 5,
        "source": "Nagpur",
        "destination": "Pune",
        "cargo_weight": 450,
        "distance": 800
    }

    Response:
    {
        "success": true,
        "message": "Trip created successfully",
        "data": {...}
    }
    """
    pass


@router.patch("/{trip_id}/dispatch")
def dispatch_trip(trip_id: int):
    """
    Business Rules:
    - Vehicle must be Available
    - Driver must be Available
    - Driver license must be valid
    - Cargo <= Vehicle Capacity
    - Update Trip status -> Dispatched
    - Update Driver status -> On Trip
    - Update Vehicle status -> On Trip
    """
    pass


@router.patch("/{trip_id}/complete")
def complete_trip(trip_id: int):
    """
    Request:
    {
        "final_odometer": 19200,
        "fuel_used": 35
    }

    Business Rules:
    - Trip -> Completed
    - Driver -> Available
    - Vehicle -> Available
    - Create Fuel Log
    """
    pass


@router.patch("/{trip_id}/cancel")
def cancel_trip(trip_id: int):
    """
    Business Rules:
    - Restore Driver status
    - Restore Vehicle status
    """
    pass