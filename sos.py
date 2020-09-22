import csv
import os
import pandas as pd
import numpy as np
import json
import codecs
from helpers import *
import sys

export = open('export.json')
data = json.load(codecs.open('export.json', 'r+', 'utf-8-sig'))
jsonoutput = open('edited.json', mode='w')


if get_phase(data) != 5:
    sys.exit('Please sim to draft first.')

year = str(get_current_year(data))

f = open(year+ "schedule.csv", "r")
f2 = open(year+"standings.csv","r")
f3 = open(year+"standings.csv","r")
schedule=list(csv.reader(f))
records=list(csv.reader(f2))
records_now=list(csv.reader(f3))



with open('abbrev.csv', mode='r') as infile:
    reader = csv.reader(infile)
    with open('coors_new.csv', mode='w') as outfile:
        mydict = {rows[1]:rows[0] for rows in reader}

o = open("fsn.txt", "w+")

def write_team(df,team):
    o.write("**{0}. {1}**\n".format(int(df.loc[team,"sos_rank"]),team))
    o.write("SOS: {0}\n".format(round(df.loc[team,"sos"],3)))


def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)



teams=[]
for i in range(1,len(schedule)):
    teams.append(schedule[i][0])


#sort teams alphabetically and assign tid
tid_list={}
i=0
for t in sorted(teams):
    tid_list[t]={}
    tid_list[t]["tid"]=i
    i+=1


counter=0
for i in range(0,len(records),1):

    team=records[i][0]
    try:
        a = team[-1]
    except:
        team='dummy'
    if team[-1] in ['x','y','o','z']:
        team=team[:-2]
    if hasNumbers(team):
        team=team[3:]
        if team in teams:
            tid_list[team]["playoffs"] = 1
    elif team in teams:
        tid_list[team]["playoffs"] = 0

    if team in teams:
        tid_list[team]["wins"]=records[i][1]
        tid_list[team]["losses"]=records[i][2]
        print(team)
        tid_list[team]["winrate"]=float(records[i][1])/(float(records[i][2])+float(records[i][1])) #winrate
        counter+=1


print('Parsed '+ str(counter) + ' teams.')

b={}
for i in range(1,len(schedule)):

    tid_list[schedule[i][0]]["sos"]=0
    a=[]
    for j in range(1,len(schedule[0])):
    #for j in range(1,len(schedule[0])):
        team=schedule[i][j]
        if team=="BYE":
            continue
        elif team[0]=="@":
            team=team[1:]
        print(team)
        tid_list[schedule[i][0]]["sos"]+=tid_list[team]["winrate"]


        a.append((team,tid_list[team]["winrate"],tid_list[team]["wins"],tid_list[team]["losses"]))
    #print("\n"+schedule[i][0])
    a = sorted(a, key=lambda a_entry: a_entry[1])
    #print(a)
    b[team]=a
    tid_list[schedule[i][0]]["sos"]=tid_list[schedule[i][0]]["sos"]/16

#print(b["Detroit Muscle"][15])
print('sos done')
df=pd.DataFrame(tid_list)

df=df.T

cols=["wins","losses","winrate","sos", "playoffs","tid"]
df=df[cols]
#print(df.sort_values('tid',ascending=True))
print('df done')


print(df.sort_values('tid')['sos'])

#didnt make playoffs(tiebreakers)
df.loc["Pittsburgh Rivers"]['playoffs']=0
df.loc["Tampa Turtles"]['playoffs']=0
#made playoffs(tiebreakers)
df.loc["Philadelphia Liberty"]['playoffs']=1
#won 1 playoff game
df.loc["Los Angeles Earthquakes"]['playoffs']=2
df.loc["Mexico City Aztecs"]['playoffs']=2
df.loc["Pittsburgh Rivers"]['playoffs']=2
df.loc["Denver High"]['playoffs']=2
# won 2 playoff games
df.loc["Minneapolis Blizzard"]['playoffs']=3
df.loc["Montreal Mounties"]['playoffs']=3
# won 3 playoff games
df.loc["Phoenix Vultures"]['playoffs']=5
df.loc["New York Bankers"]['playoffs']=4


df=df.sort_values(["playoffs","winrate","sos"],ascending=[True,True,True])
#df['pick']=df.rank()
df['pick'] = np.arange(1,len(df)+1)
#print(df)

df["sos_rank"]=df["sos"].rank()

df["owner"]=df["tid"]



#f3=open("sos_out.csv","w+")
df.to_csv("sos_out.csv")
df.to_excel("sos_out.xlsx")

#write_team(df,"Detroit Muscle")
df=df.reset_index()






for pick in data['draftPicks']:
    if pick['season']==get_current_year(data):
        pick['pick']=int(df.loc[df.tid == pick['originalTid'],'pick'].values[0])
        if pick['round'] == 1 and pick['originalTid'] != pick['tid']:
            df.loc[df.tid == pick['originalTid'],'owner']=pick['tid']
json.dump(data, jsonoutput, indent=0)


df.index.name = 'newhead'
print(df)
print(df.loc[df.tid==0,"index"].values[0])


for index, row in pd.DataFrame(np.arange(160).reshape(32,5))[::-1].iterrows():
    if df.loc[index,"tid"] == df.loc[index,"owner"]:
        print('{0}. :{2}: @{1}'.format(index+1,df.loc[index,"index"],mydict[df.loc[index,"index"]]))
    else:
        print('{0}. :{2}: @{1} (from :{4}: {3})'.format(index+1,df.loc[df.tid==df.loc[index,"owner"],"index"].values[0],mydict[df.loc[df.tid==df.loc[index,"owner"],"index"].values[0]],df.loc[index,"index"],mydict[df.loc[index,"index"]]))




























    #print("
