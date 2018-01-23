from django.db import models
from django.db import IntegrityError
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


def add_instance_using_validated_params(cls, validated_params, rqst_errors):
    rqst_email = validated_params['email']
    rqst_db_instance_values = {
        'full_name': validated_params['full_name'],
        'company_name': validated_params['company_name'],
        'phone_number': validated_params['phone_number'],
    }

    care_advisor_customer_instance, care_advisor_customer_instance_created = cls.objects.get_or_create(email=rqst_email,
                                                                                                       defaults=rqst_db_instance_values)
    if not care_advisor_customer_instance_created:
        rqst_errors.append('Row in care_advisor_customer table already exists for the email: {}'.format(rqst_email))
        care_advisor_customer_instance = None
    else:
        care_advisor_customer_instance.save()

    return care_advisor_customer_instance
add_instance_using_validated_params = classmethod(add_instance_using_validated_params)
CareAdvisorCustomer.add_instance_using_validated_params = add_instance_using_validated_params


def modify_instance_using_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        care_advisor_customer_instance = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row in care_advisor_customer table does not exist for the id: {}'.format(rqst_id))
        care_advisor_customer_instance = None

    if care_advisor_customer_instance:
        if 'email' in validated_params:
            rqst_email = validated_params['email']
            care_advisor_customer_instance.email = rqst_email
        else:
            rqst_email = care_advisor_customer_instance.email
        if 'full_name' in validated_params:
            care_advisor_customer_instance.full_name = validated_params['full_name']
        if 'company_name' in validated_params:
            care_advisor_customer_instance.company_name = validated_params['company_name']
        if 'phone_number' in validated_params:
            care_advisor_customer_instance.phone_number = validated_params['phone_number']

        try:
            care_advisor_customer_instance.save()
        except IntegrityError:
            rqst_errors.append('Row in care_advisor_customer table already exists for the email: {}'.format(rqst_email))
            care_advisor_customer_instance = None

    return care_advisor_customer_instance
modify_instance_using_validated_params = classmethod(modify_instance_using_validated_params)
CareAdvisorCustomer.modify_instance_using_validated_params = modify_instance_using_validated_params


def delete_instance_using_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        care_advisor_customer_instance = cls.objects.get(id=rqst_id)
        care_advisor_customer_instance.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row in care_advisor_customer table does not exist for the id: {}'.format(rqst_id))
delete_instance_using_validated_params = classmethod(delete_instance_using_validated_params)
CareAdvisorCustomer.delete_instance_using_validated_params = delete_instance_using_validated_params
