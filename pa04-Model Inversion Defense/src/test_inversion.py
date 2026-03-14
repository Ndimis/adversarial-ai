import pytest
import numpy as np
from inversion_defense import PrivacyGuard

def test_output_rounding():
    """Ensure output is rounded to 2 decimal places to hide precision."""
    guard = PrivacyGuard()
    raw = np.array([0.987654, 0.012345])
    secure = guard.secure_output(raw)
    
    for val in secure:
        # Check if the value has more than 2 decimal places
        assert len(str(val).split('.')[-1]) <= 2

def test_privacy_noise():
    """Ensure the output is different from the raw input due to noise."""
    guard = PrivacyGuard(epsilon=0.1)
    raw = np.array([0.5, 0.5])
    secure = guard.secure_output(raw)
    
    # It's highly unlikely (nearly impossible) for noise-injected data 
    # to match the raw data exactly.
    assert not np.array_equal(raw, np.array(secure))

def test_normalization():
    """Ensure the secure output still roughly represents probabilities (sums to ~1)."""
    guard = PrivacyGuard()
    raw = np.array([0.8, 0.1, 0.1])
    secure = guard.secure_output(raw)
    assert 0.9 <= sum(secure) <= 1.1