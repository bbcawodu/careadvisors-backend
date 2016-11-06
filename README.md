# Consumer Metrics and Appointments Backend

This is the code for the backend component of our metrics and appointments apps. It enables the API that transmits data between the frontend and the backend.



## Installation

This app runs on a django installation hosted on Heroku. To install Heroku for code editing, go to: https://devcenter.heroku.com/articles/getting-started-with-python#introduction and follow the instructions for your particular operating system.



## Presence Healthcare Appointment Scheduler Backend

### Presence Healthcare Appointment Addition API
To add an appointment to the database using our appointments API, make a POST request to: http://picbackend.herokuapp.com/submitappointment/. The POST data should be a JSON document which has the following format:

```
{
 "First Name": String,
 "Last Name": String,
 "Email": String,
 "Phone Number": String,
 "Preferred Language": String (Not Required),
 "Best Contact Time": String (Not Required),
 "Appointment": {
                 "Name": String,
                 "Street Address": String,
                 "City": String,
                 "State": String,
                 "Zip Code": String,
                 "Phone Number": String,
                 "Appointment Slot": {
                                      "Date": {
                                               "Month": Integer,
                                               "Day": Integer,
                                               "Year": Integer
                                              },
                                      "Start Time": {
                                                     "Hour": Integer,
                                                     "Minutes": Integer
                                                    },
                                      "End Time": {
                                                   "Hour": Integer,
                                                   "Minutes": Integer
                                                  }
                                     },
                 "Point of Contact": {
                                      "First Name": String,
                                      "Last Name": String,
                                      "Email": String,
                                      "Type": String
                                     }
                }
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the Appointment class corresponding to the POSTed JSON doc will be created and saved in the database.
        - If there isn't a consumer database entry with an email field corresponding to the POST, one is created.
        - If there isn't a location database entry with a name field corresponding to the POST, one is created.
        - If there isn't a staff database entry with an email field corresponding to the POST, one is created.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.



### Presence Healthcare Appointments Viewer
Go to http://picbackend.herokuapp.com/viewappointments to view what appointments have been submitted by consumers and to whom they have been assigned.



## Staff Account Backend API

### Staff Data Submission API
To modify or add members of the PICStaff class in the database, submit a POST request to: http://picbackend.herokuapp.com/editstaff/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Last Name": String,
"Email": String,
"User Type": String,
"User County": String,
"Base Location Names": [Strings (Can be None or empty string)],
"MPN": String(Can be None or empty string),
"Database ID": Integer(Required when "Database Action" == "Staff Modification" or "Staff Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a staff member database entry.
    - To add a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a staff member database entry.
    - To modify a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a staff member database entry.
    - To delete a staff member database entry, the value for "Database Action" in the POST request must equal "Staff Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Staff Data Retrieval API
- To retrieve staff data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/staff? with the following optional parameters: "fname", "lname", "email", "mpn", "id"
    - "fname" corresponds to first name.
    - "lname" corresponds to last name.
    - "email" corresponds to email.
    - "mpn" corresponds to mpn.
    - "county" corresponds to email.
    - "id" corresponds to database id.
        - passing "all" as the value will return all staff members
    - All parameters may have a single or multiple values separated by commas
    - One parameter is allowed at a time (only "fname" and "lname" can be grouped)
        - If "fname" and "lname" are given simultaneously as parameters, only one value each is permitted.
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Type": String,
                "Database ID": Integer,
                "County": String,
                "Region": String,
                "First Name": String,
                "Last Name": String,
                "Base Location": [{
                                    "Location Name": String,
                                    "Address Line 1": String,
                                    "Address Line 2": String,
                                    "City": String,
                                    "State": String,
                                    "Zipcode": String,
                                    "Country": String,
                                    "Database Action": String
                                 },
                                  ...(Can be Empty)],
                "MPN": String,
                "Consumers":[
                                {
                                "First Name": String,
                                "Best Contact Time": String,
                                "Database ID": Integer,
                                "Last Name": String,
                                "Preferred Language": String,
                                "Navigator": String,
                                "Phone Number": String,
                                "Email": String
                                },
                                ....
                            ],
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If staff members are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If staff members are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.



## Consumer Account Backend API

### Consumer Data Submission API
To modify or add members of the PICConsumer class in the database, submit a POST request to: http://picbackend.herokuapp.com/editconsumer/. The POST data a JSON document using the following template:

```
{
"First Name": String,
"Middle Name": String (Can be empty),
"Last Name": String,
"Email": String,
"Phone Number": String (Can be empty),
"Zipcode": String,
"Address": String (Can be empty),
"Met Navigator At": String,
"Household Size": Integer,
"Navigator Notes": [
                        "These are",
                        "sample notes",
                        "navigators write about consumers",
                        ...
                    ](Can be an empty array),
"Plan": String (Can be empty),
"Preferred Language": String (Can be empty),
"Navigator Database ID": Integer,
"Consumer Database ID": Integer(Required when "Database Action" == "Consumer Modification" or "Consumer Deletion"),
"Database Action": String,
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a consumer database entry.
    - To add a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Addition".
    - All other fields except "Consumer Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a consumer database entry.
    - To modify a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Consumer Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a consumer database entry.
    - To delete a consumer database entry, the value for "Database Action" in the POST request must equal "Consumer Deletion".
    - The only other field should be "Consumer Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Data Retrieval API
- To retrieve consumer data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/consumers? with the following parameters(at least one required)
    - A maximum of 20 consumer records with full fields will be returned due to size constraints
        - The rest are consumer database IDs
        - Links to pages with the rest of the full records for your query will be given if you request without "page" parameter
    - "fname" corresponds to consumer first name.
    - "lname" corresponds to consumer last name.
        - "fname" and "lname" can be given simultaneously as parameters. If so, only one value each is permitted.
    - "email" corresponds to consumer email.
    - "region" corresponds to consumer region.
    - "id" corresponds to consumer class database id.
        - passing "all" as the value will return all staff members
    - "navid" corresponds to staff member class database id. (Can be combined with any of the above parameters)
    - "page" corresponds to the current page of consumer instances to be displayed with full fields. 
        - if this parameter is missing, the first 20 consumer instances will be displayed with full fields.
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Email": String,
                "Phone Number": String,
                "Database ID": Integer,
                "Preferred Language": String,
                "First Name": String,
                "Middle Name": String,
                "Last Name": String,
                "Navigator": String,
                "Zipcode": String,
                "Navigator Notes": [
                                        "These are",
                                        "sample notes",
                                        "navigators write about consumers",
                                        ...
                                    ],
                "Address": String,
                "Met Navigator At": String,
                "Household Size": Integer,
                "Plan": String,
                "Best Contact Time": String,
            },
            ...,
            ...,
            ...,
            up to 20 full record consumer entries,
            2(Database IDs for the rest),
            6,
            9
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        },
        "Page URLs": Array of strings (Will be missing if "page" parameter is given OR less than 20 consumers in results)
    }
    ```

- If consumers are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If consumers are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
- If "page" parameter is missing and there is more than one page of customer instances to display with all fields, "Page
    URLs" key will be present in the root response dictionary. 
    
    
    
## Consumer Metrics Backend API

### Consumer Metrics Submission API
To submit an entry of consumer metrics data corresponding to a specific staff member, make a POST request to: http://picbackend.herokuapp.com/submitmetrics/. The POST data should be a JSON document which has the following format:

```
{
"Email": String,
"User Type": "IPC" or "Navigator",
"Consumer Metrics": {"Metrics Date":{"Day": Integer,
                                    "Month": Integer,
                                    "Year": Integer,},
                    "County": String,
                    "Location": String,
                    "no_general_assis": "Number of consumers assisted with general questions about health insurance" (Integer),
                    "no_plan_usage_assis": "Number of consumers assisted with using their healthcare plan " (Integer),
                    "no_locating_provider_assis": "Number of consumers assisted with locating providers " (Integer),
                    "no_billing_assis": "Number of consumers assisted with billing and payment questions " (Integer),
                    "no_enroll_apps_started": "Number of enrollment applications started" (Integer),
                    "no_enroll_qhp": "Number of consumers enrolled in QHP " (Integer),
                    "no_enroll_abe_chip": "Number of consumers enrolled in ABE/CHIP " (Integer),
                    "no_enroll_shop": "Number of consumers enrolled in SHOP " (Integer),
                    "no_referrals_agents_brokers": "Number of referrals to agents/brokers " (Integer),
                    "no_referrals_ship_medicare": "Number of referrals to SHIP Counselor/Medicare " (Integer),
                    "no_referrals_other_assis_programs": "Number of referrals to other consumer assistance/health insurance programs " (Integer),
                    "no_referrals_issuers": "Number of referrals to issuers (e.g. You had to call Ambetter to get replacement insurance card.)" (Integer),
                    "no_referrals_doi": "Number of referrals to DOI (Illinois Department of Insurance grievances or insurance complaints)" (Integer),
                    "no_mplace_tax_form_assis": "Number of consumers assisted with Marketplace Tax Forms (1095-A)" (Integer),
                    "no_mplace_exempt_assis": "Number of consumers assisted with Marketplace Exemptions" (Integer),
                    "no_qhp_abe_appeals": "Number of submitted QHP/ABE appeals (How many appeals did you submit for Marketplace and Medicaid)" (Integer),
                    "no_data_matching_mplace_issues": "Number of data matching issues/Marketplace issues (Issue with getting consumer identity confirmed)" (Integer),
                    "no_sep_eligible": "Number of SEP eligible" (Integer),
                    "no_employ_spons_cov_issues": "Number of employer-sponsored coverage issues (non-Marketplace or Medicaid)" (Integer),
                    "no_aptc_csr_assis": "Number of consumers assisted with APTC/CSR (Advanced Premium Tax Credit issues or customer service issues with call center)" (Integer),
                    "cmplx_cases_mplace_issues": "Complex cases and other Marketplace issues (Note other issues or trends not listed. You may mark N/A if nothing to report on this day)" (String - Can be empty string),
                    "Plan Stats": [
                                    {"Issuer Name": String,
                                    "Enrollments": Integer,
                                    "Premium Type": String,
                                    "Metal Level": String},
                                    {},
                                    ....
                                  ],
                    }
}
```


The Following is a list of possible Plan Issuer Names with corresponding model constant names:
```
[
    MISCELLANEOUS = "Miscellaneous"
    HEALTH_ALLIANCE_MEDICAL_PLANS = 'Health Alliance Medical Plans, Inc.'
    BLUE_CROSS_BLUE_SHIELD_OF_ILLINOIS = 'Blue Cross Blue Shield of Illinois'
    HUMANA_HEALTH_PLAN = 'Humana Health Plan, Inc.'
    CELTIC_INSURANCE_COMPANY = "Celtic Insurance Company"
    CIGNA_HEALTHCARE_OF_ILLINOIS = 'Cigna HealthCare of Illinois, Inc.'
    PREMERA_BLUE_CROSS_BLUE_SHIELD_OF_ALASKA = 'Premera Blue Cross Blue Shield of Alaska'
    BLUE_CROSS_AND_BLUE_SHIELD_OF_ALABAMA = 'Blue Cross and Blue Shield of Alabama'
    QUALCHOICE_LIFE_AND_HEALTH_INSURANCE_COMPANY = "QualChoice Life & Health Insurance Company, Inc."
    USABLE_MUTUAL_INSURANCE_COMPANY = "USAble Mutual Insurance Company"
    QCA_HEALTH_PLAN = "QCA Health Plan, Inc."
    FLORIDA_HEALTH_CARE_PLAN = "Florida Health Care Plan, Inc."
    MEDICA_INSURANCE_COMPANY = "Medica Insurance Company"
    CARESOURCE_INDIANA = "CareSource Indiana, Inc."
    BLUE_CROSS_AND_BLUE_SHIELD_OF_ARIZONA = "Blue Cross and Blue Shield of Arizona, Inc."
    BLUE_CROSS_AND_BLUE_SHIELD_OF_FLORIDA = "Blue Cross and Blue Shield of Florida"
    HEALTH_OPTIONS = "Health Options, Inc."
    AETNA_LIFE_INSURANCE_COMPANY = "Aetna Life Insurance Company"
    AETNA_HEALTH_INC_A_PA_CORP = "Aetna Health Inc. (a PA corp.)"
    HIGHMARK_BCBSD = "Highmark BCBSD Inc."
    HEALTH_NET_OF_ARIZONA = "Health Net of Arizona, Inc."
    HEALTH_FIRST_COMMERCIAL_PLANS = 'Health First Commercial Plans, Inc.'
    HUMANA_MEDICAL_PLAN = 'Humana Medical Plan, Inc.'
    MOLINA_HEALTHCARE_OF_FLORIDA = "Molina Healthcare of Florida, Inc"
    ALLIANT_HEALTH_PLANS = 'Alliant Health Plans'
    BLUE_CROSS_BLUE_SHIELD_HEALTHCARE_PLAN_OF_GEORGIA = 'Blue Cross Blue Shield Healthcare Plan of Georgia, Inc.'
    KAISER_FOUNDATION_HEALTH_PLAN_OF_GEORGIA = 'Kaiser Foundation Health Plan of Georgia'
    AMBETTER_OF_PEACH_STATE = 'Ambetter of Peach State Inc.'
    HUMANA_EMPLOYERS_HEALTH_PLAN_OF_GEORGIA = 'Humana Employers Health Plan of Georgia, Inc.'
    WELLMARK_VALUE_HEALTH_PLAN = 'Wellmark Value Health Plan, Inc.'
    CARESOURCE_KENTUCKY_CO = 'CareSource Kentucky Co.'
    GUNDERSEN_HEALTH_PLAN = 'Gundersen Health Plan, Inc.'
    WELLMARK_SYNERGY_HEALTH = 'Wellmark Synergy Health, Inc.'
    ANTHEM_INS_COMPANIES_INC_ANTHEM_BCBS = 'Anthem Ins Companies Inc(Anthem BCBS)'
    MDWISE_MARKETPLACE = 'MDwise Marketplace, Inc.'
    HAWAII_MEDICAL_SERVICE_ASSOCIATION = 'Hawaii Medical Service Association'
    KAISER_FOUNDATION_HEALTH_PLAN = 'Kaiser Foundation Health Plan, Inc.'
    AETNA_HEALTH_OF_IOWA = 'Aetna Health of Iowa Inc.'
    BLUECROSS_BLUESHIELD_KANSAS_SOLUTIONS = 'BlueCross BlueShield Kansas Solutions, Inc.'
    BLUE_CROSS_AND_BLUE_SHIELD_OF_KANSAS_CITY = 'Blue Cross and Blue Shield of Kansas City'
    ANTHEM_HEALTH_PLANS_OF_KY_ANTHEM_BCBS = 'Anthem Health Plans of KY(Anthem BCBS)'
    HUMANA_HEALTH_BENEFIT_PLAN_OF_LOUISIANA = 'Humana Health Benefit Plan of Louisiana, Inc.'
    HMO_LOUISIANA = 'HMO Louisiana, Inc.'
    VANTAGE_HEALTH_PLAN = 'Vantage Health Plan, Inc.'
    LOUISIANA_HEALTH_SERVICE_AND_INDEMNITY_COMPANY = 'Louisiana Health Service & Indemnity Company'
    MAINE_COMMUNITY_HEALTH_OPTIONS = 'Maine Community Health Options'
    ANTHEM_HEALTH_PLANS_OF_ME_ANTHEM_BCBS = 'Anthem Health Plans of ME(Anthem BCBS)'
    HARVARD_PILGRIM_HEALTH_CARE = 'Harvard Pilgrim Health Care Inc.'
    BLUE_CROSS_BLUE_SHIELD_OF_MICHIGAN_MUTUAL_INSURANCE_COMPANY = 'Blue Cross Blue Shield of Michigan Mutual Insurance Company'
    MCLAREN_HEALTH_PLAN_COMMUNITY = 'McLaren Health Plan Community'
    PRIORITY_HEALTH = 'Priority Health'
    BLUE_CARE_NETWORK_OF_MICHIGAN = 'Blue Care Network of Michigan'
    HEALTH_ALLIANCE_PLAN_HAP = 'Health Alliance Plan (HAP)'
    MERIDIAN_HEALTH_PLAN_OF_MICHIGAN = 'Meridian Health Plan of Michigan, Inc.'
    HUMANA_MEDICAL_PLAN_OF_MICHIGAN = 'Humana Medical Plan of Michigan, Inc.'
    MOLINA_HEALTHCARE_OF_MICHIGAN = 'Molina Healthcare of Michigan, Inc.'
    HUMANA_NSURANCE_COMPANY = 'Humana Insurance Company'
    PHYSICIANS_HEALTH_PLAN = 'Physicians Health Plan'
    HEALTHY_ALLIANCE_LIFE_CO_ANTHEM_BCBS = 'Healthy Alliance Life Co(Anthem BCBS)'
    MEDICA_HEALTH_PLANS = 'Medica Health Plans'
    CARESOURCE = 'CareSource'
    MONTANA_HEALTH_COOPERATIVE = 'Montana Health Cooperative'
    CIGNA_HEALTH_AND_LIFE_INSURANCE_COMPANY = 'Cigna Health and Life Insurance Company'
    AMERIHEALTH_HMO = 'AmeriHealth HMO, Inc.'
    TOTAL_HEALTH_CARE_USA = 'Total Health Care USA, Inc.'
    NEW_MEXICO_HEALTH_CONNECTIONS = 'New Mexico Health Connections'
    AMBETTER_OF_MAGNOLIA = 'Ambetter of Magnolia Inc.'
    AULTCARE_INSURANCE_COMPANY = 'AultCare Insurance Company'
    PACIFICSOURCE_HEALTH_PLANS = 'PacificSource Health Plans'
    BLUE_CROSS_AND_BLUE_SHIELD_OF_MONTANA = 'Blue Cross and Blue Shield of Montana'
    HORIZON_HEALTHCARE_SERVICES = 'Horizon Healthcare Services, Inc.'
    AMERIHEALTH_INS_COMPANY_OF_NEW_JERSEY = 'AmeriHealth Ins Company of New Jersey'
    MEDICAL_HEALTH_INSURING_CORP_OF_OHIO = 'Medical Health Insuring Corp. of Ohio'
    BLUE_CROSS_BLUE_SHIELD_OF_NORTH_DAKOTA = 'Blue Cross Blue Shield of North Dakota'
    BLUE_CROSS_AND_BLUE_SHIELD_OF_NC = 'Blue Cross and Blue Shield of NC'
    CIGNA_HEALTHCARE_OF_NORTH_CAROLINA = 'Cigna HealthCare of North Carolina, Inc.'
    SANFORD_HEALTH_PLAN = 'Sanford Health Plan'
    GEISINGER_HEALTH_PLAN = 'Geisinger Health Plan'
    HARVARD_PILGRIM_HEALTH_CARE_OF_NE = 'Harvard Pilgrim Health Care of NE'
    MINUTEMAN_HEALTH = 'Minuteman Health, Inc'
    MATTHEW_THORNTON_HLTH_PLAN_ANTHEM_BCBS = 'Matthew Thornton Hlth Plan(Anthem BCBS)'
    COMMUNITY_INSURANCE_COMPANY_ANTHEM_BCBS = 'Community Insurance Company(Anthem BCBS)'
    MOLINA_HEALTHCARE_OF_NEW_MEXICO = 'Molina Healthcare of New Mexico, Inc.'
    CHRISTUS_HEALTH_PLAN = 'CHRISTUS Health Plan'
    BLUE_CROSS_BLUE_SHIELD_OF_NEW_MEXICO = 'Blue Cross Blue Shield of New Mexico'
    PROMINENCE_HEALTHFIRST = 'Prominence HealthFirst'
    ROCKY_MOUNTAIN_HOSPITAL_AND_MEDICAL_SERVICE_INC_DBA_ANTHEM_BLUE_CROSS_AND_BLUE_SHIELD = 'Rocky Mountain Hospital and Medical Service, Inc., dba Anthem Blue Cross and Blue Shield'
    HMO_COLORADO_INC_DBA_HMO_NEVADA = 'HMO Colorado, Inc., dba HMO Nevada'
    HEALTH_PLAN_OF_NEVADA = 'Health Plan of Nevada, Inc.'
    MOLINA_HEALTHCARE_OF_OHIO = 'Molina Healthcare of Ohio, Inc.'
    BUCKEYE_COMMUNITY_HEALTH_PLAN = 'Buckeye Community Health Plan'
    PREMIER_HEALTH_PLAN = 'Premier Health Plan, Inc.'
    HUMANA_HEALTH_PLAN_OF_OHIO = 'Humana Health Plan of Ohio, Inc.'
    PARAMOUNT_INSURANCE_COMPANY = 'Paramount Insurance Company'
    CONSUMERS_LIFE_INSURANCE_COMPANY = 'Consumers Life Insurance Company'
    SUMMA_INSURANCE_COMPANY = 'Summa Insurance Company, Inc.'
    MODA_HEALTH_PLAN = 'Moda Health Plan, Inc.'
    BRIDGESPAN_HEALTH_COMPANY = 'BridgeSpan Health Company'
    BLUE_CROSS_BLUE_SHIELD_OF_OKLAHOMA = 'Blue Cross Blue Shield of Oklahoma'
    KAISER_FOUNDATION_HEALTHPLAN_OF_THE_NW = 'Kaiser Foundation Healthplan of the NW'
    ATRIO_HEALTH_PLANS = 'ATRIO Health Plans'
    FIRST_PRIORITY_HEALTH = 'First Priority Health'
    INDEPENDENCE_BLUE_CROSS_QCC_INS_CO = 'Independence Blue Cross (QCC Ins. Co.)'
    KEYSTONE_HEALTH_PLAN_EAST = 'Keystone Health Plan East, Inc'
    HIGHMARK_INC = 'Highmark Inc.'
    HIGHMARK_HEALTH_INSURANCE_COMPANY = 'Highmark Health Insurance Company'
    UPMC_HEALTH_OPTIONS = 'UPMC Health Options, Inc.'
    BLUE_CROSS_AND_BLUE_SHIELD_OF_SOUTH_CAROLINA = 'Blue Cross and Blue Shield of South Carolina'
    PROVIDENCE_HEALTH_PLAN = 'Providence Health Plan'
    CAPITAL_ADVANTAGE_ASSURANCE_COMPANY = 'Capital Advantage Assurance Company'
    AVERA_HEALTH_PLANS = 'Avera Health Plans, Inc.'
    UNITY_HEALTH_PLANS_INSURANCE_CORPORATION = 'Unity Health Plans Insurance Corporation'
    MERCYCARE_HMO = 'MercyCare HMO, Inc.'
    BLUE_CROSS_BLUE_SHIELD_OF_TENNESSEE = 'Blue Cross Blue Shield of Tennessee'
    MEDICA_HEALTH_PLANS_OF_WISCONSIN = 'Medica Health Plans of Wisconsin'
    OPTIMA_HEALTH_PLAN = 'Optima Health Plan'
    BLUE_CROSS_BLUE_SHIELD_OF_TEXAS = 'Blue Cross Blue Shield of Texas'
    HUMANA_HEALTH_PLAN_OF_TEXAS = 'Humana Health Plan of Texas, Inc.'
    SHA_LLC_DBA_FIRSTCARE_HEALTH_PLANS = 'SHA, LLC DBA FirstCare Health Plans'
    GROUP_HOSPITALIZATION_AND_MEDICAL_SERVICES = 'Group Hospitalization and Medical Services Inc.'
    KAISER_FOUNDATION_HEALTH_PLAN_OF_THE_MID_ATLANTIC_STATES = 'Kaiser Foundation Health Plan of the Mid-Atlantic States, Inc.'
    HEALTHKEEPERS_INC = 'HealthKeepers, Inc.'
    SENDERO_HEALTH_PLANS = 'Sendero Health Plans, inc.'
    OSCAR_INSURANCE_COMPANY_OF_TEXAS = 'Oscar Insurance Company of Texas'
    COMMUNITY_HEALTH_CHOICE = 'Community Health Choice, Inc.'
    PIEDMONT_COMMUNITY_HEALTHCARE = 'Piedmont Community HealthCare, Inc.'
    PROMINENCE_HEALTHFIRST_OF_TEXAS = 'Prominence HealthFirst of Texas, Inc.'
    INNOVATION_HEALTH_INSURANCE_COMPANY = 'Innovation Health Insurance Company'
    UNITEDHEALTHCARE_OF_THE_MID_ATLANTIC = 'UnitedHealthcare of the Mid-Atlantic Inc'
    MOLINA_HEALTHCARE_OF_TEXAS = 'Molina Healthcare of Texas, Inc.'
    PIEDMONT_COMMUNITY_HEALTHCARE_HMO = 'Piedmont Community HealthCare HMO, Inc.'
    CAREFIRST_BLUECHOICE = 'CareFirst BlueChoice, Inc.'
    SELECTHEALTH = 'SelectHealth'
    MOLINA_HEALTHCARE_OF_UTAH = 'Molina Healthcare of Utah'
    UNIVERSITY_OF_UTAH_HEALTH_INSURANCE_PLANS = 'University of Utah Health Insurance Plans'
    GROUP_HEALTH_COOPERATIVE_OF_SOUTH_CENTRAL_WISCONSIN = 'Group Health Cooperative of South Central Wisconsin'
    HEALTH_TRADITION_HEALTH_PLAN = 'Health Tradition Health Plan'
    CHILDRENS_COMMUNITY_HEALTH_PLAN = "Children's Community Health Plan"
    CARESOURCE_WEST_VIRGINIA_CO = 'CareSource West Virginia Co.'
    SECURITY_HEALTH_PLAN_OF_WISCONSIN = 'Security Health Plan of Wisconsin, Inc.'
    DEAN_HEALTH_PLAN = 'Dean Health Plan'
    ASPIRUS_ARISE_HEALTH_PLAN_OF_WISCONSIN = 'Aspirus Arise Health Plan of Wisconsin, Inc.'
    MOLINA_HEALTHCARE_OF_WISCONSIN = 'Molina Healthcare of Wisconsin, Inc.'
    COMPCARE_HEALTH_SERV_INS_CO_ANTHEM_BCBS = 'Compcare Health Serv Ins Co(Anthem BCBS)'
    COMMON_GROUND_HEALTHCARE_COOPERATIVE = 'Common Ground Healthcare Cooperative'
    HEALTHPARTNERS_INSURANCE_COMPANY = 'HealthPartners Insurance Company'
    NETWORK_HEALTH_PLAN = 'Network Health Plan'
    HIGHMARK_BLUE_CROSS_BLUE_SHIELD_WEST_VIRGINIA = 'Highmark Blue Cross Blue Shield West Virginia'
    BLUE_CROSS_BLUE_SHIELD_OF_WYOMING = 'Blue Cross Blue Shield of Wyoming'
]
```

The following is a list of contact numbers for plan issuers
```
[
    'Health Alliance Medical Plans, Inc.' = '1-800-851-3379, option 3'
    'Blue Cross Blue Shield of Illinois' = '866-514-8044'
    'Humana Health Plan, Inc.' = '1-800-833-6917
    "Celtic Insurance Company" = "1-800-477-7870"
    'Cigna HealthCare of Illinois, Inc.' = '1.866.494.2111'
]
```

The Following is a list of possible Plan Premium Types with corresponding model constant names:
```
[
    HMO = "HMO"
    PPO = "PPO"
    POS = 'POS'
    EPO = 'EPO'
]
```

The Following is a list of possible Plan Metal Levels with corresponding model constant names:
```
[
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = 'Platinum'
    CATASTROPHIC = "Catastrophic"
]
```


In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
           }
}
```

