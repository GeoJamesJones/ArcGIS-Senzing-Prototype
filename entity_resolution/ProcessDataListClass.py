from __future__ import annotations

import arcpy

from typing import List, Dict
from entity_resolution import ProcessedDataResult

class ProcessDataList:
    def __init__(self, data_list: List[Dict[str, str | List[str]]]) -> None:
        self.data_list = data_list
        
        return

    def process_export(self) -> ProcessedDataResult:
        from copy import deepcopy
        
        addresses = []
        names = []
        phones = []
        records = []
        resolved_entities = []
        related_entities_list = []

        num_items = len(self.data_list)

        for k in self.data_list:
            k_copy = deepcopy(k)
            
            try:
                del k_copy['RESOLVED_ENTITY']['FEATURES']
                del k_copy['RESOLVED_ENTITY']['RECORDS']
                del k_copy['RELATED_ENTITIES']
            except TypeError:
                if num_items > 1:
                    break
                else:
                    arcpy.AddWarning(arcpy.GetIDMessage(117))
                    result = ProcessedDataResult(addresses=addresses,
                                                 names=names,
                                                 phones=phones,
                                                 records=records,
                                                 resolved_entities=resolved_entities,
                                                 related_entities=related_entities_list)

                    return result
            
            resolved_entities.append(k_copy.get('RESOLVED_ENTITY'))
            
            resolved_entity = k.get('RESOLVED_ENTITY')
            related_entities = k.get('RELATED_ENTITIES')
            
            entity_id = resolved_entity.get('ENTITY_ID')
            
            resolved_entity_features = resolved_entity.get('FEATURES')
            
            address = resolved_entity_features.get("ADDRESS")
            if address:
                for a in address:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    addresses.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            name = resolved_entity_features.get("NAME")
            if name:
                for a in name:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    names.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            phone = resolved_entity_features.get("PHONE")
            if phone:
                for a in phone:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    phones.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            resolved_entity_records = resolved_entity.get('RECORDS')
            
            for record in resolved_entity_records:
                record['ENTITY_ID'] = entity_id
                records.append(record)

            for related in related_entities:
                related['SOURCE_ENTITY_ID'] = entity_id
                related_entities_list.append(related)

        result = ProcessedDataResult(addresses=addresses,
                                    names=names,
                                    phones=phones,
                                    records=records,
                                    resolved_entities=resolved_entities,
                                    related_entities=related_entities_list)
        
        return result

    def process_search(self) -> ProcessedDataResult:
        from copy import deepcopy
        
        addresses = []
        names = []
        phones = []
        records = []
        resolved_entities = []
        related_entities_list = []

        num_items = len(self.data_list)

        for k in self.data_list:
            k_copy = deepcopy(k)

            arcpy.AddMessage(k_copy)
            
            try:
                del k_copy['RESOLVED_ENTITY']['FEATURES']
                del k_copy['RESOLVED_ENTITY']['RECORDS']
                del k_copy['RELATED_ENTITIES']
            except TypeError:
                if num_items > 1:
                    break
                else:
                    arcpy.AddWarning(arcpy.GetIDMessage(117))
                    result = ProcessedDataResult(addresses=addresses,
                                                 names=names,
                                                 phones=phones,
                                                 records=records,
                                                 resolved_entities=resolved_entities,
                                                 related_entities=related_entities_list)

                    return result
            
            resolved_entities.append(k_copy.get('RESOLVED_ENTITY'))
            
            resolved_entity = k.get('RESOLVED_ENTITY')
            related_entities = k.get('RELATED_ENTITIES')
            
            related_entities_list.append(related_entities)
            
            entity_id = resolved_entity.get('ENTITY_ID')
            
            resolved_entity_features = resolved_entity.get('FEATURES')
            
            address = resolved_entity_features.get("ADDRESS")
            if address:
                for a in address:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    addresses.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            name = resolved_entity_features.get("NAME")
            if name:
                for a in name:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    names.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            phone = resolved_entity_features.get("PHONE")
            if phone:
                for a in phone:
                    feat = a.get('FEAT_DESC')
                    lib_feat_id = a.get('LIB_FEAT_ID')
                    u_type_code = a.get('U_TYPE_CODE')
                    
                    phones.append({
                        "ENTITY_ID": entity_id,
                        "FEAT_DESC": feat,
                        "LIB_FEAT_ID": lib_feat_id,
                        "U_TYPE_CODE": u_type_code
                    })
                    
            resolved_entity_records = resolved_entity.get('RECORDS')
            
            for record in resolved_entity_records:
                record['ENTITY_ID'] = entity_id
                records.append(record)

        result = ProcessedDataResult(addresses=addresses,
                                    names=names,
                                    phones=phones,
                                    records=records,
                                    resolved_entities=resolved_entities,
                                    related_entities=related_entities_list)
        
        return result