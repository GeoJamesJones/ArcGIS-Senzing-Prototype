import arcpy
import os

from entity_resolution import SenzingConfig

class CreateEntityStore:
    def __init__(self, out_path: str, out_name: str) -> None:
        self.out_path = out_path
        self.out_name = out_name

        self.les = os.path.join(out_path, out_name + ".geodatabase")

        self.entity_fields = [
            ["ENTITY_ID", 'Long', 'Entity ID'],
            ["ENTITY_NAME", 'TEXT', '', 255],
            ["RECORDS_COUNT", "Long", "Records Count"],
            ["DATA_SOURCES", "Long", "Data Sources"]
        ]

        self.record_fields = [
            ["ENTITY_ID", 'Long', 'Entity ID'],
            ["DATA_SOURCE", 'TEXT', '', 255],
            ['RECORD_ID', 'TEXT', '', 255],
            ['ENTITY_TYPE', 'TEXT', '', 255],
            ["ENTITY_DESC", 'TEXT', '', 255],
            ["LAST_SEEN_DT", "Date", "Last Seen"]
        ]

        self.related_fields = [
            ["SOURCE_ENTITY_ID", 'Long', 'Source Entity ID'],
            ["TARGET_ENTITY_ID", 'Long', 'Target Entity ID'],
            ["MATCH_LEVEL_CODE", 'TEXT', '', 255],
            ["MATCH_KEY", 'TEXT', '', 255],
        ]

    def create(self):
        arcpy.AddMessage("Creating Local Entity Store")
        
        arcpy.CreateFileGDB_management(self.out_path, self.out_name)
        arcpy.CreateMobileGDB_management(self.out_path, self.out_name)

        arcpy.AddMessage("Creating Feature Classes")

        sr = arcpy.SpatialReference("WGS 1984")

        arcpy.management.CreateFeatureclass(self.les, 
                                            "Entity_Points", 
                                            "POINT", 
                                            None, 
                                            "DISABLED", 
                                            "DISABLED", 
                                            sr, 
                                            '', 
                                            0, 
                                            0, 
                                            0, 
                                            '')

        arcpy.management.CreateFeatureclass(self.les, 
                                            "Entity_Polygons", 
                                            "POLYGON", 
                                            None, 
                                            "DISABLED", 
                                            "DISABLED", 
                                            sr, 
                                            '', 
                                            0, 
                                            0, 
                                            0, 
                                            '')

        arcpy.management.CreateFeatureclass(self.les, 
                                            "Entity_Polylines", 
                                            "POLYLINE", 
                                            None, 
                                            "DISABLED", 
                                            "DISABLED", 
                                            sr, 
                                            '', 
                                            0, 
                                            0, 
                                            0, 
                                            '')

        arcpy.management.AddFields(os.path.join(self.les, 'Entity_Points'), "RECORD_ID TEXT # 255 # #")
        arcpy.management.AddFields(os.path.join(self.les, 'Entity_Polygons'), "RECORD_ID TEXT # 255 # #")
        arcpy.management.AddFields(os.path.join(self.les, 'Entity_Polylines'), "RECORD_ID TEXT # 255 # #")

        arcpy.management.CreateTable(self.les, "resolved_entities", "", '', '')
        arcpy.management.AddFields(os.path.join(self.les, "resolved_entities"), self.entity_fields)
    

        arcpy.management.CreateTable(self.les, "records", "", '', '')
        arcpy.management.AddFields(os.path.join(self.les, "records"), self.record_fields)

        arcpy.management.CreateTable(self.les, "related_entities", "", '', '')
        arcpy.management.AddFields(os.path.join(self.les, "related_entities"), self.related_fields)
        
        arcpy.AddMessage("Creating Senzing Tables")
        
        SenzingConfig(entity_store=self.les).configure_entity_store()
        
        return