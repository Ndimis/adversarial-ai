import unittest
from red_team import JailbreakTester

# ---------------------------------------------------------
# 1. MOCK FIREWALLS FOR TESTING
# ---------------------------------------------------------

def strict_firewall(text):
    """
    A simulated 'perfect' firewall. 
    Matches keywords from all 4 adversarial payloads.
    """
    forbidden = [
        "Ignore all previous", # Catches DAN_MODE
        "malicious",           # Catches TRANSLATOR_BYPASS
        "villain", "ethics",   # Catches CHARACTER_ROLEPLAY
        "SHowIG1l"             # Catches BASE64_OBFUSCATION
    ]
    # Returns True if SAFE, False if BLOCKED
    return not any(word.lower() in text.lower() for word in forbidden)

def leaky_firewall(text):
    """A simulated 'broken' firewall that lets everything through."""
    return True

# ---------------------------------------------------------
# 2. THE UNIT TEST CLASS
# ---------------------------------------------------------

class TestJailbreakTester(unittest.TestCase):

    def setUp(self):
        """Initialize the tester instances before each test method."""
        self.tester_strict = JailbreakTester(strict_firewall)
        self.tester_leaky = JailbreakTester(leaky_firewall)

    def test_payload_integrity(self):
        """Verify the attack library is populated with the correct keys."""
        expected_keys = [
            "DAN_MODE", 
            "TRANSLATOR_BYPASS", 
            "CHARACTER_ROLEPLAY", 
            "BASE64_OBFUSCATION"
        ]
        for key in expected_keys:
            self.assertIn(key, self.tester_strict.payloads)
            self.assertIsInstance(self.tester_strict.payloads[key], str)

    def test_audit_perfect_score(self):
        """Verify that a strict firewall achieves 4 blocks and 0 bypasses."""
        results = self.tester_strict.run_audit()
        
        # This will now PASS because our strict_firewall looks for 'villain'
        self.assertEqual(results["blocked"], 4, "Should have blocked all 4 attacks")
        self.assertEqual(results["bypassed"], 0, "Zero attacks should have leaked through")

    def test_audit_total_failure(self):
        """Verify that a leaky firewall reports 4 bypasses."""
        results = self.tester_leaky.run_audit()
        self.assertEqual(results["blocked"], 0)
        self.assertEqual(results["bypassed"], 4)

    def test_result_keys(self):
        """Ensure the audit returns the expected dictionary structure."""
        results = self.tester_strict.run_audit()
        self.assertTrue(all(k in results for k in ("blocked", "bypassed")))

if __name__ == "__main__":
    unittest.main()