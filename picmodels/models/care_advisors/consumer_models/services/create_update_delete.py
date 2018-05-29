import json
import picmodels
from django.db import IntegrityError


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    consumer_instance = None
    backup_consumer_obj = None
    matching_consumer_instances = None

    force_create_consumer = None
    if 'force_create_consumer' in validated_params:
        force_create_consumer = validated_params['force_create_consumer']

    found_consumers = cls.objects.filter(
        first_name__iexact=validated_params['first_name'],
        last_name__iexact=validated_params['last_name']
    )

    if found_consumers and not force_create_consumer:
        query_params = {
            "first_name": validated_params['first_name'],
            "last_name": validated_params['last_name']
        }
        rqst_errors.append('Consumer database entry(s) already exists for the parameters: {!s}'.format(
            json.dumps(query_params)))
        matching_consumer_instances = found_consumers.all()
    else:
        address_instance = None
        if validated_params['address_line_1'] != '' and validated_params['city'] != '' and \
                        validated_params['state_province'] != '' and validated_params['zipcode'] != '':
            address_instance, address_instance_created = picmodels.models.Address.objects.get_or_create(
                address_line_1=validated_params['address_line_1'],
                address_line_2=validated_params['address_line_2'],
                city=validated_params['city'],
                state_province=validated_params['state_province'],
                zipcode=validated_params['zipcode'],
                country=picmodels.models.Country.objects.all()[0]
            )

        consumer_instance = cls(
            first_name=validated_params['first_name'],
            middle_name=validated_params['middle_name'],
            last_name=validated_params['last_name'],
            email=validated_params['email'],
            phone=validated_params['phone'],
            plan=validated_params['plan'],
            preferred_language=validated_params['preferred_language'],
            best_contact_time=validated_params['best_contact_time'],
            address=address_instance,
            date_met_nav=validated_params['date_met_nav'],
            met_nav_at=validated_params['met_nav_at'],
            household_size=validated_params['household_size'],
        )
        if 'gender' in validated_params:
            consumer_instance.gender = validated_params['gender']
            if not consumer_instance.check_gender_choices():
                rqst_errors.append(
                    "gender: {!s} is not a valid choice".format(consumer_instance.gender)
                )

        if "navigator_row" in validated_params:
            consumer_instance.navigator = validated_params['navigator_row']
        if "cm_client_row_for_routing" in validated_params:
            consumer_instance.cm_client_for_routing = validated_params['cm_client_row_for_routing']

        consumer_instance.save()

        for consumer_note in validated_params['consumer_notes']:
            consumer_note_object = picmodels.models.ConsumerNote(
                consumer=consumer_instance,
                navigator_notes=consumer_note
            )
            consumer_note_object.save()

        if "validated_create_c_m_params" in validated_params:
            validated_create_c_m_params = validated_params['validated_create_c_m_params']

            picmodels.models.CaseManagementStatus.create_c_m_rows_w_validated_params(
                consumer_instance,
                validated_create_c_m_params,
                rqst_errors
            )

        if 'add_referring_cm_clients' in validated_params:
            referring_cm_clients_ids = validated_params['add_referring_cm_clients']
            referring_cm_clients_rows = []
            for referring_cm_client_id in referring_cm_clients_ids:
                referring_cm_clients_rows.append(
                    get_case_management_client_row_with_given_id(referring_cm_client_id, rqst_errors)
                )
            if not rqst_errors:
                check_referring_cm_clients_for_given_rows(
                    consumer_instance.referring_cm_clients.all(),
                    referring_cm_clients_rows,
                    consumer_instance,
                    rqst_errors
                )
                if not rqst_errors:
                    for case_management_client_row in referring_cm_clients_rows:
                        consumer_instance.referring_cm_clients.add(case_management_client_row)

        update_indiv_seeking_nav_columns_for_row(consumer_instance, validated_params, rqst_errors)
        if rqst_errors:
            consumer_instance.delete()
            consumer_instance = None

        if validated_params['validated_cps_info_dict'] and consumer_instance:
            add_cps_info_to_consumer_instance(consumer_instance, validated_params['validated_cps_info_dict'], rqst_errors)

        if validated_params['validated_hospital_info_dict'] and consumer_instance:
            add_hospital_info_to_consumer_instance(consumer_instance, validated_params['validated_hospital_info_dict'], rqst_errors)

        if not rqst_errors and validated_params['create_backup'] and consumer_instance:
            backup_consumer_obj = create_backup_consumer_obj(consumer_instance)

    return matching_consumer_instances, consumer_instance, backup_consumer_obj


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    consumer_instance = None
    backup_consumer_obj = None

    def modify_consumers_address():
        address_instance = consumer_instance.address
        if address_instance:
            if 'address_line_1' in validated_params:
                address_instance.address_line_1 = validated_params['address_line_1']
            if 'address_line_2' in validated_params:
                address_instance.address_line_2 = validated_params['address_line_2']
            if 'city' in validated_params:
                address_instance.city = validated_params['city']
            if 'state_province' in validated_params:
                address_instance.state_province = validated_params['state_province']
            if 'zipcode' in validated_params:
                address_instance.zipcode = validated_params['zipcode']
        else:
            there_are_any_address_fields_in_validated_params = 'address_line_1' in validated_params or \
                                                               'city' in validated_params or \
                                                               'state_province' in validated_params or \
                                                               'zipcode' in validated_params or \
                                                               'address_line_2' in validated_params
            if there_are_any_address_fields_in_validated_params:
                there_are_enough_fields_to_create_address_instance = 'address_line_1' in validated_params and \
                                                                     'city' in validated_params and \
                                                                     'state_province' in validated_params and \
                                                                     'zipcode' in validated_params
                if there_are_enough_fields_to_create_address_instance:
                    if 'address_line_2' not in validated_params:
                        validated_params['address_line_2'] = ''
                    required_address_fields_are_not_empty_strings = validated_params['address_line_1'] != '' and \
                                                                    validated_params['city'] != '' and \
                                                                    validated_params['state_province'] != '' and \
                                                                    validated_params['zipcode'] != ''

                    if required_address_fields_are_not_empty_strings:
                        address_instance, address_instance_created = picmodels.models.Address.objects.get_or_create(
                            address_line_1=validated_params['address_line_1'],
                            address_line_2=validated_params['address_line_2'],
                            city=validated_params['city'],
                            state_province=validated_params['state_province'],
                            zipcode=validated_params['zipcode'],
                            country=picmodels.models.Country.objects.all()[0])

                        consumer_instance.address = address_instance
                # else:
                #     rqst_errors.append("There are not enough fields to create an address instance.")

    try:
        consumer_instance = cls.objects.get(id=validated_params['id'])
    except cls.DoesNotExist:
        rqst_errors.append('Consumer database entry does not exist for the id: {!s}'.format(
            str(validated_params['id'])))
    except cls.MultipleObjectsReturned:
        rqst_errors.append(
            'Multiple database entries exist for the id: {!s}'.format(str(validated_params['id'])))
    except IntegrityError:
        rqst_errors.append(
            'Database entry already exists for the id: {!s}'.format(str(validated_params['id'])))
    else:
        modify_consumers_address()

        if 'add_referring_cm_clients' in validated_params:
            referring_cm_clients_ids = validated_params['add_referring_cm_clients']
            referring_cm_clients_rows = []
            for referring_cm_client_id in referring_cm_clients_ids:
                referring_cm_clients_rows.append(
                    get_case_management_client_row_with_given_id(referring_cm_client_id, rqst_errors)
                )
            if not rqst_errors:
                check_referring_cm_clients_for_given_rows(
                    consumer_instance.referring_cm_clients.all(),
                    referring_cm_clients_rows,
                    consumer_instance,
                    rqst_errors
                )
                if not rqst_errors:
                    for case_management_client_row in referring_cm_clients_rows:
                        consumer_instance.referring_cm_clients.add(case_management_client_row)
        elif 'remove_referring_cm_clients' in validated_params:
            referring_cm_clients_ids = validated_params['remove_referring_cm_clients']
            referring_cm_clients_rows = []
            for referring_cm_client_id in referring_cm_clients_ids:
                referring_cm_clients_rows.append(
                    get_case_management_client_row_with_given_id(referring_cm_client_id, rqst_errors)
                )
            if not rqst_errors:
                check_referring_cm_clients_for_not_given_rows(
                    consumer_instance.referring_cm_clients.all(),
                    referring_cm_clients_rows,
                    consumer_instance,
                    rqst_errors
                )
                if not rqst_errors:
                    for case_management_client_row in referring_cm_clients_rows:
                        consumer_instance.referring_cm_clients.remove(case_management_client_row)

        if not rqst_errors:
            if "first_name" in validated_params:
                consumer_instance.first_name = validated_params['first_name']
            if "middle_name" in validated_params:
                consumer_instance.middle_name = validated_params['middle_name']
            if "last_name" in validated_params:
                consumer_instance.last_name = validated_params['last_name']
            if 'gender' in validated_params:
                consumer_instance.gender = validated_params['gender']
                if not consumer_instance.check_gender_choices():
                    rqst_errors.append(
                        "gender: {!s} is not a valid choice".format(consumer_instance.gender)
                    )
            if "phone" in validated_params:
                consumer_instance.phone = validated_params['phone']
            if "plan" in validated_params:
                consumer_instance.plan = validated_params['plan']
            if "met_nav_at" in validated_params:
                consumer_instance.met_nav_at = validated_params['met_nav_at']
            if "household_size" in validated_params:
                consumer_instance.household_size = validated_params['household_size']
            if "preferred_lang" in validated_params:
                consumer_instance.preferred_language = validated_params['preferred_lang']
            if "best_contact_time" in validated_params:
                consumer_instance.best_contact_time = validated_params['best_contact_time']
            if "email" in validated_params:
                consumer_instance.email = validated_params['email']
            if "date_met_nav" in validated_params:
                consumer_instance.date_met_nav = validated_params['date_met_nav']
            if "cps_info_dict" in validated_params:
                if validated_params['cps_info_dict']:
                    modify_consumer_cps_info(consumer_instance, validated_params['validated_cps_info_dict'], rqst_errors)
                else:
                    if consumer_instance.cps_info:
                        consumer_instance.cps_info.delete()

            if "navigator_row" in validated_params:
                consumer_instance.navigator = validated_params['navigator_row']
            navigator_row = consumer_instance.navigator
            if "cm_client_row_for_routing" in validated_params:
                consumer_instance.cm_client_for_routing = validated_params['cm_client_row_for_routing']
            cm_client_row_for_routing = consumer_instance.cm_client_for_routing
            if not ((navigator_row != None) ^ (cm_client_row_for_routing != None)):
                rqst_errors.append(
                    "Valid navigator logical exclusive or case_management_client_for_roouting must be given for consumer assignment.")

        if not rqst_errors:
            update_indiv_seeking_nav_columns_for_row(consumer_instance, validated_params, rqst_errors)
            address_instance = consumer_instance.address
            if address_instance:
                address_instance.save()

            consumer_instance.save()

            if 'consumer_notes' in validated_params:
                old_consumer_notes = picmodels.models.ConsumerNote.objects.filter(consumer=consumer_instance.id)
                for old_consumer_note in old_consumer_notes:
                    old_consumer_note.delete()

                for consumer_note in validated_params['consumer_notes']:
                    consumer_note_object = picmodels.models.ConsumerNote(consumer=consumer_instance, navigator_notes=consumer_note)
                    consumer_note_object.save()

            if "validated_create_c_m_params" in validated_params:
                validated_create_c_m_params = validated_params['validated_create_c_m_params']

                picmodels.models.CaseManagementStatus.create_c_m_rows_w_validated_params(
                    consumer_instance,
                    validated_create_c_m_params,
                    rqst_errors
                )
            if "validated_update_c_m_params" in validated_params:
                validated_update_c_m_params = validated_params['validated_update_c_m_params']

                picmodels.models.CaseManagementStatus.update_c_m_rows_w_validated_params(
                    consumer_instance,
                    validated_update_c_m_params,
                    rqst_errors
                )
            if "validated_delete_c_m_params" in validated_params:
                validated_delete_c_m_params = validated_params['validated_delete_c_m_params']

                picmodels.models.CaseManagementStatus.delete_c_m_rows_w_validated_params(
                    validated_delete_c_m_params,
                    rqst_errors
                )

            if 'create_backup' in validated_params:
                if validated_params['create_backup']:
                    backup_consumer_obj = create_backup_consumer_obj(consumer_instance)

    return consumer_instance, backup_consumer_obj


