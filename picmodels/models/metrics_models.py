"""
This file defines the data models for the picproject app
"""

from django.db import models
from picmodels.models import PICStaff, NavMetricsLocation


class MetricsSubmission(models.Model):
    # fields for MetricsSubmission model
    staff_member = models.ForeignKey(PICStaff, on_delete=models.CASCADE)
    location = models.ForeignKey(NavMetricsLocation, blank=True, null=True, on_delete=models.SET_NULL)
    submission_date = models.DateField(blank=True, null=True)
    county = models.CharField(max_length=1000, default="")
    date_created = models.DateTimeField(blank=True, auto_now_add=True, null=True)

    no_general_assis = models.IntegerField(default=0)
    no_plan_usage_assis = models.IntegerField(default=0)
    no_locating_provider_assis = models.IntegerField(default=0)
    no_billing_assis = models.IntegerField(default=0)
    no_enroll_apps_started = models.IntegerField(default=0)
    no_enroll_qhp = models.IntegerField(default=0)
    no_enroll_abe_chip = models.IntegerField(default=0)
    no_enroll_shop = models.IntegerField(default=0)
    no_referrals_agents_brokers = models.IntegerField(default=0)
    no_referrals_ship_medicare = models.IntegerField(default=0)
    no_referrals_other_assis_programs = models.IntegerField(default=0)
    no_referrals_issuers = models.IntegerField(default=0)
    no_referrals_doi = models.IntegerField(default=0)
    no_mplace_tax_form_assis = models.IntegerField(default=0)
    no_mplace_exempt_assis = models.IntegerField(default=0)
    no_qhp_abe_appeals = models.IntegerField(default=0)
    no_data_matching_mplace_issues = models.IntegerField(default=0)
    no_sep_eligible = models.IntegerField(default=0)
    no_employ_spons_cov_issues = models.IntegerField(default=0)
    no_aptc_csr_assis = models.IntegerField(default=0)
    cmplx_cases_mplace_issues = models.CharField(max_length=5000, blank=True, default="")
    no_cps_consumers = models.IntegerField(default=0)

    def return_values_dict(self):
        valuesdict = {"no_general_assis": self.no_general_assis,
                      "no_plan_usage_assis": self.no_plan_usage_assis,
                      "no_locating_provider_assis": self.no_locating_provider_assis,
                      "no_billing_assis": self.no_billing_assis,
                      "no_enroll_apps_started": self.no_enroll_apps_started,
                      "no_enroll_qhp": self.no_enroll_qhp,
                      "no_enroll_abe_chip": self.no_enroll_abe_chip,
                      "no_enroll_shop": self.no_enroll_shop,
                      "no_referrals_agents_brokers": self.no_referrals_agents_brokers,
                      "no_referrals_ship_medicare": self.no_referrals_ship_medicare,
                      "no_referrals_other_assis_programs": self.no_referrals_other_assis_programs,
                      "no_referrals_issuers": self.no_referrals_issuers,
                      "no_referrals_doi": self.no_referrals_doi,
                      "no_mplace_tax_form_assis": self.no_mplace_tax_form_assis,
                      "no_mplace_exempt_assis": self.no_mplace_exempt_assis,
                      "no_qhp_abe_appeals": self.no_qhp_abe_appeals,
                      "no_data_matching_mplace_issues": self.no_data_matching_mplace_issues,
                      "no_sep_eligible": self.no_sep_eligible,
                      "no_employ_spons_cov_issues": self.no_employ_spons_cov_issues,
                      "no_aptc_csr_assis": self.no_aptc_csr_assis,
                      "cmplx_cases_mplace_issues": self.cmplx_cases_mplace_issues,
                      "no_cps_consumers": self.no_cps_consumers,
                      "Database ID": self.id,

                      "Staff Member ID": self.staff_member_id,
                      "Date Created": self.date_created.isoformat(),
                      "Submission Date": self.submission_date.isoformat(),
                      "County": self.county,
                      "Location": None,
                      "Plan Stats": [],
                      }

        plan_stats = self.planstat_set.all()
        if len(plan_stats):
            plan_stats_list = []
            for plan_stat in plan_stats:
                plan_stats_list.append(plan_stat.return_values_dict())
            valuesdict["Plan Stats"] = plan_stats_list

        if self.location:
            valuesdict["Location"] = self.location.return_values_dict()

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