- If there are no errors in the POSTed JSON doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the MetricsSubmission class corresponding to the POSTed JSON doc will be created and saved in the database.
        - Only one metrics submission is allowed per day.
    
- If there are errors in the POSTed JSON doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
### Consumer Metrics Retrieval API.
- To retrieve metrics data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/metrics? with the following optional parameters: "fname", "lname", "email", "mpn", "id", "time", "groupby", "startdate", "enddate", "time", "zipcode", "location", "fields"
    - "fname" corresponds to staff member first name.
    - "lname" corresponds to staff member last name.
    - "email" corresponds to staff member email.
    - "mpn" corresponds to staff member mpn.
    - "id" corresponds to staff member class database id.
        - passing "all" as the value will return all staff members
    - One of the above parameters is allowed at a time (only "fname" and "lname" can be grouped)
        - If "fname" and "lname" are given simultaneously as parameters, only one value each is permitted.
    - The following parameters can be added without limit to the query: "startdate", "enddate", "time", "zipcode", "groupby", "location", "fields"
        - "startdate" and "enddate" must be given in "YYYY-MM-DD" format
        - "time" must be an integer amount of days to look up in the past
        - "zipcode" must be a non empty comma separated string of zipcodes
        - "location" must be a percent encoded string that corresponds to the name of the location you desire to search for
        - "grouby" can be "zipcode" to group the metrics submissions returned by zipcode
        - "fields" must be a percent encoded list of fields that you would like each metrics report to include.
            - If no valid fields are given, all fields of each metrics report will be returned
        
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {
                "Metrics Data": [
                {
                "no_general_assis": "Number of consumers assisted with general questions about health insurance" (Integer),
                "no_plan_usage_assis": "Number of consumers assisted with using their healthcare plan " (Integer),
                "no_locating_provider_assis": "Number of consumers assisted with locating providers " (Integer),
                "no_billing_assis": "Number of consumers assisted with billing and payment questions " (Integer),
                "no_enroll_apps_started": "Number of enrollment applications started" (Integer),
                "no_enroll_qhp": "Number of consumers enrolled in QHP " (Integer),
                "no_enroll_abe_chip": "Number of consumers enrolled in ABE/CHIP " (Integer),
                "no_enroll_shop": "Number of consumers enrolled in SHOP " (Integer),
                "no_referrals_agents_brokers": "Number of referrals to agents/brokers " (Integer),
                "no_referrals_ship_medicare": "Number of referrals to SHIP Counselor/Medicare " (Integer),
                "no_referrals_other_assis_programs": "Number of referrals to other consumer assistance/health insurance programs " (Integer),
                "no_referrals_issuers": "Number of referrals to issuers (e.g. You had to call Ambetter to get replacement insurance card.)" (Integer),
                "no_referrals_doi": "Number of referrals to DOI (Illinois Department of Insurance grievances or insurance complaints)" (Integer),
                "no_mplace_tax_form_assis": "Number of consumers assisted with Marketplace Tax Forms (1095-A)" (Integer),
                "no_mplace_exempt_assis": "Number of consumers assisted with Marketplace Exemptions" (Integer),
                "no_qhp_abe_appeals": "Number of submitted QHP/ABE appeals (How many appeals did you submit for Marketplace and Medicaid)" (Integer),
                "no_data_matching_mplace_issues": "Number of data matching issues/Marketplace issues (Issue with getting consumer identity confirmed)" (Integer),
                "no_sep_eligible": "Number of SEP eligible" (Integer),
                "no_employ_spons_cov_issues": "Number of employer-sponsored coverage issues (non-Marketplace or Medicaid)" (Integer),
                "no_aptc_csr_assis": "Number of consumers assisted with APTC/CSR (Advanced Premium Tax Credit issues or customer service issues with call center)" (Integer),
                "cmplx_cases_mplace_issues": "Complex cases and other Marketplace issues (Note other issues or trends not listed. You may mark N/A if nothing to report on this day)" (String),
                "Date Created": String,
                "County": String,
                "Staff Member ID": Integer,
                "Submission Date": String,
                },
                ...,
                ...,
                ...,
                ],
                "Staff Information": {
                "Database ID": Integer,
                "First Name": String,
                "County": String,
                "Type": String,
                "Last Name": String,
                "Email": String
                }
            },
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If metrics reports are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If metrics reports are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.
    

