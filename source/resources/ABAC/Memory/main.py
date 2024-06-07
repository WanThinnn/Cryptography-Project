#main.py
import argparse
from policy import create_pdp, check_access
from utils import get_wifi_ip

def main(args):
    # Create the PDP
    pdp = create_pdp()

    # Get the IP address of the Wi-Fi network
    ip_address = get_wifi_ip()

    if ip_address is not None:
        # Check access for the given action
        action_method = args.action_methods
        check_access(pdp, args.role, args.department, args.position, args.resource_type, action_method)
    else:
        print("Could not retrieve Wi-Fi IP address.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check access policy for a given request")
    parser.add_argument("role", type=str, help="Role of the subject")
    parser.add_argument("department", type=str, help="Department of the subject")
    parser.add_argument("position", type=str, help="Position of the subject")
    parser.add_argument("resource_type", type=str, help="Type of the resource")
    parser.add_argument("action_methods", type=str, nargs='?', help="Method of the action")

    args = parser.parse_args()

    main(args)
