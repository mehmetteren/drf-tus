# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from abc import ABCMeta, abstractmethod

from django.core.files import File
from six import with_metaclass

from django.utils.module_loading import import_string

from rest_framework_tus import signals
from .settings import TUS_SAVE_HANDLER_CLASS, TUS_USE_TEMP_FILE
import logging
from django.core.files.base import ContentFile
from typing import Dict

class AbstractUploadSaveHandler(with_metaclass(ABCMeta, object)):
    def __init__(self, upload):
        self.upload = upload

    @abstractmethod
    def handle_save(self):
        pass

    def run(self):
        # Trigger state change
        self.upload.start_saving()
        self.upload.save()

        # Initialize saving
        self.handle_save()

    def finish(self):
        # Trigger signal
        signals.saved.send(sender=self.__class__, instance=self)

        # Finish
        self.upload.finish()
        self.upload.save()


class DefaultSaveHandler(AbstractUploadSaveHandler):
    destination_file_field = 'uploaded_file'

    def handle_save(self):
        # Save temporary field to file field
        file_field = getattr(self.upload, self.destination_file_field)

        if TUS_USE_TEMP_FILE:
            file_field.save(self.upload.filename, File(open(self.upload.temporary_file_path, 'rb')))
        else:
            content_file = ContentFile(in_memory_navigator.get(self.upload))
            file_field.save(self.upload.filename, content_file)
        
        # Finish upload
        self.finish()


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class InMemoryNavigator(metaclass=Singleton):
    """
    Class for storing in memory files through the upload process
    """
    def __init__(self):
        self.files: Dict[str, bytearray] = {}


    def create(self, upload, in_memory_file=None):
        if upload.guid not in self.files:

            if in_memory_file is not None:
                self.files[upload.guid] = in_memory_file
            else:
                self.files[upload.guid] = bytearray(upload.upload_length)

        else:
            raise Exception("File already exists in memory")


    def update(self, upload, in_memory_file):
        if upload.guid in self.files:
            self.files[upload.guid] = in_memory_file
        else:
            raise Exception("File does not exist in memory")
        

     # TODO: memory performance optimization?
    def write_data(self, upload, data):
        file = self.files.get(upload.guid, None)

        if file is not None:

            for i in range(len(data)):
                file[i + upload.upload_offset] = data[i]

            return i + 1
        
    def get(self, upload):
        return self.files.get(upload.guid, None)

    def delete(self, upload):
        try:
            del self.files[upload.guid]
        except KeyError:
            logging.warning(f"File {upload.guid} does not exist in memory")

    def exists(self, upload):
        return upload.guid in self.files



in_memory_navigator = InMemoryNavigator()



def get_save_handler(import_path=None):
    return import_string(import_path or TUS_SAVE_HANDLER_CLASS)


