# Project Chronos: Time Dilation Integration Plan

## Overview
Integrate special relativity physics into the Galaxium Travels booking system to show travelers how time dilation affects their journey based on flight velocity.

## Physics Foundation

### Lorentz Factor Formula
```
γ = 1 / √(1 - v²/c²)
```
Where:
- γ (gamma) = Lorentz factor (time dilation multiplier)
- v = velocity of the spacecraft
- c = speed of light
- v/c = velocity as fraction of light speed (0.0 to 1.0)

### Time Dilation Effect
```
Earth_time = γ × Ship_time
```
For every hour experienced on the ship, γ hours pass on Earth.

## Architecture Decisions

### 1. Velocity Storage
- **Format**: Decimal (0.0 to 1.0) representing v/c
- **Rationale**: Most intuitive for calculations, avoids unit conversion overhead
- **Example**: 0.75 = 75% of light speed

### 2. Database Schema Changes
**File**: [`booking_system_backend/models.py`](booking_system_backend/models.py:19)

Add to `Flight` model:
```python
velocity = Column(Float, nullable=False, default=0.0)  # v/c ratio (0.0-1.0)
```

### 3. API Response Schema
**File**: [`booking_system_backend/schemas.py`](booking_system_backend/schemas.py:32)

Extend `FlightOut`:
```python
velocity: float  # v/c ratio
lorentz_factor: float  # γ
ship_duration_hours: float  # Time experienced onboard
earth_duration_hours: float  # Time that passes on Earth
```

### 4. Physics Utility Module
**File**: `booking_system_backend/utils.py` (NEW)

```python
def calculate_lorentz_factor(v: float) -> float:
    """
    Calculate Lorentz factor (γ) for time dilation.
    
    Args:
        v: Velocity as fraction of light speed (0.0 to 1.0)
    
    Returns:
        Lorentz factor γ = 1/√(1 - v²/c²)
    
    Raises:
        ValueError: If v < 0 or v >= 1
    """

def calculate_time_dilation(ship_hours: float, v: float) -> dict:
    """
    Calculate time dilation effects.
    
    Args:
        ship_hours: Duration in ship reference frame
        v: Velocity as fraction of light speed
    
    Returns:
        {
            'ship_hours': float,
            'earth_hours': float,
            'lorentz_factor': float,
            'velocity': float
        }
    """
```

## Implementation Steps

### Backend Changes

#### Step 1: Create Physics Utility Module
**File**: `booking_system_backend/utils.py`
- Implement `calculate_lorentz_factor(v)`
- Implement `calculate_time_dilation(ship_hours, v)`
- Add input validation and edge case handling
- Include docstrings with physics explanations

#### Step 2: Update Database Model
**File**: [`booking_system_backend/models.py`](booking_system_backend/models.py:19)
- Add `velocity` column to `Flight` class
- Set default=0.0 for backward compatibility
- Add comment explaining v/c ratio

#### Step 3: Update Response Schema
**File**: [`booking_system_backend/schemas.py`](booking_system_backend/schemas.py:32)
- Add velocity, lorentz_factor, ship_duration_hours, earth_duration_hours to `FlightOut`
- Add docstring explaining time dilation fields

#### Step 4: Modify Flight Service
**File**: [`booking_system_backend/services/flight.py`](booking_system_backend/services/flight.py:17)
- Import utils module
- In `list_flights()`, after calculating duration_hours:
  ```python
  from utils import calculate_time_dilation
  
  # Calculate time dilation
  time_dilation = calculate_time_dilation(duration_hours, f.velocity)
  
  flight_dict = {
      # ... existing fields ...
      'velocity': f.velocity,
      'lorentz_factor': time_dilation['lorentz_factor'],
      'ship_duration_hours': time_dilation['ship_hours'],
      'earth_duration_hours': time_dilation['earth_hours']
  }
  ```

#### Step 5: Update Seed Data
**File**: [`booking_system_backend/seed.py`](booking_system_backend/seed.py:35)
- Extend flight_data tuples to include velocity
- Assign realistic velocities based on route distance:
  - Short routes (Earth-Moon): 0.3-0.4c
  - Medium routes (Earth-Mars): 0.5-0.6c
  - Long routes (Earth-Jupiter): 0.7-0.8c
  - Very long routes (Earth-Pluto): 0.85-0.9c

Example:
```python
flight_data = [
    ("Earth", "Mars", "2099-01-01T09:00:00Z", "2099-01-01T17:00:00Z", 1000000, 10, 0.55),
    # ... (origin, destination, departure, arrival, base_price, total_seats, velocity)
]
```

