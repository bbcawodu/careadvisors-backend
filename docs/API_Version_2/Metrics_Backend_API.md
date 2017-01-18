## Consumer Metrics Backend API

### Consumer Metrics Submission API
To submit an entry of consumer metrics data corresponding to a specific staff member, make a PUT request to: http://picbackend.herokuapp.com/v2/metrics/.

- The headers of the request should include: 
    - "Content-Type: "application/json""
    
The body of the request should be a JSON document which has the following format:

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
            "Version": 2.0,
            "Errors": Array
           }
}
```

- If there are no errors in the JSON Body doc:
    - "Error Code" will be 0.
    - There will be no "Errors" key in the "Status" dictionary.
    - An instance of the MetricsSubmission class corresponding to the JSON Body doc will be created and saved in the database.
        - Only one metrics submission is allowed per day.
    
- If there are errors in the JSON Body doc:
    - "Error Code" will be 1.
    - An array of length > 0 will be the value for the "Errors" key in the "Status" dictionary.
        - Each item in the array is a string corresponding to an error in the JSON Body doc.
    - No changes are made to the database.
    
### Consumer Metrics Retrieval API.
- To retrieve metrics data stored in the backend, submit a GET request to http://picbackend.herokuapp.com/v2/metrics/ with the following optional parameters: "fname", "lname", "email", "mpn", "id", "time", "groupby", "startdate", "enddate", "time", "zipcode", "location", "fields"
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
            "Version": 2.0,
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
        -Each item in the array is a string corresponding to an error in the JSON Body doc.
    - Array corresponding to the "Data" key will be empty.