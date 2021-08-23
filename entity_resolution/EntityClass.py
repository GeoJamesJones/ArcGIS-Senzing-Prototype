from __future__ import annotations

import json

from typing import List, Dict

from entity_resolution import EntityResolution

class Entity:
    def __init__(self, entity_fields: List[str], 
                       data: List[str], 
                       source_fields: List[str], 
                       attr_dicts: List[Dict[str, List[str] | str]],
                       record_type: str):
        self.entity_fields = entity_fields
        self.data = data
        self.source_fields = source_fields
        self.attr_dicts = attr_dicts
        self.record_type = record_type

        skip_values = [
            EntityResolution.NAME_FULL.value,
            EntityResolution.NAME_ORG.value,
            EntityResolution.NAME_LAST.value,
            EntityResolution.NAME_FIRST.value,
            EntityResolution.NAME_MIDDLE.value,
            EntityResolution.NAME_PREFIX.value,
            EntityResolution.NAME_SUFFIX.value,
            EntityResolution.ADDR_FULL.value,
            EntityResolution.ADDR_LINE1.value,
            EntityResolution.ADDR_LINE2.value,
            EntityResolution.ADDR_LINE3.value,
            EntityResolution.ADDR_LINE4.value,
            EntityResolution.ADDR_LINE5.value,
            EntityResolution.ADDR_LINE6.value,
            EntityResolution.ADDR_CITY.value,
            EntityResolution.ADDR_STATE.value,
            EntityResolution.ADDR_ZIP.value,
            EntityResolution.ADDR_COUNTRY.value,
            EntityResolution.ADDR_FD.value,
            EntityResolution.ADDR_TD.value,
            EntityResolution.PHONE_NUM.value,
            EntityResolution.PHONE_FD.value,
            EntityResolution.PHONE_TD.value,
        ]

        field_map = {}

        for i,j in enumerate(self.source_fields):
            field_map[j] = i

        self.data_dict = {key:str(value) for (key,value) in zip(self.entity_fields, self.data) if key not in skip_values}

        self.data_dict["RECORD_TYPE"] = self.record_type

        for d in attr_dicts:
            
            if EntityResolution.NAME_TYPE.value in d.keys():
                name = {EntityResolution.NAME_TYPE.value: d[EntityResolution.NAME_TYPE.value]}

                data_index = []
                
                for i in d['source_fields']:
                    data_index.append(field_map[i])

                for x in data_index:
                    name[entity_fields[x]] = str(data[x])

                if 'NAME_LIST' not in self.data_dict.keys():
                    self.data_dict['NAME_LIST'] = []
                    self.data_dict['NAME_LIST'].append(name)
                else:
                    self.data_dict['NAME_LIST'].append(name)

            if EntityResolution.ADDR_TYPE.value in d.keys():
                addr = {EntityResolution.ADDR_TYPE.value: d[EntityResolution.ADDR_TYPE.value]}

                data_index = []
                
                for i in d['source_fields']:
                    data_index.append(field_map[i])

                for x in data_index:
                    addr[entity_fields[x]] = str(data[x])

                if 'ADDR_LIST' not in self.data_dict.keys():
                    self.data_dict['ADDR_LIST'] = []
                    self.data_dict['ADDR_LIST'].append(addr)
                else:
                    self.data_dict['ADDR_LIST'].append(addr)

            if EntityResolution.PHONE_TYPE.value in d.keys():
                phone = {EntityResolution.PHONE_TYPE.value: d[EntityResolution.PHONE_TYPE.value]}

                data_index = []
                
                for i in d['source_fields']:
                    data_index.append(field_map[i])

                for x in data_index:
                    phone[entity_fields[x]] = str(data[x])

                if 'PHONE_LIST' not in self.data_dict.keys():
                    self.data_dict['PHONE_LIST'] = []
                    self.data_dict['PHONE_LIST'].append(phone)
                else:
                    self.data_dict['PHONE_LIST'].append(phone)

    def to_json(self) -> str:
        return json.dumps(self.data_dict)
