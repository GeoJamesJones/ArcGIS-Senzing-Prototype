DROP INDEX IX_EVAL_QUEUE ;
ALTER TABLE SYS_EVAL_QUEUE RENAME TO SYS_EVAL_QUEUE_PRE_V1_14 ;
CREATE TABLE SYS_EVAL_QUEUE (MSG_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, LENS_CODE VARCHAR(25) NOT NULL, ETYPE_CODE VARCHAR(25) NOT NULL, DSRC_CODE VARCHAR(25) NOT NULL, ENT_SRC_KEY VARCHAR(200) NOT NULL, MSG CLOB) ;
CREATE UNIQUE INDEX IX_EVAL_QUEUE ON SYS_EVAL_QUEUE(ENT_SRC_KEY, DSRC_CODE, ETYPE_CODE, LENS_CODE) ;
INSERT INTO SYS_EVAL_QUEUE (LENS_CODE,ETYPE_CODE,DSRC_CODE,ENT_SRC_KEY,MSG) SELECT LENS_CODE,ETYPE_CODE,DSRC_CODE,ENT_SRC_KEY,MSG FROM SYS_EVAL_QUEUE_PRE_V1_14; 
UPDATE SYS_VARS SET VAR_VALUE='1.14' WHERE VAR_GROUP='VERSION' AND VAR_CODE='SCHEMA' ;

