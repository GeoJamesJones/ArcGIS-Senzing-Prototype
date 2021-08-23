from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import List

class IAddRecordsBuilder(metaclass=ABCMeta):

    @abstractmethod
    def source_table(self, table_path: str) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def entity_store(self, entity_store_path: str) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def feature_store(self, feature_store_path) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def entity_type(self, entity_type: str) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def name_fields(self, name_type: str, name_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def alias_fields(self, alias_type: str, alias_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def address_fields(self, address_type: str, address_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def alternate_address_fields(self, address_type: str, address_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def phone_fields(self, phone_type: str, phone_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def alternate_phone_fields(self, phone_type: str, phone_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def identifier_fields(self, identifier_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def digital_identifier_fields(self, digital_identifier_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def group_association_fields(self, group_association_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def physical_characteristics(self, physical_characteristic_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def other_attributes(self, other_attribute_fields: List[str]) -> IAddRecordsBuilder:
        ...

    @abstractmethod
    def load(self) -> int:
        ...