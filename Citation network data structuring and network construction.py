# -*- coding: utf-8 -*-
"""
Created on Fri Jun 24 15:44:22 2022

@author: edvar
"""
"""
Edvard August Eggen Sveum
FU Berlin
Matricelnummber: 5501132
"""
import pandas as pd
import jsonlines
import json
from difflib import get_close_matches
import numpy as np
import string
import random
import time
import datetime as dt

#path_or_buf = 'D:/OneDrive/Python/Master/Patent test/Export_test.jsonl'

def JsonLRead(path):
    List_of_patent_dictionaries = []
    with jsonlines.open(path) as reader:
        for obj in reader:
            List_of_patent_dictionaries.append(obj)
    reader.close()
    return List_of_patent_dictionaries
#Lidar_test_list = JsonLRead(path_or_buf) #added to be able to work with a smaller dataset
def JsonLRead_G(path_l):
    List_of_patent_dictionaries = []
    for path in path_l:
        with jsonlines.open(path) as reader:
            for obj in reader:
                List_of_patent_dictionaries.append(obj)
        #reader.close()
    return pd.json_normalize(List_of_patent_dictionaries)

Paths_G =  [
    'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/Full Data/Only Granted Patents/Granted Extended/Extended_exporv2t1900-2009.jsonl',
    'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/Full Data/Only Granted Patents/Granted Extended/Extended_exporv2t2009-2015.jsonl',
    'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/Full Data/Only Granted Patents/Granted Extended/Extended_exporv2t2015-2020.jsonl',
    'D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/Full Data/Only Granted Patents/Granted Extended/Extended_exporv2t2020-2022.jsonl'
             ]

