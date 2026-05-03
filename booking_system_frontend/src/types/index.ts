// API Data Models matching backend schemas

export type SeatClass = 'economy' | 'business' | 'galaxium';

export interface Flight {
  flight_id: number;
  origin: string;
  destination: string;
  departure_time: string;
  arrival_time: string;
  base_price: number;
  economy_seats_available: number;
  business_seats_available: number;
  galaxium_seats_available: number;
  economy_price: number;
  business_price: number;
  galaxium_price: number;
  // Time dilation fields (Project Chronos)
  velocity: number;  // Fraction of speed of light (0.0-0.99)
  lorentz_factor: number;  // γ = 1/√(1-v²/c²)
  time_dilation_factor: number;  // How much slower time passes on ship
  proper_time_hours: number;  // Time experienced by passengers
}

export interface Booking {
  booking_id: number;
  user_id: number;
  flight_id: number;
  status: 'booked' | 'cancelled' | 'completed';
  booking_time: string;
  seat_class: SeatClass;
  price_paid: number;
}

export interface User {
  user_id: number;
  name: string;
  email: string;
}

// Request/Response types
export interface BookingRequest {
  user_id: number;
  name: string;
  flight_id: number;
  seat_class?: SeatClass;
}

export interface UserRegistration {
  name: string;
  email: string;
}

export interface ErrorResponse {
  success: false;
  error: string;
  error_code: string;
  details?: string;
}

// Extended types for UI
export interface BookingWithFlight extends Booking {
  flight?: Flight;
}

export interface FlightFilters {
  origin?: string;
  destination?: string;
  minPrice?: number;
  maxPrice?: number;
  searchTerm?: string;
}

// User context type
export interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
  logout: () => void;
}

// Java Inventory Hold Service types

export interface Quote {
  quoteId: string;
  flightId: number;
  seatClass: string;
  quantity: number;
  travelerId: number;
  travelerName: string;
  pricePerSeat: number;
  totalPrice: number;
  expiresAt: string;
  status: 'CREATED';
  createdAt: string;
}

export type HoldStatus = 'HELD' | 'EXPIRED' | 'CONFIRMED' | 'RELEASED' | 'CONFIRMATION_FAILED';

export interface Hold {
  holdId: string;  // Normalized to string in API layer (Java returns number)
  quoteId?: string;  // Optional - Java service doesn't use quotes
  flightId?: number;  // From Java Hold entity
  seatClass?: string;  // From Java Hold entity
  quantity?: number;  // From Java Hold entity
  pricePerSeat?: number;  // From Java Hold entity
  totalPrice?: number;  // From Java Hold entity
  status: HoldStatus | string;  // Java uses ACTIVE/EXPIRED/RELEASED/CONFIRMED
  expiresAt: string;  // Java service uses 'expiresAt', not 'reservedUntil'
  externalBookingReference?: string;
  errorMessage?: string;
  createdAt: string;
  updatedAt?: string;  // Optional - may not be present initially
}

// Persisted hold data (stored in localStorage for MyBookings display)
export interface StoredHold {
  holdId: string;
  quoteId: string;
  flightId: number;
  seatClass: SeatClass;
  pricePerSeat: number;
  totalPrice: number;
  reservedUntil: string;
}

// Made with Bob
