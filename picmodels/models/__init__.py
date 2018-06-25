import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('rest_url',)

from .utils import *
from .chicago_public_schools import *
from .care_advisors import *
