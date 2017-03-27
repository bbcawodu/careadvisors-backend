from django.db import models
from django.conf import settings


class CallToAction(models.Model):
    # fields for CallToAction model
    intent = models.CharField(max_length=1000)
    cta_image = models.ImageField(upload_to='call_to_actions/', default=settings.DEFAULT_CTA_PIC_URL)

    def return_values_dict(self):
        valuesdict = {"Intent": self.intent,
                      "Picture": self.cta_image.url,
                      "Database ID": self.id
                      }

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'
