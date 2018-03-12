import json
import picmodels.models


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(validated_params['rqst_carrier_id'], rqst_errors)

    healthcare_plan = None
    if healthcare_carrier_obj and not rqst_errors:
        found_healthcare_plan_objs = cls.check_for_healthcare_plan_objs_with_given_name_county_and_carrier(
            validated_params['rqst_plan_name'],
            healthcare_carrier_obj,
            validated_params['county'],
            rqst_errors
        )

        if not found_healthcare_plan_objs and not rqst_errors:
            healthcare_plan = populate_new_plan_fields_and_save(
                cls(),
                validated_params,
                healthcare_carrier_obj,
                rqst_errors
            )

    return healthcare_plan


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        healthcare_plan_obj = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        healthcare_plan_obj = None
        rqst_errors.append("Healthcare plan does not exist for database id: {}".format(rqst_id))

    if healthcare_plan_obj and not rqst_errors:
        if 'rqst_carrier_id' in validated_params:
            healthcare_carrier_obj = return_healthcare_carrier_obj_with_given_id(
                validated_params['rqst_carrier_id'],
                rqst_errors
            )
        else:
            healthcare_carrier_obj = healthcare_plan_obj.carrier

        if healthcare_carrier_obj and not rqst_errors:
            if 'rqst_plan_name' in validated_params:
                plan_name = validated_params['rqst_plan_name']
            else:
                plan_name = healthcare_plan_obj.name

            if 'county' in validated_params:
                county = validated_params['county']
            else:
                county = healthcare_plan_obj.name

            found_healthcare_plan_objs = cls.check_for_healthcare_plan_objs_with_given_name_county_and_carrier(
                plan_name,
                healthcare_carrier_obj,
                county,
                rqst_errors,
                rqst_id
            )

            if not found_healthcare_plan_objs and not rqst_errors:
                healthcare_plan_obj = update_plan_row_fields_and_save(
                    healthcare_plan_obj,
                    validated_params,
                    healthcare_carrier_obj,
                    rqst_errors
                )

                if rqst_errors:
                    healthcare_plan_obj = None

    return healthcare_plan_obj


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    rqst_id = validated_params['rqst_id']

    try:
        healthcare_plan_obj = cls.objects.get(id=rqst_id)
        healthcare_plan_obj.delete()
    except cls.DoesNotExist:
        rqst_errors.append("Healthcare plan does not exist for database id: {}".format(rqst_id))


def return_healthcare_carrier_obj_with_given_id(carrier_id, post_errors):
    try:
        healthcare_carrier_obj = picmodels.models.HealthcareCarrier.objects.get(id=carrier_id)
    except picmodels.models.HealthcareCarrier.DoesNotExist:
        healthcare_carrier_obj = None
        post_errors.append("No HealthcareCarrier objects found for id: {}".format(carrier_id))

    return healthcare_carrier_obj


def check_for_healthcare_plan_objs_with_given_name_county_and_carrier(cls, plan_name, healthcare_carrier_obj, county, post_errors, current_healthcare_plan_id=None):
    found_healthcare_plan_obj = False

    healthcare_plan_objs = cls.objects.filter(name__iexact=plan_name, carrier=healthcare_carrier_obj, county__iexact=county)

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