"""
def Un_pack_all_patents(data, SF_l, SE_l, Jur_list):
    Ind = 0
    DF = pd.DataFrame(columns = ['jurisdiction','date','doc key','family S', 'family E', 'cited by','lens_id','application_reference', 'application_reference date'])
    for i, d in enumerate(data):
        Jur_int = 0

        
        if 'claims' in d['biblio']['priority_claims'].keys():
            for Priorty_jur in d['biblio']['priority_claims']['claims']: #jur_de in d['families']['simple_family']['members']:  checks patent jurisdiction, if the Juristictions are included within a patent familiy or the jurisdiction of the patent in question the patent data will be unpacked 
                if Priorty_jur['jurisdiction'] in Jur_list and 'claim':
                #jur_de['document_id']['jurisdiction']in Jur_list or d['jurisdiction'] in Jur_list:
                    Jur_int = Jur_int + 1
       
        if Jur_int > 0:
            
            Patent_biblo = d['biblio']
            if 'kind' in d.keys() and 'kind' in Patent_biblo['application_reference'].keys():
                PIP2 = Patent_biblo['application_reference']['jurisdiction']+Patent_biblo['application_reference']['doc_number'] +' '+ Patent_biblo['application_reference']['kind']
                PIP = d['jurisdiction']+d['doc_number'] +' '+ d['kind']
            elif 'kind' in d.keys() and 'kind' not in Patent_biblo['application_reference'].keys():
                PIP = d['jurisdiction']+d['doc_number'] +' '+ d['kind']
                PIP2 = Patent_biblo['application_reference']['jurisdiction']+Patent_biblo['application_reference']['doc_number']


            else:
                PIP2 = Patent_biblo['application_reference']['jurisdiction']+Patent_biblo['application_reference']['doc_number']
                PIP = d['jurisdiction']+d['doc_number']

            DF.at[PIP,'jurisdiction'] = d['jurisdiction']
            DF.at[PIP,'lens_id'] = d['lens_id']
            #DF.at[PIP,'kind'] = d['kind']
            if 'applicants' in Patent_biblo['parties'].keys():
                DF.at[PIP,'Applicants'] = Patent_biblo['parties']['applicants']
    
            DF.at[PIP,'publication_type'] = d['publication_type']
            if 'classifications_cpc' in Patent_biblo.keys():
                for clasific in Patent_biblo['classifications_cpc']['classifications']:
                    DF.at[PIP, clasific['symbol']] = 1
            else:
                pass
            #DF.at[PIP,'classifications_cpc'] = Patent_biblo['classifications_cpc']
            if 'date_published' in d: 
                DF.at[PIP,'date'] = datetime.datetime.strptime(d['date_published'] ,'%Y-%m-%d')
            else:
                        pass
            if 'doc_key' in d.keys():                        
                DF.at[PIP,'doc key'] = d['doc_key'] 
            else:
                pass
            DF.at[PIP,'application_reference'] = PIP2
            if 'date' in Patent_biblo['application_reference'].keys():
                DF.at[PIP,'application_reference date']= Patent_biblo['application_reference']['date']
            if len(d['biblio']['cited_by']) > 0:
                DF.at[PIP,'cited by'] = d['biblio']['cited_by']['patents'] 
            if DF.loc[PIP,'family S'] != str:
                Ind = Ind + 1

                DF.at[PIP, 'family S'] = SF_l[Ind]
                DF.at[PIP, 'family E'] = SE_l[Ind]
                for fm in d['families']['simple_family']['members']:
                    DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'family S'] = SF_l[Ind]
                    DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'lens_id'] = fm['lens_id']
                    if 'date' in fm['document_id'].keys():
                        DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'date'] =  datetime.datetime.strptime(fm['document_id']['date'],'%Y-%m-%d')
                    else :
                        pass
                for fm in d['families']['extended_family']['members']:
                    DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'family E'] = SE_l[Ind]
                    DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'lens_id'] = fm['lens_id']
                    if 'date' in fm['document_id'].keys():
                        DF.at[fm['document_id']['jurisdiction']+fm['document_id']['doc_number']+' '+fm['document_id']['kind'],'date'] =  datetime.datetime.strptime(fm['document_id']['date'],'%Y-%m-%d')
                    else:
                        pass
                if 'priority_claims' in d['biblio'].keys():
                    if 'claims' in d['biblio']['priority_claims'].keys(): 
                        for p in d['biblio']['priority_claims']['claims']:
                            if 'date' in p.keys():
                                DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'priority date'] = datetime.datetime.strptime( p['date'],'%Y-%m-%d')
                            else:
                                pass
                            if 'jurisdiction' in p.keys():
                                DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'jurisdiction'] = p['jurisdiction']
                            else:
                                pass
                            DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'priority'] = 'True'
                            if 'sequence' in p.keys():
                                DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'sequence'] = p['sequence']
                            else:
                                pass
                            DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'family S'] = SF_l[Ind]
                            DF.at[p['jurisdiction']+' '+p['doc_number']+' '+p['kind'],'family E'] = SE_l[Ind]
                    else:
                        pass
                else: 
                   pass
                   #Ind = Ind + 1
            elif type(DF.loc[PIP,'family S']) == str:
                pass
            
        elif Jur_int == 0:
            pass
        print(i/len(data)*100,'% of dataset restructrued') # only added to function as progress bar
    return DF
"""
def fam_name(NN):
    SF = []
    #SE = []
    while NN > len(SF):
        test = list(string.ascii_lowercase)
        random.shuffle(test)
        numb = np.random.randint(0,10000)
        fs_name = str(numb) + test[0]
        #fe_name = str(numb) + test[1] + test[2]
        if (fs_name not in SF): #& (fe_name not in SE)
            SF.append(str(fs_name))
            #SE.append(fe_name)
    return SF#, #SE

DF_Patents = JsonLRead_G(Paths_G)

SF = fam_name(160000)
Jur_list = ['US','DE','JP','KR']

#Patent_data = Un_pack_all_patents(Datalist, SF, SE, Jur_list)
#Patent_data.to_json('Citation_prep.json')
#Test =  Un_pack_all_patents(Lidar_test_list, SF, SE, Jur_list)


##### a shorter version of the code to assign Patent family IDs and set patent IDs as index values 

def set_index_Patent_id(Df):
    return Df.set_index(Df['Patent Jur']+Df['doc_number']+Df['kind'])


def Priority_Patents_info(Df):
    priotiry_normalised1 = pd.json_normalize(Df['biblio.priority_claims.claims'])
    PN2 = pd.json_normalize(priotiry_normalised1[0])
    temp = pd.DataFrame()
    Date = PN2['date']
    temp['ID'] = PN2['jurisdiction']+PN2['doc_number']+PN2['kind']
    Jur = PN2['jurisdiction']
    Df_new =  pd.concat([Df,Date,temp,Jur],axis=1)
    return Df_new


