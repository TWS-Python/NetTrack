import psutil
import socket
from fpdf import FPDF

def get_network_stats():
    """Retrieve network statistics."""
    stats = psutil.net_io_counters()
    return {
        "bytes_sent": stats.bytes_sent,
        "bytes_received": stats.bytes_recv,
        "packets_sent": stats.packets_sent,
        "packets_received": stats.packets_recv
    }

def get_ip_address():
    """Retrieve the IP address of the system."""
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_interface_stats():
    """Retrieve network interface statistics."""
    interfaces = psutil.net_if_addrs()
    stats = {}
    for interface, address_list in interfaces.items():
        for address in address_list:
            if address.family == socket.AF_INET:
                stats[interface] = address.address
    return stats

def export_to_pdf(data, filename="network_stats.pdf"):
    """Export data to a PDF report."""
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Network Statistics Report", ln=True, align='C')

    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)

    pdf.output(filename)