def delete_row_w_validated_params(cls, validated_params, post_errors):
    backup_consumer_obj = None
    rqst_id = validated_params['id']
    if 'create_backup' in validated_params:
        rqst_create_backup = validated_params['create_backup']
    else:
        rqst_create_backup = False

    try:
        consumer_instance = cls.objects.get(id=rqst_id)

        if rqst_create_backup:
            backup_consumer_obj = create_backup_consumer_obj(consumer_instance)

        consumer_instance.delete()
    except cls.DoesNotExist:
        post_errors.append('Consumer database entry does not exist for the id: {}'.format(rqst_id))

    return backup_consumer_obj


def create_c_m_rows_w_validated_params(cls, consumer_instance, validated_create_c_m_params, rqst_errors):
    if validated_create_c_m_params:
        for c_m_param_index, c_m_params in enumerate(validated_create_c_m_params):
            try:
                c_m_status_row = cls(
                    management_step=c_m_params['rqst_management_step'],
                    management_notes=c_m_params['rqst_management_notes'],
                )

                c_m_status_row.contact = consumer_instance
                c_m_status_row.save()
            except IntegrityError:
                rqst_errors.append(
                    "Error at create_case_management_rows[{!s}] creating case management step row for params: {!s}".format(
                        c_m_param_index, json.dumps(c_m_params)))


