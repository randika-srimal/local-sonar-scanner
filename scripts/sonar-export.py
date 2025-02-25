import pandas as pd
import requests
import base64
from datetime import datetime, timedelta
import os

# SonarQube parameters
APP_PORT = os.getenv("APP_PORT")
SONARQUBE_URL = 'http://app:'+APP_PORT+'/api/issues/search' #Sonar Instance URL
PROJECT_KEY = os.getenv("PROJECT_KEY")
TOKEN = os.getenv("PROJECT_TOKEN")

# Validate user input for start_date
def get_start_date():
    while True:
        user_input = input("Enter start date (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(user_input, "%Y-%m-%d")
        except ValueError:
            print("Invalid format. Please enter the date in YYYY-MM-DD format.")

# Fetch issues from SonarQube
auth = base64.b64encode(f'{TOKEN}:'.encode()).decode()
headers = {'Authorization': f'Basic {auth}'}
page_size = 500  # Page size, maximum allowed by SonarQube

# Adjust date ranges as necessary to ensure each range returns less than 10,000 issues
start_date = get_start_date()  # Example start date
end_date = datetime.now()  # Current date and time
delta = timedelta(days=30)  # Adjust the range to ensure < 10,000 results

current_start_date = start_date
all_issues = []

while current_start_date < end_date:
    current_end_date = current_start_date + delta
    if current_end_date > end_date:
        current_end_date = end_date

    params = { #Ajdust as required
        'componentKeys': PROJECT_KEY,
        'createdAfter': current_start_date.strftime('%Y-%m-%d'),
        'createdBefore': current_end_date.strftime('%Y-%m-%d'),
        'ps': page_size,
        'p': 1
    }

    while True:
        response = requests.get(SONARQUBE_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            try:
                data = response.json()
                issues = data.get('issues', [])
                all_issues.extend(issues)
                
                # Check if there are more pages
                if len(issues) < page_size:
                    break  # No more pages
                else:
                    params['p'] += 1  # Next page
            except requests.exceptions.JSONDecodeError as e:
                print('Failed to parse JSON response:', e)
                print('Response content:', response.text)
                break
        else:
            print(f'Failed to fetch issues. Status code: {response.status_code}')
            print('Response content:', response.text)
            break

    current_start_date = current_end_date

if all_issues:
    # Convert to DataFrame
    df = pd.DataFrame(all_issues)
    # Save to Excel
    df.to_excel(f"./reports/{end_date.strftime('%Y-%m-%d_%H%M%S')}_{PROJECT_KEY}_sonarqube_issues.xlsx", index=False)
    print('Issues exported to sonarqube_issues.xlsx')
else:
    print('No issues found.')