import datetime
import json
from picmodels.models import PICStaff
from picmodels.models import PICConsumer
from picmodels.models import PICConsumerBackup
from picmodels.models import ConsumerNote
from picmodels.models import Address
from picmodels.models import Country
from picmodels.models import ConsumerCPSInfoEntry
from picmodels.models import NavMetricsLocation
from django.db import IntegrityError
from django.core.validators import validate_email
from django import forms