def update_c_m_rows_w_validated_params(cls, consumer_instance, validated_update_c_m_params, rqst_errors):
    if validated_update_c_m_params:
        for c_m_param_index, c_m_params in enumerate(validated_update_c_m_params):
            rqst_management_status_id = c_m_params['rqst_management_status_id']

            try:
                c_m_status_row = cls.objects.get(id=rqst_management_status_id)

                c_m_status_row.management_step = c_m_params['rqst_management_step']
                c_m_status_row.management_notes = c_m_params['rqst_management_notes']

                c_m_status_row.contact = consumer_instance
                c_m_status_row.save()
            except cls.DoesNotExist:
                rqst_errors.append('Case Management Status Row does not exist for the id: {!s}'.format(
                    str(rqst_management_status_id)))
            except cls.MultipleObjectsReturned:
                rqst_errors.append(
                    'Multiple Case Management Status Rows exist for the id: {!s}'.format(
                        str(rqst_management_status_id)))
            except IntegrityError:
                rqst_errors.append(
                    "Error at create_case_management_rows[{!s}] creating case management step row for params: {!s}".format(
                        c_m_param_index, json.dumps(c_m_params)))


def delete_c_m_rows_w_validated_params(cls, validated_delete_c_m_params, rqst_errors):
    if validated_delete_c_m_params:
        for c_m_param_index, c_m_params in enumerate(validated_delete_c_m_params):
            rqst_management_status_id = c_m_params['rqst_management_status_id']

            try:
                c_m_status_row = cls.objects.get(id=rqst_management_status_id)

                c_m_status_row.delete()
            except cls.DoesNotExist:
                rqst_errors.append('Case Management Status Row does not exist for the id: {!s}'.format(
                    str(rqst_management_status_id)))
            except cls.MultipleObjectsReturned:
                rqst_errors.append(
                    'Multiple Case Management Status Rows exist for the id: {!s}'.format(
                        str(rqst_management_status_id)))
            except IntegrityError:
                rqst_errors.append(
                    "Error at create_case_management_rows[{!s}] creating case management step row for params: {!s}".format(
                        c_m_param_index, json.dumps(c_m_params)))


