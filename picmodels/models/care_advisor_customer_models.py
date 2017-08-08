from django.db import models
import urllib


class CareAdvisorCustomer(models.Model):
    full_name = models.TextField()
    email = models.EmailField(unique=True)
    company_name = models.TextField()
    phone_number = models.TextField()

    def return_values_dict(self):
        valuesdict = {
            "full_name": self.full_name,
            "url_encoded_full_name": urllib.parse.quote(self.full_name) if self.full_name else None,
            "email": self.email,
            "company_name": self.company_name,
            "url_encoded_company_name": urllib.parse.quote(self.company_name) if self.company_name else None,
            "phone_number": self.phone_number,
            "id": self.id
        }

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
