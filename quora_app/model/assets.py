import os
from uuid import uuid4
from .base import Base
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from utility.constants import FILE_SIZE, BYTES_PER_MB


def file_size(value):
    limit = FILE_SIZE * BYTES_PER_MB
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 3 MiB.')

def path_and_rename(instance, filename):
    from datetime import datetime
    upload_to = "static"
    ext = filename.split(".")[-1]
    if instance.pk:
        filename = f"{uuid4().hex}{instance.pk}.{ext}"
    else:
        date_str = (str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_").replace("-", "_"))
        filename = f"{uuid4().hex}{date_str}.{ext}"
    return os.path.join(upload_to, filename)

class Assets(Base):
    file_name = models.FileField(upload_to=path_and_rename, null=True)
    # file_type = models.CharField(max_length=155, null=True, blank=True, db_index=True)
    # file_size = models.FloatField(unique=False, null=True, blank=True, db_index=True)
    actual_file_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)


    class Meta:
        db_table = "assets"

    def to_dict(self, instance=None):
        resp_data = {}
        instance = instance if instance else self
        resp_data['id'] = instance.id
        resp_data['file_name'] = str(instance.file_name)
        resp_data['actual_file_name'] = instance.actual_file_name
        # resp_data['file_type'] = instance.file_type
        # resp_data['file_size'] = instance.file_size
        return resp_data