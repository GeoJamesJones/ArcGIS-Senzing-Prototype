import os
import arcpy
import json

from entity_resolution import ERBase, SenzingConfig, ProcessDataList

import senzing.g2.sdk.python.G2Exception as G2Exception
from senzing.g2.sdk.python.G2Engine import G2Engine

class RelationshipsFromArea(ERBase):
    def __init__(self, feature_set: str, feature_store: str, entity_store: str, out_file: str) -> None:
        self.feature_set = feature_set
        self.feature_store = feature_store
        self.entity_store = entity_store
        self.out_file = out_file

    def find(self) -> None:
        from intel.utilities import create_temp_table_name

        temp_fc = create_temp_table_name("memory")

        arcpy.CopyFeatures_management(self.feature_set, temp_fc)
        
        selected_points = arcpy.SelectLayerByLocation_management(os.path.join(self.feature_store, 'main.Entity_Points'), 'INTERSECT', temp_fc)
        selected_polys = arcpy.SelectLayerByLocation_management(os.path.join(self.feature_store, 'main.Entity_Polygons'),'INTERSECT', temp_fc)
        selected_lines = arcpy.SelectLayerByLocation_management(os.path.join(self.feature_store, 'main.Entity_Polylines'), 'INTERSECT', temp_fc)

        points_entities = set(row[0] for row in arcpy.da.SearchCursor(selected_points, ['ENTITY_ID']))
        polys_entities = set(row[0] for row in arcpy.da.SearchCursor(selected_polys, ['ENTITY_ID']))
        lines_entities = set(row[0] for row in arcpy.da.SearchCursor(selected_lines, ['ENTITY_ID']))

        entities = set().union(*[points_entities, polys_entities, lines_entities])

        arcpy.AddMessage(entities)

        data = []

        g2_engine = SenzingConfig(entity_store=self.entity_store).initialize()
        g2_engine_flags = G2Engine.G2_EXPORT_DEFAULT_FLAGS

        entity_list = {
            "ENTITIES": []}

        for entity in entities:
            entity_list['ENTITIES'].append({"ENTITY_ID": entity})

        """entity_list_as_json = json.dumps(entity_list)

        response_bytearray = bytearray()

        try:
            g2_engine.findNetworkByEntityIDV2(
                entityList=entity_list_as_json,
                maxDegree=4,
                buildOutDegree=2,
                maxEntities=1000,
                flags=g2_engine_flags,
                response=response_bytearray)

        except G2Exception.G2ModuleGenericException as err:
            print(g2_engine.getLastException())"""
        
        #result = ProcessDataList(data['ENTITIES']).process_export()

        #self.create_output_tables()
        #self.add_records_to_tables(result)

        arcpy.AddMessage(json.dumps(entity_list))

        return