def Priority_Patents_info2(Df):
    New_df = pd.DataFrame()
    Df = Df[pd.notnull(Df['biblio.priority_claims.claims'])]
    for indexN, index in enumerate(Df.index):
        PN = pd.json_normalize(Df.at[index,'biblio.priority_claims.claims'])
        #PN = PN.set_index(PN['jurisdiction']+PN['doc_number']+PN['kind'])
        if 'date' in PN.columns:
            PN2 = PN[pd.notnull(PN['date'])]
            PN3 = PN2[PN2['date'] == PN2['date'].min()]
            PN3 = PN3[PN3['sequence'] ==  PN3['sequence'].min()]
            temp = pd.DataFrame(data = [index], columns= ['ID'])
            #Date = PN2['date']
            #if 'kind' in PN2.columns:
             #   if 'jurisdiction' in PN2.columns:
              #      if 'doc_number' in PN2.columns:
              #          temp['PA'] = PN2['jurisdiction']+PN2['doc_number']+PN2['kind']
            #Jur = PN2['jurisdiction']
            Temp =  pd.concat([temp,PN3], axis = 1)
            #print(Temp)
            New_df = pd.concat([New_df,Temp],ignore_index=True)
        print(indexN/len(Df.index)*100,'% of dataset restructrued')
    return New_df



DF_Patents = DF_Patents.drop(columns=(['abstract'])).rename(columns={'jurisdiction':'Patent Jur'})
DF_Patents = DF_Patents.drop_duplicates(subset = 'lens_id',keep='first')
PPV1 = Priority_Patents_info2(DF_Patents)
PPV1.to_excel('Priotiry_Patents.xlsx')
PPV1 = PPV1.dropna(subset = ['ID'])
PPV1 = PPV1.rename(columns= {'lens_id':'lens_id_P',  'doc_number':'doc_number_P', 'kind':'kind_P'})
PPV1 = PPV1.set_index('ID')

#DF_Patents = DF_Patents.drop(columns=(['date','jurisdiction']))
#DF_Patents = set_index_Patent_id(DF_Patents)
DF_Patents.to_json('Citation_CPFv1.json')
New_DF = pd.concat([DF_Patents, PPV1], axis = 1)
#New_DF = pd.merge(DF_Patents, PPV1,how='outer')
def asign_patent_families_S(Df, SF, Jur):
    Df['SF']  = np.NAN
    for index, index_v in enumerate(Df.index):
        if pd.isnull(Df.at[index_v, 'SF']):
            #if Df.at[index_v, 'jurisdiction'] in Jur:
            TFDF = pd.json_normalize(Df.at[index_v, 'families.simple_family.members'])
            TFDF = TFDF.set_index(TFDF['document_id.jurisdiction']+TFDF['document_id.doc_number']+TFDF['document_id.kind'])
            for sub_index_v in TFDF.index:
                Df.at[sub_index_v, 'SF'] = SF[index]
                if pd.DataFrame(Df.at[sub_index_v, 'date_published']):

                            #Df.at[sub_index_v, 'lens_id'] = TFDF.at[sub_index_v,'lens_id']
                        Df.at[sub_index_v, 'date_published'] = TFDF.at[sub_index_v,'document_id.date']
                           # Df.at[sub_index_v, 'Patent Jur'] = TFDF.at[sub_index_v,'document_id.jurisdiction']
        print(index/len(Df.index)*100,'% of dataset restructrued')
    return Df


def asign_patent_families_S2(Df, SF):
    #Df['SF']  = np.NAN
    Df = Df.dropna(subset = ['families.simple_family.members'])
    Temp = pd.DataFrame()
    for index, index_v in enumerate(Df.index):
        if Df.at[index_v,'lens_id'] in Temp :
            pass
        else:
            TFDF = pd.json_normalize(Df.at[index_v, 'families.simple_family.members'])
            TFDF = TFDF.set_index(TFDF['document_id.jurisdiction']+TFDF['document_id.doc_number']+TFDF['document_id.kind'])
            TFDF['SF'] = SF[index]
            Temp = pd.concat([Temp, TFDF])
        print(index/len(Df.index)*100,'% of dataset restructrued')
    return  Temp
