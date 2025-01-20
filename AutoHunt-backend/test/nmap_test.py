import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.nmap_handler import NmapHandler

nmap = NmapHandler()
#result = nmap.discover_network(subnet="10.94.115.0/24")
try:
    targetPortScan = nmap.scan_ports("10.94.115.69")
except PermissionError as pe:
    print(f"Permission Error {pe}")