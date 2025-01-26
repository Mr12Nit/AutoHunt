import json
import ipaddress
import os
import re

from services.log_setup import setup_logger
from services.commands_handler import CommandsHandler

logger = setup_logger("CommandsHandler", "Nmap_log.txt")

class NmapHandler:
    """
    A class to handle Nmap operations for network discovery and port scanning.
    
    Methods:
        discover_network(subnet): Performs a network discovery scan.
        scan_ports(ip): Performs a detailed port scan on a given IP address.
        _validate_subnet(subnet): Validates the subnet format.
        _parse_nmap_output(output): Parses the raw Nmap output into a structured format.
    """
    DEFAULT_NMAP_FLAGS = {
        "network_scan": ["-n", "-sS", "-T3", "--open", "--host-timeout", "5m", "--max-retries", "2", "--randomize-hosts", "--min-hostgroup", "32", "--min-parallelism", "5"],
        "port_scan": ["-sV", "-sS", "-O", "--top-ports=1000", "--reason", "--open"],
    }


    def __init__(self):
        """
        Initialize the NmapHandler with a CommandsHandler instance.
        """
        self.command_handler = CommandsHandler()
        self.ensure_sudo()
    
    def ensure_sudo(self):
        """
        Ensure the script is running with sudo privileges.

        Raises:
            PermissionError: If the script is not running with sudo privileges.
        """
        if os.geteuid() != 0:
            raise PermissionError("This script must be run with sudo privileges. Use 'sudo' to run the script.")


    def discover_network(self, subnet: str) -> list:
        """
        Perform a network discovery scan to identify active devices.

        Args:
            subnet (str): The subnet to scan (e.g., "192.168.1.0/24").

        Returns:
            list: A list of up and running IP addresses.
        """
        logger.info("discovering network has started")

        if not self._validate_subnet(subnet):
            logger.error(f"Nmap scan failed due to invalid subnet: {subnet}")
            raise ValueError(f"Invalid subnet format: {subnet}")

        # Optimal Nmap command for stealthy network discovery
        command = ["nmap"] + self.DEFAULT_NMAP_FLAGS["network_scan"] + [subnet]


        return_code, stdout, stderr = self.command_handler.execute_command(command)

        if self.command_handler.check_command_success(return_code):
            return self._extract_up_ips(stdout)
        else:
            raise RuntimeError(f"Nmap scan failed: {stderr.strip()}")

    def scan_ports(self, ip: str) -> dict:
        """
        Perform a detailed port and service scan on a specific IP.

        Args:
            ip (str): The IP address to scan.

        Returns:
            dict: A structured result of the scan including open ports and service details.
        """
        
        command = ["nmap"] + self.DEFAULT_NMAP_FLAGS["port_scan"] + [ip]
        return_code, stdout, stderr = self.command_handler.execute_command(command)

        if self.command_handler.check_command_success(return_code):
            return self._parse_nmap_output(stdout)
        else:
            return {"error": stderr.strip()}

    def _validate_subnet(self, subnet: str) -> bool:
        """
        Validate the subnet format. Ensures it is a valid network in CIDR notation
        and represents an actual subnet (not a single host).

        Args:
            subnet (str): The subnet to validate (e.g., "192.168.1.0/24").

        Returns:
            bool: True if the subnet is valid, False otherwise.
        """
        try:
            network = ipaddress.ip_network(subnet, strict=True)
            # Ensure it's a valid subnet (not a single host like /32 or /128)
            if network.prefixlen == network.max_prefixlen:
                return False
            return True
        except ValueError:
            return False

    def _extract_up_ips(self, output: str) -> list[str]:
        """
        Extract the IP addresses of devices that are up from Nmap output.

        Args:
            output (str): The raw Nmap output.

        Returns:
            list: A list of IP addresses that are up.
        """
        logger.info("Scan has completed, Now extracting the ips")
        up_ips = []
        for line in output.splitlines():
            if "Nmap scan report for" in line:
                ip = line.split()[-1]
                up_ips.append(ip)
        return up_ips

    def _parse_nmap_output(self, output: str) -> list[dict]:

        """
        Parses the plain text Nmap output and extracts useful information.

        Args:
            output (str): Plain text output from Nmap.

        Returns:
            list: List of dictionaries with IP, ports, and services, including versions if available.
            Example:
            [
                {
                    "ip": "192.168.1.1",
                    "ports": [
                        {"port": "22", "service": "ssh", "version": "OpenSSH 7.4"},
                        {"port": "80", "service": "http", "version": "Apache 2.4.41"}
                    ]
                }
            ]
        """
        try:
            if not isinstance(output, str):
                logger.error("Nmap output must be normal text")
                raise TypeError("Output must be a string.")

            results = []
            lines = output.splitlines()
            current_host = None

            for line in lines:
                # Match the IP address of the host
                host_match = re.match(r"^Nmap scan report for (.+)", line)
                if host_match:
                    current_host = {"ip": host_match.group(1), "ports": []}
                    results.append(current_host)
                    continue

                # Match open ports and their details, including service version
                port_match = re.match(r"^(\d{1,5})/tcp\s+open\s+(\S+)(?:\s+(.+))?", line)
                if port_match and current_host:
                    port_data = {
                        "port": port_match.group(1),
                        "service": port_match.group(2),
                        "version": port_match.group(3) if port_match.group(3) else "Unknown"
                    }
                    current_host["ports"].append(port_data)

            return results

        except Exception as e:
            logger.error("Error occurred while parsing Nmap output")
            print(f"Error parsing Nmap output: {e}")
            return [{"error": "Failed to parse output", "details": str(e)}]

# Example usage:
if __name__ == "__main__":
    nmap_handler = NmapHandler()

    try:
        print("Discovering network...")
        devices = nmap_handler.discover_network("192.168.1.0/24")
        print("Up devices:", devices)
    except ValueError as ve:
        print(f"Validation error: {ve}")
    except PermissionError as pe:
        print(f"Permission error: {pe}")
    except RuntimeError as re:
        print(f"Runtime error: {re}")

    try:
        print("Scanning target IP...")
        scan_result = nmap_handler.scan_ports("192.168.1.101")
        print("Scan result:", scan_result)
    except PermissionError as pe:
        print(f"Permission error: {pe}")
    except RuntimeError as re:
        print(f"Runtime error: {re}")
