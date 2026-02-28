import re
import logging
import sys

# Windows UTF-8 Fix
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger("PIIGuard")

class PIIGuard:
    def __init__(self):
        # Professional-grade Regex patterns for sensitive data
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "CREDIT_CARD": r'\b(?:\d[ -]*?){13,16}\b',
            "IPV4": r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            "API_KEY": r'sk-[a-zA-Z0-9]{32,}'
        }

    def scrub(self, ai_response):
        """
        Scans AI output for PII and redacts it before user delivery.
        """
        scrubbed_text = ai_response
        leaks_found = []

        for label, pattern in self.patterns.items():
            matches = re.findall(pattern, scrubbed_text)
            if matches:
                leaks_found.append(label)
                # Redact the sensitive data
                scrubbed_text = re.sub(pattern, f"[{label}_REDACTED]", scrubbed_text)

        if leaks_found:
            logger.warning(f"🚨 PII LEAK BLOCKED: {', '.join(leaks_found)}")
        
        return scrubbed_text

if __name__ == "__main__":
    guard = PIIGuard()
    
    # Example AI response that accidentally leaks sensitive developer data
    ai_output = "I can provide the logs. The admin is dev@company.com and the internal IP is 10.0.0.5."
    
    clean_text = guard.scrub(ai_output)
    print(f"\n--- SCRUBBED OUTPUT ---\n{clean_text}")