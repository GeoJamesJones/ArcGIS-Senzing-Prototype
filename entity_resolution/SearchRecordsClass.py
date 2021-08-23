import json
import arcpy

from typing import List

from entity_resolution import SenzingConfig

import senzing as G2Exception
from senzing import G2Engine

class SearchRecords:
    def __init__(self, entity_store: str, search_terms: List[str]) -> None:
        self.entity_store = entity_store
        self.search_terms = search_terms

        self.DEBUG = True

    def search(self):
        self.senzing_config = SenzingConfig(entity_store=self.entity_store)
        self.senzing_config.configure_g2_config()
        self.senzing_config.configure_g2_cfg_mgr()
        config_id = self.senzing_config.check_for_default_config()
        self.senzing_config.configure_g2_engine(config_id=config_id, prime_engine=False)

        g2_engine_flags = G2Engine.G2_EXPORT_DEFAULT_FLAGS

        search_dict = {item[1]:item[0] for item in self.search_terms}

        response_bytearray = bytearray()

        try:
            self.senzing_config.g2_engine.searchByAttributesV2(
                                            json.dumps(search_dict),
                                            g2_engine_flags,
                                            response_bytearray)

        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(self.senzing_config.g2_engine.getLastException())

        decoded_response = response_bytearray.decode()

        #result = ProcessDataList([json.loads(decoded_response)]).process()

        arcpy.AddMessage(json.dumps(json.loads(decoded_response)))