
## LOAD CSV INTO TABLE:

COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2017_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2016_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2015_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';

COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2014_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2013_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2012_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';

COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2011_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2010_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY f5500_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/f_5500_2009_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';

## Drop columns that are only in 2017 file (not in 2016 or 2015):
ALTER TABLE f5500_full
DROP COLUMN LAST_RPT_PLAN_NAME,
DROP COLUMN SPONS_MANUAL_SIGNED_DATE,
DROP COLUMN SPONS_MANUAL_SIGNED_NAME,
DROP COLUMN DFE_MANUAL_SIGNED_DATE,
DROP COLUMN DFE_MANUAL_SIGNED_NAME;

## Drop columns not in 2014 and earlier files:
ALTER TABLE f5500_full
DROP COLUMN ADMIN_MANUAL_SIGNED_DATE,
DROP COLUMN ADMIN_MANUAL_SIGNED_NAME;

## Drop columns not in 2013 and earlier files:
ALTER TABLE f5500_full
DROP COLUMN TOT_ACT_PARTCP_BOY_CNT,
DROP COLUMN SUBJ_M1_FILING_REQ_IND,
DROP COLUMN COMPLIANCE_M1_FILING_REQ_IND,
DROP COLUMN M1_RECEIPT_CONFIRMATION_CODE;

## Drop columns not in 2011 and earlier files:
ALTER TABLE f5500_full
DROP COLUMN ADMIN_NAME_SAME_SPON_IND,
DROP COLUMN ADMIN_ADDRESS_SAME_SPON_IND,
DROP COLUMN PREPARER_NAME,
DROP COLUMN PREPARER_FIRM_NAME,
DROP COLUMN PREPARER_US_ADDRESS1,
DROP COLUMN PREPARER_US_ADDRESS2,
DROP COLUMN PREPARER_US_CITY,
DROP COLUMN PREPARER_US_STATE,
DROP COLUMN REPARER_US_ZIP,
DROP COLUMN PREPARER_FOREIGN_ADDRESS1,
DROP COLUMN PREPARER_FOREIGN_ADDRESS2,
DROP COLUMN PREPARER_FOREIGN_CITY,
DROP COLUMN PREPARER_FOREIGN_PROV_STATE,
DROP COLUMN PREPARER_FOREIGN_CNTRY,
DROP COLUMN PREPARER_FOREIGN_POSTAL_CD,
DROP COLUMN PREPARER_PHONE_NUM,
DROP COLUMN PREPARER_PHONE_NUM_FOREIGN;

## Drop columns not in 2010 and earlier files:
ALTER TABLE f5500_full
DROP COLUMN ADMIN_PHONE_NUM_FOREIGN,
DROP COLUMN SPONS_DFE_PHONE_NUM_FOREIGN;

## CREATE TABLE - ALL FIELDS:

