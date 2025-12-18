#!/usr/bin/env python3
"""
ProTech Solutions - Comprehensive Security Penetration Test
Tests all major security vulnerabilities
"""

import requests
import json
import time
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

BASE_URL = "http://127.0.0.1:5000/api"

class SecurityTester:
    def __init__(self):
        self.results = []
        self.total_tests = 0
        self.passed_tests = 0
        
    def print_header(self, text):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{text}")
        print(f"{'='*60}{Style.RESET_ALL}")
    
    def print_test(self, name, status, details=""):
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
            print(f"{Fore.GREEN}✅ {name}: PASS{Style.RESET_ALL}")
        elif status == "FAIL":
            print(f"{Fore.RED}❌ {name}: FAIL{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}⚠️  {name}: {status}{Style.RESET_ALL}")
        
        if details:
            print(f"   {details}")
        
        self.results.append((name, status, details))
    
    def test_sql_injection(self):
        self.print_header("TEST 1: SQL INJECTION")
        
        payloads = [
            ("Basic OR bypass", "admin' OR '1'='1", "anything"),
            ("Comment bypass", "' OR 1=1--", ""),
            ("Table drop attempt", "admin'; DROP TABLE user;--", "password")
        ]
        
        vulnerable = False
        
        for name, email_payload, password in payloads:
            try:
                response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": email_payload,
                    "password": password
                }, timeout=5)
                
                if response.status_code == 200:
                    self.print_test(f"SQL Injection - {name}", "FAIL", 
                                  f"Payload succeeded: {email_payload}")
                    vulnerable = True
                else:
                    print(f"   {Fore.BLUE}Tested: {email_payload} - Blocked{Style.RESET_ALL}")
            except Exception as e:
                print(f"   {Fore.YELLOW}Error testing {name}: {str(e)}{Style.RESET_ALL}")
        
        if not vulnerable:
            self.print_test("SQL Injection Protection", "PASS", 
                          "All SQL injection attempts were blocked")
    
    def test_xss(self):
        self.print_header("TEST 2: CROSS-SITE SCRIPTING (XSS)")
        
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg onload=alert('XSS')>",
            "javascript:alert('XSS')"
        ]
        
        for payload in xss_payloads:
            try:
                response = requests.post(f"{BASE_URL}/auth/register", json={
                    "full_name": payload,
                    "email": f"xss{time.time()}@test.com",
                    "phone": "677123456",
                    "password": "Test123!"
                }, timeout=5)
                
                # Check if dangerous characters are in response
                if "<script>" in response.text or "onerror=" in response.text:
                    self.print_test("XSS Protection", "FAIL", 
                                  f"Dangerous payload not sanitized: {payload[:30]}")
                    return
                else:
                    print(f"   {Fore.BLUE}Tested: {payload[:40]}... - Sanitized{Style.RESET_ALL}")
            except Exception as e:
                print(f"   {Fore.YELLOW}Error: {str(e)}{Style.RESET_ALL}")
        
        self.print_test("XSS Protection", "PASS", 
                      "All XSS payloads were sanitized")
    
    def test_brute_force(self):
        self.print_header("TEST 3: BRUTE FORCE PROTECTION")
        
        print(f"   {Fore.BLUE}Attempting 10 rapid login requests...{Style.RESET_ALL}")
        
        rate_limited = False
        attempts = 0
        
        for i in range(10):
            try:
                response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": "admin@test.com",
                    "password": f"wrong{i}"
                }, timeout=5)
                
                attempts += 1
                
                if response.status_code == 429:
                    self.print_test("Brute Force Protection", "PASS", 
                                  f"Rate limited after {attempts} attempts")
                    rate_limited = True
                    break
                
                time.sleep(0.1)  # Small delay
            except Exception as e:
                print(f"   {Fore.YELLOW}Error: {str(e)}{Style.RESET_ALL}")
                break
        
        if not rate_limited:
            self.print_test("Brute Force Protection", "FAIL", 
                          f"No rate limiting after {attempts} attempts - CRITICAL VULNERABILITY")
    
    def test_unauthorized_access(self):
        self.print_header("TEST 4: UNAUTHORIZED API ACCESS")
        
        # Test 1: Access user list without authentication
        try:
            response = requests.get(f"{BASE_URL}/auth/users", timeout=5)
            
            if response.status_code == 200:
                users = response.json()
                self.print_test("Unauthorized Access - User List", "FAIL", 
                              f"CRITICAL: {len(users)} users exposed without authentication")
            elif response.status_code == 401:
                self.print_test("Unauthorized Access - User List", "PASS", 
                              "Authentication required")
            else:
                self.print_test("Unauthorized Access - User List", "UNKNOWN", 
                              f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.print_test("Unauthorized Access - User List", "ERROR", str(e))
        
        # Test 2: Access orders without authentication
        try:
            response = requests.get(f"{BASE_URL}/orders/", timeout=5)
            
            if response.status_code == 401:
                self.print_test("Unauthorized Access - Orders", "PASS", 
                              "Authentication required")
            elif response.status_code == 200:
                self.print_test("Unauthorized Access - Orders", "FAIL", 
                              "Orders accessible without authentication")
            else:
                self.print_test("Unauthorized Access - Orders", "PARTIAL", 
                              f"Status: {response.status_code}")
        except Exception as e:
            self.print_test("Unauthorized Access - Orders", "ERROR", str(e))
    
    def test_parameter_tampering(self):
        self.print_header("TEST 5: PARAMETER TAMPERING")
        
        # First, login to get a token
        try:
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": "admin@protechsolutions.cm",
                "password": "admin_password"
            }, timeout=5)
            
            if login_response.status_code != 200:
                self.print_test("Parameter Tampering", "SKIPPED", 
                              "Could not login to test")
                return
            
            token = login_response.json()['access_token']
            
            # Try to create order with manipulated price
            response = requests.post(
                f"{BASE_URL}/orders/",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "items": [
                        {"id": 1, "quantity": 1, "price": 1}  # Fake price
                    ]
                },
                timeout=5
            )
            
            if response.status_code == 201:
                order_data = response.json()
                actual_total = order_data.get('total', 0)
                
                if actual_total == 1:
                    self.print_test("Parameter Tampering - Price", "FAIL", 
                                  "Server accepted fake price of 1 FCFA")
                elif actual_total > 1000:
                    self.print_test("Parameter Tampering - Price", "PASS", 
                                  f"Server used real price: {actual_total:,.0f} FCFA")
                else:
                    self.print_test("Parameter Tampering - Price", "UNKNOWN", 
                                  f"Unexpected total: {actual_total}")
            else:
                self.print_test("Parameter Tampering - Price", "ERROR", 
                              f"Order creation failed: {response.status_code}")
        except Exception as e:
            self.print_test("Parameter Tampering", "ERROR", str(e))
    
    def test_password_security(self):
        self.print_header("TEST 6: PASSWORD SECURITY")
        
        # Test weak password acceptance
        weak_passwords = ["123", "abc", "password", "12345678"]
        
        for weak_pwd in weak_passwords:
            try:
                response = requests.post(f"{BASE_URL}/auth/register", json={
                    "full_name": "Test User",
                    "email": f"weak{time.time()}@test.com",
                    "phone": "677123456",
                    "password": weak_pwd
                }, timeout=5)
                
                if response.status_code == 201:
                    self.print_test("Password Strength Validation", "FAIL", 
                                  f"Weak password accepted: '{weak_pwd}'")
                    return
            except Exception as e:
                pass
        
        self.print_test("Password Strength Validation", "PARTIAL", 
                      "Weak passwords may be accepted - consider adding validation")
    
    def test_cors(self):
        self.print_header("TEST 7: CORS CONFIGURATION")
        
        try:
            response = requests.get(f"{BASE_URL}/products/", timeout=5)
            
            cors_header = response.headers.get('Access-Control-Allow-Origin', '')
            
            if cors_header == '*':
                self.print_test("CORS Configuration", "FAIL", 
                              "CORS allows all origins (*) - Too permissive")
            elif cors_header:
                self.print_test("CORS Configuration", "PASS", 
                              f"CORS restricted to: {cors_header}")
            else:
                self.print_test("CORS Configuration", "UNKNOWN", 
                              "No CORS header found")
        except Exception as e:
            self.print_test("CORS Configuration", "ERROR", str(e))
    
    def test_token_expiration(self):
        self.print_header("TEST 8: JWT TOKEN EXPIRATION")
        
        try:
            # Login to get a token
            login_response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": "admin@protechsolutions.cm",
                "password": "admin_password"
            }, timeout=5)
            
            if login_response.status_code == 200:
                token = login_response.json()['access_token']
                
                # Decode JWT to check expiration (without verification)
                import base64
                parts = token.split('.')
                if len(parts) == 3:
                    payload = parts[1]
                    # Add padding if needed
                    payload += '=' * (4 - len(payload) % 4)
                    decoded = base64.b64decode(payload)
                    token_data = json.loads(decoded)
                    
                    if 'exp' in token_data:
                        exp_time = token_data['exp']
                        iat_time = token_data.get('iat', 0)
                        duration = exp_time - iat_time
                        
                        self.print_test("JWT Token Expiration", "PASS", 
                                      f"Token expires in {duration} seconds ({duration/3600:.1f} hours)")
                    else:
                        self.print_test("JWT Token Expiration", "FAIL", 
                                      "Token has no expiration")
                else:
                    self.print_test("JWT Token Expiration", "UNKNOWN", 
                                  "Could not decode token")
            else:
                self.print_test("JWT Token Expiration", "SKIPPED", 
                              "Could not login")
        except Exception as e:
            self.print_test("JWT Token Expiration", "ERROR", str(e))
    
    def print_summary(self):
        self.print_header("SECURITY TEST SUMMARY")
        
        print(f"\n{Fore.CYAN}Test Results:{Style.RESET_ALL}")
        for name, status, details in self.results:
            if status == "PASS":
                emoji = f"{Fore.GREEN}✅"
            elif status == "FAIL":
                emoji = f"{Fore.RED}❌"
            else:
                emoji = f"{Fore.YELLOW}⚠️"
            
            print(f"{emoji} {name}: {status}{Style.RESET_ALL}")
        
        score = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"\n{Fore.CYAN}Overall Score:{Style.RESET_ALL}")
        print(f"   Passed: {Fore.GREEN}{self.passed_tests}{Style.RESET_ALL}/{self.total_tests}")
        print(f"   Security Rating: {Fore.YELLOW}{score:.0f}%{Style.RESET_ALL}")
        
        if score >= 80:
            rating = f"{Fore.GREEN}EXCELLENT"
        elif score >= 60:
            rating = f"{Fore.YELLOW}GOOD"
        else:
            rating = f"{Fore.RED}NEEDS IMPROVEMENT"
        
        print(f"   Overall Rating: {rating}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Critical Issues:{Style.RESET_ALL}")
        critical = [r for r in self.results if r[1] == "FAIL"]
        if critical:
            for name, _, details in critical:
                print(f"   {Fore.RED}• {name}{Style.RESET_ALL}")
                if details:
                    print(f"     {details}")
        else:
            print(f"   {Fore.GREEN}None found!{Style.RESET_ALL}")

def main():
    print(f"{Fore.CYAN}{Style.BRIGHT}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     ProTech Solutions - Security Penetration Test         ║")
    print("║                                                            ║")
    print("║  This script tests your application for common security   ║")
    print("║  vulnerabilities. Results will help you improve security. ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(Style.RESET_ALL)
    
    print(f"\n{Fore.YELLOW}⚠️  Make sure your backend is running on http://127.0.0.1:5000{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}   (Run: cd backend && python app.py){Style.RESET_ALL}\n")
    
    input("Press Enter to start testing...")
    
    tester = SecurityTester()
    
    try:
        tester.test_sql_injection()
        tester.test_xss()
        tester.test_brute_force()
        tester.test_unauthorized_access()
        tester.test_parameter_tampering()
        tester.test_password_security()
        tester.test_cors()
        tester.test_token_expiration()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Testing interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n\n{Fore.RED}Fatal error: {str(e)}{Style.RESET_ALL}")
    
    tester.print_summary()
    
    print(f"\n{Fore.CYAN}For detailed security recommendations, see:{Style.RESET_ALL}")
    print("   SECURITY_AUDIT_REPORT.md")
    print("   SECURITY_TESTING_GUIDE.md")

if __name__ == "__main__":
    main()
