#utils.py
import netifaces

def get_wifi_ip():
    # Get the IP address of the connected Wi-Fi network
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        if iface.startswith('wlan') or iface.startswith('wlp'):
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs:
                for addr_info in addrs[netifaces.AF_INET]:
                    return addr_info['addr']
    return None
