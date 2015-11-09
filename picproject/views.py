"""
Defines views that are mapped to url configurations
"""



from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django import forms
from django.db import models
from django.contrib.auth.models import User
from picproject.forms import AssessmentFormOne, AssessmentFormTwo, UserCreateForm
from picmodels.models import PICUser
import datetime



#defines view for home page
def index(request):
    return render(request, "home_page.html")



#defines view for registration page
def registration(request):
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['date_joined'] = datetime.date.today()
        form = UserCreateForm(form_data)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/memberlist/")
    else:
        form = UserCreateForm()
    return render(request, "registration.html", {'form': form})



#defines view for member list display page
def memberlist(request):
    all_members = PICUser.objects.all()
    return render(request, "member_list.html", {'member_list': all_members})



#defines view for part 1 of risk assessment page
def risk_assessment(request):
    if request.method == 'POST':
        post_data = request.POST
        form_one = AssessmentFormOne(post_data)
        if form_one.is_valid():
            cd = form_one.cleaned_data
            request.session['form_data'] = cd
            return HttpResponseRedirect('/riskassessment/next/')
    else:
        form_one = AssessmentFormOne()
    return render(request, 'assessment.html', {'form_one': form_one})



#defines view for part 2 of risk assessment page
def risk_assessment_2(request):
    form_data = request.session.get('form_data')
    if form_data:
        for key in form_data:
            form_data[key] =int(form_data[key])
    else:
        raise Http404('need old post data')

    if request.method == 'POST':
        current_post_data = request.POST
        form_one = AssessmentFormTwo(form_data, current_post_data)
        if form_one.is_valid():
            cd = form_one.cleaned_data
            health_risk = 0
            for key in form_data:
                answer = form_data[key]
                if key == 'is_employed' or key == 'has_insurance' or key == 'has_primary_doctor':
                    if answer == 0:
                        health_risk += 1
                else:
                    if answer == 1:
                        health_risk += 1
            for key in cd:
                if int(cd[key]) == 1:
                    health_risk += 1
            health_risk_score = (float(health_risk)/11)*100
            health_risk_string = str(int(health_risk_score))
            return render(request, 'assessment_score.html', {'score': health_risk_string})
    else:
        form_one = AssessmentFormTwo(previous_form_data=form_data)
        return render(request, 'assessment_2.html', {'form_one': form_one})

    return render(request, 'assessment_2.html', {'form_one': form_one})