#### Step 6: Add Unit Tests
**File**: `booking_system_backend/tests/test_utils.py` (NEW)
- Test `calculate_lorentz_factor()`:
  - v=0 → γ=1 (no time dilation)
  - v=0.5 → γ≈1.155
  - v=0.866 → γ=2 (time doubles)
  - v=0.99 → γ≈7.089
  - v≥1 → ValueError
  - v<0 → ValueError
- Test `calculate_time_dilation()`:
  - Verify ship_hours × γ = earth_hours
  - Edge cases with v=0

### Frontend Changes

#### Step 7: Update TypeScript Types
**File**: [`booking_system_frontend/src/types/index.ts`](booking_system_frontend/src/types/index.ts:5)
```typescript
export interface Flight {
  // ... existing fields ...
  velocity: number;  // v/c ratio (0.0-1.0)
  lorentz_factor: number;  // γ factor
  ship_duration_hours: number;  // Time onboard
  earth_duration_hours: number;  // Time on Earth
}
```

#### Step 8: Create Physics Details Component
**File**: `booking_system_frontend/src/components/flights/PhysicsDetails.tsx` (NEW)
- Expandable section with toggle button
- Display velocity as percentage
- Show Lorentz factor with explanation
- Compare ship time vs Earth time
- Add educational tooltip explaining time dilation

#### Step 9: Update FlightCard Component
**File**: [`booking_system_frontend/src/components/flights/FlightCard.tsx`](booking_system_frontend/src/components/flights/FlightCard.tsx:12)
- Import PhysicsDetails component
- Add badge for high-velocity flights (v > 0.7c)
- Integrate expandable Physics Details section
- Use Zap icon from lucide-react for relativistic badge

Layout:
```tsx
{/* Existing flight info */}

{/* High-velocity badge */}
{flight.velocity > 0.7 && (
  <div className="flex items-center gap-1 text-alien-green">
    <Zap size={16} />
    <span className="text-xs">Relativistic Speed</span>
  </div>
)}

{/* Physics Details Section */}
<PhysicsDetails flight={flight} />
```

#### Step 10: Style Physics Details
- Use space theme colors (cosmic-purple, alien-green)
- Smooth expand/collapse animation
- Clear visual hierarchy
- Mobile-responsive layout

### Documentation

#### Step 11: Create Documentation
**File**: `PROJECT_CHRONOS.md` (NEW)
- Explain the physics behind time dilation
- Show example calculations
- Document API changes
- Include user-facing explanation
- Add references to special relativity

## Testing Strategy

### Unit Tests
- Physics calculations accuracy
- Edge cases (v=0, v→1)
- Input validation
- Error handling

### Integration Tests
- Flight listing with time dilation data
- Seed data with velocities
- API response structure

### Manual Testing
- Frontend display of physics data
- Expandable section functionality
- Badge visibility for high-velocity flights
- Mobile responsiveness

## Example Calculations

### Earth to Mars (v = 0.55c)
```
Duration: 8 hours (ship time)
γ = 1/√(1 - 0.55²) ≈ 1.198
Earth time = 1.198 × 8 ≈ 9.58 hours

Display: "For every 1 hour onboard, 1.2 hours pass on Earth"
```

### Earth to Pluto (v = 0.9c)
```
Duration: 24 hours (ship time)
γ = 1/√(1 - 0.9²) ≈ 2.294
Earth time = 2.294 × 24 ≈ 55.06 hours

Display: "For every 1 hour onboard, 2.3 hours pass on Earth"
```

## Migration Notes

### Database Migration
Since this is a demo using SQLite with ephemeral data:
- No formal migration needed
- Schema created via `Base.metadata.create_all()`
- Existing data will be re-seeded with velocities

### Backward Compatibility
- Default velocity=0.0 for any existing flights
- Frontend gracefully handles missing fields
- API remains compatible with old clients

## Success Criteria

✅ Lorentz factor calculation is mathematically correct
✅ Time dilation data appears in flight listings
✅ Frontend displays physics information clearly
✅ High-velocity flights show special badge
✅ Unit tests pass with >90% coverage
✅ Documentation explains the feature
✅ No breaking changes to existing API

## Future Enhancements

- Add velocity filter in flight search
- Show time dilation in booking confirmation
- Calculate "biological age" savings for travelers
- Add length contraction visualization
- Support for acceleration phases (non-constant velocity)

## References

- Einstein, A. (1905). "On the Electrodynamics of Moving Bodies"
- Taylor & Wheeler. "Spacetime Physics"
- [Lorentz Factor Calculator](https://www.omnicalculator.com/physics/lorentz-factor)

---

**Ready for Implementation**: This plan is ready to be executed in Code mode.