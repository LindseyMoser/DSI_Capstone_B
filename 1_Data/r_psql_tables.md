
## Load CSV Files into Tables:

COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2017_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2016_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2015_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';

COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2014_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2013_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';
COPY r_full FROM '/Users/moserfamily/Documents/DSI/DSI_Capstone_B/1_Data/form5500_data/F_SCH_R_2012_latest.csv' DELIMITER ',' CSV HEADER QUOTE '"';

## Alter column type:
ALTER TABLE r_full ALTER COLUMN LAST_OPIN_ADVISORY_SERIAL_NUM TYPE character varying(20);

## Drop columns not in 2015 and prior:
ALTER TABLE r_full
DROP COLUMN PEN_401K_DESIGN_BASED_SAFE_IND ,
DROP COLUMN PEN_401K_PRIOR_YEAR_ADP_IND ,
DROP COLUMN PEN_401K_CURRENT_YEAR_ADP_IND,
DROP COLUMN PEN_401K_NA_IND,
DROP COLUMN PEN_MTHD_RATIO_PRCNT_TEST_IND,
DROP COLUMN PEN_MTHD_AVG_BNFT_TEST_IND,
DROP COLUMN PEN_MTHD_NA_IND;

## Drop columns not in 2014 and prior:


## CREATE TABLE - ALL FIELDS:

CREATE TABLE r_full (
  ACK_ID character varying,
  SCH_R_PLAN_YEAR_BEGIN_DATE date,
  SCH_R_TAX_PRD character varying,
  SCH_R_PN int,
  SCH_R_EIN bigint,
  PEN_VALUE_DSTRB_PD_PRPTY_AMT numeric,
  PEN_PAYOR_01_EIN bigint,
  PEN_PAYOR_02_EIN bigint,
  PEN_BNFT_DISTRIB_SNGL_SUM_CNT bigint,
  PEN_ELEC_SATISFY_CODE_412_IND character varying,
  PEN_FNDNG_WVRS_DATE date,
  PEN_EMPLR_CONTRIB_RQR_AMT numeric,
  PEN_EMPLR_CONTRIB_PAID_AMT numeric,
  PEN_FUNDING_DEFICIENCY_AMT numeric,
  PEN_FUNDING_DEADLINE_IND character varying(1),
  PEN_CHG_FNDNG_METHOD_IND character varying(1),
  PEN_AMDMT_INCR_VAL_BNFT_CD character varying(1),
  PEN_SEC_REPAY_LOAN_IND character varying(1),
  ESOP_PREF_IND character varying(1),
  ESOP_BACK_TO_BACK_IND character varying(1),
  ESOP_STOCK_NOT_TRADABLE_IND character varying(1),
  PEN_NO_CONTRIB_CUR_YR_CNT bigint,
  PEN_NO_CONTRIB_PREV_YR_CNT bigint,
  PEN_NO_CONTRIB_2ND_PREV_YR_CNT bigint,
  PEN_NO_CONTRIB_CUR_PREV_PRCNT numeric,
  PEN_NO_CONTR_CUR_2ND_PREV_PRC numeric,
  PEN_EMPLRS_WITHDRW_PREV_CNT int,
  PEN_WITHDRW_LIAB_AMT numeric,
  PEN_ASSET_LIAB_TRANSFER_IND character varying(1),
  PEN_LIAB_MULT_PLANS_IND character varying(1),
  PEN_STOCK_PRCNT numeric,
  PEN_INVST_GRADE_DEBT_PRCNT numeric,
  PEN_HI_YLD_DEBT_PRCNT numeric,
  PEN_REAL_ESTATE_PRCNT numeric,
  PEN_OTH_ASSET_PRCNT numeric,
  PEN_AVERAGE_DURATION_CD character varying(1),
  PEN_DURATION_MEASURE_CD character varying(1),
  PEN_OTHER_DURATION_TYPE_TEXT character varying(25),
  F_401K_PLAN_IND character varying(1),
  F_401K_SATISFY_RQMTS_IND character varying(1),
  ADP_ACP_TEST_IND character varying(1),
  MTHD_USED_SATISFY_RQMTS_IND character varying(1),
  PLAN_SATISFY_TESTS_IND character varying(1),
  PLAN_TIMELY_AMENDED_IND character varying(1),
  LAST_PLAN_AMENDMENT_DATE date,
  TAX_CODE character varying(1),
  LAST_OPIN_ADVISORY_DATE date,
  LAST_OPIN_ADVISORY_SERIAL_NUM character varying(20),
  FAV_DETERM_LTR_DATE date,
  PLAN_MAINTAIN_US_TERRITORY_IND character varying(1),
  PEN_401K_DESIGN_BASED_SAFE_IND character varying(1),
  PEN_401K_PRIOR_YEAR_ADP_IND character varying(1),
  PEN_401K_CURRENT_YEAR_ADP_IND character varying(1),
  PEN_401K_NA_IND character varying(1),
  PEN_MTHD_RATIO_PRCNT_TEST_IND character varying(1),
  PEN_MTHD_AVG_BNFT_TEST_IND character varying(1),
  PEN_MTHD_NA_IND character varying(1)
  );
