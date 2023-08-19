import requests

# Define the base URL of your Flask application
base_url = "http://localhost:5000"

# Trigger the report generation
trigger_report_url = f"{base_url}/trigger_report"
response = requests.post(trigger_report_url)
if response.status_code == 200:
    # Report generation triggered successfully
    report_id = response.json()["report_id"]
    print(f"Report generation triggered. Report ID: {report_id}")
else:
    # Handle error
    print(f"Failed to trigger report generation. Error: {response.text}")

# Get the report data
get_report_url = f"{base_url}/get_report?report_id={report_id}"
response = requests.get(get_report_url)
if response.status_code == 200:
    # Report data retrieved successfully
    report_data = response.json()["report_data"]
    print("Report Data:")
    for store_report in report_data:
        print(store_report)
else:
    # Handle error
    print(f"Failed to retrieve report data. Error: {response.text}")