# = DF_Patents.drop_duplicates(subset = 'lens_id',keep = 'first')
Temp = asign_patent_families_S2(DF_Patents, SF)
Temp['ID'] = Temp.index
Temp = Temp.rename(columns=({'document_id.jurisdiction':'Patent Jur','document_id.doc_number':'doc_number','document_id.date':'date_published','document_id.kind':'kind'}))
Temp = Temp.drop_duplicates(subset='ID', keep = 'first')
#DF_Patents['ID'] = DF_Patents.index
#DF2_Patents = pd.merge(DF_Patents, Temp, how= 'outer')
#DF_Patents.to_json('Citation_CPF2.json')
Temp.to_csv('Patent_families_and_total_patents.csv')
#DF2_Patents.to_json('Citation_CPF2v1.json')
#DF2_Patents = DF2_Patents.set_index(DF2_Patents['ID'])

#DF2v1_Patents = pd.merge(DF_Patents, Temp, how= 'outer')
#DF2v1_Patents = DF2v1_Patents.set_index(DF2v1_Patents['ID'])
#DF2v1_Patents = DF2v1_Patents.drop(DF2v1_Patents['lens_id'])
#DF2v1_Patents.to_json('Citation_CPF2v1.json')
DF_F = pd.merge(Temp, New_DF, how = 'left')
DF_F = DF_F.dropna(subset=['ID'])
DF_F = DF_F.set_index(DF_F['ID'])
DF_F.to_json('Cition_test.json')
#Tester = pd.read_json('Citation_CPF2.json')
"""
def asign_patent_families_E(Df, SE): #not need, will only consider simple patent families for the sake of simplisity
    Df['SF']  =  0 #np.ones
    for index, index_v in enumerate(Df.index):
        if Df.at[index_v, 'SF'] == 0:
            Df.at[index_v, 'SF'] = SF[index]
            for V in Df['families.extended_family.members'][index_v]:
                v = V['document_id']
                if 'jurisdiction' and 'doc_number' and 'kind' not in v.keys():
                    pass
                elif 'jurisdiction' and 'doc_number' in v.keys():
                    Df.at[v['jurisdiction']+v['doc_number'], 'SF'] = SF[index]
                elif 'jurisdiction' and 'doc_number' and 'kind' in v.keys(): 
                    Df.at[v['jurisdiction']+v['doc_number']+v['kind'], 'SF'] = SF[index]
    return Df
"""
#DF2_Patents = DF2_Patents.reset_index()
def Mark_priority(Df, Jur):
    rel_jur = Df[(Df['jurisdiction'].isin(Jur)) & (Df['publication_type'] == 'GRANTED_PATENT')]
    Marker = pd.DataFrame()
    for i, SF in enumerate(set(rel_jur['SF'].values)):
        Sub = rel_jur[rel_jur['SF'] == SF]
        RSub = Sub[Sub['Patent Jur'].isin(Jur)]
        RSub = RSub[RSub['date_published']== RSub['date_published'].min()]
        ID = RSub.index
        tempID = pd.DataFrame(data=[ID])
       #tempM = pd.DataFrame(data = ['Include'])
        #temp = pd.concat([tempID, tempM],axis = 1)
        Marker = pd.concat([Marker, tempID])
        print(i/len(set(rel_jur['SF'].values))*100,'% of dataset restructrued')
    Marker['Marker'] = 'Include'
    return Marker
Patent_Marker = Mark_priority(DF_F, Jur_list)
Patent_Marker = Patent_Marker.rename(columns={0:'ID'}).drop(columns=[1,2,3])
Patent_Marker = Patent_Marker.dropna(subset= ['ID'])
Patent_Marker = Patent_Marker.set_index('ID')
#DF_F2 = pd.concat([DF_F, Patent_Marker],axis = 1)
#DF_F2 = pd.merge(Patent_Marker, DF_F)

#DF2_Patents.to_json('Citation_CPF3.json')

