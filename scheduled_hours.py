import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

# Load variables from .env file
dyflexis_api_token = os.getenv("DYFLEXIS_API_TOKEN")
dyflexis_api_url = os.getenv("DYFLEXIS_API_URL")
dyflexis_system_name = os.getenv("DYFLEXIS_SYSTEM_NAME")

# Create a GET request function
def get_request(start_date, end_date, department_id):
    page = 1
    all_data = []
    page_count = float('inf')  # Initialize with infinity, we will update it with pageCount

    while page <= page_count:
        # Define the full URL and endpoint
        url = dyflexis_api_url + dyflexis_system_name

        # If departmentId is None don't use the parameter
        if department_id is not None:
            endpoint = f"api/business/v3/scheduled?startDate={start_date}&endDate={end_date}&departmentId={department_id}&page={page}"
        else:
            endpoint = f"api/business/v3/scheduled?startDate={start_date}&endDate={end_date}&page={page}"

        full_url = url + endpoint

        headers = {
            "Authorization": "Token " + dyflexis_api_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # Get request with full_url and endpoint
        response = requests.get(full_url, headers=headers)

        # Check if request was successful
        if response.status_code == 200:
            # Turn response into JSON data
            data = response.json()
            shifts = data['shifts']
            
            # Append shifts to all_data
            all_data.extend(shifts)

            # Update page_count with pageCount if not initialized
            if page == 1:
                page_count = data['pageCount']

            # Increment page number
            page += 1

        else:
            print(f"Error: {response.status_code} - {response.text}")
            break  # Exit loop on error

    # Create DataFrame from all_data
    df = pd.DataFrame(all_data)

    return df

if __name__ == "__main__":
    # Define parameters
    start_date = "2024-02-01"
    end_date = "2024-02-28"
    department_id = None

    # Create DataFrame
    df = get_request(start_date, end_date, department_id)
    print(df)

    # Turn DataFrame into an Excel file and save locally
    df.to_excel("dyflexis_scheduled_hours.xlsx", index=False)
    