def add_hospital_info_to_consumer_instance(consumer_instance, validated_hospital_info_params, post_errors):
    consumer_hospital_info_row = picmodels.models.ConsumerHospitalInfo()

    if 'treatment_site' in validated_hospital_info_params:
        consumer_hospital_info_row.treatment_site = validated_hospital_info_params['treatment_site']
    if 'account_number' in validated_hospital_info_params:
        consumer_hospital_info_row.account_number = validated_hospital_info_params['account_number']
    if 'mrn' in validated_hospital_info_params:
        consumer_hospital_info_row.mrn = validated_hospital_info_params['mrn']
    if 'date_of_birth' in validated_hospital_info_params:
        consumer_hospital_info_row.date_of_birth = validated_hospital_info_params['date_of_birth']
    if 'ssn' in validated_hospital_info_params:
        consumer_hospital_info_row.ssn = validated_hospital_info_params['ssn']
    if 'state' in validated_hospital_info_params:
        consumer_hospital_info_row.state = validated_hospital_info_params['state']
    if 'p_class' in validated_hospital_info_params:
        consumer_hospital_info_row.p_class = validated_hospital_info_params['p_class']
    if 'admit_date' in validated_hospital_info_params:
        consumer_hospital_info_row.admit_date = validated_hospital_info_params['admit_date']
    if 'discharge_date' in validated_hospital_info_params:
        consumer_hospital_info_row.discharge_date = validated_hospital_info_params['discharge_date']
    if 'medical_charges' in validated_hospital_info_params:
        consumer_hospital_info_row.medical_charges = validated_hospital_info_params['medical_charges']
    if 'referred_date' in validated_hospital_info_params:
        consumer_hospital_info_row.referred_date = validated_hospital_info_params['referred_date']
    if 'no_date' in validated_hospital_info_params:
        consumer_hospital_info_row.no_date = validated_hospital_info_params['no_date']
    if 'type' in validated_hospital_info_params:
        consumer_hospital_info_row.type = validated_hospital_info_params['type']
    if 'no_reason' in validated_hospital_info_params:
        consumer_hospital_info_row.no_reason = validated_hospital_info_params['no_reason']
    if 'case_status' in validated_hospital_info_params:
        consumer_hospital_info_row.case_status = validated_hospital_info_params["case_status"]
        if not consumer_hospital_info_row.check_case_status_choices():
            post_errors.append("case_status: {!s} is not a valid choice".format(consumer_hospital_info_row.case_status))

    if not post_errors:
        consumer_hospital_info_row.save()
        consumer_instance.consumer_hospital_info = consumer_hospital_info_row

        consumer_instance.save()
    else:
        consumer_instance.delete()


