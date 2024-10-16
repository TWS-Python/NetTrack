import psutil
import sqlite3
from datetime import datetime
import time


# Monitor real-time network traffic
def get_real_time_traffic():
    prev_bytes_sent = psutil.net_io_counters().bytes_sent
    prev_bytes_recv = psutil.net_io_counters().bytes_recv
    while True:
        time.sleep(1)
        current_bytes_sent = psutil.net_io_counters().bytes_sent
        current_bytes_recv = psutil.net_io_counters().bytes_recv
        sent_speed = current_bytes_sent - prev_bytes_sent
        recv_speed = current_bytes_recv - prev_bytes_recv
        prev_bytes_sent = current_bytes_sent
        prev_bytes_recv = current_bytes_recv
        yield sent_speed, recv_speed


# Create database connection for bandwidth tracking
def create_db():
    conn = sqlite3.connect('nettrack_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS bandwidth_usage 
                      (date TEXT, bytes_sent INTEGER, bytes_recv INTEGER)''')
    conn.commit()
    return conn, cursor


# Insert daily bandwidth usage
def log_bandwidth_usage(bytes_sent, bytes_recv):
    conn, cursor = create_db()
    date_today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''INSERT INTO bandwidth_usage (date, bytes_sent, bytes_recv)
                      VALUES (?, ?, ?)''', (date_today, bytes_sent, bytes_recv))
    conn.commit()
    conn.close()


# Retrieve bandwidth data (daily, weekly, or monthly)
def get_bandwidth_usage(period):
    conn, cursor = create_db()
    query = "SELECT SUM(bytes_sent), SUM(bytes_recv) FROM bandwidth_usage WHERE date >= ?"

    if period == 'daily':
        cursor.execute(query, (datetime.now().strftime('%Y-%m-%d'),))
    elif period == 'weekly':
        last_week = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute(query, (last_week,))
    elif period == 'monthly':
        last_month = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        cursor.execute(query, (last_month,))

    result = cursor.fetchone()
    conn.close()
    return result if result else (0, 0)

# Get connected network devices (by interface names)
def get_connected_devices():
    devices = []
    interfaces = psutil.net_if_addrs()
    for interface, addr_info in interfaces.items():
        for addr in addr_info:
            if addr.family == psutil.AF_LINK:  # MAC address
                devices.append((interface, addr.address))
    return devices

# Set alerts for speed drops or data limits
def check_alerts(sent_speed, recv_speed, limit_speed=50000):  # example limit in bytes
    if sent_speed < limit_speed or recv_speed < limit_speed:
        return "Warning: Speed dropped below threshold!"
    return "Speed is normal."
import csv
from fpdf import FPDF

# Export bandwidth usage to CSV
def export_bandwidth_to_csv():
    conn, cursor = create_db()
    cursor.execute("SELECT * FROM bandwidth_usage")
    rows = cursor.fetchall()
    conn.close()

    with open('bandwidth_report.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Bytes Sent', 'Bytes Received'])
        writer.writerows(rows)

# Export bandwidth usage to PDF
def export_bandwidth_to_pdf():
    conn, cursor = create_db()
    cursor.execute("SELECT * FROM bandwidth_usage")
    rows = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Bandwidth Report", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(40, 10, 'Date', 1)
    pdf.cell(40, 10, 'Bytes Sent', 1)
    pdf.cell(40, 10, 'Bytes Received', 1)
    pdf.ln(10)

    for row in rows:
        pdf.cell(40, 10, row[0], 1)
        pdf.cell(40, 10, str(row[1]), 1)
        pdf.cell(40, 10, str(row[2]), 1)
        pdf.ln(10)

    pdf.output('bandwidth_report.pdf')