### Navigator Hub Location Submission URL
- To add a hub location where navigators can submit metrics reports, visit http://picbackend.herokuapp.com/addlocation

The following is a list of the current 2016 Navigator Hub Locations(As of 10/28/16):
```
[
    ['Presence Holy Family Medical Center', '100 North River Road', '', 'Des Plaines', 'IL', '60016', 'United States of America'],
    ['Presence Resurrection Medical Center', '7435 West Talcott Avenue', '', 'Chicago', 'IL', '60631', 'United States of America'],
    ['Community First Medical Center', '5645 W Addison Ave', '', 'Chicago', 'IL', '60634', 'United States of America'],
    ['Mile Square Health Center- Englewood', '641 West 63rd Street', '', 'Chicago', 'IL', '60621', 'United States of America'],
    ['Presence Saint Francis Medical Center', '355 Ridge Avenue', '', 'Evanston', 'IL', '60202', 'United States of America'],
    ['Presence Saint Joseph, Chicago', '2900 North Lake Shore Drive', '', 'Chicago', 'IL', '60657', 'United States of America'],
    ['Thorek Memorial Hospital', '830 E Irving Park Rd', '', 'Chicago', 'IL', '60613', 'United States of America'],
    ['Mile Square Health Center- Main', '1220 S Wood', '', 'Chicago', 'IL', '60608', 'United States of America'],
    ['Presence Saints Mary and Elizabeth Medical Center', '2233 W Division Ave', '', 'Chicago', 'IL', '60622', 'United States of America'],
    ['Illinois Department of Employment Security- Lawrence', '2444 W Lawrence Ave', '', 'Chicago', 'IL', '60625', 'United States of America'],
    ['Illinois Department of Employment Security- Arlington Heights', '723 W Algonquin Rd', '', 'Arlington Heights', 'IL', '60005', 'United States of America'],
    ['Target Area Development Corporation', '1542 W 79th St', '', 'Chicago', 'IL', '60620', 'United States of America'],
    ['Trina Davila Community Services Center', '4345 W Armitage Ave', '', 'Chicago', 'IL', '60639', 'United States of America'],
    ['Chicago Reed Mental Health Center', '4200 N Oak Park Ave', '', 'Chicago', 'IL', '60634', 'United States of America'],
    ["Ann & Robert Lurie Children's Hospital of Chicago- Outpatient Center", '2515 N Clark St', '', 'Chicago', 'IL', '60614', 'United States of America'],
    ['John Madden Mental Health Center', '1200 S 1st Ave', '', 'Hines', 'IL', '60141', 'United States of America'],
    ["Ann & Robert Lurie Children's Hospital of Chicago- Main Hospital", '225 E Chicago Ave', '', 'Chicago', 'IL', '60611', 'United States of America'],
    ['Lincoln Belmont Library', '1659 W Melrose St', '', 'Chicago', 'IL', '60657', 'United States of America'],
    ['James Thompson Center', '100 W Randolph ', '', 'Chicago', 'IL', '60601', 'United States of America'],
    ['PIC Chicago Office - Administrative Office', '222 Merchandise Mart Plaza #1230', '', 'Chicago', 'IL', '60654', 'United States of America'],
    ['Pacific Garden Mission', '1458 S Canal St', '', 'Chicago', 'IL', '60607', 'United States of America'],
    ['Esperanza Health Center- Marquette School Based Health Center', '6550 S Richmond St', '', 'Chicago', 'IL', '60629', 'United States of America'],
    ['Esperanza Health Center', '2001 S California', '', 'Chicago', 'IL', '60608', 'United States of America'],
    ['Maywood TASC Court Office', '1500 N Maybrook Drive', '', 'Maywood', 'IL', '60153', 'United States of America'],
    ['Mexican Consulate', '204 S Ashland', '', 'Chicago', 'IL', '60607', 'United States of America'],
    ['New Age Services Corporation', '1330 S Kostner Ave', '', 'Chicago', 'IL', '60623', 'United States of America'],
    ['Uptown Library', '929 W Buena Ave', '', 'Chicago', 'IL', '60613', 'United States of America'],
    ['Yorkville Library', '902 Game Farm Rd', '', 'Yorkville', 'IL', '60560', 'United States of America'],
    ['McHenry PADS', '14411 Kishwaukee Valley Rd', '', 'Woodstock', 'IL', '60098', 'United States of America'],
    ['Advocate Sherman Hospital ', '1425 N Randall Rd', '', 'Elgin', 'IL', '60123', 'United States of America'],
    ['Advocate Good Shepherd Hospital ', '450 West Highway 22', '', 'Barrington', 'IL', '60010', 'United States of America'],
    ['Advocate Good Sherpherd Immediate Care Center- Crystal Lake ', '525 Congress Pkwy #100', '', 'Crystal Lake', 'IL', '60014', 'United States of America'],
    ['Access DuPage', '511 Thornhill Drive, Suite M', '', 'Carol Stream', 'IL', '60188', 'United States of America'],
    ['DHS Family Community Resource Center', '146 W Roosevelt Rd, Suite 2', '', 'Villa Park', 'IL', '60181', 'United States of America'],
    ['Oswego Public Library', '32 Jefferson St', '', 'Oswego', 'IL', '60543', 'United States of America'],
    ['Plano Community Library', '15 W North St', '', 'Plano', 'IL', '60545', 'United States of America'],
    ['The Church of the Holy Apostles', '26238 N IL RT 59', '', 'Wauconda', 'IL', '60084', 'United States of America'],
    ['Willow Creek Care Center', '67 Algonquin Rd', '', 'South Barrington', 'IL', '60010', 'United States of America'],
    ['Waubonsee Community College', '2060 Ogden Ave.', '', 'Aurora', 'IL', '60504', 'United States of America'],
    ['Lee County Health Department', '309 S Galena Ave', '', 'Dixon', 'IL', '61021', 'United States of America'],
    ['Ogle County Health Department', '907 West Pines Road', '', 'Oregon', 'IL', '61061', 'United States of America'],
    ['Stephenson County Health Department', '10 W. Linden Street', '', 'Freeport', 'IL', '61032', 'United States of America'],
    ['PIC Rockford Office / Winnebago County Public Health Department - Enrollment Site', '555 N Court Street Suite 204', '', 'Rockford', 'IL', '61103', 'United States of America'],
    ['Workforce Connection (Unemployment Office)', '303 N Main St', '', 'Rockford', 'IL', '61101', 'United States of America'],
    ['Bureau County Health Department', '526 Bureau Valley Parkway', '', 'Princeton', 'IL', '61356', 'United States of America'],
    ['LaSalle County Health Department', '717 Etna Road', '', 'Ottawa', 'IL', '61350', 'United States of America'],
    ['PIC LaSalle Office - Enrollment Site', '654 1st St', '', 'LaSalle', 'IL', '61301', 'United States of America'],
    ['Kroger', '2321 N Wisconsin Ave', '', 'Peoria', 'IL', '61603', 'United States of America'],
    ['Princeton Public Library ', '698 E Peru St', '', 'Princeton', 'IL', '61356', 'United States of America'],
    ['Presence Covenant Medical Center', '1400 W Park St', '', 'Urbana', 'IL', '61821', 'United States of America'],
    ['Iroquois Memorial Hospital', '200 E Fairman Ave', '', 'Watseka', 'IL', '60970', 'United States of America'],
    ['Presence United Samaritans Way Medical Center', '812 North Logan Avenue', '', 'Danville', 'IL', '61832', 'United States of America'],
    ['Livingston County Housing Authority', '903 W. North St', '', 'Pontiac', 'IL', '61764', 'United States of America'],
    ['Livingston County Health Department', '310 E Torrance', '', 'Pontiac', 'IL', '61764', 'United States of America'],
    ['Life Center for Independent Living', '2201 Eastland Drive #1', '', 'Bloomington', 'IL', '61704', 'United States of America'],
    ['Adams County Health Department', '330 Vermont', '', 'Quincy', 'IL', '62301', 'United States of America'],
    ['DHS Family Community Resource Center', '45 S. Central Park Plaza', '', 'Jacksonville', 'IL', '62650', 'United States of America'],
    ['Pike County Public Health Department*', '113 E Jefferson', '', 'Pittsfield', 'IL', '62363', 'United States of America'],
    ['Scott County Public Health Department', '335 W Cherry St', '', 'Winchester', 'IL', '62694', 'United States of America'],
    ['Thomas H Boyd Memorial Hospital ', '800 School St', '', 'Carrollton', 'IL', '62016', 'United States of America'],
    ['Calhoun Health Department', '210 French St', '', 'Hardin', 'IL', '62047', 'United States of America'],
    ['Jerseyville Public Library', '105 N Liberty St', '', 'Jerseyville', 'IL', '62052', 'United States of America'],
    ['Brighton Memorial Library', '110 North Main Street', '', 'Brighton', 'IL', '62012', 'United States of America'],
    ['Bond County Health Department', '1520 South Fourth Street', '', 'Greenville', 'IL', '62246', 'United States of America'],
    ['Fayette County Hospital', '509 West Edwards, P.O. Box 340', '', 'Vandalia', 'IL', '62471', 'United States of America'],
    ['Marion County Health Department', '118 Cross Creek Blvd', '', 'Salem', 'IL', '62881', 'United States of America'],
    ['Hillsboro Public Library (Montgomery County)', '214 School St', '', 'Hillsboro', 'IL', '62049', 'United States of America'],
    ['Montgomery County Health Department', '11191 Illinois Route 185, P.O. Box 128', '', 'Hillsboro', 'IL', '62049', 'United States of America'],
    ['Edwardsville Public Library (Madison County)', '112 S Kansas St', '', 'Edwardsville', 'IL', '62025', 'United States of America'],
    ["HSHS St. Joseph's Hospital, Highland", '12866 Troxler Ave.', '', 'Highland', 'IL', '62249', 'United States of America'],
    ['SIUE Health Services', '1 Hairpin Dr.', '', 'Edwardsville', 'IL', '62025', 'United States of America'],
    ['Belleville Public Library', '101 S. Illinois St', '', 'Belleville', 'IL', '62220', 'United States of America'],
    ['Nashville Public Library ', '219 E Elm St', '', 'Nashville', 'IL', '62263', 'United States of America'],
    ['Carbondale Township Office', '217 E Main St ', '', 'Carbondale', 'IL', '62901', 'United States of America'],
    ['Monroe County Health Department', '901 Illinois Avenue', '', 'Waterloo', 'IL', '62298', 'United States of America'],
    ['Pickneyville Public Library', '312 South Walnut St', '', 'Pickneyville', 'IL', '62274', 'United States of America'],
    ['DuQuoin Public Library', '28 S Washington St', '', 'DuQuoin', 'IL', '62832', 'United States of America'],
    ['LIHEAP DuQuoin (Perry County)', '317 S Washington', '', 'DuQuoin', 'IL', '62832', 'United States of America'],
    ['Randolph Public Health Department', '2515 State Street', '', 'Chester', 'IL', '62233', 'United States of America']
]
```