def add_cps_info_to_consumer_instance(consumer_instance, validated_cps_info_params, post_errors):
    cps_info_object = picmodels.models.ConsumerCPSInfoEntry()

    rqst_cps_location = validated_cps_info_params["rqst_cps_location"]
    try:
        cps_location_object = picmodels.models.NavMetricsLocation.objects.get(name=rqst_cps_location)
        if not cps_location_object.cps_location:
            post_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
        else:
            cps_info_object.cps_location = cps_location_object
    except picmodels.models.NavMetricsLocation.DoesNotExist:
        post_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))

    cps_info_object.apt_date = validated_cps_info_params["rqst_apt_date"]
    cps_info_object.target_list = validated_cps_info_params["rqst_target_list"]
    cps_info_object.phone_apt = validated_cps_info_params["rqst_phone_apt"]
    cps_info_object.case_mgmt_type = validated_cps_info_params["rqst_case_mgmt_type"]

    cps_info_object.case_mgmt_status = validated_cps_info_params["rqst_case_mgmt_status"]
    if not cps_info_object.check_case_mgmt_status_choices():
        post_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_object.case_mgmt_status))
    cps_info_object.app_type = validated_cps_info_params["rqst_app_type"]
    if not cps_info_object.check_app_type_choices():
        post_errors.append("app_type: {!s} is not a valid choice".format(cps_info_object.app_type))
    cps_info_object.app_status = validated_cps_info_params["rqst_app_status"]
    if not cps_info_object.check_app_status_choices():
        post_errors.append("app_status: {!s} is not a valid choice".format(cps_info_object.app_status))
    cps_info_object.point_of_origin = validated_cps_info_params["rqst_point_of_origin"]
    if not cps_info_object.check_point_of_origin_choices():
        post_errors.append("point_of_origin: {!s} is not a valid choice".format(cps_info_object.point_of_origin))

    if not post_errors:
        primary_dependent_object = validated_cps_info_params["primary_dependent_object"]
        if primary_dependent_object._state.adding:
            primary_dependent_object.save()
        cps_info_object.primary_dependent = primary_dependent_object

        secondary_dependents_list = validated_cps_info_params["secondary_dependents_list"]
        if secondary_dependents_list:
            for secondary_dependent_instance in secondary_dependents_list:
                if secondary_dependent_instance._state.adding:
                    secondary_dependent_instance.save()
        # instance must be saved before many to many relationship can be set
        cps_info_object.save()
        cps_info_object.secondary_dependents = secondary_dependents_list

        cps_info_object.save()
        consumer_instance.cps_info = cps_info_object

        consumer_instance.save()
    else:
        consumer_instance.delete()


