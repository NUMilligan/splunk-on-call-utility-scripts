import requests
     
# Define keys for Splunk On-Call API.
api_id="2sh110zhj2odraenp62bmi1ey"
api_key="735f5075000c4f1bb7f7ac2460f08281"
 
# Define base URL for Splunk On-Call API
url = "https://api.victorops.com/api-public"
 
# Define headers for HTTP request
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "X-VO-Api-Id": api_id,
    "X-VO-Api-Key": api_key
}

def get_teams() -> list:
    """Retrieve the list of teams from the Splunk On-Call account.
        Return a list of team slugs.
    """
    try:
        response = requests.get(url + "/v1/team", headers=headers, timeout=10)
        if response.status_code == 200:
            teams_data = response.json()
            team_names = [{'slug':team['slug'], 'name':team['name']} for team in teams_data]
            return team_names
        else:
            print("Error retrieving teams:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Error retrieving teams:", str(ex))
        return []

def get_team_oncalls(slug: str) -> list:
    """Retrieve the list of on-call schedules from the Splunk On-Call account.
        Return a list of on-call schedule slugs.
    """
    try:
        response = requests.get(url + "/v2/team/" + slug + "/oncall/schedule?daysForward=1", headers=headers, timeout=10)
        if response.status_code == 200:
            oncalls_data = response.json()
            for schedule in oncalls_data['schedules']:
                print(f"  Schedule: {schedule['policy']['name']}")
                for item in schedule['schedule']:
                    if item.get('overrideOnCallUser'):
                        print(f"    User: {item['overrideOnCallUser']['username']} (Overrides user in rotation)")
                    elif item.get('onCallUser'):
                        user_details = get_user(item['onCallUser']['username'])
                        print(f"    On-Call: {user_details['firstName']} {user_details['lastName']}")
                    else:
                        print("    User: None")
            #oncall_names = [{oncall['slug']: oncall['name']} for oncall in oncalls_data]
            #return oncall_names
        else:
            print("Error retrieving on-calls:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Error retrieving on-calls:", str(ex))
        return []

def get_user(username: str) -> dict:
    """Retrieve user details by username from the Splunk On-Call account.
        Return user details as a dictionary.
    """
    try:
        response = requests.get(url + "/v1/user/" + username, headers=headers, timeout=10)
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            print("Error retrieving user:", response.status_code, response.text)
            return {}
    except Exception as ex:
        print("Error retrieving user:", str(ex))
        return {}

if __name__ == '__main__':

    teams = get_teams()
    if teams:
        print("Teams retrieved successfully:")
        for team in teams:
            print(team['name'])
            get_team_oncalls(team['slug'])
    else:
        print("No teams found or error occurred.")    