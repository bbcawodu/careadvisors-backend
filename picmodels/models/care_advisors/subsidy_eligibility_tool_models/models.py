from django.db import models
from django.core.validators import MinValueValidator

from .services.create_update_delete import create_row_w_validated_params
from .services.create_update_delete import update_row_w_validated_params
from .services.create_update_delete import delete_row_w_validated_params
from .services.create_update_delete import check_for_rows_w_given_family_size

from .services.read import retrieve_healthcare_subsidy_eligibility_data_by_id
from .services.read import retrieve_healthcare_subsidy_eligibility_data_by_family_size


class HealthcareSubsidyEligibilityByFamSize(models.Model):
    # Unique
    family_size = models.IntegerField(validators=[MinValueValidator(0), ])

    medicaid_income_limit = models.FloatField(validators=[MinValueValidator(0.0), ])
    tax_cred_for_marketplace_income_limit = models.FloatField(validators=[MinValueValidator(0.0), ])
    marketplace_without_subsidies_income_level = models.FloatField(validators=[MinValueValidator(0.0), ])

    def return_values_dict(self):
        values_dict = {
            "family_size": self.family_size,
            "medicaid_income_limit": self.medicaid_income_limit,
            "tax_cred_for_marketplace_income_limit": self.tax_cred_for_marketplace_income_limit,
            "marketplace_without_subsidies_income_level": self.marketplace_without_subsidies_income_level,
            "Database ID": self.id
        }

        return values_dict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


HealthcareSubsidyEligibilityByFamSize.create_row_w_validated_params = classmethod(create_row_w_validated_params)
HealthcareSubsidyEligibilityByFamSize.update_row_w_validated_params = classmethod(update_row_w_validated_params)
HealthcareSubsidyEligibilityByFamSize.delete_row_w_validated_params = classmethod(delete_row_w_validated_params)

HealthcareSubsidyEligibilityByFamSize.check_for_rows_w_given_family_size = classmethod(check_for_rows_w_given_family_size)

HealthcareSubsidyEligibilityByFamSize.retrieve_healthcare_subsidy_eligibility_data_by_id = classmethod(retrieve_healthcare_subsidy_eligibility_data_by_id)
HealthcareSubsidyEligibilityByFamSize.retrieve_healthcare_subsidy_eligibility_data_by_family_size = classmethod(retrieve_healthcare_subsidy_eligibility_data_by_family_size)
