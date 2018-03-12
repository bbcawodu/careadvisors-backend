from django.db import models
import urllib

from .services.create_update_delete import add_instance_using_validated_params
from .services.create_update_delete import modify_instance_using_validated_params
from .services.create_update_delete import delete_instance_using_validated_params

from .services.read import retrieve_table_data_by_id
from .services.read import retrieve_table_data_by_full_name
from .services.read import retrieve_table_data_by_email
from .services.read import retrieve_table_data_by_company_name
from .services.read import retrieve_table_data_by_phone_number


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


CareAdvisorCustomer.add_instance_using_validated_params = classmethod(add_instance_using_validated_params)
CareAdvisorCustomer.modify_instance_using_validated_params = classmethod(modify_instance_using_validated_params)
CareAdvisorCustomer.delete_instance_using_validated_params = classmethod(delete_instance_using_validated_params)

CareAdvisorCustomer.retrieve_table_data_by_id = classmethod(retrieve_table_data_by_id)
CareAdvisorCustomer.retrieve_table_data_by_full_name = classmethod(retrieve_table_data_by_full_name)
CareAdvisorCustomer.retrieve_table_data_by_email = classmethod(retrieve_table_data_by_email)
CareAdvisorCustomer.retrieve_table_data_by_company_name = classmethod(retrieve_table_data_by_company_name)
CareAdvisorCustomer.retrieve_table_data_by_phone_number = classmethod(retrieve_table_data_by_phone_number)
