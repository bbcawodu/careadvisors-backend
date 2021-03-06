from django.db import IntegrityError
from django.apps import apps


def create_row_w_validated_params(cls, validated_params, rqst_errors):
    if "step_name" not in validated_params:
        rqst_errors.append("'step_name' is a required key in the validated_params argument")
        return None
    if "step_class_name" not in validated_params:
        rqst_errors.append("'step_class_name' is a required key in the validated_params argument")
        return None
    if "step_number" not in validated_params:
        rqst_errors.append("'step_number' is a required key in the validated_params argument")
        return None

    row = cls()

    step_table_class = get_step_table_class_with_given_class_name(validated_params["step_class_name"], rqst_errors)
    if rqst_errors:
        return None

    if 'step_table_name' in validated_params:
        step_table_name_found = check_db_schema_for_table_name(validated_params['step_table_name'], rqst_errors)
        if not step_table_name_found:
            return None

    if rqst_errors:
        return None

    row.step_class_name = step_table_class.__name__
    row.step_table_name = step_table_class._meta.db_table
    if hasattr(step_table_class._meta, "rest_url") and step_table_class._meta.rest_url:
        row.rest_url = step_table_class._meta.rest_url
    row.step_name = validated_params['step_name']
    row.step_number = validated_params['step_number']

    if 'step_table_name' in validated_params:
        row.step_table_name = validated_params['step_table_name']
    if 'rest_url' in validated_params:
        row.rest_url = validated_params['rest_url']

    try:
        row.save()
    except IntegrityError:
        rqst_errors.append(
            "'step_name', 'step_table_name', and 'step_class_name' must be unique for row to be saved. A row already with the same values for those columns."
        )
        return None

    return row


def update_row_w_validated_params(cls, validated_params, rqst_errors):
    if "id" in validated_params:
        rqst_id = validated_params['id']
    else:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

    try:
        row = cls.objects.get(id=rqst_id)
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {}'.format(rqst_id))
        return None

    if "step_class_name" in validated_params:
        step_table_class = get_step_table_class_with_given_class_name(validated_params["step_class_name"], rqst_errors)
        if rqst_errors:
            return None
        row.step_class_name = step_table_class.__name__

    if "step_table_name" in validated_params:
        step_table_name_found = check_db_schema_for_table_name(validated_params['step_table_name'], rqst_errors)
        if not step_table_name_found:
            return None

        row.step_table_name = validated_params["step_table_name"]
    if "step_name" in validated_params:
        row.step_name = validated_params["step_name"]
    if "step_number" in validated_params:
        row.step_number = validated_params["step_number"]
    if 'rest_url' in validated_params:
        row.rest_url = validated_params['rest_url']

    if not rqst_errors:
        try:
            row.save()
        except IntegrityError:
            rqst_errors.append(
                "'step_name', 'step_table_name', and 'step_class_name' must be unique for row to be saved. A row already with the same values for those columns."
            )
            return None
    else:
        return None

    return row


def delete_row_w_validated_params(cls, validated_params, rqst_errors):
    if "id" in validated_params:
        rqst_id = validated_params['id']
    else:
        rqst_errors.append("'id' is a required key in the validated_params argument")
        return None

    try:
        row = cls.objects.get(id=rqst_id)
        row.delete()
    except cls.DoesNotExist:
        rqst_errors.append('Row does not exist for the id: {!s}'.format(str(rqst_id)))


def get_step_table_class_with_given_class_name(step_class_name, rqst_errors):
    step_table_class = None

    if step_class_name:
        app_models = apps.get_app_config('picmodels').get_models()
        # app_models = get_models(apps, include_auto_created=True)

        for model in app_models:
            if model.__name__ == step_class_name:
                step_table_class = model
                break

        if not step_table_class:
            rqst_errors.append("No class found in app for given step_class_name")

    return step_table_class


def check_db_schema_for_table_name(table_name, rqst_errors):
    table_name_found = False

    if table_name:
        app_models = apps.get_app_config('picmodels').get_models()

        for model in app_models:
            if model._meta.db_table_ == table_name:
                table_name_found = True
                break

        if not table_name_found:
            rqst_errors.append("No table in db found for given table_name")

    return table_name_found