# getattr(object, field_name)
# need to manually copy consumer notes
def create_backup_consumer_obj(consumer_instance):
    consumer_instance_fields = consumer_instance._meta.get_fields()
    non_null_field_name_list = []
    for field in consumer_instance_fields:
        try:
            if getattr(consumer_instance, field.name) is not None and field.name != 'id':
                non_null_field_name_list.append(field.name)
        except AttributeError:
            pass

    backup_consumer_obj = picmodels.models.PICConsumerBackup()
    for orig_field in non_null_field_name_list:
        orig_field_value = getattr(consumer_instance, orig_field)
        if orig_field == "cps_info":
            pass
        else:
            if orig_field_value.__class__.__name__ != 'ManyRelatedManager':
                setattr(backup_consumer_obj, orig_field, orig_field_value)
    backup_consumer_obj.save()

    if "cps_info" in non_null_field_name_list:
        cps_info_copy = picmodels.models.ConsumerCPSInfoEntry()
        cps_info_orig = getattr(consumer_instance, "cps_info")
        cps_info_orig_fields = cps_info_orig._meta.get_fields()

        for cps_info_orig_field in cps_info_orig_fields:
            try:
                cps_info_orig_field_value = getattr(cps_info_orig, cps_info_orig_field.name)

                if cps_info_orig_field.name == 'secondary_dependents':
                    # Need to implement something to copy secondary dependents, breaks if you omit this
                    pass
                elif cps_info_orig_field.name != 'id':
                    setattr(cps_info_copy, cps_info_orig_field.name, cps_info_orig_field_value)
            except AttributeError:
                pass
        cps_info_copy.save()

        setattr(backup_consumer_obj, "cps_info", cps_info_copy)
        backup_consumer_obj.save()

    orig_consumer_notes = picmodels.models.ConsumerNote.objects.filter(consumer=consumer_instance.id)
    for consumer_note in orig_consumer_notes:
        consumer_note_copy_object = picmodels.models.ConsumerNote(consumer_backup=backup_consumer_obj,
                                                 navigator_notes=consumer_note.navigator_notes)
        consumer_note_copy_object.save()

    return backup_consumer_obj


