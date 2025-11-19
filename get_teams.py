import requests
     
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

def get_teams() -> list:
    """Get a list of teams from Splunk On-Call.
        If the request is successful, return a list of teams.
        If the request fails, return an empty list.
    """
    try:
        response = requests.get(url + "/team", headers=headers, timeout=10)
        if response.status_code == 200:
            teams = response.json()
            return teams
        else:
            print("Error getting teams:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Error getting teams:", str(ex))
        return []
    
if __name__ == '__main__':

    for team in get_teams():
        print(team['name'])