def Mark_priority2(Df, Jur): #Do not use
    rel_jur = Df[(Df['jurisdiction'].isin(Jur)) & (Df['publication_type'] == 'GRANTED_PATENT')]
    #Marker = pd.DataFrame()
    for i, SF in enumerate(set(rel_jur['SF'].values)):
        Sub = rel_jur[rel_jur['SF'] == SF]
        RSub = Sub[Sub['Patent Jur'].isin(Jur)]
        RSub = RSub[RSub['date_published']== RSub['date_published'].min()]
        ID = str(RSub.index)
        Df.at[ID,'Marker'] = 'Citation'
        print(i/len(set(rel_jur['SF'].values))*100,'% of dataset restructrued')
    return Df
#DF_F2 = Mark_priority2(DF_F, Jur_list)

DF_F2 = pd.concat([DF_F, Patent_Marker], axis = 1)
DF_F2.to_json('Citation_inputpreped2.json')
        
"""
Target = pd.json_normalize(Through_put.at[Through_put2.index[5], 'biblio.cited_by.patents'])
temp = pd.DataFrame()
temp['Cited'] = np.full(shape = int(Through_put.at[Through_put2.index[5], 'biblio.cited_by.patent_count']), fill_value=Through_put2.index[5])
temp['Citing'] = Target['document_id.jurisdiction']+Target['document_id.doc_number']+Target['document_id.kind']
temp['Cited Date Published'] = Through_put.at[Through_put2.index[5], 'date_published']
for i,v  in enumerate(temp['Citing'].values):
    if 
    temp.at[i,'Citing Date Published'] = Through_put.at[v,'date_published']"

"""

# CPC patent classsifictions        https://www.lens.org/lens/search/patent/list?classCpc.must=B60L50%2F60&classCpc.must=B60L50%2F70&classCpc.must=B60L50%2F75&classCpc.must=B60L50%2F50
CPC_dict = { 
    'Vehicles':['H01M2250/20','Y02T90/40','B60L50/50','B60L50/60','B60L50/70','B60L50/75','B60L9/00','B60L58/30','B60L58/00'],
    'FCT':['Y02E60/50','H01M2008/1095','H01M8/083''H01M8/1004','H0M8/083'],
    'FCtype':['H01M2008/1095','H01M8/083'],
    'PEMFC':['H01M2008/1095'],
    'AFC':['H01M8/083'],
    'Hybrids':['Y02T10/62','B60L58/40','B60L50/50','B60L50/60','B60L50/70','B60L50/75','B60L58/00'],
    'Hydrorgen_storage':['F17C2221/012', 'F17C2223/0123', 'Y02E60/32'],

    
    }
def CPC_Unpacking(df, Dict): 

    Temp = pd.DataFrame() 
    In = df[pd.notnull(df['biblio.classifications_cpc.classifications'])]
    for index, index_V in enumerate(In.index):
        Id = pd.DataFrame(data = [index_V],columns=['ID'])
        for CPC_tags in Dict.keys():
            Nor = pd.json_normalize(In.at[index_V,'biblio.classifications_cpc.classifications'])
            Test =  pd.DataFrame(data= [Nor.isin(Dict[CPC_tags]).value_counts()])
            if True in Test.columns:
                tags = pd.DataFrame(data = [CPC_tags], columns=[str(CPC_tags)])
                Id = pd.concat([Id,tags],axis = 1)
            else:
                tags = pd.DataFrame(data = [np.NAN],columns=[str(CPC_tags)])
                Id = pd.concat([Id,tags],axis = 1)
        Temp = pd.concat([Temp, Id])
        print(index/len(In.index)*100,'% of dataset restructrued')

    return Temp


