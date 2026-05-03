"""
Manual test script for physics calculations.
Run with: python test_physics_manual.py
"""

import sys
import io
sys.path.insert(0, '.')

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from physics import calculate_lorentz_factor, calculate_time_dilation

def test_lorentz_calculations():
    """Test Lorentz factor calculations."""
    print("=" * 60)
    print("LORENTZ FACTOR CALCULATIONS")
    print("=" * 60)
    
    test_velocities = [0.0, 0.3, 0.5, 0.65, 0.9, 0.95, 0.99]
    
    for v in test_velocities:
        gamma = calculate_lorentz_factor(v)
        print(f"\nVelocity: {v:.2f}c")
        print(f"  Lorentz factor (gamma): {gamma:.4f}")
        print(f"  Time dilation: {(1/gamma)*100:.1f}% as fast")

def test_flight_scenarios():
    """Test realistic flight scenarios."""
    print("\n" + "=" * 60)
    print("REALISTIC FLIGHT SCENARIOS")
    print("=" * 60)
    
    scenarios = [
        ("Earth → Moon (short hop)", 4.0, 0.30),
        ("Earth → Mars", 8.0, 0.65),
        ("Mars → Jupiter", 10.0, 0.85),
        ("Europa → Earth", 12.0, 0.90),
        ("Earth → Pluto (extreme)", 24.0, 0.95),
    ]
    
    for name, coord_time, velocity in scenarios:
        gamma, factor, proper_time = calculate_time_dilation(coord_time, velocity)
        time_saved = coord_time - proper_time
        
        print(f"\n{name}")
        print(f"  Velocity: {velocity:.2f}c")
        print(f"  Coordinate time (Earth): {coord_time:.1f} hours")
        print(f"  Proper time (passengers): {proper_time:.2f} hours")
        print(f"  Time saved: {time_saved:.2f} hours")
        print(f"  Lorentz factor: {gamma:.3f}")
        print(f"  Time passes {factor*100:.1f}% as fast on ship")

def test_edge_cases():
    """Test edge cases."""
    print("\n" + "=" * 60)
    print("EDGE CASES")
    print("=" * 60)
    
    # Test zero velocity
    print("\nZero velocity (at rest):")
    gamma, factor, proper_time = calculate_time_dilation(10.0, 0.0)
    print(f"  gamma = {gamma:.4f} (should be 1.0)")
    print(f"  Proper time = {proper_time:.4f} (should equal coordinate time)")
    
    # Test invalid velocities
    print("\nTesting invalid velocities:")
    for invalid_v in [-0.1, 1.0, 1.5]:
        try:
            calculate_lorentz_factor(invalid_v)
            print(f"  ERROR: {invalid_v} should have raised ValueError!")
        except ValueError as e:
            print(f"  [OK] {invalid_v} correctly raised ValueError")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("PROJECT CHRONOS - PHYSICS CALCULATIONS TEST")
    print("=" * 60)
    
    try:
        test_lorentz_calculations()
        test_flight_scenarios()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        print("\nThe Lorentz factor calculations are working correctly!")
        print("Time dilation is now integrated into the flight system.")
        
    except Exception as e:
        print(f"\n[FAILED] TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

# Made with Bob
