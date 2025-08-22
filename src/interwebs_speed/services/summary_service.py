import csv
import os
from datetime import datetime, timedelta

from interwebs_speed.utils import bytes_to_mb, create_logger, get_config
from interwebs_speed.services import mail_service

def _load_data(file_path: str):
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['download'] = float(row['download'])
            row['upload'] = float(row['upload'])
            row['ping'] = float(row['ping'])
            data.append(row)
    return data

def _get_summary(data):
    if not data:
        return {
            "avg_download": 0, "avg_upload": 0, "avg_ping": 0,
            "min_download": 0, "min_upload": 0, "min_ping": 0,
            "max_download": 0, "max_upload": 0, "max_ping": 0,
        }

    downloads = [row['download'] for row in data]
    uploads = [row['upload'] for row in data]
    pings = [row['ping'] for row in data]

    summary = {
        "avg_download": sum(downloads) / len(downloads),
        "avg_upload": sum(uploads) / len(uploads),
        "avg_ping": sum(pings) / len(pings),
        "min_download": min(downloads),
        "min_upload": min(uploads),
        "min_ping": min(pings),
        "max_download": max(downloads),
        "max_upload": max(uploads),
        "max_ping": max(pings),
    }
    return summary

def _to_html(summary):
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Internet Speed Monthly Summary</h2>
        <table>
            <tr>
                <th>Metric</th>
                <th>Average</th>
                <th>Min</th>
                <th>Max</th>
            </tr>
            <tr>
                <td>Download (MB)</td>
                <td>{bytes_to_mb(summary['avg_download']):.2f}</td>
                <td>{bytes_to_mb(summary['min_download']):.2f}</td>
                <td>{bytes_to_mb(summary['max_download']):.2f}</td>
            </tr>
            <tr>
                <td>Upload (MB)</td>
                <td>{bytes_to_mb(summary['avg_upload']):.2f}</td>
                <td>{bytes_to_mb(summary['min_upload']):.2f}</td>
                <td>{bytes_to_mb(summary['max_upload']):.2f}</td>
            </tr>
            <tr>
                <td>Ping (ms)</td>
                <td>{summary['avg_ping']:.2f}</td>
                <td>{summary['min_ping']:.2f}</td>
                <td>{summary['max_ping']:.2f}</td>
            </tr>
        </table>
    </body>
    </html>
    """
    return html

def send_monthly_summary():
    logger = create_logger()
    logger.info("Starting monthly summary.")
    config = get_config()
    
    csv_files_path = config.get('csv_files_path')
    
    # Calculate the date for the previous month
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    file_name = last_day_of_previous_month.strftime('%m-%Y.csv')
    
    file_path = os.path.join(csv_files_path, file_name)

    if not os.path.exists(file_path):
        logger.error(f"File {file_path} not found.")
        return

    data = _load_data(file_path)
    summary = _get_summary(data)
    html_summary = _to_html(summary)

    mail_service.send_email(config, "Internet Speed Monthly Summary", html_summary, subtype="html")
    logger.info("Monthly summary sent.")
