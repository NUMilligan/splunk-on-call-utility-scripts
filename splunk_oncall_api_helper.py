import requests
import json

class SplunkOnCall ():
    """Basic helper class for interacting with the Splunk On-Call API.
    """
    def __init__(self, api_key: str, api_id: str):
        self.api_key = api_key
        self.api_id = api_id
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-VO-Api-Id": api_id,
            "X-VO-Api-Key": api_key
        }
        self.url = "https://api.victorops.com/api-public"

    def splunkoncall(self):
        print(self.url)

    def print_oncall_json(self) -> object:
        """Retrieve on-call info for Splunk On-Call teams.
            Return data as a JSON-formatted object.
        """
        retval = []

        try:
            response = requests.get(self.url + "/v1/oncall/current", headers=self.headers, timeout=10)
            data = response.json()
            teams = sorted(data['teamsOnCall'], key=lambda d: d['team']['name'])
            for team in teams:
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
                            on_call_item['username'] = self.get_user(user['onCalluser']['username'])['displayName']
                            user_contacts = self.get_user_contacts(user['onCalluser']['username'])
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
            print("Error retrieving on-calls for JSON:", str(ex))
            return []

        return json.dumps(retval)

    def print_oncall_list(self) -> str:
        """Retrieve on-call info for Splunk On-Call teams.
            Return data as a formatted list.
        """
        retval = ""

        try:
            response = requests.get(self.url + "/v1/oncall/current", headers=self.headers, timeout=10)
            data = response.json()
            teams = sorted(data['teamsOnCall'], key=lambda d: d['team']['name'])
            for team in teams:
                # If no one is on call for the team, create a placeholder entry
                # If there are on-call users, create entries for each user
                if  team['oncallNow'] == []:
                    retval += f"{team['team']['name']}\n"
                    retval += f"    No one is on call\n"
                else:
                    for oncallNow in team['oncallNow']:
                        for user in oncallNow['users']:
                            retval += f"{team['team']['name']} ({oncallNow['escalationPolicy']['name']})\n"
                            retval += f"    {self.get_user(user['onCalluser']['username'])['displayName']} is on call\n"
                            user_contacts = self.get_user_contacts(user['onCalluser']['username'])
                            if user_contacts:
                                retval += f"      Email: {user_contacts.get('Email', '')}\n"
                                retval += f"      Phone: {user_contacts.get('Phone', '')}\n"
        except Exception as ex:
            print("Error retrieving on-calls for list:", str(ex))
            return []

        return retval

    def print_contacts_list(self) -> str:
        """Retrieve contact info for Splunk On-Call users.
            Return data as a formatted list.
        """
        retval = ""

        try:
            response = requests.get(self.url + "/v2/user", headers=self.headers, timeout=10)
            data = response.json()
            users = sorted(data['users'], key=lambda d: d['lastName'])

            for user in users:
                retval += f"{user['displayName']}\n"
                user_contacts = self.get_user_contacts(user['username'])
                if user_contacts:
                    retval += f"      Email: {user_contacts.get('Email', '')}\n"
                    retval += f"      Phone: {user_contacts.get('Phone', '')}\n"
                else:
                    retval += "      No contact info for this user\n"
        except Exception as ex:
            print("Error retrieving user contact info for list:", str(ex))
            return []

        return retval

    def get_user_contacts(self, userid: str) -> dict:
        """Retrieve contact info for a Splunk On-Call user.
        Return a dictionary of contact info.
        """
        contactMethods = {}
        try:
            response = requests.get(self.url + "/v1/user/" + userid + "/contact-methods", headers=self.headers, timeout=10)
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

    def get_user(self, username: str) -> dict:
        """Retrieve user details by username from the Splunk On-Call account.
            Return user details as a dictionary.
        """
        try:
            response = requests.get(self.url + "/v1/user/" + username, headers=self.headers, timeout=10)
            if response.status_code == 200:
                user_data = response.json()
                return user_data
            else:
                print("Error retrieving user:", response.status_code, response.text)
                return {}
        except Exception as ex:
            print("Error retrieving user:", str(ex))
            return {}

    def set_maintenance_mode(self, routing_keys: list[str], message: str) -> bool:
        """Set maintenance mode for a routing key in Splunk On-Call.
            If the maintenance mode is set successfully, return True.
            If it can't be set, return False.
        """
        payload = {
            "type": "RoutingKeys",
            "names": routing_keys,
            "purpose": message
        }

        try:
            response = requests.post(self.url + "/v1/maintenancemode/start", headers=self.headers, json=payload, timeout=10)
            if response.status_code == 200:
                return True
            else:
                print("Error setting maintenance mode:", response.status_code, response.text)
                return False
        except Exception as ex:
            print("Error setting maintenance mode:", str(ex))
            return False