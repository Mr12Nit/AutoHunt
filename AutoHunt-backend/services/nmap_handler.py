import json
import ipaddress
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

    def __init__(self):
        """
        Initialize the NmapHandler with a CommandsHandler instance.
        """
        self.command_handler = CommandsHandler()

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
            logger.error(f"Nmap scan faild due to wrong subnet")
            raise ValueError(f"Invalid subnet format: {subnet}")

        # Optimal Nmap command for stealthy network discovery
        command = [
            "nmap", "-n", "-sS", "-T3", "--open", "--host-timeout", "5m", "--max-retries", "2", "--randomize-hosts",
            "--min-hostgroup", "32", "--min-parallelism", "5", subnet]


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
        command = ["nmap", "-sV","-sS", "-O" ,"--top-ports 1000","--reason","--open", ip, "-oX", "-"]  # Service version and OS detection
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

    def _extract_up_ips(self, output: str) -> list:
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

    def _parse_nmap_output(self, output: str) -> dict:
        """
        Parse the raw Nmap output into a structured format.

        Args:
            output (str): The raw Nmap output.

        Returns:
            dict: A dictionary representing the parsed scan results.
        """
        # Placeholder: Add XML or regex-based parsing logic for structured results
        return {"raw_output": output}


# Example usage :
if __name__ == "__main__":
    nmap_handler = NmapHandler()

    # Discover the network
    try:
        print("Discovering network...")
        devices = nmap_handler.discover_network("192.168.1.0/24")
        print("Up devices:", devices)
    except ValueError as ve:
        print(f"Validation error: {ve}")
    except RuntimeError as re:
        print(f"Runtime error: {re}")

    # Scan a specific IP
    try:
        print("Scanning target IP...")
        scan_result = nmap_handler.scan_ports("192.168.1.101")
        print("Scan result:", scan_result)
    except RuntimeError as re:
        print(f"Runtime error: {re}")
