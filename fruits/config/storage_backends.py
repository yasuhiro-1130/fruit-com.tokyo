from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class S3MediaStorage(S3Boto3Storage):
	bucket_name = settings.MEDIA_AWS_STORAGE_BUCKET_NAME
	default_acl = settings.MEDIA_AWS_DEFAULT_ACL

class S3StaticStorageCloudFront(S3Boto3Storage):
	location = settings.STATICFILES_LOCATION

	def __init__(self, *args, **kwargs):
			kwargs['custom_domain'] = settings.AWS_CLOUDFRONT_DOMAIN
			super(S3StaticStorageCloudFront, self).__init__(*args, **kwargs)