def CPC_Unpacking_multi(df, Dict,CPC1,CPC2): #Creates tages that are suposed to include multiple CPC classication categories 

    Temp = pd.DataFrame() 
    In = df[pd.notnull(df['biblio.classifications_cpc.classifications'])]
    for index, index_V in enumerate(In.index):
        Id = pd.DataFrame(data = [index_V],columns=['ID'])
        Nor = pd.json_normalize(In.at[index_V,'biblio.classifications_cpc.classifications'])
        Test =  pd.DataFrame(data= [(Nor.isin(Dict[CPC1]).value_counts()) & ((Nor.isin(Dict[CPC2]).value_counts()))])
        if True in Test.columns:
            tags = pd.DataFrame(data = [(str(CPC1) +'&' +str(CPC2))], columns=[(str(CPC1) +'&' +str(CPC2))])
            Id = pd.concat([Id,tags],axis = 1)
        else:
            tags = pd.DataFrame(data = [np.NAN],columns=[(str(CPC1) +'&' +str(CPC2))])
            Id = pd.concat([Id,tags],axis = 1)
        Temp = pd.concat([Temp, Id])
        print(index/len(In.index)*100,'% of dataset restructrued')

    return Temp

#DF_F2 = pd.read_json('D:/OneDrive/FU - Studentzeit/Innovations/Master/Methode and data/Full Data/Only Granted Patents/Granted Extended/CN/Citation_inputpreped.json')

Tags = CPC_Unpacking(DF_F2, CPC_dict)
Tags = Tags.set_index('ID')
TagsM = CPC_Unpacking_multi(DF_F2, CPC_dict,'FCT','Vehicles')
TagsMv2 = CPC_Unpacking_multi(DF_F2, CPC_dict,'Hydrorgen_storage','Vehicles')
TagsM = TagsM.set_index('ID')
TagsMv2 = TagsMv2.set_index('ID')


DF_MT = pd.concat([DF_F2, Tags,TagsM,TagsMv2], axis = 1)











def citations_forward(Df, Jur,IntS, IntE,tags):
    temp_df = pd.DataFrame()
    Df2 = Df[(Df['Marker'] == 'Include')]
    Df2 = Df2[(Df2['jurisdiction'] == Jur)]
    Df2 = Df2[(Df2['Patent Jur'] == Jur)]
    Df2 = Df2[(Df2[tags] == tags)]
    Df2 = Df2[(Df2['date_published'] >= str(IntS)+'-01-01') & (Df2['date_published'] <= str(IntE)+'-01-01')]
    Df2 = Df2[pd.notnull(Df2['biblio.cited_by.patents'])]
    for index, index_value in enumerate(Df2.index):
        Target = pd.json_normalize(Df2.at[index_value, 'biblio.cited_by.patents'])
        temp = pd.DataFrame()
        temp['Cited'] = np.full(shape = int(Df.at[index_value, 'biblio.cited_by.patent_count']), fill_value=index_value)
        temp['Citing'] = Target['document_id.jurisdiction']+Target['document_id.doc_number']+Target['document_id.kind']
        temp['Citing Jur'] = Target['document_id.jurisdiction']
        temp['Cited Date Published'] = Df.at[index_value, 'date_published']
        temp2 = pd.DataFrame()
        for C in temp['Citing']:
            if C in Df.index:
                Citing = pd.DataFrame(data=[Df.at[C,'date_published']]) 
                temp2 = pd.concat([temp2,Citing])
            else:
                Citing = pd.DataFrame(data=['TBD']) 
                temp2 = pd.concat([temp2,Citing])
        
        temp2 = temp2.reset_index()
        temp = pd.concat([temp,temp2], axis= 1)
        temp = temp[(temp['Citing Jur'] == Jur) | (temp['Citing Jur'] == 'WO')| (temp['Citing Jur'] == 'EP')]
        temp_df = pd.concat([temp_df,temp])
        print(index/len(set(Df2.index))*100,'% of dataset restructrued')

    return temp_df
#Cit_US = citations_forward(DF_MT, 'US',1900,1980,'FCT')
#Cit_US = Cit_US.rename(columns={0:'Citing Date Published','Cited':'Source','Citing':'Target'})#.drop(columns= ['index'])
#Cit_US.to_excel('PC_Network_test.xlsx')


def Parameter_feeder(Df, Jur, tag):
    for year in [1950,1960,1970,1980,1990,2000,2010,2023]:
        Start = 1900
        CTN = citations_forward(Df, Jur, Start, year, tag) 
        if CTN.size != 0:
            CTN.rename(columns={0:'Citing Date Published','Cited':'Source','Citing':'Target'}).to_excel(str(Jur)+'/'+str(tag)+'/'+str(Start)+'-'+str(year)+'_'+str(tag)+'_'+str(Jur)+'_PCN.xlsx')
           

