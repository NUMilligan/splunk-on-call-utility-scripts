import requests
import json
     
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

def print_oncall_json_v2() -> object:
    """Retrieve on-call info for Splunk On-Call teams.
        Return data as a JSON-formatted object.
    """
    retval = []

    try:
        response = requests.get(url + "/v1/oncall/current", headers=headers, timeout=10)
        oncalls_data = response.json()
        for team in oncalls_data['teamsOnCall']:
            # If no one is on call for the team, create a placeholder entry
            # If there are on-call users, create entries for each user
            if  team['oncallNow'] == []:
                on_call_item = {}
                on_call_item['team'] = team['team']['name']
                on_call_item['schedule'] = "No active schedule"
                on_call_item['username'] = "No one is on call"
                on_call_item['email'] = ""
                on_call_item['voice'] = ""
                on_call_item['sms'] = ""
            else:
                for oncallNow in team['oncallNow']:
                    for user in oncallNow['users']:
                        on_call_item = {}
                        on_call_item['team'] = team['team']['name']
                        on_call_item['schedule'] = oncallNow['escalationPolicy']['name']
                        on_call_item['username'] = get_user(user['onCalluser']['username'])['displayName']
                        user_contacts = get_user_contacts(user['onCalluser']['username'])
                        if not user_contacts:
                            on_call_item['email'] = ""
                            on_call_item['voice'] = ""
                            on_call_item['sms'] = ""
                        else:
                            on_call_item['email'] = user_contacts.get('Email', "")
                            on_call_item['voice'] = user_contacts.get('Phone', "")
                            on_call_item['sms'] = user_contacts.get('Phone', "")

                    retval.append(on_call_item)
    except Exception as ex:
        print("Error retrieving on-calls:", str(ex))
        return []

    return json.dumps(retval)

def print_oncall_json() -> object:
    """Retrieve on-call info for Splunk On-Call teams.
        Return data as a JSON-formatted object.
    """
    retval = []

    try:
        teams = get_teams()
    
        for team in teams:
            try:
                response = requests.get(url + "/v2/team/" + team['slug'] + "/oncall/schedule?daysForward=1", headers=headers, timeout=10)
                if response.status_code == 200:
                    oncalls_data = response.json()
                    for schedule in oncalls_data['schedules']:
                        on_call_item = {}
                        #print(f"  Schedule: {schedule['policy']['name']}")
                        on_call_item['team'] = team['name']
                        on_call_item['schedule'] = schedule['policy']['name']
                        for schedule_item in schedule['schedule']:
                            if schedule_item.get('overrideOnCallUser'):
                                #print(f"    User: {schedule_item['overrideOnCallUser']['username']} (Overrides user in rotation)")
                                on_call_item['username'] = "".join([schedule_item['overrideOnCallUser']['username']," (Overrides user in rotation)"])
                            elif schedule_item.get('onCallUser'):
                                user_details = get_user(schedule_item['onCallUser']['username'])
                                #print(f"    On-Call: {user_details['firstName']} {user_details['lastName']}")
                                on_call_item['username'] = schedule_item['onCallUser']['username']
                                user_contacts = get_user_contacts(schedule_item['onCallUser']['username'])
                                if not user_contacts:
                                    #print("        No contact info available")
                                    on_call_item['email'] = ""
                                    on_call_item['voice'] = ""
                                    on_call_item['sms'] = ""
                                else:
                                    #for method, value in user_contacts.items():
                                    #    print(f"        {method}: {value}")
                                    on_call_item['email'] = user_contacts.get('Email', "")
                                    on_call_item['voice'] = user_contacts.get('Phone', "")
                                    on_call_item['sms'] = user_contacts.get('Phone', "")
                            else:
                                #print("    On-Call: None")
                                on_call_item['username'] = "No one is on call"
                                on_call_item['email'] = ""
                                on_call_item['voice'] = ""
                                on_call_item['sms'] = ""
                        retval.append(on_call_item)
                    #oncall_names = [{oncall['slug']: oncall['name']} for oncall in oncalls_data]
                    #return oncall_names
                else:
                    print("Error retrieving on-calls:", response.status_code, response.text)
                    return []
            except Exception as ex:
                print("Error retrieving on-calls:", str(ex))
                return []
    except Exception as ex:
        print("Error retrieving teams:", str(ex))

    return json.dumps(retval)

def print_oncall() -> None:
    """Retrieve and print on-call info for Splunk On-Call teams.
    """
    try:
        teams = get_teams()
        try:
            for team in teams:
                print(f"Team: {team['name']}")
                get_team_oncalls(team['slug'])
        except Exception as ex:
            print("Error retrieving on-calls:", str(ex))
    except Exception as ex:
        print("Error retrieving teams:", str(ex))

def get_team_oncalls(slug: str) -> list:
    """Retrieve the list of on-call schedules for a Splunk On-Call team.
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
                        user_contacts = get_user_contacts(item['onCallUser']['username'])
                        if not user_contacts:
                            print("        No contact info available")
                        else:
                            for method, value in user_contacts.items():
                                print(f"        {method}: {value}")
                    else:
                        print("    On-Call: None")
            #oncall_names = [{oncall['slug']: oncall['name']} for oncall in oncalls_data]
            #return oncall_names
        else:
            print("Error retrieving on-calls:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Error retrieving on-calls:", str(ex))
        return []

def get_user_contacts(userid: str) -> dict:
    """Retrieve contact info for a Splunk On-Call user.
       Return a dictionary of contact info.
    """
    contactMethods = {}
    try:
        response = requests.get(url + "/v1/user/" + userid + "/contact-methods", headers=headers, timeout=10)
        if response.status_code == 200:
            contact_data = response.json()
            for contactMethod in contact_data['emails']['contactMethods']:
                #print(f"  Email: {contactMethod['value']}")
                contactMethods['Email'] = contactMethod['value']
            for contactMethod in contact_data['phones']['contactMethods']:
                #print(f"  Email: {contactMethod['value']}")
                contactMethods['Phone'] = contactMethod['value']
            return contactMethods
        else:
            print("Error reading contact data:", response.status_code, response.text)
            return {}
    except Exception as ex:
        print("Error fetching contact methods:", str(ex))
        return {}

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

def get_teams() -> list:
    """Retrieve a list of teams from the Splunk On-Call account.
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

if __name__ == '__main__':
    #try:
    #    print_oncall()
    #except Exception as ex:
    #    print("Error displaying on-call data:", str(ex))
        
    try:
        oncall_json = print_oncall_json_v2()
        print(oncall_json)
    except Exception as ex:
        print("Error retrieving on-call JSON data:", str(ex))