def populate_new_plan_fields_and_save(healthcare_plan_instance, validated_params, healthcare_carrier_obj, rqst_errors):
    healthcare_plan_instance.carrier = healthcare_carrier_obj

    healthcare_plan_instance.name = validated_params['rqst_plan_name']

    healthcare_plan_instance.metal_level = validated_params['rqst_plan_metal_level']
    if not healthcare_plan_instance.check_metal_choices():
        rqst_errors.append("Metal: {!s} is not a valid metal level".format(healthcare_plan_instance.metal_level))

    healthcare_plan_instance.premium_type = validated_params['rqst_plan_premium_type']
    if not healthcare_plan_instance.check_premium_choices():
        rqst_errors.append(
            "Premium Type: {!s} is not a valid premium type".format(healthcare_plan_instance.premium_type))

    healthcare_plan_instance.county = validated_params['county']

    if rqst_errors:
        healthcare_plan_instance = None
    else:
        healthcare_plan_instance.save()

        healthcare_plan_instance.medical_deductible_individual_standard = validated_params["medical_deductible_individual_standard"]
        healthcare_plan_instance.medical_out_of_pocket_max_individual_standard = validated_params["medical_out_of_pocket_max_individual_standard"]

        delete_old_healthcare_service_cost_instances(
            healthcare_plan_instance,
            "primary_care_physician_standard_cost"
        )
        healthcare_plan_instance.primary_care_physician_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["primary_care_physician_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialist_standard_cost")
        healthcare_plan_instance.specialist_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["specialist_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "emergency_room_standard_cost")
        healthcare_plan_instance.emergency_room_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["emergency_room_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "inpatient_facility_standard_cost")
        healthcare_plan_instance.inpatient_facility_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["inpatient_facility_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "generic_drugs_standard_cost")
        healthcare_plan_instance.generic_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["generic_drugs_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["preferred_brand_drugs_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "non_preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.non_preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["non_preferred_brand_drugs_standard_cost"]
        )

        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialty_drugs_standard_cost")
        healthcare_plan_instance.specialty_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["specialty_drugs_standard_cost"]
        )

        healthcare_plan_instance.medical_deductible_family_standard = validated_params["medical_deductible_family_standard"]

        healthcare_plan_instance.medical_out_of_pocket_max_family_standard = validated_params["medical_out_of_pocket_max_family_standard"]

        healthcare_plan_instance.save()

    return healthcare_plan_instance


def update_plan_row_fields_and_save(healthcare_plan_instance, validated_params, healthcare_carrier_obj, rqst_errors):
    healthcare_plan_instance.carrier = healthcare_carrier_obj

    if 'rqst_plan_name' in validated_params:
        healthcare_plan_instance.name = validated_params['rqst_plan_name']

    if 'rqst_plan_metal_level' in validated_params:
        healthcare_plan_instance.metal_level = validated_params['rqst_plan_metal_level']
        if not healthcare_plan_instance.check_metal_choices():
            rqst_errors.append("Metal: {!s} is not a valid metal level".format(healthcare_plan_instance.metal_level))

    if 'rqst_plan_premium_type' in validated_params:
        healthcare_plan_instance.premium_type = validated_params['rqst_plan_premium_type']
        if not healthcare_plan_instance.check_premium_choices():
            rqst_errors.append(
                "Premium Type: {!s} is not a valid premium type".format(healthcare_plan_instance.premium_type))

    if 'county' in validated_params:
        healthcare_plan_instance.county = validated_params['county']

    if "medical_deductible_individual_standard" in validated_params:
        healthcare_plan_instance.medical_deductible_individual_standard = validated_params["medical_deductible_individual_standard"]

    if "medical_out_of_pocket_max_individual_standard" in validated_params:
        healthcare_plan_instance.medical_out_of_pocket_max_individual_standard = validated_params["medical_out_of_pocket_max_individual_standard"]

    if "primary_care_physician_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(
            healthcare_plan_instance,
            "primary_care_physician_standard_cost"
        )
        healthcare_plan_instance.primary_care_physician_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["primary_care_physician_standard_cost"]
        )

    if "specialist_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialist_standard_cost")
        healthcare_plan_instance.specialist_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["specialist_standard_cost"]
        )

    if "emergency_room_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "emergency_room_standard_cost")
        healthcare_plan_instance.emergency_room_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["emergency_room_standard_cost"]
        )

    if "inpatient_facility_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "inpatient_facility_standard_cost")
        healthcare_plan_instance.inpatient_facility_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["inpatient_facility_standard_cost"]
        )

    if "generic_drugs_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "generic_drugs_standard_cost")
        healthcare_plan_instance.generic_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["generic_drugs_standard_cost"]
        )

    if "preferred_brand_drugs_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["preferred_brand_drugs_standard_cost"])

    if "non_preferred_brand_drugs_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "non_preferred_brand_drugs_standard_cost")
        healthcare_plan_instance.non_preferred_brand_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["non_preferred_brand_drugs_standard_cost"]
        )

    if "specialty_drugs_standard_cost" in validated_params:
        delete_old_healthcare_service_cost_instances(healthcare_plan_instance, "specialty_drugs_standard_cost")
        healthcare_plan_instance.specialty_drugs_standard_cost = save_and_return_healthcare_service_cost_instances(
            validated_params["specialty_drugs_standard_cost"])

    if "medical_deductible_family_standard" in validated_params:
        healthcare_plan_instance.medical_deductible_family_standard = validated_params["medical_deductible_family_standard"]

    if "medical_out_of_pocket_max_family_standard" in validated_params:
        healthcare_plan_instance.medical_out_of_pocket_max_family_standard = validated_params["medical_out_of_pocket_max_family_standard"]

    if not rqst_errors:
        healthcare_plan_instance.save()

    return healthcare_plan_instance


def delete_old_healthcare_service_cost_instances(healthcare_plan_instance, healthcare_plan_field):
    old_healthcare_service_cost_qset = getattr(healthcare_plan_instance, healthcare_plan_field).all()
    for old_healthcare_service_cost_instance in old_healthcare_service_cost_qset:
        old_healthcare_service_cost_instance.delete()


def save_and_return_healthcare_service_cost_instances(healthcare_service_cost_instances):
    for healthcare_service_cost_instance in healthcare_service_cost_instances:
        healthcare_service_cost_instance.save()

    return healthcare_service_cost_instances
