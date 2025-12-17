import requests
import json
from splunkoncall import SplunkOnCall
     
# Define keys for Splunk On-Call API.
api_id="2sh110zhj2odraenp62bmi1ey"
api_key="735f5075000c4f1bb7f7ac2460f08281"
 
if __name__ == '__main__':
    #try:
    #    print_oncall()
    #except Exception as ex:
    #    print("Error displaying on-call data:", str(ex))
        
    try:
        soc = SplunkOnCall(api_key=api_key, api_id=api_id)
        oncall_json = soc.print_oncall_json()
        print(oncall_json)
    except Exception as ex:
        print("Error retrieving on-call JSON data:", str(ex))
