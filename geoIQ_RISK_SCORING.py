import pandas as pd
import numpy as np
import requests
import json
import time
import datetime
from datetime import datetime, date, time
import glob
import pickle


df = pd.read_parquet('/mnt/datascience/codes/Rakesh/Risk_Scoring/RISK_SCORE_PED_v02.parquet')
df2 = pd.read_parquet('/mnt/datascience/codes/Rakesh/Risk_Scoring/RISK_SCORE_AGE_SI_PROD_GRP_PED_v02.parquet')
df3 = pd.read_parquet('/mnt/datascience/codes/Rakesh/Risk_Scoring/CHANNEL_RISK_SCORE.parquet')

a = {'[<=25]': list(range(0, 26)), '[26, 29]': list(range(26, 30)), '[30, 33]': list(range(30, 34)), '[34, 37]': list(range(34, 38)), '[38, 40]': list(range(38, 41)), 
     '[41, 43]': list(range(41, 44)), '[44, 47]': list(range(44, 48)), '[48, 51]': list(range(48, 52)), '[52, 55]': list(range(52, 56)),  '[56, 60]': list(range(56, 61)),
     '[61, 65]': list(range(61, 66)), '[>=66]': list(range(66, 200))}

b = {'[<=1.9L]': list(range(999,199999)),
 '[2L]': list(range(199999, 200000)),
 '[200001, 3L]': list(range(200000, 300000)),
 '[300001, 4.9L]': list(range(300000, 499999)),
 '[5L]': list(range(499999, 500000)),
 '[500001, 9.9L]': list(range(500000, 999999)),
 '[10L]': list(range(999999, 1000000)),
 '[>10L]': list(range(1000000, 50000000))}

def age_grp(age):
    for key, value in a.items():
        if age in value:
            return(key)
        
def SI_grp(si):
    for key, value in b.items():
        if si in value:
            return(key)

def risk_category(si, product, age, pincode, channel, MED_TEST):
    age = age_grp(age)
    si = SI_grp(si)
    pincode = str(pincode)
    rs = df[(df['SI_GRP']==si) & (df['AGE_GRP']==age) & (df['PROD_GROUPING']==product) & (df['PINCODE']==pincode[:2]) & (df['MED_TEST']==MED_TEST)][['RISK_SCORE']]
    rs2 = df2[(df2['SI_GRP']==si) & (df2['AGE_GRP']==age) & (df2['PROD_GROUPING']==product) & (df['MED_TEST']==MED_TEST)][['RISK_SCORE']]
    if rs.shape[0]!=0:
        score = rs['RISK_SCORE'].values[0]
    else:
        score = rs2['RISK_SCORE'].values[0]
    
    
#    channel score
    chrs = df3[df3['CHANNEL_CODE']==channel][['RISK_SCORE']]
    if chrs.shape[0]!=0:
        chscore = chrs['RISK_SCORE'].values[0]
    else:
        if rs.shape[0]!=0:
            chscore = rs['RISK_SCORE'].values[0]
        else:
            chscore = rs2['RISK_SCORE'].values[0]
            
    if score < 0.1 and  chscore < 0.1:
        RISK_CAT = 'G'  #Both Policy and Agent are not Risky
    elif score <0.1 and chscore >= 0.1:
        RISK_CAT = 'A'  #Policy Not Risky, Agent Risky
    elif score >= 0.1 and chscore < 0.1:
        RISK_CAT = 'A'  #Policy Not Risky, Agent Risky
    else:
        RISK_CAT = 'R'  #Both Policy and Agent are Risky!!!
    return('RISK SCORING CATEGORY: ',RISK_CAT)

def geoiq_category(text1,text2):
    geoIQ_CAT = 'A'
    return(text1+text2)