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
    
def team_exists(team: str) -> bool:
    """Check if a team exists in Splunk On-Call.
        If the team exists, return True.
        If the team doesn't exist, return False.
    """
    print(', '.join([team]))

    # Check if the team exists
    try:
        response = requests.get(url + f"/team/{team}", headers=headers, timeout=10)
        print(response)
        if response.status_code == 200:
            print(f"Team {team} exists.")
            return True
        else:
            print(f"Team {team} does not exist.")
            return False
    except Exception as ex:
        print("Error checking team existence:", str(ex))
        return False
 
def add_team(team: str) -> str:
    """Add a team to Splunk On-Call.
        If the team is added successfully, return the team's slug.
        If the team can't be added, return an empty string.
    """
    print(', '.join([team]))

    payload = {
        "name": team,
        "description": team
    }
    try:
        response = requests.post(url + "/team", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json().get('slug', '')
        else:
            print("Error adding team:", response.status_code, response.text)
            return None
    except Exception as ex:
        print("Error adding team:", str(ex))
        return None

def add_member(slug: str, username:str) -> bool:
    """Add a member to a team in Splunk On-Call.
        If the member is added successfully, return True.
        If the member can't be added, return False.
    """
    print(', '.join([slug]))

    # Add the user to the team
    payload = {
        "username": username
    }
    print(url + f"/team/{slug}/members")
    try:
        response = requests.post(url + f"/team/{slug}/members", headers=headers, json=payload, timeout=10)
        if response.status_code == 200:
            return True
        else:
            print(f"Error adding member {username} to team {slug}:", response.status_code, response.text)
            return False
    except Exception as ex:
        print(f"Error adding member {username} to team {slug}:", str(ex))
        return False
    
if __name__ == '__main__':

    # Read an excel file with user data
    df = pd.read_excel('C:\\Users\\amm606\\OneDrive - Northwestern University\\Documents\\Opsgenie integrations mailing list.xlsx', sheet_name='Remaining members')

    for index, row in df.iterrows():
        # Replace spaces with underscores in team names
        teamname = row['Team']
        username = row['samAccountName']

        # Refresh the list of teams in case a new team was added in a previous iteration
        teams = get_teams()
        team_details = list(filter(lambda team: team['name'] == teamname, teams))
        team_slug = team_details[0]['slug'] if team_details else None

        if team_slug == None:
            print(f"Team {teamname} does not exist. Adding team...")
            team_slug = add_team(teamname)
            if team_slug:
                print(f"Team {teamname} added successfully with slug {team_slug}.")
            else:
                print(f"Failed to add team {teamname}.")   
        else:
            print(f"Team {teamname} exists. Adding users to team...") 

        if add_member(team_slug, username):
            print(f"User {username} added to team {teamname} successfully.")
        else:
            print(f"Failed to add user {username} to team {teamname}.")
        time.sleep(1)  # To avoid hitting rate limits