class PlanStat(models.Model):
    #Why is using variables in addition to touplesis better? Error prevention and logic separation.
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

    PLAN_CHOICES = (
                    (MISCELLANEOUS, "Miscellaneous"),
                    (HEALTH_ALLIANCE_MEDICAL_PLANS, 'Health Alliance Medical Plans, Inc.'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_ILLINOIS, 'Blue Cross Blue Shield of Illinois'),
                    (HUMANA_HEALTH_PLAN, 'Humana Health Plan, Inc.'),
                    (CELTIC_INSURANCE_COMPANY, "Celtic Insurance Company"),
                    (CIGNA_HEALTHCARE_OF_ILLINOIS, 'Cigna HealthCare of Illinois, Inc.'),
                    (PREMERA_BLUE_CROSS_BLUE_SHIELD_OF_ALASKA, 'Premera Blue Cross Blue Shield of Alaska'),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_ALABAMA, 'Blue Cross and Blue Shield of Alabama'),
                    (QUALCHOICE_LIFE_AND_HEALTH_INSURANCE_COMPANY, "QualChoice Life & Health Insurance Company, Inc."),
                    (USABLE_MUTUAL_INSURANCE_COMPANY, "USAble Mutual Insurance Company"),
                    (QCA_HEALTH_PLAN, "QCA Health Plan, Inc."),
                    (FLORIDA_HEALTH_CARE_PLAN, "Florida Health Care Plan, Inc."),
                    (MEDICA_INSURANCE_COMPANY, "Medica Insurance Company"),
                    (CARESOURCE_INDIANA, "CareSource Indiana, Inc."),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_ARIZONA, "Blue Cross and Blue Shield of Arizona, Inc."),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_FLORIDA, "Blue Cross and Blue Shield of Florida"),
                    (HEALTH_OPTIONS, "Health Options, Inc."),
                    (AETNA_LIFE_INSURANCE_COMPANY, "Aetna Life Insurance Company"),
                    (AETNA_HEALTH_INC_A_PA_CORP, "Aetna Health Inc. (a PA corp.)"),
                    (HIGHMARK_BCBSD, "Highmark BCBSD Inc."),
                    (HEALTH_NET_OF_ARIZONA, "Health Net of Arizona, Inc."),
                    (HEALTH_FIRST_COMMERCIAL_PLANS, 'Health First Commercial Plans, Inc.'),
                    (HUMANA_MEDICAL_PLAN, 'Humana Medical Plan, Inc.'),
                    (MOLINA_HEALTHCARE_OF_FLORIDA, "Molina Healthcare of Florida, Inc"),
                    (ALLIANT_HEALTH_PLANS, 'Alliant Health Plans'),
                    (BLUE_CROSS_BLUE_SHIELD_HEALTHCARE_PLAN_OF_GEORGIA, 'Blue Cross Blue Shield Healthcare Plan of Georgia, Inc.'),
                    (KAISER_FOUNDATION_HEALTH_PLAN_OF_GEORGIA, 'Kaiser Foundation Health Plan of Georgia'),
                    (AMBETTER_OF_PEACH_STATE, 'Ambetter of Peach State Inc.'),
                    (HUMANA_EMPLOYERS_HEALTH_PLAN_OF_GEORGIA, 'Humana Employers Health Plan of Georgia, Inc.'),
                    (WELLMARK_VALUE_HEALTH_PLAN, 'Wellmark Value Health Plan, Inc.'),
                    (CARESOURCE_KENTUCKY_CO, 'CareSource Kentucky Co.'),
                    (GUNDERSEN_HEALTH_PLAN, 'Gundersen Health Plan, Inc.'),
                    (WELLMARK_SYNERGY_HEALTH, 'Wellmark Synergy Health, Inc.'),
                    (ANTHEM_INS_COMPANIES_INC_ANTHEM_BCBS, 'Anthem Ins Companies Inc(Anthem BCBS)'),
                    (MDWISE_MARKETPLACE, 'MDwise Marketplace, Inc.'),
                    (HAWAII_MEDICAL_SERVICE_ASSOCIATION, 'Hawaii Medical Service Association'),
                    (KAISER_FOUNDATION_HEALTH_PLAN, 'Kaiser Foundation Health Plan, Inc.'),
                    (AETNA_HEALTH_OF_IOWA, 'Aetna Health of Iowa Inc.'),
                    (BLUECROSS_BLUESHIELD_KANSAS_SOLUTIONS, 'BlueCross BlueShield Kansas Solutions, Inc.'),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_KANSAS_CITY, 'Blue Cross and Blue Shield of Kansas City'),
                    (ANTHEM_HEALTH_PLANS_OF_KY_ANTHEM_BCBS, 'Anthem Health Plans of KY(Anthem BCBS)'),
                    (HUMANA_HEALTH_BENEFIT_PLAN_OF_LOUISIANA, 'Humana Health Benefit Plan of Louisiana, Inc.'),
                    (HMO_LOUISIANA, 'HMO Louisiana, Inc.'),
                    (VANTAGE_HEALTH_PLAN, 'Vantage Health Plan, Inc.'),
                    (LOUISIANA_HEALTH_SERVICE_AND_INDEMNITY_COMPANY, 'Louisiana Health Service & Indemnity Company'),
                    (MAINE_COMMUNITY_HEALTH_OPTIONS, 'Maine Community Health Options'),
                    (ANTHEM_HEALTH_PLANS_OF_ME_ANTHEM_BCBS, 'Anthem Health Plans of ME(Anthem BCBS)'),
                    (HARVARD_PILGRIM_HEALTH_CARE, 'Harvard Pilgrim Health Care Inc.'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_MICHIGAN_MUTUAL_INSURANCE_COMPANY, 'Blue Cross Blue Shield of Michigan Mutual Insurance Company'),
                    (MCLAREN_HEALTH_PLAN_COMMUNITY, 'McLaren Health Plan Community'),
                    (PRIORITY_HEALTH, 'Priority Health'),
                    (BLUE_CARE_NETWORK_OF_MICHIGAN, 'Blue Care Network of Michigan'),
                    (HEALTH_ALLIANCE_PLAN_HAP, 'Health Alliance Plan (HAP)'),
                    (MERIDIAN_HEALTH_PLAN_OF_MICHIGAN, 'Meridian Health Plan of Michigan, Inc.'),
                    (HUMANA_MEDICAL_PLAN_OF_MICHIGAN, 'Humana Medical Plan of Michigan, Inc.'),
                    (MOLINA_HEALTHCARE_OF_MICHIGAN, 'Molina Healthcare of Michigan, Inc.'),
                    (HUMANA_NSURANCE_COMPANY, 'Humana Insurance Company'),
                    (PHYSICIANS_HEALTH_PLAN, 'Physicians Health Plan'),
                    (HEALTHY_ALLIANCE_LIFE_CO_ANTHEM_BCBS, 'Healthy Alliance Life Co(Anthem BCBS)'),
                    (MEDICA_HEALTH_PLANS, 'Medica Health Plans'),
                    (CARESOURCE, 'CareSource'),
                    (MONTANA_HEALTH_COOPERATIVE, 'Montana Health Cooperative'),
                    (CIGNA_HEALTH_AND_LIFE_INSURANCE_COMPANY, 'Cigna Health and Life Insurance Company'),
                    (AMERIHEALTH_HMO, 'AmeriHealth HMO, Inc.'),
                    (TOTAL_HEALTH_CARE_USA, 'Total Health Care USA, Inc.'),
                    (NEW_MEXICO_HEALTH_CONNECTIONS, 'New Mexico Health Connections'),
                    (AMBETTER_OF_MAGNOLIA, 'Ambetter of Magnolia Inc.'),
                    (AULTCARE_INSURANCE_COMPANY, 'AultCare Insurance Company'),
                    (PACIFICSOURCE_HEALTH_PLANS, 'PacificSource Health Plans'),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_MONTANA, 'Blue Cross and Blue Shield of Montana'),
                    (HORIZON_HEALTHCARE_SERVICES, 'Horizon Healthcare Services, Inc.'),
                    (AMERIHEALTH_INS_COMPANY_OF_NEW_JERSEY, 'AmeriHealth Ins Company of New Jersey'),
                    (MEDICAL_HEALTH_INSURING_CORP_OF_OHIO, 'Medical Health Insuring Corp. of Ohio'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_NORTH_DAKOTA, 'Blue Cross Blue Shield of North Dakota'),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_NC, 'Blue Cross and Blue Shield of NC'),
                    (CIGNA_HEALTHCARE_OF_NORTH_CAROLINA, 'Cigna HealthCare of North Carolina, Inc.'),
                    (SANFORD_HEALTH_PLAN,'Sanford Health Plan'),
                    (GEISINGER_HEALTH_PLAN, 'Geisinger Health Plan'),
                    (HARVARD_PILGRIM_HEALTH_CARE_OF_NE, 'Harvard Pilgrim Health Care of NE'),
                    (MINUTEMAN_HEALTH, 'Minuteman Health, Inc'),
                    (MATTHEW_THORNTON_HLTH_PLAN_ANTHEM_BCBS, 'Matthew Thornton Hlth Plan(Anthem BCBS)'),
                    (COMMUNITY_INSURANCE_COMPANY_ANTHEM_BCBS, 'Community Insurance Company(Anthem BCBS)'),
                    (MOLINA_HEALTHCARE_OF_NEW_MEXICO, 'Molina Healthcare of New Mexico, Inc.'),
                    (CHRISTUS_HEALTH_PLAN, 'CHRISTUS Health Plan'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_NEW_MEXICO, 'Blue Cross Blue Shield of New Mexico'),
                    (PROMINENCE_HEALTHFIRST, 'Prominence HealthFirst'),
                    (ROCKY_MOUNTAIN_HOSPITAL_AND_MEDICAL_SERVICE_INC_DBA_ANTHEM_BLUE_CROSS_AND_BLUE_SHIELD, 'Rocky Mountain Hospital and Medical Service, Inc., dba Anthem Blue Cross and Blue Shield'),
                    (HMO_COLORADO_INC_DBA_HMO_NEVADA, 'HMO Colorado, Inc., dba HMO Nevada'),
                    (HEALTH_PLAN_OF_NEVADA, 'Health Plan of Nevada, Inc.'),
                    (MOLINA_HEALTHCARE_OF_OHIO,'Molina Healthcare of Ohio, Inc.'),
                    (BUCKEYE_COMMUNITY_HEALTH_PLAN, 'Buckeye Community Health Plan'),
                    (PREMIER_HEALTH_PLAN, 'Premier Health Plan, Inc.'),
                    (HUMANA_HEALTH_PLAN_OF_OHIO, 'Humana Health Plan of Ohio, Inc.'),
                    (PARAMOUNT_INSURANCE_COMPANY, 'Paramount Insurance Company'),
                    (CONSUMERS_LIFE_INSURANCE_COMPANY, 'Consumers Life Insurance Company'),
                    (SUMMA_INSURANCE_COMPANY, 'Summa Insurance Company, Inc.'),
                    (MODA_HEALTH_PLAN, 'Moda Health Plan, Inc.'),
                    (BRIDGESPAN_HEALTH_COMPANY, 'BridgeSpan Health Company'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_OKLAHOMA, 'Blue Cross Blue Shield of Oklahoma'),
                    (KAISER_FOUNDATION_HEALTHPLAN_OF_THE_NW, 'Kaiser Foundation Healthplan of the NW'),
                    (ATRIO_HEALTH_PLANS, 'ATRIO Health Plans'),
                    (FIRST_PRIORITY_HEALTH, 'First Priority Health'),
                    (INDEPENDENCE_BLUE_CROSS_QCC_INS_CO , 'Independence Blue Cross (QCC Ins. Co.)'),
                    (KEYSTONE_HEALTH_PLAN_EAST, 'Keystone Health Plan East, Inc'),
                    (HIGHMARK_INC, 'Highmark Inc.'),
                    (HIGHMARK_HEALTH_INSURANCE_COMPANY, 'Highmark Health Insurance Company'),
                    (UPMC_HEALTH_OPTIONS, 'UPMC Health Options, Inc.'),
                    (BLUE_CROSS_AND_BLUE_SHIELD_OF_SOUTH_CAROLINA, 'Blue Cross and Blue Shield of South Carolina'),
                    (PROVIDENCE_HEALTH_PLAN, 'Providence Health Plan'),
                    (CAPITAL_ADVANTAGE_ASSURANCE_COMPANY, 'Capital Advantage Assurance Company'),
                    (AVERA_HEALTH_PLANS, 'Avera Health Plans, Inc.'),
                    (UNITY_HEALTH_PLANS_INSURANCE_CORPORATION, 'Unity Health Plans Insurance Corporation'),
                    (MERCYCARE_HMO, 'MercyCare HMO, Inc.'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_TENNESSEE, 'Blue Cross Blue Shield of Tennessee'),
                    (MEDICA_HEALTH_PLANS_OF_WISCONSIN, 'Medica Health Plans of Wisconsin'),
                    (OPTIMA_HEALTH_PLAN, 'Optima Health Plan'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_TEXAS, 'Blue Cross Blue Shield of Texas'),
                    (HUMANA_HEALTH_PLAN_OF_TEXAS, 'Humana Health Plan of Texas, Inc.'),
                    (SHA_LLC_DBA_FIRSTCARE_HEALTH_PLANS, 'SHA, LLC DBA FirstCare Health Plans'),
                    (GROUP_HOSPITALIZATION_AND_MEDICAL_SERVICES, 'Group Hospitalization and Medical Services Inc.'),
                    (KAISER_FOUNDATION_HEALTH_PLAN_OF_THE_MID_ATLANTIC_STATES, 'Kaiser Foundation Health Plan of the Mid-Atlantic States, Inc.'),
                    (HEALTHKEEPERS_INC, 'HealthKeepers, Inc.'),
                    (SENDERO_HEALTH_PLANS, 'Sendero Health Plans, inc.'),
                    (OSCAR_INSURANCE_COMPANY_OF_TEXAS, 'Oscar Insurance Company of Texas'),
                    (COMMUNITY_HEALTH_CHOICE, 'Community Health Choice, Inc.'),
                    (PIEDMONT_COMMUNITY_HEALTHCARE, 'Piedmont Community HealthCare, Inc.'),
                    (PROMINENCE_HEALTHFIRST_OF_TEXAS, 'Prominence HealthFirst of Texas, Inc.'),
                    (INNOVATION_HEALTH_INSURANCE_COMPANY, 'Innovation Health Insurance Company'),
                    (UNITEDHEALTHCARE_OF_THE_MID_ATLANTIC, 'UnitedHealthcare of the Mid-Atlantic Inc'),
                    (MOLINA_HEALTHCARE_OF_TEXAS, 'Molina Healthcare of Texas, Inc.'),
                    (PIEDMONT_COMMUNITY_HEALTHCARE_HMO, 'Piedmont Community HealthCare HMO, Inc.'),
                    (CAREFIRST_BLUECHOICE, 'CareFirst BlueChoice, Inc.'),
                    (SELECTHEALTH, 'SelectHealth'),
                    (MOLINA_HEALTHCARE_OF_UTAH, 'Molina Healthcare of Utah'),
                    (UNIVERSITY_OF_UTAH_HEALTH_INSURANCE_PLANS, 'University of Utah Health Insurance Plans'),
                    (GROUP_HEALTH_COOPERATIVE_OF_SOUTH_CENTRAL_WISCONSIN, 'Group Health Cooperative of South Central Wisconsin'),
                    (HEALTH_TRADITION_HEALTH_PLAN, 'Health Tradition Health Plan'),
                    (CHILDRENS_COMMUNITY_HEALTH_PLAN, "Children's Community Health Plan"),
                    (CARESOURCE_WEST_VIRGINIA_CO, 'CareSource West Virginia Co.'),
                    (SECURITY_HEALTH_PLAN_OF_WISCONSIN, 'Security Health Plan of Wisconsin, Inc.'),
                    (DEAN_HEALTH_PLAN, 'Dean Health Plan'),
                    (ASPIRUS_ARISE_HEALTH_PLAN_OF_WISCONSIN, 'Aspirus Arise Health Plan of Wisconsin, Inc.'),
                    (MOLINA_HEALTHCARE_OF_WISCONSIN, 'Molina Healthcare of Wisconsin, Inc.'),
                    (COMPCARE_HEALTH_SERV_INS_CO_ANTHEM_BCBS, 'Compcare Health Serv Ins Co(Anthem BCBS)'),
                    (COMMON_GROUND_HEALTHCARE_COOPERATIVE, 'Common Ground Healthcare Cooperative'),
                    (HEALTHPARTNERS_INSURANCE_COMPANY, 'HealthPartners Insurance Company'),
                    (NETWORK_HEALTH_PLAN, 'Network Health Plan'),
                    (HIGHMARK_BLUE_CROSS_BLUE_SHIELD_WEST_VIRGINIA, 'Highmark Blue Cross Blue Shield West Virginia'),
                    (BLUE_CROSS_BLUE_SHIELD_OF_WYOMING, 'Blue Cross Blue Shield of Wyoming'),)

    HMO = "HMO"
    PPO = "PPO"
    POS = 'POS'
    EPO = 'EPO'
    N_A = "Not Available"
    PREMIUM_CHOICES = ((HMO, "HMO"),
                       (PPO, "PPO"),
                       (POS, 'POS'),
                       (EPO, 'EPO'),
                       (N_A, "Not Available"))

    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = 'Platinum'
    CATASTROPHIC = "Catastrophic"
    METAL_CHOICES = ((BRONZE, "Bronze"),
                     (SILVER, "Silver"),
                     (GOLD, "Gold"),
                     (PLATINUM, 'Platinum'),
                     (CATASTROPHIC, "Catastrophic"),
                     (N_A, "Not Available"))

    metrics_submission = models.ForeignKey(MetricsSubmission, on_delete=models.CASCADE, blank=True, null=True)
    plan_name = models.CharField(max_length=1000,
                                 choices=PLAN_CHOICES,
                                 default=MISCELLANEOUS)
    premium_type = models.CharField(max_length=1000, blank=True, null=True, choices=PREMIUM_CHOICES, default=N_A)
    metal_level = models.CharField(max_length=1000, blank=True, null=True, choices=METAL_CHOICES, default=N_A)
    enrollments = models.IntegerField()

    def check_plan_choices(self,):
        for plan_tuple in self.PLAN_CHOICES:
            if plan_tuple[1].lower() == self.plan_name.lower():
                return True
        return False

    def check_premium_choices(self,):
        for premium_tuple in self.PREMIUM_CHOICES:
            if premium_tuple[1].lower() == self.premium_type.lower():
                return True
        return False

    def check_metal_choices(self,):
        for metal_tuple in self.METAL_CHOICES:
            if metal_tuple[1].lower() == self.metal_level.lower():
                return True
        return False

    def return_values_dict(self):
        valuesdict = {"Enrollments": self.enrollments,
                      "Metal Level": self.metal_level,
                      "Premium Type": self.premium_type,
                      "Issuer Name": self.plan_name}

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
