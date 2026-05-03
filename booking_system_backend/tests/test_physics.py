"""
Tests for physics calculations (Lorentz factor and time dilation).
"""

import pytest
import math
from physics import (
    calculate_lorentz_factor,
    calculate_time_dilation,
    get_velocity_description,
    get_time_dilation_description
)


class TestLorentzFactor:
    """Tests for Lorentz factor calculation."""
    
    def test_zero_velocity(self):
        """At rest, Lorentz factor should be 1."""
        gamma = calculate_lorentz_factor(0.0)
        assert gamma == 1.0
    
    def test_half_light_speed(self):
        """At 0.5c, gamma should be approximately 1.155."""
        gamma = calculate_lorentz_factor(0.5)
        assert abs(gamma - 1.155) < 0.001
    
    def test_high_velocity(self):
        """At 0.9c, gamma should be approximately 2.294."""
        gamma = calculate_lorentz_factor(0.9)
        assert abs(gamma - 2.294) < 0.001
    
    def test_very_high_velocity(self):
        """At 0.99c, gamma should be approximately 7.089."""
        gamma = calculate_lorentz_factor(0.99)
        assert abs(gamma - 7.089) < 0.001
    
    def test_invalid_velocity_negative(self):
        """Negative velocity should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_lorentz_factor(-0.1)
    
    def test_invalid_velocity_too_high(self):
        """Velocity >= 1.0 should raise ValueError."""
        with pytest.raises(ValueError):
            calculate_lorentz_factor(1.0)
        with pytest.raises(ValueError):
            calculate_lorentz_factor(1.5)
    
    def test_lorentz_factor_always_greater_than_one(self):
        """Lorentz factor should always be >= 1."""
        for v in [0.0, 0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]:
            gamma = calculate_lorentz_factor(v)
            assert gamma >= 1.0


class TestTimeDilation:
    """Tests for time dilation calculations."""
    
    def test_no_time_dilation_at_rest(self):
        """At rest, proper time equals coordinate time."""
        gamma, factor, proper_time = calculate_time_dilation(8.0, 0.0)
        assert gamma == 1.0
        assert factor == 1.0
        assert proper_time == 8.0
    
    def test_time_dilation_at_half_c(self):
        """At 0.5c, time passes slower on ship."""
        gamma, factor, proper_time = calculate_time_dilation(8.0, 0.5)
        assert gamma > 1.0
        assert factor < 1.0
        assert proper_time < 8.0
        # At 0.5c, passengers experience about 6.93 hours
        assert abs(proper_time - 6.93) < 0.1
    
    def test_time_dilation_at_high_velocity(self):
        """At 0.9c, significant time dilation occurs."""
        gamma, factor, proper_time = calculate_time_dilation(8.0, 0.9)
        # Lorentz factor ~2.294
        assert abs(gamma - 2.294) < 0.01
        # Time dilation factor ~0.436
        assert abs(factor - 0.436) < 0.01
        # Proper time ~3.49 hours
        assert abs(proper_time - 3.49) < 0.1
    
    def test_extreme_time_dilation(self):
        """At 0.99c, extreme time dilation occurs."""
        gamma, factor, proper_time = calculate_time_dilation(24.0, 0.99)
        # Lorentz factor ~7.089
        assert abs(gamma - 7.089) < 0.01
        # Passengers experience only ~3.39 hours
        assert abs(proper_time - 3.39) < 0.1
    
    def test_time_dilation_factor_is_reciprocal(self):
        """Time dilation factor should be 1/gamma."""
        for v in [0.3, 0.5, 0.7, 0.9]:
            gamma, factor, _ = calculate_time_dilation(10.0, v)
            assert abs(factor - (1.0 / gamma)) < 0.0001


class TestDescriptions:
    """Tests for human-readable descriptions."""
    
    def test_velocity_descriptions(self):
        """Test velocity description formatting."""
        assert get_velocity_description(0.0) == "Stationary"
        assert "0.50" in get_velocity_description(0.005)
        assert "5.0%" in get_velocity_description(0.05)
        assert "0.50c" in get_velocity_description(0.5)
        assert "0.90c" in get_velocity_description(0.9)
    
    def test_time_dilation_descriptions(self):
        """Test time dilation description formatting."""
        desc_rest = get_time_dilation_description(1.0)
        assert "Negligible" in desc_rest
        
        desc_half_c = get_time_dilation_description(1.155)
        assert "86.6%" in desc_half_c or "86.5%" in desc_half_c
        
        desc_high = get_time_dilation_description(2.294)
        assert "43.6%" in desc_high or "43.5%" in desc_high


class TestRealWorldScenarios:
    """Tests based on actual flight scenarios."""
    
    def test_earth_to_mars_flight(self):
        """Test Earth-Mars flight at 0.65c for 8 hours."""
        gamma, factor, proper_time = calculate_time_dilation(8.0, 0.65)
        
        # At 0.65c, gamma ≈ 1.32
        assert 1.3 < gamma < 1.35
        
        # Passengers experience about 6 hours
        assert 5.9 < proper_time < 6.1
        
        # Time passes about 76% as fast
        assert 0.75 < factor < 0.77
    
    def test_earth_to_pluto_extreme_flight(self):
        """Test Earth-Pluto flight at 0.95c for 24 hours."""
        gamma, factor, proper_time = calculate_time_dilation(24.0, 0.95)
        
        # At 0.95c, gamma ≈ 3.2
        assert 3.1 < gamma < 3.3
        
        # Passengers experience only about 7.5 hours
        assert 7.0 < proper_time < 8.0
        
        # Time passes about 31% as fast
        assert 0.30 < factor < 0.33
    
    def test_moon_short_hop(self):
        """Test Earth-Moon short hop at 0.3c for 4 hours."""
        gamma, factor, proper_time = calculate_time_dilation(4.0, 0.3)
        
        # At 0.3c, minimal time dilation (gamma ≈ 1.05)
        assert 1.04 < gamma < 1.06
        
        # Passengers experience about 3.8 hours
        assert 3.7 < proper_time < 3.9
        
        # Time passes about 95% as fast
        assert 0.94 < factor < 0.96

# Made with Bob