### Navigator Hub Location Management URL
- To manage and edit hub locations where navigators can submit metrics reports, visit http://picbackend.herokuapp.com/managelocations


### Navigator Hub Location Data Modification API
To modify or add navigator hub locations in the database programatically, submit a POST request to: http://picbackend.herokuapp.com/edithublocation/. The POST data a JSON document using the following template:

```
{
"Location Name": String,
"Address Line 1": String,
"Address Line 2": String,
"City": String,
"State": String,
"Zipcode": String,
"Country": String,
"Database Action": String
}
```

In response, a JSON document will be displayed with the following format:
```
{
 "Status": {
            "Error Code": Integer,
            "Version": Float,
            "Errors": Array
            "Data": Dictionary Object or "Deleted",
           }
}
```

- Adding a navigator hub location database entry.
    - To add a navigator hub location database entry, the value for "Database Action" in the POST request must equal "Location Addition".
    - All other fields except "Database ID" must be filled.
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the added database entry.
    
- Modifying a navigator hub location database entry.
    - To modify a navigator hub location database entry, the value for "Database Action" in the POST request must equal "Location Modification".
    - All other fields must be filled.
    - All key value pairs in the POSTed JSON document correspond to updated fields for specified "Database ID"
    - The response JSON document will have a dictionary object as the value for the "Data" key with key value pairs for all the fields of the updated database entry.

