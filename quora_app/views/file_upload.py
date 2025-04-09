from django.core.files.base import *
from utility.constants import BYTES_PER_MB

from utility.utils import *
from utility.response import ApiResponse

"""Serializers"""
from ..serializers.assets_serializer import AssetsSerializer

"""Models"""
from ..models import Assets


class FileUploadView(MultipleFieldPKModelMixin, CreateRetrieveUpdateViewSet, ApiResponse):
    serializer_class = AssetsSerializer
    singular_name = "File"
    model_class = Assets.objects

    def get_object(self, pk):
        try:
            return self.model_class.get(pk=pk)
        except:
            return None

    def post(self, request, *args, **kwargs):
        file_type, file_size, file_name = None, None, None

        data = request.data
        if file_meta := data.get("file_name"):
            file_meta = file_meta.__dict__

            response = super(FileUploadView, self).create(request, *args, **kwargs)

            # file_size = file_meta.get("size")  # Size in bytes from request
            # file_type = file_meta.get("content_type")
            file_name = file_meta.get("_name")

            if file_instance := self.model_class.filter(id=response.data.get("id")).first():
                # file_instance.file_type = file_type
                # Converting bytes to megabytes before saving
                # file_instance.file_size = convert_filesize_bits_to_mega_bytes(file_size)  # Stored in MB
                file_instance.actual_file_name = file_name
                file_instance.save()
                
                response.data['file_name'] = str(file_instance.file_name)
                # response.data['file_type'] = file_instance.file_type
                # response.data['file_size'] = file_instance.file_size  # Size in MB
                response.data['actual_file_name'] = file_name

                return ApiResponse.response_ok(self, data=response.data, message=f"{self.singular_name} uploaded.")

        return ApiResponse.response_bad_request(self, message=f"{self.singular_name} not found.")

    def delete(self, request, *args, **kwargs):
        """
        :To delete the single record.
        """
        get_id = self.kwargs.get("id")

        """ get instance """
        instance = self.get_object(get_id)

        if not instance:
            return ApiResponse.response_not_found(self, message=f"{self.singular_name} not found.")

        instance.file_name.delete(save=False)
        instance.delete()

        """ return success """
        return ApiResponse.response_ok(self, message=f"{self.singular_name} deleted.")


def convert_filesize_bits_to_mega_bytes(bits):
    """
    Convert file size from bytes to megabytes
    :param bits: File size in bytes
    :return: File size in megabytes rounded to 4 decimal places
    """
    return round(bits / BYTES_PER_MB, 4)
