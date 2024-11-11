import re
from collections import defaultdict

# Regular expression patterns
wireless_pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"wireless\[\d+\]: <\d+> \d+ .+STA (?P<mac>[\w:]+) .+ associated"
)
dhcp_pattern = re.compile(
    r"(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) "
    r"dhcps\[\d+\]: <\d+> \d+ send ack ip (?P<ip>[\d.]+) .+ to (?P<mac>[\w:]+)"
)

# Function to parse log file and count connected nodes
def parse_router_connections(file_path):
    wireless_connections = defaultdict(set)  # mac: {ip addresses}
    dhcp_assignments = {}  # mac: ip

    with open(file_path, 'r') as file:
        for line in file:
            # Check for wireless connection events
            wireless_match = wireless_pattern.search(line)
            if wireless_match:
                mac = wireless_match.group("mac")
                wireless_connections[mac]  # Track MACs seen in connection events

            # Check for DHCP ACK (IP assignment) events
            dhcp_match = dhcp_pattern.search(line)
            if dhcp_match:
                mac = dhcp_match.group("mac")
                ip = dhcp_match.group("ip")
                dhcp_assignments[mac] = ip  # Store IP assignment for each MAC

    # Summarize results
    print("Connected Devices Report")
    print("------------------------")
    for mac, ip in dhcp_assignments.items():
        if mac in wireless_connections:
            print(f"MAC: {mac} -> IP: {ip} (Connected wirelessly)")
    
    print("\nTotal number of unique wireless connections:", len(wireless_connections))

# Example usage
file_path = "dfi_router.log"
parse_router_connections(file_path)
