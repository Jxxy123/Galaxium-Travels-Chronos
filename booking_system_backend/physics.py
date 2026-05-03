"""
Physics calculations for relativistic space travel.

This module implements special relativity calculations for Project Chronos,
including Lorentz factor and time dilation effects.
"""

import math
from typing import Tuple


def calculate_lorentz_factor(velocity: float) -> float:
    """
    Calculate the Lorentz factor (gamma) for a given velocity.
    
    The Lorentz factor is: γ = 1/√(1-v²/c²)
    
    Args:
        velocity: Velocity as a fraction of the speed of light (0.0 to 0.99)
                 For example, 0.5 means 50% of light speed
    
    Returns:
        The Lorentz factor (gamma). Always >= 1.0
        - At v=0: γ=1 (no time dilation)
        - At v=0.5c: γ≈1.15 (15% time dilation)
        - At v=0.9c: γ≈2.29 (time passes 2.29x slower)
        - At v=0.99c: γ≈7.09 (time passes 7x slower)
    
    Raises:
        ValueError: If velocity is outside valid range [0, 0.99]
    """
    if velocity < 0 or velocity >= 1.0:
        raise ValueError(f"Velocity must be between 0 and 0.99 (got {velocity})")
    
    # Handle edge case of zero velocity
    if velocity == 0:
        return 1.0
    
    # Calculate γ = 1/√(1-v²/c²)
    # Since velocity is already as fraction of c, we use v² directly
    v_squared = velocity ** 2
    denominator = math.sqrt(1 - v_squared)
    
    return 1.0 / denominator


def calculate_time_dilation(coordinate_time_hours: float, velocity: float) -> Tuple[float, float, float]:
    """
    Calculate time dilation effects for a space journey.
    
    Args:
        coordinate_time_hours: Duration in stationary reference frame (Earth time)
        velocity: Velocity as fraction of speed of light (0.0 to 0.99)
    
    Returns:
        Tuple of (lorentz_factor, time_dilation_factor, proper_time_hours)
        - lorentz_factor: The γ value
        - time_dilation_factor: How much slower time passes (1/γ)
        - proper_time_hours: Time experienced by passengers (τ = t/γ)
    
    Example:
        For an 8-hour flight at 0.9c:
        >>> calculate_time_dilation(8.0, 0.9)
        (2.294, 0.436, 3.488)
        
        This means:
        - Lorentz factor is 2.294
        - Time passes 43.6% as fast on the ship
        - Passengers experience only 3.488 hours
    """
    lorentz_factor = calculate_lorentz_factor(velocity)
    
    # Time dilation factor: how much slower time passes (1/γ)
    time_dilation_factor = 1.0 / lorentz_factor
    
    # Proper time: time experienced by passengers (τ = t/γ)
    proper_time_hours = coordinate_time_hours * time_dilation_factor
    
    return lorentz_factor, time_dilation_factor, proper_time_hours


def get_velocity_description(velocity: float) -> str:
    """
    Get a human-readable description of the velocity.
    
    Args:
        velocity: Velocity as fraction of speed of light
    
    Returns:
        Description string like "50% light speed" or "0.9c"
    """
    if velocity == 0:
        return "Stationary"
    elif velocity < 0.01:
        return f"{velocity*100:.2f}% light speed"
    elif velocity < 0.1:
        return f"{velocity*100:.1f}% light speed"
    else:
        return f"{velocity:.2f}c"


def get_time_dilation_description(lorentz_factor: float) -> str:
    """
    Get a human-readable description of time dilation effects.
    
    Args:
        lorentz_factor: The Lorentz factor (gamma)
    
    Returns:
        Description like "Time passes 43.6% as fast on ship"
    """
    if lorentz_factor <= 1.01:
        return "Negligible time dilation"
    
    time_dilation_factor = 1.0 / lorentz_factor
    percentage = time_dilation_factor * 100
    
    return f"Time passes {percentage:.1f}% as fast on ship"

# Made with Bob
