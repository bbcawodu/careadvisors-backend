import json
from picmodels.models import HealthcareCarrier
from picmodels.models import HealthcarePlan


def add_instance_using_validated_params(add_plan_params, post_errors):
    healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(add_plan_params['rqst_carrier_id'], post_errors)

    healthcare_plan = None
    if healthcare_carrier_obj and not post_errors:
        found_healthcare_plan_objs = check_for_healthcare_plan_objs_with_given_name_county_and_carrier(
            add_plan_params['rqst_plan_name'], healthcare_carrier_obj, add_plan_params['county'], post_errors)

        if not found_healthcare_plan_objs and not post_errors:
            healthcare_plan = create_and_save_new_plan_obj(add_plan_params, healthcare_carrier_obj, post_errors)

    return healthcare_plan


def return_healthcare_carrier_obj_with_given_id(carrier_id, post_errors):
    try:
        healthcare_carrier_obj = HealthcareCarrier.objects.get(id=carrier_id)
    except HealthcareCarrier.DoesNotExist:
        healthcare_carrier_obj = None
        post_errors.append("No HealthcareCarrier objects found for id: {}".format(carrier_id))

    return healthcare_carrier_obj


def check_for_healthcare_plan_objs_with_given_name_county_and_carrier(plan_name, healthcare_carrier_obj, county, post_errors, current_healthcare_plan_id=None):
    found_healthcare_plan_obj = False

    healthcare_plan_objs = HealthcarePlan.objects.filter(name__iexact=plan_name, carrier=healthcare_carrier_obj, county__iexact=county)

    if healthcare_plan_objs:
        found_healthcare_plan_obj = True
        plan_ids = healthcare_plan_objs.values_list('id', flat=True)

        if len(healthcare_plan_objs) > 1:
            post_errors.append(
                "Multiple healthcare plans with name: {}, carrier: {}, and county: {} already exist in db. (Hint - Delete one and modify the remaining) id's: {}".format(
                    plan_name, healthcare_carrier_obj.name, county, json.dumps(plan_ids)))
        else:
            if not current_healthcare_plan_id or current_healthcare_plan_id not in plan_ids:
                post_errors.append(
                    "Healthcare plan with name: {}, carrier: {}, and county: {} already exists in db. (Hint - Modify that entry) id: {}".format(
                        plan_name, healthcare_carrier_obj.name, county, plan_ids[0]))
            else:
                found_healthcare_plan_obj = False

    return found_healthcare_plan_obj


def create_and_save_new_plan_obj(plan_params, healthcare_carrier_obj, post_errors):
    healthcare_plan = populate_plan_fields_and_save(HealthcarePlan(), plan_params, healthcare_carrier_obj, post_errors)

    return healthcare_plan


def populate_plan_fields_and_save(healthcare_plan_instance, plan_params, healthcare_carrier_obj, post_errors):
    healthcare_plan_instance.name = plan_params['rqst_plan_name']
    healthcare_plan_instance.carrier = healthcare_carrier_obj
    healthcare_plan_instance.metal_level = plan_params['rqst_plan_metal_level']
    if not healthcare_plan_instance.check_metal_choices():
        post_errors.append("Metal: {!s} is not a valid metal level".format(healthcare_plan_instance.metal_level))
    healthcare_plan_instance.premium_type = plan_params['rqst_plan_premium_type']
    if not healthcare_plan_instance.check_premium_choices():
        post_errors.append(
            "Premium Type: {!s} is not a valid premium type".format(healthcare_plan_instance.premium_type))
    healthcare_plan_instance.county = plan_params['county']

    if post_errors:
        healthcare_plan_instance = None
    else:
        healthcare_plan_instance.save()

        def delete_old_healthcare_service_cost_instances(healthcare_plan_instance, healthcare_plan_field):
            old_healthcare_service_cost_qset = getattr(healthcare_plan_instance, healthcare_plan_field).all()
            for old_healthcare_service_cost_instance in old_healthcare_service_cost_qset:
                old_healthcare_service_cost_instance.delete()

        def save_and_return_healthcare_service_cost_instances(healthcare_service_cost_instances):
            for healthcare_service_cost_instance in healthcare_service_cost_instances:
                healthcare_service_cost_instance.save()

            return healthcare_service_cost_instances

        healthcare_plan_instance.medical_deductible_individual_standard = plan_params[
            "medical_deductible_individual_standard"]
        healthcare_plan_instance.medical_out_of_pocket_max_individual_standard = plan_params[
            "medical_out_of_pocket_max_individual_standard"]
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance,
                                                     "primary_care_physician_standard_cost")
        healthcare_plan_instance.primary_care_physician_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["primary_care_physician_standard_cost"])

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialist_standard_cost")
        healthcare_plan_instance.specialist_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["specialist_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "emergency_room_standard_cost")
        healthcare_plan_instance.emergency_room_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["emergency_room_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "inpatient_facility_standard_cost")
        healthcare_plan_instance.inpatient_facility_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["inpatient_facility_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "generic_drugs_standard_cost")
        healthcare_plan_instance.generic_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["generic_drugs_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["preferred_brand_drugs_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "non_preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.non_preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["non_preferred_brand_drugs_standard_cost"])
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialty_drugs_standard_cost")
        healthcare_plan_instance.specialty_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            plan_params["specialty_drugs_standard_cost"])

        healthcare_plan_instance.medical_deductible_family_standard = plan_params["medical_deductible_family_standard"]
        healthcare_plan_instance.medical_out_of_pocket_max_family_standard = plan_params[
            "medical_out_of_pocket_max_family_standard"]

        healthcare_plan_instance.save()

    return healthcare_plan_instance


def modify_instance_using_validated_params(modify_plan_params, rqst_plan_id, post_errors):
    healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(modify_plan_params['rqst_carrier_id'], post_errors)

    healthcare_plan_obj = None
    if healthcare_carrier_obj and not post_errors:
        found_healthcare_plan_objs = check_for_healthcare_plan_objs_with_given_name_county_and_carrier(
            modify_plan_params['rqst_plan_name'], healthcare_carrier_obj, modify_plan_params['county'],  post_errors, rqst_plan_id)

        if not found_healthcare_plan_objs and not post_errors:
            healthcare_plan_obj = modify_plan_obj(rqst_plan_id, modify_plan_params, healthcare_carrier_obj, post_errors)

    return healthcare_plan_obj


def modify_plan_obj(plan_id, plan_params, healthcare_carrier_obj, post_errors):
    try:
        healthcare_plan_obj = HealthcarePlan.objects.get(id=plan_id)
        healthcare_plan_obj = populate_plan_fields_and_save(healthcare_plan_obj, plan_params, healthcare_carrier_obj, post_errors)
    except HealthcarePlan.DoesNotExist:
        healthcare_plan_obj = None
        post_errors.append("Healthcare plan does not exist for database id: {}".format(plan_id))

    return healthcare_plan_obj


def delete_instance_using_validated_params(rqst_plan_id, post_errors):
    try:
        healthcare_plan_obj = HealthcarePlan.objects.get(id=rqst_plan_id)
        healthcare_plan_obj.delete()
    except HealthcarePlan.DoesNotExist:
        post_errors.append("Healthcare plan does not exist for database id: {}".format(rqst_plan_id))
