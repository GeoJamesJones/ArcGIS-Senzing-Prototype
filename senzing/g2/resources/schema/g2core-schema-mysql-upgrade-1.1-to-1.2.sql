CREATE TABLE SYS_CFG (CFG_ID SMALLINT NOT NULL, CONFIG_DATA_ID BIGINT NOT NULL, CONFIG_DATA LONGTEXT NOT NULL, SYS_CREATE_DT DATETIME NOT NULL) ;
ALTER TABLE SYS_CFG ADD CONSTRAINT SYS_CFG_PK PRIMARY KEY(CFG_ID) ;
CREATE TABLE SYS_STATUS (SYSTEM_CODE VARCHAR(50) NOT NULL, LAST_TOUCH_DT DATETIME) ;
ALTER TABLE SYS_STATUS ADD CONSTRAINT SYS_STATUS_PK PRIMARY KEY(SYSTEM_CODE) ;
ALTER TABLE RES_FEAT_EKEY ADD COLUMN SUPPRESSED CHAR(1);
