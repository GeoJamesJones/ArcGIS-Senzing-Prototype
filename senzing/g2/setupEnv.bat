
@echo off

REM Set required path variables
SET SENZING_ROOT=C:\repos\Senzing-EntityResolution\senzing
SET PATH=%SENZING_ROOT%\g2\bin;%SENZING_ROOT%\g2\lib;%PATH%
SET PYTHONPATH=%PYTHONPATH%;%SENZING_ROOT%\g2\sdk\python
