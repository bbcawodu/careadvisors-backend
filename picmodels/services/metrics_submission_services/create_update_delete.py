from picmodels.models import MetricsSubmission
from picmodels.models import PICStaff


def create_or_update_metrics_obj_using_validated_params(validated_metrics_params, rqst_errors):
    metrics_instance = None
    metrics_action_message = None

    rqst_usr_email = validated_metrics_params['rqst_usr_email']
    metrics_date = validated_metrics_params['metrics_date']
    location_instance_for_metrics = validated_metrics_params['location_instance_for_metrics']

    try:
        user_instance = PICStaff.objects.get(email__iexact=validated_metrics_params['rqst_usr_email'])
    except PICStaff.DoesNotExist:
        rqst_errors.append("Staff database entry does not exist for email: {!s}".format(rqst_usr_email))
    else:
        try:
            metrics_instance = MetricsSubmission.objects.get(staff_member=user_instance, submission_date=metrics_date)
            metrics_action_message = 'Metrics Entry Updated'
        except MetricsSubmission.DoesNotExist:
            metrics_instance = MetricsSubmission(staff_member=user_instance, submission_date=metrics_date)
            metrics_action_message = 'Metrics Entry Created'
        except MetricsSubmission.MultipleObjectsReturned:
            rqst_errors.append("Multiple metrics entries exist for this date")

        if metrics_instance:
            metrics_instance.no_general_assis = validated_metrics_params['rqst_no_general_assis']
            metrics_instance.no_plan_usage_assis = validated_metrics_params['rqst_no_plan_usage_assis']
            metrics_instance.no_locating_provider_assis = validated_metrics_params['rqst_no_locating_provider_assis']
            metrics_instance.no_billing_assis = validated_metrics_params['rqst_no_billing_assis']
            metrics_instance.no_enroll_apps_started = validated_metrics_params['rqst_no_enroll_apps_started']
            metrics_instance.no_enroll_qhp = validated_metrics_params['rqst_no_enroll_qhp']
            metrics_instance.no_enroll_abe_chip = validated_metrics_params['rqst_no_enroll_abe_chip']
            metrics_instance.no_enroll_shop = validated_metrics_params['rqst_no_enroll_shop']
            metrics_instance.no_referrals_agents_brokers = validated_metrics_params['rqst_no_referrals_agents_brokers']
            metrics_instance.no_referrals_ship_medicare = validated_metrics_params['rqst_no_referrals_ship_medicare']
            metrics_instance.no_referrals_other_assis_programs = validated_metrics_params['rqst_no_referrals_other_assis_programs']
            metrics_instance.no_referrals_issuers = validated_metrics_params['rqst_no_referrals_issuers']
            metrics_instance.no_referrals_doi = validated_metrics_params['rqst_no_referrals_doi']
            metrics_instance.no_mplace_tax_form_assis = validated_metrics_params['rqst_no_mplace_tax_form_assis']
            metrics_instance.no_mplace_exempt_assis = validated_metrics_params['rqst_no_mplace_exempt_assis']
            metrics_instance.no_qhp_abe_appeals = validated_metrics_params['rqst_no_qhp_abe_appeals']
            metrics_instance.no_data_matching_mplace_issues = validated_metrics_params['rqst_no_data_matching_mplace_issues']
            metrics_instance.no_sep_eligible = validated_metrics_params['rqst_no_sep_eligible']
            metrics_instance.no_employ_spons_cov_issues = validated_metrics_params['rqst_no_employ_spons_cov_issues']
            metrics_instance.no_aptc_csr_assis = validated_metrics_params['rqst_no_aptc_csr_assis']
            metrics_instance.no_cps_consumers = validated_metrics_params['rqst_no_cps_consumers']
            metrics_instance.cmplx_cases_mplace_issues = validated_metrics_params['rqst_cmplx_cases_mplace_issues']
            metrics_instance.county = validated_metrics_params['rqst_metrics_county']
            metrics_instance.location = location_instance_for_metrics
            metrics_instance.zipcode = location_instance_for_metrics.address.zipcode

            if len(rqst_errors) == 0:
                metrics_instance.save()

                metrics_instance_current_plan_stats = metrics_instance.planstat_set.all()
                for current_plan_stat_instance in metrics_instance_current_plan_stats:
                    current_plan_stat_instance.delete()

                unsaved_plan_stat_objs = validated_metrics_params['unsaved_plan_stat_objs']
                for unsaved_plan_stat_obj in unsaved_plan_stat_objs:
                    unsaved_plan_stat_obj.metrics_submission = metrics_instance
                    unsaved_plan_stat_obj.save()

    return metrics_instance, metrics_action_message


def delete_instance_using_validated_params(rqst_id, post_errors):
    try:
        metrics_instance = MetricsSubmission.objects.get(id=rqst_id)
        metrics_instance.delete()
    except MetricsSubmission.DoesNotExist:
        post_errors.append("Metrics instance does not exist for database id: {}".format(rqst_id))
