#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import math
import pandas as pd
import os
import json
import glob
from csv import DictWriter
import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon


# In[ ]:


def distance(x1, y1, x2, y2):
    result = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return result


# # degree

# In[ ]:


dir_path = input('파일 경로를 입력해주세요 : ')

dataFrame_add = None
dataFrame_add_2 = None

# file_load
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        file_path = os.path.join(root, file)
        
        # jpg_size
        if '.jpg' in file_path:
            jpg_file_name = os.path.splitext(file)[0]
            jpg_size = os.path.getsize(file_path)
            
            contents_2 = [jpg_file_name, jpg_size]
            dataFrame_add_2 = pd.concat([pd.DataFrame(contents_2).transpose(), dataFrame_add_2])
            
        if '.json' in file_path:
            json_files = file_path
            file_name = os.path.splitext(file)[0]
            gate = file_name.split('_')[3]
            
            
            # read_json
            with open(json_files, encoding="UTF-8-sig") as f:
                json_data = json.load(f)

                for item in json_data["annotations"] :            
                    if item["bbox"]["classid"] in 'BIC':
                        
                        if item["bbox"]["ocrdirection"] == '0':
                            x1 = item["bbox"]["points"][0][0]
                            y1 = item["bbox"]["points"][0][1]
                            x2= item["bbox"]["points"][1][0]
                            y2 = item["bbox"]["points"][1][1]
                            
                            lenx = distance(x1,y1,x2,y2)
                            leny = distance(x1,y1,x2,y1)
                            lenz = distance(x2,y2,x2,y1)

                            seta = math.degrees(math.acos(leny/lenx))
                            seta_data= abs(90-round(seta, 3))
                            
                        else:
                            x1 = item["bbox"]["points"][0][0]
                            y1 = item["bbox"]["points"][0][1]
                            x2= item["bbox"]["points"][3][0]
                            y2 = item["bbox"]["points"][3][1]

                            lenx = distance(x1,y1,x2,y2)
                            leny = distance(x1,y1,x1,y2)
                            lenz = distance(x2,y2,x1,y2)

                            seta = math.degrees(math.acos(leny/lenx))
                            seta_data= abs(90-round(seta, 3))

                        
                        x3= item["bbox"]["points"][2][0]
                        y3 = item["bbox"]["points"][2][1]
                        

                        if y2>y3:
                            nomal_data = 1
                        elif x1>x3 or y1>y3:
                            nomal_data = 1
                        elif leny < lenz:
                            nomal_data = 1
                        else:
                            nomal_data = 0
            
            
                        # DataFrame
                        contents = [file_name, seta_data, nomal_data, gate]
                        dataFrame_add = pd.concat([pd.DataFrame(contents).transpose(), dataFrame_add])
                        

# csv
dataFrame_add.columns = ['File_Name', 'Degree', 'Normal', 'Divison']
dataFrame_add_2.columns = ['File_Name', 'Jpg_Size']

dataFrame = pd.merge(dataFrame_add,dataFrame_add_2)
ran = list(range(0,len(dataFrame.index)))
dataFrame.index = ran

dataFrame.sort_values(by=['Normal', 'Degree', 'Jpg_Size'],ascending=[False, True, True],inplace=True)
dataFrame['Rank'] = ran

dataFrame.to_csv("{}/makefromJson.csv".format(dir_path), sep=",", index=True, encoding="UTF-8-sig")


# # plot

# In[ ]:


fig = plt.figure(figsize=(15, 15))
annotations=["A","B","C","D"]
num = 0

json_files = glob.glob("{}/*.json".format(dir_path))

for i in range(0,len(json_files)):
    with open(json_files[i], encoding="UTF-8-sig") as f:
        json_data = json.load(f)
        file_name = os.path.basename(json_files[i])[:-5]
        
        for item in json_data["annotations"] :
            ring = LinearRing(item["bbox"]["points"])
            x,y = ring.xy
            num += 1

            ax = fig.add_subplot(len(json_files)//(len(json_files)//2),len(json_files)//2+1, num)
            ax.plot(x, y, color='#e35f62', linewidth=3, solid_capstyle='round', zorder=2)
            plt.axis('scaled')
            plt.gca().invert_yaxis() #y축 반전
            for i, label in enumerate(annotations):
                plt.text(x[i], y[i],label)
            for k in item["bbox"]["points"]:
                plt.axhline(k[1],0,1, color='r', linestyle='--', alpha=0.4)
                plt.axvline(k[0],0,1, color='b', linestyle='--', alpha=0.4)

