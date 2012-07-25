# -*- coding: cp1251 -*-
#-------------------------------------------------------------------------------
# Name:        модуль1
# Purpose:
#
# Author:      sergey-dolzhkin
#
# Created:     14.07.2012
# Copyright:   (c) sergey-dolzhkin 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def getSattings(setFile):
    settingsArray=[]
    settingsFile = open (setFile, 'r')
    while True:
        line=settingsFile.readline()
        if not line:
            break
        while line[len(line)-1] == '\n' or line[len(line)-1] == ' ':
            line=line[:-1]
        setLine=line.split(':')[1]
        if len(setLine.split(','))>1:
            for i in range(0,len(setLine.split(','))):
                settingsArray.append(setLine.split(',')[i])
        else:
            settingsArray.append(setLine)
    settingsFile.close()
    return settingsArray
print getSattings('sattings.ini');

def createConf(basicFile, configFile, sattingsArray):
    basFile = open (basicFile, 'r')
    confFile = open (configFile, 'w')
    while True:
        line=basFile.readline()
        while len(line) >= 1 and (line[len(line)-1] == '\n' or line[len(line)-1] == ' '):
            line=line[:-1]
        if line =='interface gigabitEthernet':
            line = line+'0/0/0.'+sattingsArray[3]+'0'+sattingsArray[2]
        if line == ' qos-parameter INTERNET-BANDWIDTH-NOPPPOE':
            line=line+' '+str(int(sattingsArray[1])*1024*1024)
        if line == ' svlan id':
            line=line+' '+sattingsArray[3]+' '+sattingsArray[2]
        if line == ' ip description':
            line=line+' CORP_'+sattingsArray[0].upper()+'_IPOE'
        if line==' ip policy-parameter reference-rate INTERNET-RATE-NOPPPOE':
            line=line+' '+str(int(sattingsArray[1])*1024*1024)
        if (line=='ip route *.*.*.*  255.255.255.255 GigabitEthernet0/0/0.*') and (len(sattingsArray)>5):
            lineArray=line.split('*.*.*.*')
            lineArray[1]=lineArray[1][:-1]
            for i in range(4,len(sattingsArray)):
                line=lineArray[0]+sattingsArray[i]+lineArray[1]+sattingsArray[3]+'0'+sattingsArray[2]
                confFile.write(line+'\n')
        if (line=='ip route *.*.*.*  255.255.255.255 GigabitEthernet0/0/0.*'):
            lineArray=line.split('*.*.*.*')
            lineArray[1]=lineArray[1][:-1]
            line=lineArray[0]+sattingsArray[4]+lineArray[1]+sattingsArray[3]+'0'+sattingsArray[2]
        if line=='port vlan-stacking vlan * stack-vlan *':
            lineArray=line.split('*')
            line=lineArray[0]+sattingsArray[2]+lineArray[1]+sattingsArray[3]
        if line=="create vlan * tag":
            lineArray=line.split('*')
            line=lineArray[0]+sattingsArray[2]+lineArray[1]+' '+sattingsArray[2]
        if line=='conf vlan * add tagged 25-28':
            lineArray=line.split('*')
            line=lineArray[0]+sattingsArray[2]+lineArray[1]
        confFile.write(line+'\n')
        if not line:
            break
    basFile.close()
    confFile.close()

def createArchive(configFile, sattingsArray):
    confFile = open (configFile, 'r')
    archiveFile=open('archive/'+sattingsArray[0].upper()+'.txt','w')
    archiveFile.writelines((confFile.readlines()))
    archiveFile.close()
    confFile.close()

createConf('basic/basic.txt','config.txt', getSattings('sattings.ini'))
createArchive('config.txt', getSattings('sattings.ini'))