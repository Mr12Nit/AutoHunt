import requests
from typing import Dict, Any, Optional

class HttpHandler:
    """
    A class to handle HTTP requests and responses.
    """

    @staticmethod
    def make_request(
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
    ) -> requests.Response:
        """
        Makes an HTTP request using the specified method.

        Args:
            method (str): HTTP method (GET, POST, etc.).
            url (str): The URL to make the request to.
            headers (Optional[Dict[str, str]]): HTTP headers.
            params (Optional[Dict[str, Any]]): Query parameters.
            data (Optional[Dict[str, Any]]): Data to send in the request body.
            timeout (int): Request timeout in seconds.

        Returns:
            requests.Response: The response object from the HTTP request.
        """
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
            )
            return response
        except requests.RequestException as e:
            raise RuntimeError(f"HTTP request failed: {str(e)}")

    @staticmethod
    def check_response_success_status(response: requests.Response) -> bool:
        """
        Checks if the response status code indicates success.

        Args:
            response (requests.Response): The response object to check.

        Returns:
            bool: True if the status code is 2xx, False otherwise.
        """
        if 200 <= response.status_code < 300:
            return True
        return False

    
