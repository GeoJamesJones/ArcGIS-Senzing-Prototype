ALTER TABLE RES_RELATE ADD COLUMN MATCH_LEVELS VARCHAR(50) ;
UPDATE SYS_VARS SET VAR_VALUE='2.0' WHERE VAR_GROUP='VERSION' AND VAR_CODE='SCHEMA' ;
