import json
import arcpy

from typing import List

from entity_resolution import SenzingConfig

import senzing.g2.sdk.python.G2Exception as G2Exception
from senzing import G2Engine

class RedoRecords:
    def __init__(self, entity_store: str) -> None:
        self.entity_store = entity_store

        self.DEBUG = True

    def process(self):
        self.senzing_config = SenzingConfig(entity_store=self.entity_store)
        self.senzing_config.configure_g2_config()
        self.senzing_config.configure_g2_cfg_mgr()
        config_id = self.senzing_config.check_for_default_config()
        self.senzing_config.configure_g2_engine(config_id=config_id, prime_engine=False)

        

        try:
            return_code = self.senzing_config.g2_engine.countRedoRecords()

            arcpy.AddMessage(f"There are a total of {return_code} redo records")

            if return_code > 0:

                for _ in range(return_code):
                    response_bytearray = bytearray()
                    self.senzing_config.g2_engine.getRedoRecord(response_bytearray)

                    process_response_bytearray = bytearray()

                    self.senzing_config.g2_engine.processWithInfo(
                        response_bytearray.decode(),
                        process_response_bytearray)

        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(self.senzing_config.g2_engine.getLastException())