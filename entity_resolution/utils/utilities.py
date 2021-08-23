import arcpy
import logging

from typing import List

ENTITY_RECORD_FIELDS: List[str] = [
                'ENTITY_ID', 
                'ENTITY_NAME', 
                "RECORDS_COUNT", 
                "DATA_SOURCES"
            ]

RECORDS_RECORD_FIELDS: List[str] = [
                "ENTITY_ID",
                "DATA_SOURCE",
                'RECORD_ID',
                'ENTITY_TYPE',
                "ENTITY_DESC",
                "LAST_SEEN_DT",
            ]

RELATED_RECORD_FIELDS: List[str] = [
                "SOURCE_ENTITY_ID",
                "TARGET_ENTITY_ID",
                "MATCH_LEVEL_CODE",
                "MATCH_KEY",
            ]

SHAPE_RECORD_FIELDS: List[str] = [
                "SHAPE@JSON", 
                "RECORD_ID"
            ]

def error_handler(exception_obj: Exception, 
                  message: str,
                  logger: logging.Logger, 
                  debug: bool = False, 
                  exit_: bool = True) -> None:
    
    logger.error(message)
    
    if debug:
        import sys
        import traceback
        
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = '{}\n{}\n{}'.format(tbinfo,
                                    str(sys.exc_info()[1]),
                                    arcpy.GetMessages(2))

        logger.error(exception_obj.__class__.__name__)
        logger.error(pymsg)
    if exit_:
        exit()