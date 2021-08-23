from __future__ import annotations
from logging import error
from typing import List

from entity_resolution.AddRecordClass import AddRecords
from entity_resolution.interfaces import IAddRecordsBuilder
from entity_resolution.utils import error_handler, Logger

class AddRecordToEntityStore(IAddRecordsBuilder):
    def __init__(self) -> None:
        self.add_records = AddRecords()
        self.DEBUG = True
        self.logger = Logger(__name__, level='DEBUG')

    def source_table(self, table_path: str) -> AddRecordToEntityStore:
        self.add_records.in_table = table_path
        return self

    def entity_store(self, entity_store_path: str) -> AddRecordToEntityStore:
        self.add_records.entity_store = entity_store_path
        return self

    def feature_store(self, feature_store_path) -> AddRecordToEntityStore:
        self.add_records.feature_store = feature_store_path
        return self

    def entity_type(self, entity_type: str) -> AddRecordToEntityStore:
        self.add_records.entity_type = entity_type
        return self
    
    def name_fields(self, name_type: str, name_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.name_type = name_type
        self.add_records.name_fields = name_fields
        return self

    def alias_fields(self, alias_type: str, alias_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.alias_type = alias_type
        self.add_records.alias_fields = alias_fields
        return self 

    def address_fields(self, address_type: str, address_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.address_type = address_type
        self.add_records.address_fields = address_fields
        return self

    def alternate_address_fields(self, address_type: str, address_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.alternate_address_type = address_type
        self.add_records.alt_address_fields = address_fields
        return self

    def phone_fields(self, phone_type: str, phone_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.phone_type = phone_type
        self.add_records.phone_fields = phone_fields
        return self

    def alternate_phone_fields(self, phone_type: str, phone_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.alternate_phone_type = phone_type
        self.add_records.alt_phone_fields = phone_fields  
        return self

    def identifier_fields(self, identifier_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.identifier_fields = identifier_fields
        return self

    def digital_identifier_fields(self, digital_identifier_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.digital_identifier_fields = digital_identifier_fields
        return self

    def group_association_fields(self, group_association_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.group_association_fields = group_association_fields
        return self

    def physical_characteristics(self, physical_characteristic_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.physical_characteristics = physical_characteristic_fields
        return self

    def other_attributes(self, other_attribute_fields: List[str]) -> AddRecordToEntityStore:
        self.add_records.other_attributes = other_attribute_fields
        return self

    def load(self) -> int:
        try:
            result = self.add_records.execute()

            if result and self.DEBUG:
                self.logger.debug("Add Records completed successfully")
            elif not result and self.DEBUG:
                self.logger.error("Add Records finished with an exit code of 1.")

            return result

        except Exception as e:
            error_handler(e, "Error in Add Records Builder class", self.logger, self.DEBUG)
        
        return 