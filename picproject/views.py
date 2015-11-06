from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render_to_response, render
from django import forms
from picproject.forms import AssessmentFormOne
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    html = t.render(Context({'current_date': now}))
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

def search(request):
    if 'q' in request.GET:
        message = 'You searched for: %r' % request.GET['q']
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def search_form(request):
    return render(request, 'search_form.html')

class UserCreationForm(forms.Form):
    username = forms.CharField(max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2

def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            do_something_with(form.cleaned_data)
            return redirect("create_user_success")
    else:
        form = UserCreationForm()

    return render_to_response("signup/form.html", {'form': form})

def risk_assessment(request):
    if request.method == 'POST':
        post_data = request.POST
        form_one = AssessmentFormOne(post_data)
        if form_one.is_valid():
            cd = form_one.cleaned_data
            request.session['_old_post'] = cd
            return HttpResponseRedirect('/riskassessment/next/')
    else:
        form_one = AssessmentFormOne()
    return render(request, 'assessment.html', {'form_one': form_one})

def risk_assessment_2(request):
    old_post = request.session.get('_old_post')
    if old_post:
        return render(request, 'search_form.html')
        if request.method == 'POST':
            post_data = request.POST
            form_one = AssessmentFormOne(post_data)
            if form_one.is_valid():
                cd = form_one.cleaned_data
                return render(request, 'assessment.html', {'form_one': form_one})
        else:
            form_one = AssessmentFormOne()
        return render(request, 'assessment.html', {'form_one': form_one})
    else:
        raise Http404('Only POSTs are allowed')



