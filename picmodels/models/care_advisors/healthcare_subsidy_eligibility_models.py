from django.db import models
from django.core.validators import MinValueValidator


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