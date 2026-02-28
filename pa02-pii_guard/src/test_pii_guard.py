import pytest
from pii_guard import PIIGuard

@pytest.fixture
def guard():
    return PIIGuard()

def test_email_redaction(guard):
    input_text = "Contact me at test@example.com for details."
    output = guard.scrub(input_text)
    assert "[EMAIL_REDACTED]" in output
    assert "test@example.com" not in output

def test_ip_redaction(guard):
    input_text = "The server is located at 192.168.1.1."
    output = guard.scrub(input_text)
    assert "[IPV4_REDACTED]" in output

def test_multiple_leaks(guard):
    input_text = "Email: a@b.com, IP: 1.1.1.1"
    output = guard.scrub(input_text)
    assert "[EMAIL_REDACTED]" in output
    assert "[IPV4_REDACTED]" in output

def test_clean_text(guard):
    input_text = "This is a perfectly safe sentence."
    output = guard.scrub(input_text)
    assert output == input_text