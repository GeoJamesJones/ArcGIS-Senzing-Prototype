from __future__ import annotations

import arcpy
import os

from typing import Tuple, List, Any
from logging import Logger

from entity_resolution.utils import Logger
from entity_resolution.utils.utilities import error_handler

class CopySourceData:
    def __init__(self, cursor_fields: List[str],
                       data_records: List[List[Any]],
                       feature_class: str,
                       feature_store: str,
                       feature_type: str,
                       datasource: str, 
                       spatial_reference: arcpy.SpatialReference | None,
                       debug_level: str) -> None:
        
        self._cursor_fields = cursor_fields
        self._feature_class = feature_class
        self._feature_store = feature_store
        self._feature_type = feature_type
        self._datasource = datasource
        self._spatial_reference = spatial_reference
        self._data_records = data_records

        self.logger = Logger(__name__, debug_level)

        if debug_level == 'DEBUG':
            self.DEBUG = True
        
        return

    def __del__(self) -> None:
        del self._cursor_fields
        del self._feature_class
        del self._feature_store
        del self._feature_type
        del self._datasource
        del self._spatial_reference
        del self._data_records

    @property
    def cursor_fields(self) -> List[str]:
        return self._cursor_fields

    @property
    def feature_class(self) -> str:
        return self._feature_class

    @property
    def fields_types(self) -> List[Tuple[str, str]]:
        return self._fields_types
    
    @property
    def feature_store(self) -> str:
        return self._feature_store
    
    @property
    def feature_type(self) -> str:
        return self._feature_type

    @property
    def datasource(self) -> str:
        return self._datasource
    @datasource.setter
    def datasource(self, value: str) -> None:
        self._datasource = value

    @property
    def spatial_reference(self) -> arcpy.SpatialReference | None:
        return self._spatial_reference

    @property
    def feature_class_path(self) -> str:
        return self._fc_path

    @property
    def data_records(self) -> List[List[Any]]:
        return self._data_records

    def get_field_types(self) -> List[List[str, str]]:
        self._fields_types = [[f.name, f.type.upper()] for f in arcpy.ListFields(self.feature_class) if f.name in self.cursor_fields]

        for f in self.fields_types:
            if f[1] == 'STRING':
                f[1] = 'TEXT'
            elif f[1] == 'INTEGER':
                f[1] = 'LONG'
        
        self.cursor_fields.append("RECORD_ID")
        self._fields_types.append(["RECORD_ID", "TEXT"])
        
        if self.DEBUG:
            self.logger.debug(f"Fields to add: {self.fields_types}")
        
        return self._fields_types

    def create_feature_table(self) -> str:
        try:
            if self.feature_type in ['Point', 'Polyline', 'Polygon']:
                if arcpy.Exists(os.path.join(self.feature_store, self.datasource)):
                    self.datasource = arcpy.CreateUniqueName(self.datasource, self.feature_store)

                arcpy.CreateFeatureclass_management(self.feature_store, 
                                                    self.datasource, 
                                                    geometry_type=self.feature_type.upper(),
                                                    spatial_reference=self.spatial_reference)

            else:
                arcpy.CreateTable_management(self.feature_store, self.datasource)
        except Exception as e:
            error_handler(e, "Error creating copy feature class", self.logger, self.DEBUG)

        self._fc_path = os.path.join(self.feature_store, self.datasource)

        if self.DEBUG:
            self.logger.debug(f"Feature Class Path: {self.feature_class_path}")

        return self._fc_path

    def add_fields(self) -> None:
        try:
            arcpy.AddFields_management(self.feature_class_path, self.fields_types)
        except Exception as e:
            error_handler(e, "Error adding fields to copy feature class", self.logger, self.DEBUG)

    def insert_records(self) -> None:
        try:
            if self.DEBUG:
                self.logger.debug("Beginning insertion of copied source records")

            insert_errors = 0
            with arcpy.da.InsertCursor(self.feature_class_path, self.cursor_fields) as cursor:
                for i in self.data_records:
                    try:
                        cursor.insertRow(i)
                    except:
                        insert_errors +=1

            if self.DEBUG:
                self.logger.debug(f"There were {str(insert_errors)} errors while copying source features.")

            if self.DEBUG:
                self.logger.debug("Finished insertion of copied source records")
        except Exception as e:
            error_handler(e, "Error inserting copied records", self.logger, self.DEBUG)

    def copy(self) -> None:
        self.get_field_types()
        self.create_feature_table()
        self.add_fields()
        self.insert_records()
