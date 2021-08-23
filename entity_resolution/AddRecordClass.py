from __future__ import annotations

import arcpy
import os
import json
import time

from typing import Any, List, Dict
from datetime import datetime

from entity_resolution import EntityResolution, SenzingConfig, Entity
from entity_resolution.data_classes import EntityRecord, \
                                           RecordsRecord, \
                                           RelatedRecord, \
                                           ShapeRecord, \
                                           EsriJSON
from entity_resolution.utils import Logger, \
                                    error_handler, \
                                    InsertRecords, \
                                    RELATED_RECORD_FIELDS, \
                                    SHAPE_RECORD_FIELDS, \
                                    CopySourceData

import senzing.g2.sdk.python.G2Exception as G2Exception
from senzing import G2Engine

class AddRecords:
    def __init__(self) -> None:

        self._in_table: str 
        self._entity_store: str 
        self._entity_type: str 
        self._feature_store: str 
        
        self._name_type: str 
        self._name_fields: List[str]
        self._alias_type: str 
        self._alias_fields: List[str] 
        
        self._address_type: str 
        self._address_fields: List[str] 
        self._alternate_address_type: str 
        self._alt_address_fields: List[str] 

        self._phone_type: str 
        self._phone_fields: List[str] 
        self._alt_phone_type: str 
        self._alt_phone_fields: List[str] 

        self._identifier_fields: List[str] 

        self._digital_identifier_fields: List[str] 

        self._group_association_fields: List[str] 

        self._physical_characteristics: List[str] 

        self._other_attributes: List[str] 

        self.DEBUG: bool = True

        if self.DEBUG:
            self.log_level = "DEBUG"
            self.logger = Logger(__name__ , self.log_level)
        else:
            self.log_level = 'WARN'
            self.logger = Logger(__name__)

        self.g2_engine_flags = G2Engine.G2_EXPORT_DEFAULT_FLAGS

        return

    @property
    def in_table(self) -> str:
        return self._in_table
    @in_table.setter
    def in_table(self, table_path: str) -> None:
        self._in_table = table_path

    @property
    def feature_store(self) -> str:
        return self._feature_store
    @feature_store.setter
    def feature_store(self, feature_store_path: str) -> None:
        self._feature_store = feature_store_path

    @property
    def entity_store(self) -> str:
        return self._entity_store
    @entity_store.setter
    def entity_store(self, entity_store_path: str) -> None:
        self._entity_store = entity_store_path

    @property
    def entity_type(self) -> str:
        return self._entity_type
    @entity_type.setter
    def entity_type(self, entity_type: str) -> None:
        self._entity_type = entity_type

    @property
    def name_type(self) -> str:
        return self._name_type
    @name_type.setter
    def name_type(self, name_type: str) -> None:
        self._name_type = name_type

    @property
    def name_fields(self) -> List[str]:
        return self._name_fields
    @name_fields.setter
    def name_fields(self, name_fields: List[str]) -> None:
        self._name_fields = name_fields

    @property
    def alias_type(self) -> str:
        return self._alias_type
    @alias_type.setter
    def alias_type(self, alias_type: str) -> None:
        self._alias_type = alias_type

    @property
    def alias_fields(self) -> List[str]:
        return self._alias_fields
    @alias_fields.setter
    def alias_fields(self, alias_fields: List[str]) -> None:
        self._alias_fields = alias_fields

    @property
    def address_type(self) -> str:
        return self._address_type
    @address_type.setter
    def address_type(self, address_type: str) -> None:
        self._address_type = address_type

    @property
    def address_fields(self) -> List[str]:
        return self._address_fields
    @address_fields.setter
    def address_fields(self, address_fields: List[str]) -> None:
        self._address_fields = address_fields  

    @property
    def alternate_address_type(self) -> str:
        return self._alternate_address_type
    @alternate_address_type.setter
    def alternate_address_type(self, alternate_address_type: str) -> None:
        self._alternate_address_type = alternate_address_type

    @property
    def alt_address_fields(self) -> List[str]:
        return self._alt_address_fields
    @alt_address_fields.setter
    def alt_address_fields(self, alt_address_fields: List[str]) -> None:
        self._alt_address_fields = alt_address_fields

    @property
    def phone_type(self) -> str:
        return self._phone_type
    @phone_type.setter
    def phone_type(self, phone_type: str) -> None:
        self._phone_type = phone_type

    @property
    def phone_fields(self) -> List[str]:
        return self._phone_fields
    @phone_fields.setter
    def phone_fields(self, phone_fields: List[str]) -> None:
        self._phone_fields = phone_fields  

    @property
    def alternate_phone_type(self) -> str:
        return self._alternate_phone_type
    @alternate_phone_type.setter
    def alternate_phone_type(self, alternate_phone_type: str) -> None:
        self._alternate_phone_type = alternate_phone_type

    @property
    def alt_phone_fields(self) -> List[str]:
        return self._alt_phone_fields
    @alt_phone_fields.setter
    def alt_phone_fields(self, alt_phone_fields: List[str]) -> None:
        self._alt_phone_fields = alt_phone_fields

    @property
    def identifier_fields(self) -> List[str]:
        return self._identifier_fields
    @identifier_fields.setter
    def identifier_fields(self, identifier_fields: List[str]) -> None:
        self._identifier_fields = identifier_fields

    @property
    def digital_identifier_fields(self) -> List[str]:
        return self._digital_identifier_fields
    @digital_identifier_fields.setter
    def digital_identifier_fields(self, digital_identifier_fields: List[str]) -> None:
        self._digital_identifier_fields = digital_identifier_fields

    @property
    def group_association_fields(self) -> List[str]:
        return self._group_association_fields
    @group_association_fields.setter
    def group_association_fields(self, group_association_fields: List[str]) -> None:
        self._group_association_fields = group_association_fields

    @property
    def physical_characteristics(self) -> List[str]:
        return self._physical_characteristics
    @physical_characteristics.setter
    def physical_characteristics(self, physical_characteristics: List[str]) -> None:
        self._physical_characteristics = physical_characteristics

    @property
    def other_attributes(self) -> List[str]:
        return self._other_attributes
    @other_attributes.setter
    def other_attributes(self, other_attributes: List[str]) -> None:
        self._other_attributes = other_attributes

    @property
    def entities(self) -> str:
        return self._entities

    @property
    def records(self) -> str:
        return self._records

    @property  
    def related(self) -> str:
        return self._related

    def update_field_lists(self, list_obj: List[str]) -> None:
        for i,j in enumerate(list_obj):
            if j[0].value not in self.cursor_fields:
                self.cursor_fields.append(j[0].value)
                self.entity_fields.append(j[1])

    def adjust_alias_fields(self, list_obj: List[str], alias: str) -> None:
        adjusted_list = []
        for i in list_obj:
            adjusted_list.append(f"{alias}_{i}")

        list_obj = adjusted_list

    def prepare_data(self) -> None:
        if self.DEBUG:
            self.logger.debug("Creating attribute dictionaries")
        
        self.cursor_fields: List[str] = []
        self.entity_fields: List[str] = []

        self.attribute_dicts: List[Dict[str, List[str] | str]] = []

        if self.name_fields:
            self.update_field_lists(self.name_fields)
            self.create_attribute_dict(feature_type=EntityResolution.NAME_TYPE.value,
                                       attr_type=self.name_type,
                                       list_obj=self.name_fields)
        if self.alias_fields:
            self.adjust_alias_fields(self.alias_fields, self.alias_type)
            self.update_field_lists(self.alias_fields)
            self.create_attribute_dict(feature_type=EntityResolution.NAME_TYPE.value,
                                       attr_type=EntityResolution.AKA.value,
                                       list_obj=self.alias_fields)
        if self.address_fields:
            self.update_field_lists(self.address_fields)
            self.create_attribute_dict(feature_type=EntityResolution.ADDR_TYPE.value,
                                       attr_type=self.address_type,
                                       list_obj=self.address_fields)
        if self.alt_address_fields:
            self.adjust_alias_fields(self.alt_address_fields, self.alternate_address_type)
            self.update_field_lists(self.alt_address_fields)
            self.create_attribute_dict(feature_type=EntityResolution.ADDR_TYPE.value,
                                       attr_type=self.alternate_address_type,
                                       list_obj=self.alt_address_fields)
        if self.phone_fields:
            self.update_field_lists(self.phone_fields)
            self.create_attribute_dict(feature_type=EntityResolution.PHONE_TYPE.value,
                                       attr_type=self.phone_type,
                                       list_obj=self.phone_fields)
        if self.alt_phone_fields:
            self.adjust_alias_fields(self.alt_phone_fields, self.alternate_phone_type)
            self.update_field_lists(self.alt_phone_fields)
            self.create_attribute_dict(feature_type=EntityResolution.PHONE_TYPE.value,
                                       attr_type=self.alternate_phone_type,
                                       list_obj=self.alt_phone_fields)
        if self.identifier_fields:
            self.update_field_lists(self.identifier_fields)
        if self.digital_identifier_fields:
            self.update_field_lists(self.digital_identifier_fields)
        if self.group_association_fields:
            self.update_field_lists(self.group_association_fields)
        if self.physical_characteristics:
            self.update_field_lists(self.physical_characteristics)
        if self.other_attributes:
            self.update_field_lists(self.other_attributes)

        self._entities = os.path.join(self.feature_store, "resolved_entities")
        self._related = os.path.join(self.feature_store, "related_entities")
        self._records = os.path.join(self.feature_store, "records")
    
        if self.d.datasetType == "FeatureClass":          
            self.cursor_fields.append("SHAPE@JSON")
            self.entity_fields.append("SHAPE")

            self.source_sr = self.d.spatialReference
            self.shape_type = self.d.shapeType

            if self.d.shapeType == 'Point':
                self.ADD_FEATURES = True
                self.fc = os.path.join(self.feature_store, 'Entity_Points')

            elif self.d.shapeType == 'Polygon':
                self.ADD_FEATURES = True
                self.fc = os.path.join(self.feature_store, 'Entity_Polygons')

            elif self.d.shapeType == 'Polyline':
                self.ADD_FEATURES = True
                self.fc = os.path.join(self.feature_store, 'Entity_Polylines')

            else:
                self.ADD_FEATURES = False

        else:
            self.ADD_FEATURES = False
            self.source_sr = None
            self.shape_type = 'Table'

        if self.DEBUG:
            self.logger.debug(f"Cursor Fields: {self.cursor_fields}")
            self.logger.debug(f"Entity Fields: {self.entity_fields}")

    def create_attribute_dict(self, feature_type: str, attr_type:str, list_obj: List[str]) -> None:

        attr_dict = {
            feature_type: attr_type,
            "entity_fields": [j[1] for i,j in enumerate(list_obj)],
            "source_fields": [j[0].value for i,j in enumerate(list_obj)]
        }

        if attr_dict not in self.attribute_dicts:
            self.attribute_dicts.append(attr_dict)

    def process_entity_response(self, response_obj: bytearray) -> None:
        try:
            response_json = json.loads(response_obj)

            resolved_entity = response_json['RESOLVED_ENTITY']
            records = response_json['RESOLVED_ENTITY']['RECORDS']
            related_entities = response_json['RELATED_ENTITIES']

            source_entity_id = resolved_entity['ENTITY_ID']

            entity_row = EntityRecord(
                entity_id=resolved_entity['ENTITY_ID'], 
                entity_name=resolved_entity['ENTITY_NAME'],
                records_count=len(records),
                data_sources=len(set(i["DATA_SOURCE"] for i in records))
            )
            
            self.entities_dict[resolved_entity['ENTITY_ID']] = entity_row

            if records:
                for record in records:
                    record_id = record["RECORD_ID"]
                    self.record_ids.add(record_id) 
                    iRow = RecordsRecord(
                        entity_id= source_entity_id,
                        data_source=record["DATA_SOURCE"],
                        record_id=record_id,
                        entity_type=record['ENTITY_TYPE'],
                        entity_desc=record["ENTITY_DESC"],
                        last_seen=datetime.now()
                    )
                
                    self.records_dict[record_id] = iRow

            if related_entities:
                for item in related_entities:
                    iRow = RelatedRecord(
                        source_entity_id,
                        item["ENTITY_ID"],
                        item["MATCH_LEVEL_CODE"],
                        item["MATCH_KEY"]
                    )
                    
                    self.related_list.append(iRow)

        except Exception as e:
            error_handler(e, "Error processing entity response object", self.logger, self.DEBUG)

    def replicate(self, response: Dict[str, str]) -> None:

        try:
            if len(response['AFFECTED_ENTITIES']) == 1: 
                entity_id = response['AFFECTED_ENTITIES'][0]['ENTITY_ID']
            else:
                entity_id = 0

            self.record_ids.add(response["RECORD_ID"])

            shape: EsriJSON = response['SHAPE']

            self.shapes.append(ShapeRecord(shape, response["RECORD_ID"]))

            for e in response["AFFECTED_ENTITIES"]:
                response_bytearray = bytearray()
                self.senzing_config.g2_engine.getEntityByEntityIDV2(e['ENTITY_ID'], self.g2_engine_flags, response_bytearray)

                self.entity_ids.add(e['ENTITY_ID'])

                self.process_entity_response(response_bytearray)
        except Exception as e:
            error_handler(e, "Error replicating data", self.logger, self.DEBUG)

    def get_table_datasource_code(self) -> str:
        datasource_code = arcpy.ValidateTableName(self.baseName, self.feature_store).upper()

        self.senzing_config.CONFIG_COMMENT = f"ArcGISProIntel data source {datasource_code} added at {time.time()}"

        return datasource_code

    def add_records(self, datasource_code: str) -> None:
        try:
            record_id = None
            load_id = None

            if self.DEBUG:
                self.logger.debug(f"Data Source Code: {datasource_code}")
                self.logger.debug("Adding records")

            count = 0
            invalid_records = 0
            with arcpy.da.SearchCursor(self.in_table, self.cursor_fields) as cursor:
                for row in cursor:
                    try:
                        shape = row[len(row) - 1]

                        

                        ent = Entity(self.entity_fields, row, self.cursor_fields, self.attribute_dicts, self.entity_type)

                        g2_engine_flags = G2Engine.G2_EXPORT_DEFAULT_FLAGS
                        response_bytearray = bytearray()
                        self.senzing_config.g2_engine.addRecordWithInfo(datasource_code,
                                                                        record_id,
                                                                        ent.to_json(),
                                                                        response_bytearray,
                                                                        load_id,
                                                                        g2_engine_flags)
                    
                        response_json = json.loads(response_bytearray)
                        response_json['SHAPE'] = shape

                        row_list = list(row)
                        row_list.append(response_json["RECORD_ID"])
                        self.data_records.append(row_list)
                        
                        self.replicate(response_json)

                        count +=1

                    except G2Exception.G2ModuleGenericException as err:
                        self.logger.warning(f'ERROR engine add: {self.senzing_config.g2_engine.getLastException()}')
                        invalid_records +=1

            if self.DEBUG:
                self.logger.debug(f"Added {str(count)} records to {self.entity_store}")
                self.logger.debug(f"Encountered {str(invalid_records)} entity errors while processing {self.in_table}")
        
        except Exception as e:
            error_handler(e, "Error resolving entities", self.logger, self.DEBUG)

    def execute(self) -> int:

        arcpy.AddMessage("Initializing Entity Resolution engine")
        self.senzing_config = SenzingConfig(entity_store=self.entity_store)
        self.entity_ids = set()
        self.record_ids = set()

        self.d = arcpy.Describe(self.in_table)
        self.baseName = self.d.name
        
        self.entities_dict: Dict[int, EntityRecord] = {}
        self.records_dict: Dict[str, RecordsRecord] = {}
        self.related_list: List[RelatedRecord] = []
        self.shapes: List[ShapeRecord] = []
        self.data_records: List[List[Any]] = []

        self.prepare_data()

        data_source_code = self.get_table_datasource_code()

        self.senzing_config.configure_g2_cfg_mgr()
        self.senzing_config.configure_g2_config()

        config_id = self.senzing_config.check_for_default_config()

        if not config_id:
            self.logger.warning('No default config exists in the Senzing repository, adding default template configuration')
            active_config_id = self.senzing_config.add_default_config()
        else:
            arcpy.AddMessage(f'\nDefault config exists in the Senzing repository: {config_id}')
            active_config_id = config_id

        self.senzing_config.configure_g2_engine(config_id=active_config_id, prime_engine=False)

        if not self.senzing_config.data_source_exists(active_config_id, data_source_code):
            active_config_id = self.senzing_config.add_data_source(active_config_id, data_source_code)
            self.senzing_config.g2_engine.reinitV2(active_config_id)

        
        arcpy.AddMessage("Resolving records")
        self.add_records(data_source_code)

        arcpy.AddMessage("Copying source records")

        csd = CopySourceData(self.cursor_fields, 
                                self.data_records, 
                                self.in_table,
                                self.feature_store,
                                self.shape_type,
                                data_source_code,
                                self.source_sr,
                                self.log_level)

        csd.copy()

        

        arcpy.AddMessage("Adding records to local entity store")

        ir  = InsertRecords(debug_level=self.log_level)

        ir.insert_entity_records(entities_fc=self.entities,
                                    entity_ids=self.entity_ids,
                                    entities_dict=self.entities_dict)

        ir.insert_record_records(records_fc=self.records,
                                    record_ids=self.record_ids,
                                    records_dict=self.records_dict)

        ir.insert_records(feature_class=self.related,
                            records_list=self.related_list,
                            fields=RELATED_RECORD_FIELDS)

        if self.ADD_FEATURES:
            ir.insert_records(feature_class=self.fc,
                                records_list=self.shapes,
                                fields=SHAPE_RECORD_FIELDS)

        ir.delete_duplicate_entities(feature_class=self.entities)

        
        
        self.senzing_config.house_keeping()


        if self.DEBUG:
            self.logger.debug("Deleting helper classes")

        try:
            del ir.logger
            del csd.logger
        except Exception:
            pass

        try:
            del csd
            del ir
        except Exception:
            pass
        
        if self.DEBUG:
            self.logger.debug("Deleted helper classes")

        try:
            del self.logger
        except Exception:
            pass
