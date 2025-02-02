# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from dateutil import relativedelta
from django.conf import settings as django_settings

# Retrieve root settings dict
REST_FRAMEWORK_TUS = getattr(django_settings, 'REST_FRAMEWORK_TUS', {})


# Retrieve settings
TUS_UPLOAD_MODEL = REST_FRAMEWORK_TUS.get('UPLOAD_MODEL', 'rest_framework_tus.Upload')
TUS_UPLOAD_EXPIRES = REST_FRAMEWORK_TUS.get('UPLOAD_EXPIRES', relativedelta.relativedelta(days=1))
TUS_UPLOAD_DIR = REST_FRAMEWORK_TUS.get('UPLOAD_DIR', os.path.join(django_settings.BASE_DIR, 'tmp/uploads/'))
TUS_RESPONSE_BODY_ENABLED = REST_FRAMEWORK_TUS.get('RESPONSE_BODY_ENABLED', False)
TUS_SAVE_HANDLER_CLASS = \
    REST_FRAMEWORK_TUS.get('SAVE_HANDLER_CLASS', 'rest_framework_tus.storage.DefaultSaveHandler')
TUS_MAX_FILE_SIZE = REST_FRAMEWORK_TUS.get('MAX_FILE_SIZE', 4294967296)  # in bytes
TUS_FILENAME_METADATA_FIELD = REST_FRAMEWORK_TUS.get('FILENAME_METADATA_FIELD', 'filename')


TUS_USE_TEMP_FILE = REST_FRAMEWORK_TUS.get('USE_TEMP_FILE', True) # if set to False, the file will be held in memory
