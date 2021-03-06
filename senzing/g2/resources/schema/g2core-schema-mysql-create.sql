CREATE TABLE SRD_PRODUCT_VERSIONS(product CHAR(50), version CHAR(50));
CREATE TABLE SYS_SEQUENCE (SEQUENCE_NAME VARCHAR(50) NOT NULL, NEXT_SEQUENCE BIGINT NOT NULL, CACHE_SIZE BIGINT NOT NULL, SCATTER CHAR(1) NOT NULL) ;
ALTER TABLE SYS_SEQUENCE ADD CONSTRAINT SYS_SEQUENCE_PK PRIMARY KEY(SEQUENCE_NAME) ;
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('ER_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('LIB_FEAT_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('LIB_FELEM_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('LIB_TOKEN_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('OBS_ENT_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('OBS_ID',1,1000,'N');
INSERT INTO SYS_SEQUENCE (SEQUENCE_NAME,NEXT_SEQUENCE,CACHE_SIZE,SCATTER) VALUES ('RES_REL_ID',1,1000,'N');
CREATE TABLE SYS_CFG (CONFIG_DATA_ID BIGINT NOT NULL, CONFIG_DATA LONGTEXT NOT NULL, CONFIG_COMMENTS VARCHAR(200) NOT NULL, SYS_CREATE_DT DATETIME NOT NULL) ;
ALTER TABLE SYS_CFG ADD CONSTRAINT SYS_CFG_PK PRIMARY KEY(CONFIG_DATA_ID) ;
CREATE TABLE SYS_CODES_USED (CODE_TYPE VARCHAR(25) NOT NULL, CODE VARCHAR(25) NOT NULL, CODE_ID SMALLINT NOT NULL) ;
ALTER TABLE SYS_CODES_USED ADD CONSTRAINT SYS_CODES_USED_PK PRIMARY KEY(CODE_TYPE,CODE) ;
CREATE UNIQUE INDEX SYS_CODES_USED_SK ON SYS_CODES_USED(CODE_TYPE, CODE_ID) ;
CREATE TABLE SYS_VARS (VAR_GROUP VARCHAR(25) NOT NULL, VAR_CODE VARCHAR(25) NOT NULL, VAR_VALUE VARCHAR(25) NOT NULL, SYS_LSTUPD_DT DATETIME) ;
ALTER TABLE SYS_VARS ADD CONSTRAINT SYS_VARS_PK PRIMARY KEY(VAR_GROUP,VAR_CODE) ;
INSERT INTO SYS_VARS (VAR_GROUP,VAR_CODE,VAR_VALUE) VALUES ('VERSION','SCHEMA','2.0');
CREATE TABLE SYS_STATUS (SYSTEM_CODE VARCHAR(50) NOT NULL, LAST_TOUCH_DT DATETIME) ;
ALTER TABLE SYS_STATUS ADD CONSTRAINT SYS_STATUS_PK PRIMARY KEY(SYSTEM_CODE) ;
CREATE TABLE SYS_OOM (OOM_TYPE VARCHAR(25) NOT NULL, OOM_LEVEL VARCHAR(25) NOT NULL, LENS_ID SMALLINT, FTYPE_ID SMALLINT, LIB_FEAT_ID BIGINT, FELEM_ID SMALLINT, LIB_FELEM_ID BIGINT, THRESH1_CNT MEDIUMINT NOT NULL, THRESH1_OOM MEDIUMINT NOT NULL, NEXT_THRESH MEDIUMINT NOT NULL) ;
CREATE TABLE SYS_EVAL_QUEUE (MSG_ID BIGINT PRIMARY KEY AUTO_INCREMENT NOT NULL, LENS_CODE VARCHAR(25) NOT NULL, ETYPE_CODE VARCHAR(25) NOT NULL, DSRC_CODE VARCHAR(25) NOT NULL, ENT_SRC_KEY VARCHAR(200) NOT NULL, MSG LONGTEXT) ;
CREATE UNIQUE INDEX IX_EVAL_QUEUE ON SYS_EVAL_QUEUE(ENT_SRC_KEY, DSRC_CODE, ETYPE_CODE, LENS_CODE) ;
CREATE TABLE CFG_DSRC (DSRC_ID SMALLINT NOT NULL, DSRC_CODE VARCHAR(25) NOT NULL, DSRC_DESC VARCHAR(50), DSRC_RELY SMALLINT NOT NULL, RETENTION_LEVEL VARCHAR(25) NOT NULL, CONVERSATIONAL VARCHAR(25) NOT NULL) ;
CREATE TABLE CFG_DSRC_INTEREST (DSRC_ID SMALLINT NOT NULL, MAX_DEGREE SMALLINT NOT NULL, INTEREST_FLAG VARCHAR(25) NOT NULL) ;
CREATE TABLE CFG_ECLASS (ECLASS_ID SMALLINT NOT NULL, ECLASS_CODE VARCHAR(25) NOT NULL, ECLASS_DESC VARCHAR(50), RESOLVE VARCHAR(5) DEFAULT 'Yes' NOT NULL) ;
CREATE TABLE CFG_ETYPE (ETYPE_ID SMALLINT NOT NULL, ETYPE_CODE VARCHAR(25) NOT NULL, ETYPE_DESC VARCHAR(50), ECLASS_ID SMALLINT NOT NULL) ;
CREATE TABLE CFG_FCLASS (FCLASS_ID SMALLINT NOT NULL, FCLASS_CODE VARCHAR(25) NOT NULL, FCLASS_DESC VARCHAR(50)) ;
CREATE TABLE CFG_FTYPE (FTYPE_ID SMALLINT NOT NULL, FTYPE_CODE VARCHAR(25) NOT NULL, FTYPE_DESC VARCHAR(50), FCLASS_ID SMALLINT NOT NULL, FTYPE_FREQ VARCHAR(5) NOT NULL, FTYPE_EXCL VARCHAR(5) NOT NULL, FTYPE_STAB VARCHAR(5) NOT NULL, PERSIST_HISTORY VARCHAR(5) NOT NULL, USED_FOR_CAND VARCHAR(5) DEFAULT 'Yes' NOT NULL, DERIVED VARCHAR(5) NOT NULL, DERIVATION VARCHAR(10), RTYPE_ID SMALLINT, ANONYMIZE VARCHAR(5) DEFAULT 'No' NOT NULL, VERSION SMALLINT DEFAULT 1 NOT NULL, SHOW_IN_MATCH_KEY VARCHAR(8)) ;
CREATE TABLE CFG_FBOVR (FTYPE_ID SMALLINT NOT NULL, ECLASS_ID SMALLINT NOT NULL, UTYPE_CODE VARCHAR(50) NOT NULL, FTYPE_FREQ VARCHAR(5) NOT NULL, FTYPE_EXCL VARCHAR(5) NOT NULL, FTYPE_STAB VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_FELEM (FELEM_ID SMALLINT NOT NULL, FELEM_CODE VARCHAR(50) NOT NULL, FELEM_DESC VARCHAR(50), TOKENIZE VARCHAR(5) NOT NULL, DATA_TYPE VARCHAR(25) NOT NULL) ;
CREATE TABLE CFG_FBOM (FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL, DISPLAY_LEVEL SMALLINT NOT NULL, DISPLAY_DELIM VARCHAR(25), DERIVED VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_EBOM (ETYPE_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, UTYPE_CODE VARCHAR(50)) ;
CREATE TABLE CFG_ESCORE (BEHAVIOR_CODE VARCHAR(25) NOT NULL, GROUPER_FEAT VARCHAR(5) NOT NULL, RICHNESS_SCORE SMALLINT NOT NULL, EXCLUSIVITY_SCORE SMALLINT NOT NULL) ;
CREATE TABLE CFG_SFUNC (SFUNC_ID SMALLINT NOT NULL, SFUNC_CODE VARCHAR(25) NOT NULL, SFUNC_DESC VARCHAR(50), FUNC_LIB VARCHAR(25), FUNC_VER VARCHAR(25), CONNECT_STR VARCHAR(100)) ;
CREATE TABLE CFG_SFCALL (SFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, SFUNC_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_EFUNC (EFUNC_ID SMALLINT NOT NULL, EFUNC_CODE VARCHAR(25) NOT NULL, EFUNC_DESC VARCHAR(50), FUNC_LIB VARCHAR(25), FUNC_VER VARCHAR(25), CONNECT_STR VARCHAR(100)) ;
CREATE TABLE CFG_EFCALL (EFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, EFUNC_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL, EFEAT_FTYPE_ID SMALLINT NOT NULL, IS_VIRTUAL VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_EFBOM (EFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL, FELEM_REQ VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_CFUNC (CFUNC_ID SMALLINT NOT NULL, CFUNC_CODE VARCHAR(25) NOT NULL, CFUNC_DESC VARCHAR(50), FUNC_LIB VARCHAR(25), FUNC_VER VARCHAR(25), CONNECT_STR VARCHAR(100), ANON_SUPPORT VARCHAR(5)) ;
CREATE TABLE CFG_CFRTN (CFRTN_ID SMALLINT NOT NULL, CFUNC_ID SMALLINT NOT NULL, CFUNC_RTNVAL VARCHAR(25) NOT NULL, EXEC_ORDER SMALLINT NOT NULL, SAME_SCORE SMALLINT NOT NULL, CLOSE_SCORE SMALLINT NOT NULL, LIKELY_SCORE SMALLINT NOT NULL, PLAUSIBLE_SCORE SMALLINT NOT NULL, UN_LIKELY_SCORE SMALLINT NOT NULL) ;
CREATE TABLE CFG_CFCALL (CFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, CFUNC_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_CFBOM (CFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_DFUNC (DFUNC_ID SMALLINT NOT NULL, DFUNC_CODE VARCHAR(25) NOT NULL, DFUNC_DESC VARCHAR(50), FUNC_LIB VARCHAR(25), FUNC_VER VARCHAR(25), CONNECT_STR VARCHAR(100), ANON_SUPPORT VARCHAR(5)) ;
CREATE TABLE CFG_DFCALL (DFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, DFUNC_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_DFBOM (DFCALL_ID SMALLINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FELEM_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_ERFRAG (ERFRAG_ID SMALLINT NOT NULL, ERFRAG_CODE VARCHAR(25) NOT NULL, ERFRAG_DESC VARCHAR(50) NOT NULL, ERFRAG_SOURCE VARCHAR(1000) NOT NULL, ERFRAG_DEPENDS VARCHAR(25)) ;
CREATE TABLE CFG_ERRULE (ERRULE_ID SMALLINT NOT NULL, ERRULE_CODE VARCHAR(25) NOT NULL, ERRULE_DESC VARCHAR(50) NOT NULL, RESOLVE VARCHAR(5) NOT NULL, RELATE VARCHAR(5) NOT NULL, REF_SCORE SMALLINT NOT NULL, RTYPE_ID SMALLINT, QUAL_ERFRAG_CODE VARCHAR(1000) NOT NULL, DISQ_ERFRAG_CODE VARCHAR(1000), ERRULE_TIER SMALLINT) ;
CREATE TABLE CFG_LENS (LENS_ID SMALLINT NOT NULL, LENS_CODE VARCHAR(25) NOT NULL, LENS_DESC VARCHAR(50)) ;
CREATE TABLE CFG_LENSRL (LENS_ID SMALLINT NOT NULL, ERRULE_ID SMALLINT NOT NULL, EXEC_ORDER SMALLINT NOT NULL) ;
CREATE TABLE CFG_RCLASS (RCLASS_ID SMALLINT NOT NULL, RCLASS_CODE VARCHAR(25) NOT NULL, RCLASS_DESC VARCHAR(50), IS_DISCLOSED VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_RTYPE (RTYPE_ID SMALLINT NOT NULL, RTYPE_CODE VARCHAR(25) NOT NULL, RTYPE_DESC VARCHAR(50), RCLASS_ID SMALLINT NOT NULL, REL_STRENGTH SMALLINT NOT NULL, BREAK_RES VARCHAR(5) DEFAULT 'No' NOT NULL) ;
CREATE TABLE CFG_GPLAN (GPLAN_ID SMALLINT NOT NULL, GPLAN_CODE VARCHAR(25) NOT NULL, GPLAN_DESC VARCHAR(50)) ;
CREATE TABLE CFG_GENERIC_THRESHOLD (GPLAN_ID SMALLINT NOT NULL, BEHAVIOR VARCHAR(50) NOT NULL, FTYPE_ID SMALLINT NOT NULL, CANDIDATE_CAP BIGINT NOT NULL, SCORING_CAP BIGINT NOT NULL, SEND_TO_REDO VARCHAR(5) NOT NULL) ;
CREATE TABLE CFG_ATTR (ATTR_ID SMALLINT NOT NULL, ATTR_CODE VARCHAR(64) NOT NULL, ATTR_CLASS VARCHAR(25) NOT NULL, FTYPE_CODE VARCHAR(25), FELEM_CODE VARCHAR(25), FELEM_REQ VARCHAR(8), DEFAULT_VALUE VARCHAR(25), ADVANCED VARCHAR(5) NOT NULL, INTERNAL VARCHAR(5) NOT NULL) ;
CREATE TABLE LIB_FEAT (LIB_FEAT_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FEAT_HASH CHAR(40) NOT NULL, FEAT_DESC VARCHAR(150), FELEM_VALUES VARCHAR(3000) NOT NULL, ANONYMIZED VARCHAR(5) NOT NULL, VERSION SMALLINT NOT NULL) ;
ALTER TABLE LIB_FEAT ADD CONSTRAINT LIB_FEAT_PK PRIMARY KEY(LIB_FEAT_ID) ;
CREATE UNIQUE INDEX LIB_FEAT_SK ON LIB_FEAT(FEAT_HASH, FTYPE_ID, ANONYMIZED) ;
CREATE TABLE LIB_FEAT_HKEY (FEAT_HASH CHAR(40) NOT NULL, FTYPE_ID SMALLINT NOT NULL, ANONYMIZED VARCHAR(5) NOT NULL, LIB_FEAT_ID BIGINT NOT NULL) ;
ALTER TABLE LIB_FEAT_HKEY ADD CONSTRAINT LIB_FEAT_HKEY_PK PRIMARY KEY(FEAT_HASH,FTYPE_ID,ANONYMIZED) ;
CREATE TABLE SYS_HW_CHECK (LIB_FEAT_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, FEAT_HASH CHAR(40) NOT NULL, FEAT_DESC VARCHAR(150), FELEM_VALUES VARCHAR(3000) NOT NULL, ANONYMIZED VARCHAR(5) NOT NULL, VERSION SMALLINT NOT NULL) ;
ALTER TABLE SYS_HW_CHECK ADD CONSTRAINT SYS_HW_CHECK_PK PRIMARY KEY(LIB_FEAT_ID) ;
CREATE UNIQUE INDEX SYS_HW_CHECK_SK ON SYS_HW_CHECK(FEAT_HASH, FTYPE_ID, ANONYMIZED) ;
CREATE TABLE LIB_FELEM (LIB_FELEM_ID BIGINT NOT NULL, FELEM_ID SMALLINT NOT NULL, FELEM_VALUE VARCHAR(1000) NOT NULL) ;
ALTER TABLE LIB_FELEM ADD CONSTRAINT LIB_FELEM_PK PRIMARY KEY(LIB_FELEM_ID) ;
CREATE TABLE LIB_FELEM_SKEY (FELEM_VALUE VARCHAR(250) NOT NULL, FELEM_ID SMALLINT NOT NULL, LIB_FELEM_ID BIGINT NOT NULL) ;
ALTER TABLE LIB_FELEM_SKEY ADD CONSTRAINT LIB_FELEM_SKEY_PK PRIMARY KEY(FELEM_VALUE,FELEM_ID) ;
CREATE TABLE LIB_FELEM_FKEY (LIB_FELEM_ID BIGINT NOT NULL, LIB_FEAT_ID BIGINT NOT NULL) ;
ALTER TABLE LIB_FELEM_FKEY ADD CONSTRAINT LIB_FELEM_FKEY_PK PRIMARY KEY(LIB_FELEM_ID,LIB_FEAT_ID) ;
CREATE TABLE LIB_TOKEN (LIB_TOKEN_ID BIGINT NOT NULL, TOKEN_VALUE VARCHAR(50) NOT NULL) ;
ALTER TABLE LIB_TOKEN ADD CONSTRAINT LIB_TOKEN_PK PRIMARY KEY(LIB_TOKEN_ID) ;
CREATE TABLE LIB_TOKEN_SKEY (TOKEN_VALUE VARCHAR(50) NOT NULL, LIB_TOKEN_ID BIGINT NOT NULL) ;
ALTER TABLE LIB_TOKEN_SKEY ADD CONSTRAINT LIB_TOKEN_SKEY_PK PRIMARY KEY(TOKEN_VALUE) ;
CREATE TABLE LIB_TOKEN_FKEY (LIB_TOKEN_ID BIGINT NOT NULL, LIB_FELEM_ID BIGINT NOT NULL) ;
ALTER TABLE LIB_TOKEN_FKEY ADD CONSTRAINT LIB_TOKEN_FKEY_PK PRIMARY KEY(LIB_TOKEN_ID,LIB_FELEM_ID) ;
CREATE TABLE LIB_UTYPE (UTYPE_CODE VARCHAR(50) NOT NULL, UTYPE_DESC VARCHAR(50)) ;
ALTER TABLE LIB_UTYPE ADD CONSTRAINT LIB_UTYPE_PK PRIMARY KEY(UTYPE_CODE) ;
CREATE TABLE OBS_ENT (OBS_ENT_ID BIGINT NOT NULL, ETYPE_ID SMALLINT NOT NULL, DSRC_ID SMALLINT NOT NULL, ENT_SRC_KEY VARCHAR(250) NOT NULL, ENT_SRC_DESC VARCHAR(250), FROM_LENS_ID SMALLINT, FROM_RES_ENT_ID BIGINT, FIRST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_TOUCH_DT BIGINT, LOCKING_ID BIGINT NOT NULL, NODE_NAME VARCHAR(50) NOT NULL, LOCK_DSRC_ACTION CHAR(1)) ;
ALTER TABLE OBS_ENT ADD CONSTRAINT OBS_ENT_PK PRIMARY KEY(OBS_ENT_ID) ;
CREATE UNIQUE INDEX OBS_ENT_SK ON OBS_ENT(ENT_SRC_KEY, ETYPE_ID, DSRC_ID) ;
CREATE TABLE OBS_ENT_SKEY (ENT_SRC_KEY VARCHAR(250) NOT NULL, ETYPE_ID SMALLINT NOT NULL, DSRC_ID SMALLINT NOT NULL, OBS_ENT_ID BIGINT NOT NULL) ;
ALTER TABLE OBS_ENT_SKEY ADD CONSTRAINT OBS_ENT_SKEY_PK PRIMARY KEY(ENT_SRC_KEY,ETYPE_ID,DSRC_ID) ;
CREATE TABLE OBS_FEAT_EKEY (OBS_ENT_ID BIGINT NOT NULL, LIB_FEAT_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, UTYPE_CODE VARCHAR(50) NOT NULL, USED_FROM_DT DATETIME NULL DEFAULT NULL, USED_THRU_DT DATETIME NULL DEFAULT NULL, SYS_LSTUPD_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE OBS_FEAT_EKEY ADD CONSTRAINT OBS_FEAT_EKEY_PK PRIMARY KEY(OBS_ENT_ID,LIB_FEAT_ID,UTYPE_CODE) ;
CREATE UNIQUE INDEX OBS_FEAT_EKEY_SK ON OBS_FEAT_EKEY(LIB_FEAT_ID, OBS_ENT_ID, UTYPE_CODE) ;
CREATE TABLE OBS_FEAT_LKEY (LIB_FEAT_ID BIGINT NOT NULL, OBS_ENT_ID BIGINT NOT NULL, UTYPE_CODE VARCHAR(50) NOT NULL) ;
ALTER TABLE OBS_FEAT_LKEY ADD CONSTRAINT OBS_FEAT_LKEY_PK PRIMARY KEY(LIB_FEAT_ID,OBS_ENT_ID,UTYPE_CODE) ;
CREATE TABLE DSRC_RECORD (DSRC_ID SMALLINT NOT NULL, RECORD_ID VARCHAR(250) NOT NULL, ETYPE_ID SMALLINT NOT NULL, ENT_SRC_KEY VARCHAR(250) NOT NULL, OBS_ENT_HASH CHAR(40) NOT NULL, JSON_DATA LONGTEXT, CONFIG_ID BIGINT, FIRST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_SEEN_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE DSRC_RECORD ADD CONSTRAINT DSRC_RECORD_PK PRIMARY KEY(RECORD_ID,DSRC_ID) ;
CREATE INDEX DSRC_RECORD_SK ON DSRC_RECORD(ENT_SRC_KEY, DSRC_ID, ETYPE_ID) ;
CREATE INDEX DSRC_RECORD_HK ON DSRC_RECORD(OBS_ENT_HASH, DSRC_ID, ETYPE_ID) ;
CREATE TABLE DSRC_RECORD_HKEY (OBS_ENT_HASH CHAR(40) NOT NULL, DSRC_ID SMALLINT NOT NULL, RECORD_ID VARCHAR(250) NOT NULL) ;
ALTER TABLE DSRC_RECORD_HKEY ADD CONSTRAINT DSRC_RECORD_HKEY_P PRIMARY KEY(OBS_ENT_HASH,DSRC_ID,RECORD_ID) ;
CREATE TABLE RES_FEAT_STAT (LENS_ID SMALLINT NOT NULL, LIB_FEAT_ID BIGINT NOT NULL, ECLASS_ID SMALLINT NOT NULL, NUM_RES_ENT MEDIUMINT NOT NULL, NUM_RES_ENT_OOM MEDIUMINT NOT NULL, CANDIDATE_CAP_REACHED CHAR(1) DEFAULT 'N' NOT NULL, SCORING_CAP_REACHED CHAR(1) DEFAULT 'N' NOT NULL) ;
ALTER TABLE RES_FEAT_STAT ADD CONSTRAINT RES_FEAT_STAT_PK PRIMARY KEY(LIB_FEAT_ID,LENS_ID,ECLASS_ID) ;
CREATE TABLE RES_ENT (RES_ENT_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, ECLASS_ID SMALLINT NOT NULL, INTEREST_LEVEL SMALLINT, CONFUSION_LEVEL SMALLINT, NUM_OBS_ENT MEDIUMINT, FIRST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_TOUCH_DT BIGINT, LOCKING_ID BIGINT NOT NULL, NODE_NAME VARCHAR(50) NOT NULL, LOCK_DSRC_ACTION CHAR(1)) ;
ALTER TABLE RES_ENT ADD CONSTRAINT RES_ENT_PK PRIMARY KEY(RES_ENT_ID,LENS_ID) ;
CREATE TABLE RES_ENT_OKEY (OBS_ENT_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, RES_ENT_ID BIGINT NOT NULL, ER_ID BIGINT NOT NULL, ERRULE_ID SMALLINT NOT NULL, MATCH_KEY VARCHAR(1000), MATCH_SCORE VARCHAR(250)) ;
ALTER TABLE RES_ENT_OKEY ADD CONSTRAINT RES_ENT_OKEY_PK PRIMARY KEY(OBS_ENT_ID,LENS_ID) ;
CREATE UNIQUE INDEX RES_ENT_OKEY_SK ON RES_ENT_OKEY(RES_ENT_ID, LENS_ID, OBS_ENT_ID) ;
CREATE TABLE RES_ENT_RKEY (RES_ENT_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, OBS_ENT_ID BIGINT NOT NULL) ;
ALTER TABLE RES_ENT_RKEY ADD CONSTRAINT RES_ENT_RKEY_PK PRIMARY KEY(RES_ENT_ID,LENS_ID,OBS_ENT_ID) ;
CREATE TABLE RES_FEAT_EKEY (RES_ENT_ID BIGINT NOT NULL, ECLASS_ID SMALLINT NOT NULL, LENS_ID SMALLINT NOT NULL, LIB_FEAT_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, UTYPE_CODE VARCHAR(50) NOT NULL, SUPPRESSED CHAR(1), USED_FROM_DT DATETIME NULL DEFAULT NULL, USED_THRU_DT DATETIME NULL DEFAULT NULL, FIRST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_SEEN_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE RES_FEAT_EKEY ADD CONSTRAINT RES_FEAT_EKEY_PK PRIMARY KEY(RES_ENT_ID,LENS_ID,LIB_FEAT_ID,UTYPE_CODE) ;
CREATE UNIQUE INDEX RES_FEAT_EKEY_SK ON RES_FEAT_EKEY(LIB_FEAT_ID, LENS_ID, ECLASS_ID, RES_ENT_ID, UTYPE_CODE) ;
CREATE TABLE RES_FEAT_LKEY (LIB_FEAT_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, ECLASS_ID SMALLINT NOT NULL, RES_ENT_ID BIGINT NOT NULL, UTYPE_CODE VARCHAR(50) NOT NULL) ;
ALTER TABLE RES_FEAT_LKEY ADD CONSTRAINT RES_FEAT_LKEY_PK PRIMARY KEY(LIB_FEAT_ID,LENS_ID,ECLASS_ID,RES_ENT_ID,UTYPE_CODE) ;
CREATE TABLE RES_RELATE (RES_REL_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, MIN_RES_ENT_ID BIGINT NOT NULL, MAX_RES_ENT_ID BIGINT NOT NULL, REL_STRENGTH SMALLINT, REL_STATUS SMALLINT, IS_DISCLOSED SMALLINT, IS_AMBIGUOUS SMALLINT, INTEREST_LEVEL SMALLINT, CONFUSION_LEVEL SMALLINT, LAST_ER_ID BIGINT, LAST_REF_SCORE SMALLINT, LAST_ERRULE_ID SMALLINT, MATCH_KEY VARCHAR(1000), MATCH_SCORE VARCHAR(250), MATCH_LEVELS VARCHAR(50), FIRST_SEEN_DT DATETIME NULL DEFAULT NULL, LAST_SEEN_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE RES_RELATE ADD CONSTRAINT RES_RELATE_PK PRIMARY KEY(RES_REL_ID) ;
CREATE TABLE RES_REL_EKEY (RES_ENT_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, REL_ENT_ID BIGINT NOT NULL, RES_REL_ID BIGINT NOT NULL) ;
ALTER TABLE RES_REL_EKEY ADD CONSTRAINT RES_REL_EKEY_PK PRIMARY KEY(RES_ENT_ID,LENS_ID,REL_ENT_ID) ;
CREATE TABLE RES_RELDET (RES_REL_ID BIGINT NOT NULL, KEY_TYPE_ID SMALLINT NOT NULL, KEY_ID BIGINT NOT NULL, RTYPE_ID SMALLINT NOT NULL, ERRULE_ID SMALLINT, SYS_CREATE_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE RES_RELDET ADD CONSTRAINT RES_RELDET_PK PRIMARY KEY(RES_REL_ID,KEY_TYPE_ID,KEY_ID) ;
CREATE TABLE RES_REL_COMP (RES_REL_ID BIGINT NOT NULL, LENS_ID SMALLINT NOT NULL, ER_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, CFRTN_ID SMALLINT NOT NULL, CFRTN_SCORE SMALLINT NOT NULL, CFRTN_LEVEL SMALLINT NOT NULL, INCOMING_FEAT_ID BIGINT NOT NULL, MATCHED_FEAT_ID BIGINT NOT NULL, FEAT_WEIGHT SMALLINT, TIME_SPACE_DIFF SMALLINT) ;
ALTER TABLE RES_REL_COMP ADD CONSTRAINT RES_REL_COMP_PK PRIMARY KEY(RES_REL_ID,LENS_ID,ER_ID,FTYPE_ID,CFRTN_ID) ;
CREATE TABLE LOG_OBS (OBS_ID BIGINT NOT NULL, OBS_STATUS_ID SMALLINT NOT NULL, OBS_SRC_KEY VARCHAR(250) NOT NULL, DSRC_ID SMALLINT NOT NULL, DSRC_ACTION CHAR(1), SRC_CREATE_DT DATETIME NULL DEFAULT NULL, SRC_LSTUPD_DT DATETIME NULL DEFAULT NULL, SRC_PRUNE_BEFORE_DT DATETIME NULL DEFAULT NULL, SRC_PRUNE_AFTER_DT DATETIME NULL DEFAULT NULL, SRC_LSTUPD_USER VARCHAR(25), NODE_NAME VARCHAR(50) NOT NULL, SYS_CREATE_DT DATETIME NULL DEFAULT NULL, SYS_LSTUPD_DT DATETIME NULL DEFAULT NULL) ;
ALTER TABLE LOG_OBS ADD CONSTRAINT LOG_OBS_PK PRIMARY KEY(OBS_ID) ;
CREATE TABLE LOG_OBS_ENT (OBS_ID BIGINT NOT NULL, OBS_ENT_ID BIGINT NOT NULL, FROM_LENS_ID SMALLINT, FROM_RES_ENT_ID BIGINT, SYS_ACTION CHAR(1)) ;
ALTER TABLE LOG_OBS_ENT ADD CONSTRAINT LOG_OBS_ENT_PK PRIMARY KEY(OBS_ID,OBS_ENT_ID) ;
CREATE TABLE LOG_ER (ER_ID BIGINT NOT NULL, ER_DT DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, OBS_ID BIGINT NOT NULL, DSRC_ACTION CHAR(1) NOT NULL, LENS_ID SMALLINT NOT NULL, OBS_ENT_ID BIGINT, RES_ENT_ID BIGINT, ASSG_RES_ENT_ID BIGINT) ;
ALTER TABLE LOG_ER ADD CONSTRAINT LOG_ER_PK PRIMARY KEY(ER_ID) ;
CREATE TABLE LOG_ER_STEP (ER_ID BIGINT NOT NULL, ER_STEP SMALLINT NOT NULL, ER_PROC_ID SMALLINT NOT NULL, OBS_ENT_ID BIGINT, RES_ENT_ID BIGINT) ;
ALTER TABLE LOG_ER_STEP ADD CONSTRAINT LOG_ER_STEP_PK PRIMARY KEY(ER_ID,ER_STEP) ;
CREATE TABLE LOG_ER_CAND (ER_ID BIGINT NOT NULL, ER_STEP SMALLINT NOT NULL, CAND_ENT_ID BIGINT NOT NULL, ERRULE_ID SMALLINT, RESOLVED SMALLINT, CONFLICTED SMALLINT) ;
ALTER TABLE LOG_ER_CAND ADD CONSTRAINT LOG_ER_CAND_PK PRIMARY KEY(ER_ID,ER_STEP,CAND_ENT_ID) ;
CREATE TABLE LOG_ER_CAND_EF (ER_ID BIGINT NOT NULL, ER_STEP SMALLINT NOT NULL, CAND_ENT_ID BIGINT NOT NULL, LIB_EFEAT_ID BIGINT NOT NULL) ;
ALTER TABLE LOG_ER_CAND_EF ADD CONSTRAINT LOG_ER_CAND_EF_PK PRIMARY KEY(ER_ID,ER_STEP,CAND_ENT_ID,LIB_EFEAT_ID) ;
CREATE TABLE LOG_ER_COMP (ER_ID BIGINT NOT NULL, ER_STEP SMALLINT NOT NULL, CAND_ENT_ID BIGINT NOT NULL, FTYPE_ID SMALLINT NOT NULL, CFRTN_ID SMALLINT NOT NULL, CFRTN_SCORE SMALLINT NOT NULL, CFRTN_LEVEL SMALLINT NOT NULL, BEHAVIOR_CODE VARCHAR(25) NOT NULL, INCOMING_FEAT_ID BIGINT NOT NULL, MATCHED_FEAT_ID BIGINT NOT NULL, FEAT_WEIGHT SMALLINT, TIME_SPACE_DIFF SMALLINT) ;
ALTER TABLE LOG_ER_COMP ADD CONSTRAINT LOG_ER_COMP_PK PRIMARY KEY(ER_ID,ER_STEP,CAND_ENT_ID,FTYPE_ID,CFRTN_ID) ;
CREATE TABLE LOG_ER_RES (ER_ID BIGINT NOT NULL, ER_ACTION_NUM SMALLINT NOT NULL, ER_ACTION_ID SMALLINT NOT NULL, ER_STEP SMALLINT, CAND_ENT_ID BIGINT, ERRULE_ID SMALLINT, OBS_ENT_ID BIGINT, FROM_RES_ENT_ID BIGINT, TO_RES_ENT_ID BIGINT, RES_REL_ID BIGINT) ;
ALTER TABLE LOG_ER_RES ADD CONSTRAINT LOG_ER_RES_PK PRIMARY KEY(ER_ID,ER_ACTION_NUM) ;
DELETE FROM SRD_PRODUCT_VERSIONS WHERE PRODUCT='PIPELINE';
INSERT INTO SRD_PRODUCT_VERSIONS VALUES('PIPELINE','4.3.0.7');
