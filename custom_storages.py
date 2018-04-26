# custom_storages.py
from django.conf import settings
from storages.backends.s3boto import S3BotoStorage


# class StaticStorage(S3BotoStorage):
#     location = settings.STATICFILES_LOCATION


class PublicMediaStorage(S3BotoStorage):
    location = settings.AWS_PUBLIC_MEDIA_LOCATION
    file_overwrite = False

class PrivateMediaStorage(S3BotoStorage):
    location = settings.AWS_PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False