CREATE TABLE f5500_full (
ACK_ID character varying(30),
FORM_PLAN_YEAR_BEGIN_DATE date,
FORM_TAX_PRD character varying(10),
TYPE_PLAN_ENTITY_CD character varying(1),
TYPE_DFE_PLAN_ENTITY_CD character varying(1),
INITIAL_FILING_IND character varying(1),
AMENDED_IND character varying(1),
FINAL_FILING_IND character varying(1),
SHORT_PLAN_YR_IND character varying(1),
COLLECTIVE_BARGAIN_IND character varying(1),
F5558_APPLICATION_FILED_IND character varying(1),
EXT_AUTOMATIC_IND character varying(1),
DFVC_PROGRAM_IND character varying(1),
EXT_SPECIAL_IND character varying(1),
EXT_SPECIAL_TEXT character varying(35),
PLAN_NAME character varying(500),
SPONS_DFE_PN smallint,
PLAN_EFF_DATE date,
SPONSOR_DFE_NAME character varying(70),
SPONS_DFE_DBA_NAME character varying(70),
SPONS_DFE_CARE_OF_NAME character varying(70),
SPONS_DFE_MAIL_US_ADDRESS1 character varying(35),
SPONS_DFE_MAIL_US_ADDRESS2 character varying(35),
SPONS_DFE_MAIL_US_CITY character varying(22),
SPONS_DFE_MAIL_US_STATE character varying(2),
SPONS_DFE_MAIL_US_ZIP character varying(12),
SPONS_DFE_MAIL_FOREIGN_ADDR1 character varying(35),
SPONS_DFE_MAIL_FOREIGN_ADDR2 character varying(35),
SPONS_DFE_MAIL_FOREIGN_CITY character varying(22),
SPONS_DFE_MAIL_FORGN_PROV_ST character varying(22),
SPONS_DFE_MAIL_FOREIGN_CNTRY character varying(2),
SPONS_DFE_MAIL_FORGN_POSTAL_CD character varying(22),
SPONS_DFE_LOC_US_ADDRESS1 character varying(35),
SPONS_DFE_LOC_US_ADDRESS2 character varying(35),
SPONS_DFE_LOC_US_CITY character varying(22),
SPONS_DFE_LOC_US_STATE character varying(2),
SPONS_DFE_LOC_US_ZIP character varying(12),
SPONS_DFE_LOC_FOREIGN_ADDRESS1 character varying(35),
SPONS_DFE_LOC_FOREIGN_ADDRESS2 character varying(35),
SPONS_DFE_LOC_FOREIGN_CITY character varying(22),
SPONS_DFE_LOC_FORGN_PROV_ST character varying(22),
SPONS_DFE_LOC_FOREIGN_CNTRY character varying(2),
SPONS_DFE_LOC_FORGN_POSTAL_CD character varying(22),
SPONS_DFE_EIN integer,
SPONS_DFE_PHONE_NUM character varying(10),
BUSINESS_CODE character varying(6),
ADMIN_NAME character varying(70),
ADMIN_CARE_OF_NAME character varying(70),
ADMIN_US_ADDRESS1 character varying(35),
ADMIN_US_ADDRESS2 character varying(35),
ADMIN_US_CITY character varying(22),
ADMIN_US_STATE character varying(2),
ADMIN_US_ZIP character varying(12),
ADMIN_FOREIGN_ADDRESS1 character varying(35),
ADMIN_FOREIGN_ADDRESS2 character varying(35),
ADMIN_FOREIGN_CITY character varying(22),
ADMIN_FOREIGN_PROV_STATE character varying(22),
ADMIN_FOREIGN_CNTRY character varying(2),
ADMIN_FOREIGN_POSTAL_CD character varying(22),
ADMIN_EIN integer,
ADMIN_PHONE_NUM character varying(10),
LAST_RPT_SPONS_NAME character varying(70),
LAST_RPT_SPONS_EIN integer,
LAST_RPT_PLAN_NUM smallint,
ADMIN_SIGNED_DATE character varying(30),
ADMIN_SIGNED_NAME character varying(35),
SPONS_SIGNED_DATE character varying(30),
SPONS_SIGNED_NAME character varying(35),
DFE_SIGNED_DATE character varying(30),
DFE_SIGNED_NAME character varying(35),
TOT_PARTCP_BOY_CNT integer,
TOT_ACTIVE_PARTCP_CNT integer,
RTD_SEP_PARTCP_RCVG_CNT integer,
RTD_SEP_PARTCP_FUT_CNT integer,
SUBTL_ACT_RTD_SEP_CNT integer,
BENEF_RCVG_BNFT_CNT integer,
TOT_ACT_RTD_SEP_BENEF_CNT integer,
PARTCP_ACCOUNT_BAL_CNT integer,
SEP_PARTCP_PARTL_VSTD_CNT integer,
CONTRIB_EMPLRS_CNT integer,
TYPE_PENSION_BNFT_CODE character varying(40),
TYPE_WELFARE_BNFT_CODE character varying(40),
FUNDING_INSURANCE_IND character varying(1),
FUNDING_SEC412_IND character varying(1),
FUNDING_TRUST_IND character varying(1),
FUNDING_GEN_ASSET_IND character varying(1),
BENEFIT_INSURANCE_IND character varying(1),
BENEFIT_SEC412_IND character varying(1),
BENEFIT_TRUST_IND character varying(1),
BENEFIT_GEN_ASSET_IND character varying(1),
SCH_R_ATTACHED_IND character varying(1),
SCH_MB_ATTACHED_IND character varying(1),
SCH_SB_ATTACHED_IND character varying(1),
SCH_H_ATTACHED_IND character varying(1),
SCH_I_ATTACHED_IND character varying(1),
SCH_A_ATTACHED_IND character varying(1),
NUM_SCH_A_ATTACHED_CNT character varying(4),
SCH_C_ATTACHED_IND character varying(1),
SCH_D_ATTACHED_IND character varying(1),
SCH_G_ATTACHED_IND character varying(1),
FILING_STATUS character varying(50),
DATE_RECEIVED character varying(10),
VALID_ADMIN_SIGNATURE character varying(54),
VALID_DFE_SIGNATURE character varying(54),
VALID_SPONSOR_SIGNATURE character varying(54),
ADMIN_PHONE_NUM_FOREIGN character varying(30),
SPONS_DFE_PHONE_NUM_FOREIGN character varying(30),
ADMIN_NAME_SAME_SPON_IND character varying(1),
ADMIN_ADDRESS_SAME_SPON_IND character varying(1),
PREPARER_NAME character varying(35),
PREPARER_FIRM_NAME character varying(35),
PREPARER_US_ADDRESS1 character varying(35),
PREPARER_US_ADDRESS2 character varying(35),
PREPARER_US_CITY character varying(22),
PREPARER_US_STATE character varying(2),
PREPARER_US_ZIP character varying(12),
PREPARER_FOREIGN_ADDRESS1 character varying(35),
ARER_FOREIGN_ADDRESS2 character varying(35),
PREPARER_FOREIGN_CITY character varying(22),
PREPARER_FOREIGN_PROV_STATE character varying(22),
PREPARER_FOREIGN_CNTRY character varying(2),
PREPARER_FOREIGN_POSTAL_CD character varying(22),
PREPARER_PHONE_NUM character varying(10),
PREPARER_PHONE_NUM_FOREIGN character varying(30),
TOT_ACT_PARTCP_BOY_CNT integer,
SUBJ_M1_FILING_REQ_IND character varying(1),
COMPLIANCE_M1_FILING_REQ_IND character varying(1),
M1_RECEIPT_CONFIRMATION_CODE character varying(12),
ADMIN_MANUAL_SIGNED_DATE character varying(30),
ADMIN_MANUAL_SIGNED_NAME character varying(35),
LAST_RPT_PLAN_NAME character varying(80),
SPONS_MANUAL_SIGNED_DATE character varying(30),
SPONS_MANUAL_SIGNED_NAME character varying(35),
DFE_MANUAL_SIGNED_DATE character varying(30),
DFE_MANUAL_SIGNED_NAME character varying(35)
);
