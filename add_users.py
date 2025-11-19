import requests
import pandas as pd
import time
     
# Define keys for Splunk On-Call API.
api_id="2sh110zhj2odraenp62bmi1ey"
api_key="735f5075000c4f1bb7f7ac2460f08281"
 
# Define base URL for Splunk On-Call API
url = "https://api.victorops.com/api-public/v1"
 
# Define headers for HTTP request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-VO-Api-Id": api_id,
    "X-VO-Api-Key": api_key
}

def add_user(firstname: str, lastname: str, username: str, email: str) -> bool:
    """Add a user to the Splunk On-Call account.
        If the user is added successfully, return True.
        If the user can't be added, return False.
    """
    print(', '.join([firstname, lastname, username, email]))
    payload = {
        "firstName": firstname,
        "lastName": lastname,
        "username": username,
        "email": email
    }
    try:
        response = requests.post(url + "/user", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print("Error adding user:", response.status_code, response.text)
            return False
    except Exception as ex:
        print("Error adding user:", str(ex))
        return False
    

if __name__ == '__main__':

    # Read an excel file with user data
    df = pd.read_excel('C:\\Users\\amm606\\OneDrive - Northwestern University\\Documents\\Opsgenie integrations mailing list.xlsx', sheet_name='Remaining members')
    for index, row in df.iterrows():
        firstname = row['GivenName']
        lastname = row['Surname']
        username = row['samAccountName']
        email = row['Member']
        if add_user(firstname, lastname, username, email):
            print(f"User {username} added successfully.")
        else:
            print(f"Failed to add user {username}.")
        time.sleep(1)  # To avoid hitting rate limits
