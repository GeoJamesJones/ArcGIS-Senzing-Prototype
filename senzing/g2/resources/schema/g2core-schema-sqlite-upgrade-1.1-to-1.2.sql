CREATE TABLE SYS_CFG (CFG_ID smallint NOT NULL, CONFIG_DATA_ID BIGINT NOT NULL, CONFIG_DATA CLOB NOT NULL, SYS_CREATE_DT TIMESTAMP NOT NULL, PRIMARY KEY(CFG_ID)) ;
CREATE TABLE SYS_STATUS (SYSTEM_CODE VARCHAR(50) NOT NULL, LAST_TOUCH_DT TIMESTAMP, PRIMARY KEY(SYSTEM_CODE)) ;
ALTER TABLE RES_FEAT_EKEY ADD SUPPRESSED CHAR(1);