CREATE TABLE SYS_CODES_USED (CODE_TYPE VARCHAR(25) NOT NULL, CODE VARCHAR(25) NOT NULL, CODE_ID smallint NOT NULL, PRIMARY KEY(CODE_TYPE, CODE)) ;
CREATE UNIQUE INDEX SYS_CODES_USED_SK ON SYS_CODES_USED(CODE_TYPE, CODE_ID) ;

