from django.db import models
from django.conf import settings
from django.dispatch import receiver

from custom_storages import PublicMediaStorage

import uuid
import os


def get_cta_image_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('call_to_actions', filename)


class CallToAction(models.Model):
    # fields for CallToAction model
    intent = models.CharField(max_length=1000)
    cta_image = models.ImageField(upload_to=get_cta_image_file_path, storage=PublicMediaStorage(), blank=True, null=True)

    def return_values_dict(self):
        valuesdict = {"Intent": self.intent,
                      "Picture": None,
                      "Database ID": self.id
                      }

        if self.cta_image:
            valuesdict["Picture"] = self.cta_image.url
        else:
            valuesdict["Picture"] = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_CTA_PIC_URL)

        return valuesdict

    class Meta:
        # maps model to the picmodels module
        app_label = 'picmodels'


@receiver(models.signals.post_delete, sender=CallToAction)
def remove_file_from_s3(sender, instance, using, **kwargs):
    default_cta_image_url = "{}{}".format(settings.MEDIA_URL, settings.DEFAULT_CTA_PIC_URL)
    if instance.staff_pic.url != default_cta_image_url:
        instance.cta_image.delete(save=False)
