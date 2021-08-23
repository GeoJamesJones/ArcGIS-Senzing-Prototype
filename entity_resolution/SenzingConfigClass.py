from __future__ import annotations

import arcpy
import os
import json
import sys
import time

from typing import Optional, Dict, Any
from contextlib import suppress

import senzing.g2.sdk.python.G2Exception as G2Exception
from senzing.g2.sdk.python.G2ConfigMgr import G2ConfigMgr
from senzing.g2.sdk.python.G2Engine import G2Engine
from senzing.g2.sdk.python.G2Config import G2Config

class SenzingConfig:
    def __init__(self, entity_store: str) -> None:
        self.entity_store = entity_store

        self.senzing_root = os.path.join(r'C:\repos\entity_resolution_proto', "senzing")
        self.senzing_bin = os.path.join(self.senzing_root, 'g2', 'bin')
        self.senzing_lib = os.path.join(self.senzing_root, 'g2', 'lib')
        self.senzing_sdk = os.path.join(self.senzing_root, 'g2', 'sdk', 'python')
        self.config_path = os.path.join(self.senzing_root, 'g2', 'etc')
        self.support_path = os.path.join(self.senzing_root, 'g2', 'data')
        self.resource_path = os.path.join(self.senzing_root, 'g2', 'resources')

        self.DEBUG = True
        self._config_comment: str

        self.module_name = 'pyG2'
        if self.DEBUG:
            self.verbose_logging = True
        else:
            self.verbose_logging = False

        if self.DEBUG:
            arcpy.AddMessage(f"Senzing Root?: {self.senzing_root}")
        
        os.environ['SENZING_ROOT'] = self.senzing_root

        path_split = os.environ['PATH'].split(os.pathsep)

        if self.senzing_bin not in path_split:
            os.environ['PATH'] += os.pathsep + self.senzing_bin

        if self.senzing_lib not in path_split:
            os.environ['PATH'] += os.pathsep + self.senzing_lib

        try:
            pythonpath_split = os.environ['PYTHONPATH'].split(os.pathsep)
            if self.senzing_sdk not in pythonpath_split:
                os.environ['PYTHONPATH'] += os.pathsep + self.senzing_sdk
        except KeyError:
            os.environ['PYTHONPATH'] = self.senzing_sdk

    @property
    def CONFIG_COMMENT(self) -> str:
        return self._config_comment
    @CONFIG_COMMENT.setter
    def CONFIG_COMMENT(self, value: str) -> None:
        self._config_comment = value

    @property
    def config_bytearray(self) -> bytearray:
        return self._config_bytearray
    @config_bytearray.setter
    def config_bytearray(self, config: bytearray) -> None:
        self._config_bytearray = config

    @property
    def g2_engine(self) -> G2Engine:
        return self._g2_engine
    @g2_engine.deleter
    def g2_engine(self) -> None:
        del self._g2_engine

    @property
    def g2_config(self) -> G2Config:
        return self._g2_config
    @g2_config.deleter
    def g2_config(self) -> None:
        del self._g2_config

    @property
    def g2_config_manger(self) -> G2ConfigMgr:
        return self._g2_configuration_manager
    @g2_config_manger.deleter
    def g2_config_manger(self) -> None:
        del self._g2_configuration_manager

    @property
    def config_list(self) -> Dict[Any, Any]:
        response_bytearray = bytearray()
        try:
            self.g2_config_manger.getConfigList(response_bytearray)

        except G2Exception.G2ModuleGenericException as err:
            print(self.g2_config_manger.getLastException())

        return json.loads(response_bytearray)

    def ini_json(self) -> str:
        sql_connection = 'sqlite3://na:na@' + self.entity_store

        senzing_config_dictionary = {
            "PIPELINE": {
                "CONFIGPATH": self.config_path,
                "SUPPORTPATH": self.support_path,
                "RESOURCEPATH": self.resource_path
            },
            "SQL": {
                "CONNECTION": sql_connection,
            }
        }

        senzing_config_json = json.dumps(senzing_config_dictionary)
        return senzing_config_json

    def house_keeping(self, config_handle=None, exit_code=0, exit_=False):
        '''  Perform any clean up from exit or functions failing - e.g. destroy engines '''

        with suppress(Exception):
            self.g2_config_manger.destroy()
            del self.g2_config_manger
            if config_handle:
                self.g2_config.close(config_handle)
            self.g2_config.destroy()
            del self.g2_config
            self.g2_engine.destroy()
            del self.g2_engine

        if exit_:
            sys.exit(exit_code)

    def configure_g2_engine(self, config_id, name='G2Engine', prime_engine=False) -> G2Engine:
        '''  Initialize engine '''

        arcpy.AddMessage(f'\nEngine starting {name} with config ID {config_id}')

        try:
            self._g2_engine = G2Engine()
            self.g2_engine.initV2(name, self.ini_json(), self.DEBUG)

            if prime_engine:
                arcpy.AddMessage(f'\nPriming {name}...')
                self.g2_engine.primeEngine()

        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to init G2Engine() or prime the engine')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        return self.g2_engine

    def configure_g2_config(self) -> G2Config:
        try:
            self._g2_config = G2Config()
            self.g2_config.initV2(self.module_name, self.ini_json(), self.DEBUG)
            return self.g2_config
        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(f'Error initializing G2Config: {self.g2_config_manger.getLastException()}')
            sys.exit(1)

    def configure_g2_cfg_mgr(self) -> G2ConfigMgr:
        try:
            self._g2_configuration_manager = G2ConfigMgr()
            self.g2_config_manger.initV2(self.module_name, self.ini_json(), self.DEBUG)
            return self.g2_config_manger
        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(f'Error initializing G2ConfigManager: {self.g2_config_manger.getLastException()}')
            sys.exit(1)

    def check_for_default_config(self) -> str:
        ''' Check if there is a default Senzing configuration.
            Will return a blank str if new repository and no config yet, otherwise the current config ID
        '''

        default_config_id = bytearray()

        try:
            self.g2_config_manger.getDefaultConfigID(default_config_id)
        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to init G2ConfigMgr() or fetch default config id')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        return default_config_id.decode()

    def add_default_config(self):
        ''' Add a default template config when new repository and no config exists yet '''

        config_bytearray = bytearray()
        config_id_bytearray = bytearray()

        # Create a configuration from default template and save to string
        try:
            config_handle = self.g2_config.create()
            self.g2_config.save(config_handle, config_bytearray)
            new_config = config_bytearray.decode()
        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to init G2Config() or create template default config')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        # Populate Senzing repository with new template config
        try:
            self.g2_config_manger.addConfig(new_config, self.CONFIG_COMMENT, config_id_bytearray)
            self.g2_config_manger.setDefaultConfigID(config_id_bytearray)
            arcpy.AddWarning(f'\nNew configuration set in the Senzing repository: {config_id_bytearray.decode()}')
        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to add or set default config')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        self.g2_config.close(config_handle)

        return config_id_bytearray.decode()

    def data_sources_list(self, config_id, _return=False):
        ''' List data sources in current configuration'''

        data_sources = bytearray()
        get_config_bytearray = bytearray()

        # Fetch the data sources
        try:
            self.g2_config_manger.getConfig(config_id, get_config_bytearray)
            config_handle = self.g2_config.load(get_config_bytearray.decode())
            self.g2_config.listDataSourcesV2(config_handle, data_sources)
        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to list data sources')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        arcpy.AddMessage(f'\nData sources: {json.loads(data_sources)}')

        self.g2_config.close(config_handle)

        if _return:
            return json.loads(data_sources)

    def data_source_exists(self, config_id, data_source):
        '''  Check if a data source currently exists in config  '''

        arcpy.AddMessage(f'\nChecking if data source {data_source} exists in current configuration')

        data_sources = self.data_sources_list(config_id, _return=True)

        return False if not [ds.get('DSRC_CODE') for ds in data_sources.get('DATA_SOURCES') if ds.get('DSRC_CODE') == data_source] else True

    def configure_entity_store(self) -> None:
        try:
            import sqlite3

            conn = sqlite3.connect(os.path.splitext(self.entity_store)[0] + '.db')

            with open(os.path.join(self.resource_path, 'schema', 'g2core-schema-sqlite-create.sql'), 'r') as sql_file:
                conn.executescript(sql_file.read())

            conn.close()
        except Exception as e:
            arcpy.AddError(arcpy.GetIDMessage(190391))
            if self.DEBUG:
                import sys
                import traceback
                
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = '{}\n{}\n{}'.format(tbinfo,
                                            str(sys.exc_info()[1]),
                                            arcpy.GetMessages(2))
                
                arcpy.AddError(e.__class__.__name__)
                arcpy.AddError(pymsg)
            exit()

    def add_data_source(self, config_id, data_source) -> str:
        ''' Add a new data source to the config '''

        get_config_bytearray = bytearray()
        add_ds_bytearray = bytearray()
        datasource_json = {"DSRC_CODE": data_source}

        try:
            self.g2_config_manger.getConfig(config_id, get_config_bytearray)
            config_handle = self.g2_config.load(get_config_bytearray.decode())
            self.g2_config.addDataSourceV2(config_handle, json.dumps(datasource_json), add_ds_bytearray)
            arcpy.AddMessage(f'\nAdded data source {data_source} as: {add_ds_bytearray.decode()}')
        except G2Exception.G2ModuleGenericException as ex:
            arcpy.AddError('\nERROR: Unable to add data source')
            arcpy.AddError(f'       {ex}')
            self.house_keeping(exit_code=1)

        save_config_bytearray = bytearray()
        self.g2_config.save(config_handle, save_config_bytearray)
        #print(new_config)

        new_config_id_bytearray = bytearray()
        self.g2_config_manger.addConfig(save_config_bytearray.decode(), self.CONFIG_COMMENT, new_config_id_bytearray)
        self.g2_config_manger.setDefaultConfigID(new_config_id_bytearray)

        arcpy.AddWarning(f'\nNew configuration set in the Senzing repository: {new_config_id_bytearray.decode()}')

        self.g2_config.close(config_handle)

        # List again with the new config
        self.data_sources_list(new_config_id_bytearray.decode())

        return new_config_id_bytearray.decode()

    def initialize(self) -> SenzingConfig:


        config_id_bytearray = bytearray()
        try:
            self.g2_config_manger.getDefaultConfigID(config_id_bytearray)
            #self.g2_config_manger.getActiveConfigID(config_id_bytearray)
            
            if config_id_bytearray:
                arcpy.AddMessage("Default config already set")
            else:
                try:          
                    # Save Senzing configuration to string.
                    response_bytearray = bytearray()
                    #self.g2_config.save(self.config_handle, response_bytearray)
                    senzing_model_config_str = response_bytearray.decode()
                    
                    # Externalize Senzing configuration to the database.
                    config_comment = "ArcGISProIntel added at {0}".format(time.time())
                    config_id_bytearray = bytearray()

                    self.g2_config_manger.addConfig(senzing_model_config_str, config_comment, config_id_bytearray)
            
                    # Set new configuration as the default.
            
                    self.g2_config_manger.setDefaultConfigID(config_id_bytearray)
                except G2Exception.G2ModuleGenericException as err:
                    arcpy.AddError(f'Error setting default id for G2ConfigurationManager: {self.g2_config_manger.getLastException()}')
                    sys.exit(1)

        except G2Exception.G2ModuleGenericException as err:
            arcpy.AddError(f'ERROR obtaining default id during initialization: {self.g2_config_manger.getLastException()}')
            sys.exit(1)

        return self