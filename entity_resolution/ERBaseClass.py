from __future__ import annotations

import arcpy
import os

from entity_resolution import ProcessedDataResult

class ERBase(object):
    def __init__(self) -> None:
        self.out_file: str
        
        return

    def create_output_tables(self) -> None:
        self.out_addresses = os.path.join(self.out_file, 'addresses')
        self.out_names = os.path.join(self.out_file, 'names')
        self.out_phone_numbers = os.path.join(self.out_file, 'phone_numbers')
        self.out_resolved_entities = os.path.join(self.out_file, 'resolved_entities')
        self.out_records = os.path.join(self.out_file, 'records')
        self.out_related = os.path.join(self.out_file, "related_entities")

        arcpy.AddMessage("Adding tables")

        detail_fields = [
            ["ENTITY_ID", 'Long', 'Entity ID'],
            ["FEAT_DESC", 'TEXT', 'Feature Description', 255],
            ["LIB_FEAT_ID", 'TEXT', 'Library Feature ID', 255],
            ["U_TYPE_CODE", 'TEXT', 'U Type Code', 255]
        ]

        entity_fields = [
            ["ENTITY_ID", 'Long', 'Entity ID'],
            ["LENS_CODE", 'TEXT', 'Lens Code', 255],
            ["ENTITY_NAME", 'TEXT', '', 255],
        ]

        record_fields = [
            ["DATA_SOURCE", 'TEXT', '', 255],
            ['RECORD_ID', 'TEXT', '', 255],
            ['ENTITY_TYPE', 'TEXT', '', 255],
            ["INTERNAL_ID", 'Long',],
            ["ENTITY_KEY", 'TEXT', '', 255],
            ["ENTITY_DESC", 'TEXT', '', 255],
            ["MATCH_KEY", 'TEXT', '', 255],
            ["MATCH_LEVEL", 'Long',],
            ["MATCH_LEVEL_CODE", 'TEXT', '', 255],
            ["MATCH_SCORE", 'Long',],
            ["ERRULE_CODE", 'TEXT', '', 255],
            ["REF_SCORE", 'Long',],
            ["LAST_SEEN_DT", 'TEXT', '', 255],
            ["ENTITY_ID", 'Long', 'Entity ID']
        ]

        related_fields = [
            ["TARGET_ENTITY_ID", 'Long', 'Target Entity ID'],
            ['LENS_CODE', 'TEXT', '', 255],
            ["MATCH_LEVEL", 'Long',],
            ["MATCH_LEVEL_CODE", 'TEXT', '', 255],
            ["MATCH_KEY", 'TEXT', '', 255],
            ["MATCH_SCORE", 'Long',],
            ["ERRULE_CODE", 'TEXT', '', 255],
            ["REF_SCORE", 'Long',],
            ["IS_DISCLOSED", 'Long',],
            ["IS_AMBIGUOUS", 'Long',],
            ["SOURCE_ENTITY_ID", 'Long', 'Source Entity ID']
        ]
        

        arcpy.management.CreateTable(self.out_file, "related_entities", "", '', '')
        arcpy.management.AddFields(self.out_related, related_fields)

        print([f.name for f in arcpy.ListFields(self.out_related)])

        arcpy.management.CreateTable(self.out_file, "addresses", "", '', '')
        arcpy.management.AddFields(self.out_addresses, detail_fields)
    

        arcpy.management.CreateTable(self.out_file, "phone_numbers", "", '', '')
        arcpy.management.AddFields(self.out_phone_numbers, detail_fields)
            

        arcpy.management.CreateTable(self.out_file, "names", "", '', '')
        arcpy.management.AddFields(self.out_names, detail_fields)
    

        arcpy.management.CreateTable(self.out_file, "resolved_entities", "", '', '')
        arcpy.management.AddFields(self.out_resolved_entities, entity_fields)
    

        arcpy.management.CreateTable(self.out_file, "records", "", '', '')
        arcpy.management.AddFields(self.out_records, record_fields)




        return

    def add_records_to_tables(self, data: ProcessedDataResult) -> None:
        arcpy.AddMessage("Adding records")
        data_dict = data.to_dict()

        details_fields = ['ENTITY_ID', 'FEAT_DESC', 'LIB_FEAT_ID', 'U_TYPE_CODE']
        
        with arcpy.da.InsertCursor(self.out_addresses, details_fields) as cursor:
            for item in data_dict['addresses']:
                iRow = [
                    item['ENTITY_ID'],
                    item['FEAT_DESC'],
                    item['LIB_FEAT_ID'],
                    item['U_TYPE_CODE'],
                ]

                cursor.insertRow(iRow)

        with arcpy.da.InsertCursor(self.out_phone_numbers, details_fields) as cursor:
            for item in data_dict['phones']:
                iRow = [
                    item['ENTITY_ID'],
                    item['FEAT_DESC'],
                    item['LIB_FEAT_ID'],
                    item['U_TYPE_CODE'],
                ]

                cursor.insertRow(iRow)

        with arcpy.da.InsertCursor(self.out_names, details_fields) as cursor:
            for item in data_dict['names']:
                iRow = [
                    item['ENTITY_ID'],
                    item['FEAT_DESC'],
                    item['LIB_FEAT_ID'],
                    item['U_TYPE_CODE'],
                ]

                cursor.insertRow(iRow)

        entity_fields = ['ENTITY_ID', 'LENS_CODE', 'ENTITY_NAME']
        
        with arcpy.da.InsertCursor(self.out_resolved_entities, entity_fields) as cursor:
            for item in data_dict['resolved_entities']:
                iRow = [
                    item['ENTITY_ID'],
                    item['LENS_CODE'],
                    item['ENTITY_NAME'],
                ]

                cursor.insertRow(iRow)

        records_fields = ["DATA_SOURCE", 'RECORD_ID', 'ENTITY_TYPE', "INTERNAL_ID", "ENTITY_KEY", "ENTITY_DESC", "MATCH_KEY", "MATCH_LEVEL", "MATCH_LEVEL_CODE", "MATCH_SCORE", "ERRULE_CODE", "REF_SCORE", "LAST_SEEN_DT", "ENTITY_ID"]
        
        with arcpy.da.InsertCursor(self.out_records, records_fields) as cursor:
            for item in data_dict['records']:
                iRow = [
                    item["DATA_SOURCE"],
                    item['RECORD_ID'],
                    item['ENTITY_TYPE'],
                    item["INTERNAL_ID"],
                    item["ENTITY_KEY"],
                    item["ENTITY_DESC"],
                    item["MATCH_KEY"],
                    item["MATCH_LEVEL"],
                    item["MATCH_LEVEL_CODE"],
                    item["MATCH_SCORE"],
                    item["ERRULE_CODE"],
                    item["REF_SCORE"],
                    item["LAST_SEEN_DT"],
                    item["ENTITY_ID"]
                ]

                cursor.insertRow(iRow)

        related_fields = ["TARGET_ENTITY_ID", "LENS_CODE", "MATCH_LEVEL", "MATCH_LEVEL_CODE", "MATCH_KEY", "MATCH_SCORE", "ERRULE_CODE", "REF_SCORE", "IS_DISCLOSED", "IS_AMBIGUOUS", "SOURCE_ENTITY_ID"]
        with arcpy.da.InsertCursor(self.out_related, related_fields) as cursor:
            for item in data_dict['related_entities']:
                iRow = [
                    item["ENTITY_ID"],
                    item['LENS_CODE'],
                    item["MATCH_LEVEL"],
                    item["MATCH_LEVEL_CODE"],
                    item["MATCH_KEY"],
                    item["MATCH_SCORE"],
                    item["ERRULE_CODE"],
                    item["REF_SCORE"],
                    item["IS_DISCLOSED"],
                    item["IS_AMBIGUOUS"],
                    item["SOURCE_ENTITY_ID"]
                ]

                cursor.insertRow(iRow)


        return