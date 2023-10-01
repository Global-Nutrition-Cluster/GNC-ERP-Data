import pandas as pd
import numpy as np
import os

GNCERPKOBOID = str(os.environ.get("GNCERPKOBOID"))

DataURL = "https://eu.kobotoolbox.org/api/v2/assets/"+GNCERPKOBOID+"/export-settings/es9pvn4L6wPbZVR3wawTjB5/data.xlsx"
print(DataURL)

KoboData = pd.read_excel(DataURL)

stepCols = ['Action','Status','Due date','Responsible entity','Cost','_id','_index']


def getBlockData(groupe, step):
    # groupe = _11 and i=1
    frames = []
    for i in [1,2,3,4,5,6]:
        col = groupe + str(i)
        cols = [col, col+'_Status',col+'_Due_date_Timeframe',col+'_Responsible_entity',col+'_Cost','_id','_index']
        try:
            df = KoboData[cols]
            df.columns = stepCols
            Data = df.dropna(subset=["Action"])
            Data.loc[:,'Step']= step #'_1_Risk_Analysis_and_Monitoring'
            if i <= 3 :
                Data.loc[:,'Type'] = 'MPAs'
            else :
                Data['Type'] = 'APAs'
            frames.append(Data)
            stepData = pd.concat(frames)
        except Exception :
            pass

    return stepData

groupes=["_11", "_21", "_31","_32","_33","_34","_35","_41","_51","_52","_53","_54","_55","_61"]
steps = ["_1_Risk_Analysis_and_Monitoring", 
         "_2_Building_scenario_",
         "3.1.Coordination", "3.2.Information management", "3.3.Needs assessments","3.4.Response provision","3.5. Funding",
         "_4_Response_analysis_ly_response_planning",
         "5.1.Coordination", "5.2.Information management", "5.3.Needs assessments","5.4.Response provision","5.5. Funding and resources mobilization",
         "6.ERP plan document development"]

actions = ['1.Risk Analysis and Monitoring', 
          '2.Building scenario', 
          '3.Mapping existing capacities', 
          '4.Response analysis and early response planning',
          '5.Planning for operational arrangements',
          '6.ERP plan document development']

def getRelatedAction(id):
    action = ""
    if id <=1:
        action = actions[id]
    elif 2 <= id <= 6:
        action = actions[2]
    elif id == 7:
        action = actions[3]
    elif 7 < id <= 12 :
        action = actions[4]
    else : 
        action = actions[5]
    return action

def getERPPreparednessAction():
    stepsFrames = []
    start = 0
    while start <= len(groupes)-1:
        stepData = getBlockData(groupes[start], steps[start])
        stepData['Section'] = getRelatedAction(start)
        stepsFrames.append(stepData)
        start+=1

    stepsAllData = pd.concat(stepsFrames)

    stepsAllData.to_csv("PrepardenessActions.csv")
    print("=== Data successfully written ==")
    return True

