import os
import json
import arcpy

from entity_resolution import ERBase, SenzingConfig, ProcessDataList

import senzing.g2.sdk.python.G2Exception as G2Exception
from senzing.g2.sdk.python.G2Engine import G2Engine

class ExportRecords(ERBase):
    def __init__(self, entity_store: str, out_file: str) -> None:
        self.entity_store = entity_store
        self.out_file = out_file

        self.out_addresses = os.path.join(self.out_file, 'addresses')
        self.out_names = os.path.join(self.out_file, 'names')
        self.out_phone_numbers = os.path.join(self.out_file, 'phone_numbers')
        self.out_resolved_entities = os.path.join(self.out_file, 'resolved_entities')
        self.out_records = os.path.join(self.out_file, 'records')
        self.out_related = os.path.join(self.out_file, 'related_entities')

        self.DEBUG = True

    def export(self):
        senzing_config = SenzingConfig(entity_store=self.entity_store)

        senzing_config.configure_g2_cfg_mgr()
        senzing_config.configure_g2_config()
        config_id = senzing_config.check_for_default_config()
        senzing_config.configure_g2_engine(config_id=config_id, prime_engine=False)

        g2_engine_flags = G2Engine.G2_EXPORT_DEFAULT_FLAGS

        try:
            export_handle = senzing_config.g2_engine.exportJSONEntityReport(g2_engine_flags)

            data = []

            while True:
                response_bytearray = bytearray()
                senzing_config.g2_engine.fetchNext(export_handle, response_bytearray)
                if not response_bytearray:
                    break
                response_dictionary = json.loads(response_bytearray)
                data.append(response_dictionary)

            senzing_config.g2_engine.closeExport(export_handle)

            result = ProcessDataList(data).process_export()

            self.create_output_tables()

            self.add_records_to_tables(result)

        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(senzing_config.g2_engine.getLastException())