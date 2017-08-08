from picmodels.models import CareAdvisorCustomer
from django.db import IntegrityError


def add_instance_using_validated_params(validated_params, rqst_errors):
    rqst_email = validated_params['email']
    rqst_db_instance_values = {
        'full_name': validated_params['full_name'],
        'company_name': validated_params['company_name'],
        'phone_number': validated_params['phone_number'],
    }

    care_advisor_customer_instance, care_advisor_customer_instance_created = CareAdvisorCustomer.objects.get_or_create(email=rqst_email,
                                                                                                                       defaults=rqst_db_instance_values)
    if not care_advisor_customer_instance_created:
        rqst_errors.append('Row in care_advisor_customer table already exists for the email: {}'.format(rqst_email))
        care_advisor_customer_instance = None
    else:
        care_advisor_customer_instance.save()

    return care_advisor_customer_instance


def modify_instance_using_validated_params(validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        care_advisor_customer_instance = CareAdvisorCustomer.objects.get(id=rqst_id)
    except CareAdvisorCustomer.DoesNotExist:
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


def delete_instance_using_validated_params(validated_params, rqst_errors):
    rqst_id = validated_params['id']
    try:
        care_advisor_customer_instance = CareAdvisorCustomer.objects.get(id=rqst_id)
        care_advisor_customer_instance.delete()
    except CareAdvisorCustomer.DoesNotExist:
        rqst_errors.append('Row in care_advisor_customer table does not exist for the id: {}'.format(rqst_id))