- Deleting a navigator hub location database entry.
    - To delete a navigator hub location database entry, the value for "Database Action" in the POST request must equal "Location Deletion".
    - The only other field should be "Database ID".
    - The response JSON document will have a "Deleted" as the value for the "Data" key.
    
- If there are errors in the POSTed JSON document:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - No changes are made to the database.
    
    
### Navigator Location Data Retrieval API
- To navigator location data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v1/navlocations
    
- The response will be a JSON document with the following format:
    ```
    {
        "Data": [
            {"Name": "Presence Saint Joseph Hospital",
             "Zipcode": "60657",
             "State": "IL",
             "Address Line 1": "2900 N Lake Shore Dr.",
             "Address Line 2": "",
             "Country": "United States of America",
             "City": "Chicago"},
            ...,
            ...,
            ...,
        ],
        "Status": {
            "Version": Integer,
            "Error Code": Integer,
            "Errors": Array
        }
    }
    ```

- If navigator locations are found,
    - "Error Code" will be 0
    - Array corresponding to the "Data" key will be non empty.
- If navigator locationss are not found,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error in the POSTed JSON doc.
    - Array corresponding to the "Data" key will be empty.


### Pokitdok Trading Partner Retrieval API.
- To retrieve parsed trading partner data from pokitdok, submit a GET request to http://picbackend.herokuapp.com/v1/eligibility with the following optional parameter: "partnerid"
    - "partnerid" corresponds to the partner id provided by pokitdok for a given trading partner.
        - If this parameter is provided, results will contain valid search parameters for eligibility checks.
    
    
