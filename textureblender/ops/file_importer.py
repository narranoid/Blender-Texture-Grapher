
from abc import abstractmethod

import bpy
from bpy.types import Operator, Panel, Menu
from bpy.props import StringProperty, CollectionProperty

from bpy_extras.io_utils import ImportHelper


class FileImporterMeta(type(Operator), type(ImportHelper)):

    def __new__(cls, clsname, superclasses, attributedict, **kwargs):
        annotations = attributedict.get('__annotations__', dict())

        if 'filter_glob_default' in kwargs:
            annotations['filter_glob'] = StringProperty(
                default=kwargs['filter_glob_default'],
                options={'HIDDEN'}
            )

        annotations['directory'] = StringProperty(
            name=kwargs.get('directory_name', 'Directory'),
            subtype='DIR_PATH',
            default=kwargs.get('directory_description', ''),
            description=kwargs.get('directory_description', 'Directory')
        )

        annotations['files'] = CollectionProperty(
            type=bpy.types.OperatorFileListElement,
            options={'HIDDEN', 'SKIP_SAVE'}
        )

        attributedict['__annotations__'] = annotations

        return super().__new__(cls, clsname, superclasses, attributedict)


class FileImporter(Operator, ImportHelper,
                   metaclass=FileImporterMeta):

    def execute(self, context):
        """Do something with the selected file(s)."""

        # Check if everything is ok
        if not self.directory:
            self.report({'INFO'}, 'No Folder Selected')
            return {'CANCELLED'}
        if not self.files_valid():
            self.report({'INFO'}, 'No Files Selected')
            return {'CANCELLED'}

        return self.on_valid_files_selected(context)

    def files_valid(self):
        return len(self.files.items()) > 0 and self.files[0] is not None and len(self.files[0].name) > 0

    @property
    def file_paths(self):
        file_paths = []
        for file_list_element in self.files:
            file_paths.append(self.directory + file_list_element.name)
        return file_paths

    @abstractmethod
    def on_valid_files_selected(self, context):
        pass
