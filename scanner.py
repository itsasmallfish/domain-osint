import dns.resolver
import ssl
import socket
import requests
from datetime import datetime

class DomainScanner:
    def __init__(self, domain: str):
        self.domain = domain
        self.results = {
            "ssl": 0, "dns": 0, "surface": 0, "exposure": 0, "rep": 0,
        }

    async def run_all(self):
        """Runs all checks and returns normalized scores (0-100)"""
        self.results["ssl"] = self.check_ssl()
        self.results["dns"] = self.check_dns()
        self.results["surface"] = self.check_surface()
        # Mocking exposure for now, as HIBP requires a paid key
        self.results["exposure"] = 90 
        self.results["rep"] = 80
        
        return self.results

    def check_ssl(self) -> int:
        """Checks SSL certificate validity and expiry."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Parse expiry date
                    expire_date = datetime.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z")
                    days_left = (expire_date - datetime.utcnow()).days
                    
                    if days_left <= 0: return 0
                    if days_left < 30: return 50
                    return 100
        except:
            return 0  # No SSL or connection failed

    def check_dns(self) -> int:
        """Checks for security-related DNS records (SPF, DMARC)."""
        score = 0
        try:
            # Check SPF
            spf = dns.resolver.resolve(self.domain, 'TXT')
            if any('v=spf1' in str(r) for r in spf): score += 50
            
            # Check DMARC
            dmarc = dns.resolver.resolve(f'_dmarc.{self.domain}', 'TXT')
            if any('v=DMARC1' in str(r) for r in dmarc): score += 50
        except:
            pass
        return score

    def check_surface(self) -> int:
        """Finds subdomains via Certificate Transparency logs (crt.sh)."""
        try:
            # Using the crt.sh JSON API (no key needed!)
            url = f"https://crt.sh/?q={self.domain}&output=json"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                unique_subs = len(set(item['name_value'] for item in data))
                
                # More subdomains = Higher attack surface = Lower security score
                if unique_subs < 5: return 100
                if unique_subs < 20: return 70
                return 40
        except:
            pass
        return 50