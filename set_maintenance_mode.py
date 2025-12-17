import requests
import time
from splunk_oncall_api_helper import SplunkOnCall
     
# Define keys for Splunk On-Call API.
api_id="2sh110zhj2odraenp62bmi1ey"
api_key="735f5075000c4f1bb7f7ac2460f08281"


if __name__ == '__main__':

    routing_keys = ['Feinberg-IT-Infrastructure',
        'feinberg-it-infrastructure-tier1',
        'IT-Communications',
        'Media_Technology_Innovation',
        'NUIT-Alumni-Analysts',
        'nuit-as-ado-es-cloud-services-and-integrations',
        'nuit-as-ado-es-cloud-services-and-integrations_business-hours',
        'NUIT-AS-ADO-ESHRS-CAESAR-Technical',
        'nuit-as-ado-sysdev',
        'nuit-as-ado-sysdev_business-hours',
        'nuit-as-ado-sysdev_no-one',
        'NUIT-CI-CollaborationServices',
        'NUIT-CI-PIPS-AppDBAs',
        'NUIT-CI-PIPS-HPC',
        'NUIT-CI-PIPS-HPC_business-hours',
        'NUIT-CI-PIPS-HPC_business-hours-ext',
        'NUIT-CI-PIPS-HPC_GPFS',
        'NUIT-CI-PIPS-Infrastructure',
        'NUIT-CI-PIPS-Storage',
        'nuit-ci-so-qualitycontrol',
        'nuit-ci-tns-datanetwork_24x7',
        'nuit-ci-tns-datanetwork_never',
        'NUIT-CI-TNS-FieldOperations',
        'NUIT-CI-TNS-VoiceNetwork',
        'nuit-iso-iam',
        'NUIT_ADO_PeopleSoft_Financials',
        'NUIT_AS_ADO_MyHR',
        'NUIT_AS_OPM',
        'NUIT_CI_ServiceOperation',
        'NUIT_CI_TNS_Firewall',
        'NUIT_CI_TNS_Radio',
        'NUIT_Facilities_Management_Analysts',
        'NUIT_ISO_Security',
        'NUIT_ITSS_Teaching_Learning_Technologies',
        'NUIT_Media_Design_ESP',
        'NUIT_Media_Design_LSTS',
        'NUIT_TSS_DSS',
        'NUIT_TSS_ITServiceManagement',
        'NUIT_TSS_SupportServices',
        'weinberg_it',
        'weinberg_it_devs'
    ]
    soc = SplunkOnCall(api_key=api_key, api_id=api_id)
    
    for key in routing_keys:
        if soc.set_maintenance_mode([key], 'Team not transitioning to Splunk On-Call'):
            print(f"Maintenance mode set successfully for {key}.")
        else:
            print(f"Failed to set maintenance mode for {key}.")
        time.sleep(1)  # To avoid hitting rate limits
