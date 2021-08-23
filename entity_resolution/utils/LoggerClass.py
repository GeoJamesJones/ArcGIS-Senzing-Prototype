from __future__ import annotations

import logging
import time
import os
import arcpy

class Logger:
    def __init__(self, name: str, level: str = 'WARN') -> None:
        if level == "DEBUG":
            log_level = logging.DEBUG
        else:
            log_level = logging.WARNING

        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        if level == "DEBUG":
                     
            path = arcpy.env.scratchFolder
            log_path = os.path.join(path, "er_logs")
            if not os.path.exists(log_path):
                os.mkdir(log_path, mode=0o777)

            log_name = f"{name.replace('.','_')}_{str(int(time.time()))}.log"
            out_log = os.path.join(log_path, log_name)

            fh = logging.FileHandler(out_log)
            fh.setLevel(log_level)
            
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            
            self.logger.addHandler(fh)

            self.logger.debug(f"Log path: {out_log}")

        return

    def debug(self, msg: str) -> None:
        arcpy.AddMessage(f"DEBUG: {msg}")
        self.logger.debug(msg)

    def warning(self, msg: str) -> None:
        arcpy.AddWarning(msg)
        self.logger.warning(msg)

    def error(self, msg: str) -> None:
        arcpy.AddError(msg)
        self.logger.error(msg)