def modify_consumer_cps_info(consumer_instance, validated_cps_info_params, rqst_errors):
    cps_info_instance = consumer_instance.cps_info
    if cps_info_instance is None:
        cps_info_instance = picmodels.models.ConsumerCPSInfoEntry()

    if "rqst_cps_location" in validated_cps_info_params:
        rqst_cps_location = validated_cps_info_params["rqst_cps_location"]
        try:
            cps_location_object = picmodels.models.NavMetricsLocation.objects.get(name=rqst_cps_location)
            if not cps_location_object.cps_location:
                rqst_errors.append("{!s} is not a cps_location".format(rqst_cps_location))
            else:
                cps_info_instance.cps_location = cps_location_object
        except picmodels.models.NavMetricsLocation.DoesNotExist:
            rqst_errors.append("NavMetricsLocation object does not exist for name: {!s}".format(rqst_cps_location))
    if not cps_info_instance.cps_location:
        rqst_errors.append("cps_location is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_apt_date' in validated_cps_info_params:
        cps_info_instance.apt_date = validated_cps_info_params['rqst_apt_date']
    if not cps_info_instance.apt_date:
        rqst_errors.append("apt_date is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_target_list' in validated_cps_info_params:
        cps_info_instance.target_list = validated_cps_info_params['rqst_target_list']
    if cps_info_instance.target_list is None:
        rqst_errors.append("target_list is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_phone_apt' in validated_cps_info_params:
        cps_info_instance.phone_apt = validated_cps_info_params['rqst_phone_apt']
    if cps_info_instance.phone_apt is None:
        rqst_errors.append("phone_apt is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_case_mgmt_type' in validated_cps_info_params:
        cps_info_instance.case_mgmt_type = validated_cps_info_params['rqst_case_mgmt_type']
    if not cps_info_instance.case_mgmt_type:
        rqst_errors.append("case_mgmt_type is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_case_mgmt_status' in validated_cps_info_params:
        cps_info_instance.case_mgmt_status = validated_cps_info_params['rqst_case_mgmt_status']
        if not cps_info_instance.check_case_mgmt_status_choices():
            rqst_errors.append("case_mgmt_status: {!s} is not a valid choice".format(cps_info_instance.case_mgmt_status))
    if not cps_info_instance.case_mgmt_status:
        rqst_errors.append("case_mgmt_status is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_app_type' in validated_cps_info_params:
        cps_info_instance.app_type = validated_cps_info_params['rqst_app_type']
        if not cps_info_instance.check_app_type_choices():
            rqst_errors.append("app_type: {!s} is not a valid choice".format(cps_info_instance.app_type))
    if not cps_info_instance.app_type:
        rqst_errors.append("app_type is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_app_status' in validated_cps_info_params:
        cps_info_instance.app_status = validated_cps_info_params['rqst_app_status']
        if not cps_info_instance.check_app_status_choices():
            rqst_errors.append("app_status: {!s} is not a valid choice".format(cps_info_instance.app_status))
    if not cps_info_instance.app_status:
        rqst_errors.append("app_status is required for a cps info entry. CPS info can not be added to consumer instance.")

    if 'rqst_point_of_origin' in validated_cps_info_params:
        cps_info_instance.point_of_origin = validated_cps_info_params['rqst_point_of_origin']
        if not cps_info_instance.check_point_of_origin_choices():
            rqst_errors.append("point_of_origin: {!s} is not a valid choice".format(cps_info_instance.point_of_origin))
    if not cps_info_instance.point_of_origin:
        rqst_errors.append("point_of_origin is required for a cps info entry. CPS info can not be added to consumer instance.")

    if not rqst_errors:
        if 'primary_dependent_object' in validated_cps_info_params:
            primary_dependent_object = validated_cps_info_params['primary_dependent_object']
            if primary_dependent_object._state.adding:
                primary_dependent_object.save()
            cps_info_instance.primary_dependent = primary_dependent_object
        if not cps_info_instance.primary_dependent:
            rqst_errors.append("primary_dependent is required for a cps info entry. CPS info can not be added to consumer instance.")

        if not rqst_errors:
            if 'secondary_dependents_list' in validated_cps_info_params:
                secondary_dependents_list = validated_cps_info_params['secondary_dependents_list']

                if not cps_info_instance._state.adding and cps_info_instance.secondary_dependents:
                    cps_info_instance.secondary_dependents.clear()
                if secondary_dependents_list:
                    for secondary_dependent_instance in secondary_dependents_list:
                        if secondary_dependent_instance._state.adding:
                            secondary_dependent_instance.save()

                # instance must be saved before many to many relationship can be set
                cps_info_instance.save()
                cps_info_instance.secondary_dependents = secondary_dependents_list

            cps_info_instance.save()
            consumer_instance.cps_info = cps_info_instance
            consumer_instance.save()


def update_indiv_seeking_nav_columns_for_row(row, validated_params, rqst_errors):
    if 'billing_amount' in validated_params:
        row.billing_amount = validated_params['billing_amount']
    if 'consumer_need' in validated_params:
        row.consumer_need = validated_params['consumer_need']
        if not row.check_consumer_need_choices():
            rqst_errors.append(
                "consumer_need: {!s} is not a valid choice".format(row.consumer_need)
            )
    if 'service_expertise_need' in validated_params:
        expertise_row = get_service_expertise_row_with_given_name(
            validated_params['service_expertise_need'],
            rqst_errors
        )
        if expertise_row:
            row.service_expertise_need = expertise_row
    if 'insurance_carrier' in validated_params:
        carrier_info = validated_params['insurance_carrier']
        carrier_row = get_carrier_row_with_given_name_and_state(
            carrier_info,
            rqst_errors
        )
        if carrier_row:
            row.insurance_carrier = carrier_row

    if 'add_healthcare_locations_used' in validated_params:
        healthcare_location_info = validated_params['add_healthcare_locations_used']
        healthcare_location_rows = []
        for location_dict in healthcare_location_info:
            healthcare_location_rows.append(get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors))
        if not rqst_errors:
            check_healthcare_locations_used_for_given_rows(
                row.healthcare_locations_used.all(),
                healthcare_location_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for location_row in healthcare_location_rows:
                    row.healthcare_locations_used.add(location_row)
    elif 'remove_healthcare_locations_used' in validated_params:
        healthcare_location_info = validated_params['remove_healthcare_locations_used']
        healthcare_location_rows = []
        for location_dict in healthcare_location_info:
            healthcare_location_rows.append(
                get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors))
        if not rqst_errors:
            check_healthcare_locations_used_for_not_given_rows(
                row.healthcare_locations_used.all(),
                healthcare_location_rows,
                row,
                rqst_errors
            )
            if not rqst_errors:
                for location_row in healthcare_location_rows:
                    row.healthcare_locations_used.remove(location_row)


def get_service_expertise_row_with_given_name(name, rqst_errors):
    row = None

    if name:
        try:
            row = picmodels.models.HealthcareServiceExpertise.objects.get(name__iexact=name)
        except picmodels.models.HealthcareServiceExpertise.DoesNotExist:
            row = None
            rqst_errors.append("No HealthcareServiceExpertise row found with name: {}".format(name))

    return row


def get_carrier_row_with_given_name_and_state(validated_params, rqst_errors):
    row = None
    name = validated_params['name']
    state = validated_params['state_province']

    if name:
        try:
            row = picmodels.models.HealthcareCarrier.objects.get(name__iexact=name, state_province__iexact=state)
        except picmodels.models.HealthcareCarrier.DoesNotExist:
            row = None
            rqst_errors.append("No HealthcareCarrier row found with name: {} and state: {}".format(name, state))

    return row


def get_provider_location_row_with_given_name_and_state(location_dict, rqst_errors):
    row = None

    if location_dict:
        try:
            row = picmodels.models.ProviderLocation.objects.get(
                name__iexact=location_dict['name'],
                state_province__iexact=location_dict['state_province']
            )
        except picmodels.models.ProviderLocation.DoesNotExist:
            row = None
            rqst_errors.append(
                "No ProviderLocation row found with name: {} and state: {}".format(
                    location_dict['name'],
                    location_dict['state_province']
                )
            )

    return row


def get_case_management_client_row_with_given_id(client_id, rqst_errors):
    row = None

    if client_id:
        try:
            row = picmodels.models.CaseManagementClient.objects.get(id=client_id)
        except picmodels.models.CaseManagementClient.DoesNotExist:
            row = None
            rqst_errors.append("No CaseManagementClient row found with id: {}".format(client_id))

    return row


def check_healthcare_locations_used_for_given_rows(cur_locations_used_qset, given_locations_used_list, row, rqst_errors):
    for location_used in given_locations_used_list:
        if location_used in cur_locations_used_qset:
            rqst_errors.append(
                "Healthcare location with the name: {} and state: {} already exists in row id {}'s healthcare_locations_used list (Hint - remove from parameter 'add_healthcare_locations_used' list)".format(
                    location_used.name,
                    location_used.state_province,
                    row.id,
                )
            )


def check_healthcare_locations_used_for_not_given_rows(cur_locations_used_qset, given_locations_used_list, row, rqst_errors):
    for location_used in given_locations_used_list:
        if location_used not in cur_locations_used_qset:
            rqst_errors.append(
                "Healthcare location with the name: {} and state: {} does not exist in row id {}'s healthcare_locations_used list (Hint - remove from parameter 'add_healthcare_locations_used' list)".format(
                    location_used.name,
                    location_used.state_province,
                    row.id,
                )
            )


def check_referring_cm_clients_for_given_rows(cur_referring_cm_clients_qset, given_cm_clients_list, row, rqst_errors):
    for cm_client in given_cm_clients_list:
        if cm_client in cur_referring_cm_clients_qset:
            rqst_errors.append(
                "cm_client with id: {} already exists in row id {}'s referring_cm_clients list (Hint - remove from parameter 'add_referring_cm_clients' list)".format(
                    cm_client.id,
                    row.id,
                )
            )


def check_referring_cm_clients_for_not_given_rows(cur_referring_cm_clients_qset, given_cm_clients_list, row, rqst_errors):
    for cm_client in given_cm_clients_list:
        if cm_client not in cur_referring_cm_clients_qset:
            rqst_errors.append(
                "cm_client with id: {} does not exists in row id {}'s referring_cm_clients list (Hint - remove from parameter 'remove_referring_cm_clients' list)".format(
                    cm_client.id,
                    row.id,
                )
            )
