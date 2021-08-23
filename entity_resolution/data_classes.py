from __future__ import annotations

import json

from dataclasses import dataclass
from typing import Any, List, Dict, Union
from datetime import datetime

from entity_resolution.interfaces.IRecord import IRecord

EsriJSON = Dict[str, Union[float, int, str]]

@dataclass(frozen=True)
class ProcessedDataResult:
    addresses: List[Dict[str, str]]
    names: List[Dict[str, str]]
    phones: List[Dict[str, str]]
    records: List[Dict[str, str]]
    resolved_entities: List[Dict[str, str]]
    related_entities: List[Dict[str, str]]

    def to_dict(self) -> Dict[str, List[Dict[str, str]]]:
        return {
            "addresses": self.addresses,
            "names": self.names,
            "phones": self.phones,
            "records": self.records,
            "resolved_entities": self.resolved_entities,
            "related_entities": self.related_entities
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

@dataclass(frozen=True, order=True)
class EntityRecord(IRecord):
    entity_id: int
    entity_name: str
    records_count: int
    data_sources: int

    def to_dict(self) -> Dict[str, str | int]:
        return {
            "entity_id": self.entity_id,
            "entity_name": self.entity_name,
            "records_count": self.records_count,
            "data_sources": self.data_sources
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_list(self) -> List[str | int]:
        return [
            self.entity_id,
            self.entity_name,
            self.records_count,
            self.data_sources,
        ]

@dataclass(frozen=True, order=True)
class RecordsRecord(IRecord):
    entity_id: int
    data_source: str
    record_id: str
    entity_type: str
    entity_desc: str
    last_seen: datetime

    def to_dict(self) -> Dict[str, int | str | datetime]:
        return {
            "entity_id": self.entity_id,
            "data_source": self.data_source,
            "record_id": self.record_id,
            "entity_type": self.entity_type,
            "entity_desc": self.entity_desc,
            "last_seen": self.last_seen
        }

    def to_json(self) -> str:
        return json.dumps({
            "entity_id": self.entity_id,
            "data_source": self.data_source,
            "record_id": self.record_id,
            "entity_type": self.entity_type,
            "entity_desc": self.entity_desc,
            "last_seen": str(self.last_seen)
        })

    def to_list(self) -> List[int | str | datetime]:
        return [
            self.entity_id,
            self.data_source,
            self.record_id,
            self.entity_type,
            self.entity_desc,
            self.last_seen
        ]

@dataclass(frozen=True, order=True)
class RelatedRecord(IRecord):
    source_entity_id: int
    target_entity_id: int
    match_level_code: str
    match_key: str

    def to_dict(self) -> Dict[str, int | str]:
        return {
            "source_entity_id": self.source_entity_id,
            "target_entity_id": self.target_entity_id,
            "match_level_code": self.match_level_code,
            "match_key": self.match_key
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_list(self) -> List[int | str]:
        return [
            self.source_entity_id,
            self.target_entity_id,
            self.match_level_code,
            self.match_key
        ]

@dataclass(frozen=True, order=True)
class ShapeRecord(IRecord):
    geometry: EsriJSON
    record_id: str

    def to_dict(self) -> Dict[str, str | EsriJSON]:
        return {
            "geometry": self.geometry,
            "record_id": self.record_id
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def to_list(self) -> List[str | EsriJSON]:
        return [
            self.geometry,
            self.record_id,
        ]