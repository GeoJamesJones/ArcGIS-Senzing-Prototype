from __future__ import annotations

import arcpy

from typing import Set, Dict, List
from logging import Logger

from entity_resolution.data_classes import EntityRecord, RecordsRecord, RelatedRecord, ShapeRecord

from entity_resolution.utils.utilities import error_handler, \
                                              ENTITY_RECORD_FIELDS,\
                                              RECORDS_RECORD_FIELDS


class InsertRecords:

    def __init__(self, debug_level: str = 'WARN') -> None:
        self.logger = Logger(__name__, debug_level)

        if debug_level == 'DEBUG':
            self.DEBUG = True
        return

    
    def insert_entity_records(self,
                              entities_fc: str, 
                              entity_ids: Set[int], 
                              entities_dict: Dict[int, EntityRecord]) -> None:
        try:
            existing_entities = [row[0] for row in arcpy.da.SearchCursor(entities_fc, ['ENTITY_ID'])]

            entities_to_add = [i for i in entity_ids if i not in existing_entities]
            entities_to_update = [i for i in entity_ids if i in existing_entities]
            where = f'ENTITY_ID IN {tuple(entities_to_update)}'

            if self.DEBUG:
                self.logger.debug(f"Entities to add: {str(entities_to_add)}")
                self.logger.debug(f"Entities to update: {str(entities_to_update)}")
                self.logger.debug(f"Where clause: {where}")

            if entities_to_update:
                with arcpy.da.UpdateCursor(entities_fc, ENTITY_RECORD_FIELDS, where_clause=where) as cursor:
                    for row in cursor:
                        data = entities_dict[row[0]].to_list()
                        cursor.updateRow(data)
            
            if entities_to_add:
                with arcpy.da.InsertCursor(entities_fc, ENTITY_RECORD_FIELDS) as cursor:
                    for k,v in entities_dict.items():
                        cursor.insertRow(v.to_list())
        except Exception as e:
            error_handler(e, "Error adding entity records", self.logger, self.DEBUG)

    def insert_record_records(self,
                              records_fc: str,
                              record_ids: Set[str],
                              records_dict: Dict[str, RecordsRecord]) -> None:
        try:
            existing_records = [row[0] for row in arcpy.da.SearchCursor(records_fc, ['RECORD_ID'])]
            records_to_add = [i for i in record_ids if i not in existing_records]
            records_to_update = [i for i in record_ids if i in existing_records]
            where = f'RECORD_ID IN {tuple(records_to_update)}'

            if self.DEBUG:
                self.logger.debug(f"Records to add: {str(records_to_add)}")
                self.logger.debug(f"Records to update: {str(records_to_update)}")
                self.logger.debug(f"Where clause: {where}")

            if records_to_update:
                with arcpy.da.UpdateCursor(records_fc, RECORDS_RECORD_FIELDS, where_clause=where) as cursor:
                    for row in cursor:
                        data = records_dict[row[2]].to_list()
                        cursor.updateRow(data)
            
            if records_to_add:
                with arcpy.da.InsertCursor(records_fc, RECORDS_RECORD_FIELDS) as cursor:
                    for k,v in records_dict.items():
                        cursor.insertRow(v.to_list())

        except Exception as e:
            error_handler(e, "Error adding records", self.logger, self.DEBUG)

    def insert_records(self, 
                      feature_class: str, 
                      records_list: List[ShapeRecord | RelatedRecord],
                      fields: List[str]) -> None:
        try: 
            insert_errors = 0
            with arcpy.da.InsertCursor(feature_class, fields) as cursor:
                for row in records_list:
                    try:
                        cursor.insertRow(row.to_list())
                    except ValueError:
                        insert_errors +=1
                    except RuntimeError:
                        pass

            if self.DEBUG:
                self.logger.debug(f"There were {str(insert_errors)} errors while inserting records.")

        except Exception as e:
            error_handler(e, "Error adding related records", self.logger, self.DEBUG)

    def delete_duplicate_entities(self,
                                  feature_class: str) -> None:

        entity_ids = set()

        try:
            with arcpy.da.UpdateCursor(feature_class, ['ENTITY_ID']) as cursor:
                for row in cursor:
                    if row[0] in entity_ids:
                        cursor.deleteRow()
                    else:
                        entity_ids.add(row[0])
        
        except Exception as e:
            error_handler(e, "Error adding related records", self.logger, self.DEBUG)