import requests
import json

class SplunkOnCall ():
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
            print("Error retrieving on-calls:", str(ex))
            return []

        return json.dumps(retval)

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