- The response for requests WITHOUT partnerid provided will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": Integer,
                    "Error Code": Integer,
                    "Errors": Array
                  }
        "Data": {
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837"
                    ],
                    "name": "8th District Electrical Benefit Fund",
                    "is_enabled": true,
                    "id": "8th_district_electrical"
                    },
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837",
                    "270"
                    ],
                    "name": "AARP Medicare Complete",
                    "is_enabled": true,
                    "id": "aarp_medicare_complete"
                    },
    }
    ```
    
    
- The response for requests WITH partnerid provided will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": Integer,
                    "Error Code": Integer,
                    "Errors": Array
                  }
        "Data": {
                    {
                    "enrollment_required": [],
                    "restricted_transactions": [
                    "837"
                    ],
                    "supported_transactions": [
                    "837"
                    ],
                    "name": "8th District Electrical Benefit Fund",
                    "is_enabled": true,
                    "id": "8th_district_electrical"
                    }
    }
    ```
    
    
    
### Pokitdok Eligibility Retrieval API.
- To retrieve parsed eligibility data from pokitdok for a consumer, submit a POST request to http://picbackend.herokuapp.com/v1/eligibility The POST data a JSON document using the following template:

```
{
"Birth Date":"YYYY-MM-DD" (Can be None),
"First Name": String (Can be None),
"Last Name": String (Can be None),
"Gender": String (Can be None),
"Trading Partner ID": Plan name code which can be retrieved from trading partner API (String),
"Consumer Plan ID": String (Can be None)
}
```

