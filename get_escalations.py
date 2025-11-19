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

def get_policy(policy_slug: str) -> dict:
    """Get a specific escalation policy from Splunk On-Call by slug.
        If the request is successful, return the escalation policy.
        If the request fails, return an empty dictionary.
    """
    try:
        response = requests.get(url + "/policies/" + policy_slug, headers=headers, timeout=10)
        if response.status_code == 200:
            policy = response.json()
            return policy
        else:
            print("Error getting policy:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Exception getting policy:", str(ex))
        return []

def get_policies() -> list:
    """Get a list of escalation policies from Splunk On-Call.
        If the request is successful, return a list of escalation policies.
        If the request fails, return an empty list.
    """
    try:
        response = requests.get(url + "/policies", headers=headers, timeout=10)
        if response.status_code == 200:
            policies = response.json()["policies"]
            return policies
        else:
            print("Error getting policies:", response.status_code, response.text)
            return []
    except Exception as ex:
        print("Exception getting policies:", str(ex))
        return []
    
if __name__ == '__main__':

    for policy in get_policies():
        print("Policy:", policy['policy']['slug'],"For team:", policy['team']['name'])
        policy_details = get_policy(policy['policy']['slug'])
        # I only want to see details when the first step has more than one action
        #if policy_details and 'steps' in policy_details and len(policy_details['steps'][0]['entries']) > 1:
        #    print("Step 1:(",len(policy_details['steps'][0]['entries']),"actions)", policy_details['steps'][0])
        #else:
        #    print("Step 1:(",len(policy_details['steps'][0]['entries']),"actions)")
        # Print all steps
        if policy_details and 'steps' in policy_details:
            stepnumber = 1
            for step in policy_details['steps']:
                print("Step ", stepnumber,": ",step['entries'])
                stepnumber += 1

    