for C in ['US','JP','DE','KR']:
    for Tag in ['Vehicles', 'FCT', 'Hybrids','Hydrorgen_storage', 'FCT&Vehicles', 'Hydrorgen_storage&Vehicles','FCtype','PEMFC','AFC']:
            Parameter_feeder(DF_MT, C, Tag)









def references(Df, Jur,Df, Jur,IntS, IntE,tags): #must be rewriten
    temp_list = []
    
    Df = Df[(Df['jurisdiction'] == Jur)]
    Df = Df[(Df['Patent Jur'] == Jur)]
    Df2 = Df[(Df['Marker'] == 'Include')]
    Df2 = Df2[(Df2['date_published'] >= str(IntS)+'-01-01') & (Df2['date_published'] <= str(IntE)+'-01-01')]
    Df2 = Df2[pd.notnull(Df2['biblio.cited_by.patents'])]
    for index_value in Df.index:
        Source = np.full(shape = int(Df.at[index_value, 'biblio.cited_by.patent_count']), fill_value=index_value)
        Source_Pub = np.full(shape = int(Df.at[index_value, 'date_published']), fill_value=index_value)

        Target = pd.json_normalize(Df.at[index_value, 'biblio.cited_by.patents'])
        temp = pd.DataFrame()
        temp['Cited'] = Source
        temp['Cited Date Published'] = Source_Pub
        temp['Citing'] = Target['document_id.jurisdiction']+Target['document_id.doc_number']+Target['document_id.kind']
        temp['Citing Date Published'] = Df[Df.isin(Target['document_id.date'])]['date_published']
        temp_list.append(temp) 
    frames = pd.concat(temp_list)
    return frames.reset_index()
def Citation_input(Df,Jur):
    Cited = Df[pd.notnull(Df['biblio.cited_by.patents'])]
    Cited = Df[Df['jurisdiction'] ==str(Jur)]
    return Cited
#New_citation= citation(Cited)



#.replace(' JR ',' ').replace(' JR',' ').replace('DIP ING',' ').replace('DIPL CHE',' ').replace('DIPL EL I',' ').replace('DIPL EL ING',' ').replace('DIPL EL ING HTL',' ').replace('PROF ',' ').replace('DIPL CHEM',' ').replace('DIPL PHY',' ').replace('DIPL PHYS',' ').replace('DIPL  ING',' ').replace('DIPL ING',' ').replace(' PROF',' ').replace(' DR RER',' ').replace(' DR ING CHE',' ').replace(' DR DIPL PH',' ').replace(' DR DIPL PH',' ').replace(' DR PHYS',' ').replace(' DR DIPL CHEM',' ').replace(' DR DIPL C',' ').replace(' DIPL PHYS DR',' ').replace(' DR DIPL PHYS',' ').replace(' DR RER NAT',' ').replace(' PROF DR',' ').replace(' DR DIPL',' ').replace(' DR ING',' ').replace(' DR',' ').strip(' ')
Cit_JP = citations_forward(DF_Patents, 'JP')
Cit_DE = citations_forward(DF_Patents, 'DE')




def citations_forward_CPC_delin(Df, Jur):
    temp_list = []
    Df = Df[(Df['jurisdiction'] == Jur)]
    Df = Df[(Df['Patent Jur'] == Jur)]
    for index_value in Df.index:
        Source = np.full(shape = int(Df.at[index_value, 'biblio.cited_by.patent_count']), fill_value=index_value)
        Source_Pub = np.full(shape = int(Df.at[index_value, 'date_published']), fill_value=index_value)
        Target = pd.json_normalize(Df.at[index_value, 'biblio.cited_by.patents'])
        temp = pd.DataFrame()
        temp['Cited'] = Source
        temp['Cited Date Published'] = Source_Pub
        temp['Citing'] = Target['document_id.jurisdiction']+Target['document_id.doc_number']+Target['document_id.kind']
        temp.at['Citing Date Published'] =  Df[Df.index.isin(temp['Citing'])]['date_published']
        temp_list.append(temp)
    frames = pd.concat(temp_list)
    return frames.reset_index()