- The consumer parameters ("Trading Partner ID" is mandatory) need to match patterns according to the trading partner you are requesting. Use /v1/tradingpartners?partnerid="Trading Partner ID" to retrieve valid paramater set:


    
- The response will be a JSON document with the following format:
    ```
    {
        "Status": {
                    "Version": Integer,
                    "Error Code": Integer,
                    "Errors": Array
                  }
        "Data": {
                    "Plan Start Date": "YYYY-MM-DD",
                    "Consumer Info": {
                                        "id": Plan ID number (String),
                                        "birth_date": "YYYY-MM-DD",
                                        "address": {
                                                        "state": "XX",
                                                        "address_lines": [
                                                                            String,
                                                                            ...
                                                                         ],
                                                        "zipcode": String,
                                                        "city": String
                                                    },
                                        "first_name": String,
                                        "last_name": String,
                                        "gender": String,
                                        "middle_name": String
                                     },
                    "Payer Info": {
                                        "id": Plan code (String),
                                        "name": Plan name (String),
                                     },
                    "Insurance Type": eg. commercial, etc (String),
                    "Copay": [
                                {
                                    "copayment": {"amount": String, "currency": String},
                                    "service_type_codes": ["UC", "33", "48", "50", "86", "98"],
                                    "coverage_level": "individual",
                                    "service_types": ["urgent_care", "chiropractic", "hospital_inpatient", "hospital_outpatient",
                                    "emergency_services", "professional_physician_visit_office"],
                                    "in_plan_network": "not_applicable"
                                }
                             ],
                    "Consumer Group Number": String,
                    "Service Types": [
                                        "health_benefit_plan_coverage",
                                        "vision_optometry",
                                        "mental_health",
                                        "urgent_care",
                                        "medical_care",
                                        "chiropractic",
                                        "hospital",
                                        "hospital_inpatient",
                                        "hospital_outpatient",
                                        "emergency_services",
                                        "professional_physician_visit_office
                                     ],
                    "Coinsurance Benefits": [
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["33"],
                                                    "benefit_percent": 0.2,
                                                    "service_types": ["chiropractic"],
                                                    "in_plan_network": "not_applicable"
                                                },
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["50", "48", "98", "86", "UC"],
                                                    "benefit_percent": 0.2,
                                                    "service_types": ["hospital_outpatient", "hospital_inpatient", "professional_physician_visit_office", "emergency_services", "urgent_care"],
                                                    "in_plan_network": "yes"
                                                },
                                                {
                                                    "coverage_level": "individual",
                                                    "service_type_codes": ["48", "98", "86", "UC", "50"],
                                                    "benefit_percent": 0.4,
                                                    "service_types": ["hospital_inpatient", "professional_physician_visit_office", "emergency_services", "urgent_care", "hospital_outpatient"],
                                                    "in_plan_network": "no"
                                                }
                                            ],
                    "Plan Description": eg. "CHOICE PLUS" (String),
                    "Plan is Active": Boolean,
                    "Deductibles": {
                                        "Calendar Year Amounts": [
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "not_applicable",
                                                                        "coverage_level": "family",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "yes",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["chiropractic"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["33"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    }
                                                                ]
                                    },
                    "Out of Pocket": {
                                        "Calendar Year Amounts": [
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "yes",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    },
                                                                    {
                                                                        "time_period": "calendar_year",
                                                                        "service_types": ["health_benefit_plan_coverage"],
                                                                        "in_plan_network": "no",
                                                                        "coverage_level": "individual",
                                                                        "service_type_codes": ["30"],
                                                                        "benefit_amount": {"amount": String, "currency": String}
                                                                    }
                                                                ]
                                    }
                }
    }
    ```

- If consumer eligibility data is found and parsed with no errors,
    - "Error Code" will be 0
    - Dictionary corresponding to the "Data" key will have values for all the above keys in that format.
- If there was an error retrieving or parsing consumer eligibility data,
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        -Each item in the array is a string corresponding to an error retrieving or parsing consumer eligibility data.
    - Dictionary corresponding to the "Data" key may have keys ommitted or values of None.
    
    
    
## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license
