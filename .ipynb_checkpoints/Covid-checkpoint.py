#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 12:31:40 2020

@author: Gaurav Verma

This Module Contains Covid Cases Data taken From https://www.worldometers.info/coronavirus/

Functions and their breif Detail :

1- Track_str() : This Function returns Raw Data of All Countries in String Data Type

-------------------------------------------------------------------------------
2- Track() : This Function returns Raw Data of All Countries in integer Data Type

-------------------------------------------------------------------------------
3- Main() and Co_main() : these functions are The Backbone of All Functions
   contains data used to Create a Table

-------------------------------------------------------------------------------
4- active() : this function gives the Total Active Cases in That Day

-------------------------------------------------------------------------------
5- death_recovery_rate() : this Function have two Columns Death Rate and Recovery Rate on That day

-------------------------------------------------------------------------------
6- tatal_deaths() : this Function gives total death upto that day and Tatal Death on That day

# =============================================================================
# """
import pandas as pd
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import re

cols=['country','total_cases','new_cases','total_death','new_deaths','recovered',"SKIP",'active_cases','critical','total_cases/10Lakhs','total_death/10lakhs','total_tests','total_test/10lakhs','population']
data = pd.DataFrame(columns=cols)
try:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url= 'https://www.worldometers.info/coronavirus/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(url,headers=hdr)

    html = urlopen(req,context=ctx).read()
    soup = BeautifulSoup(html)
except:
    print("Turn Your Internet Connection On")
#create a Data frame

def Track_str():
    '''
    Print the Covid data in Text format
    '''
    
    data = pd.DataFrame(columns=cols)
    #Extracting Tags <td>
    tags=soup('td')
    Nr_tags = 19
    i=0
    j=1
    k=0
    save=True
    while i<len(tags)-Nr_tags*10:
        i+=1
        if i == j:
            j+=19
            k=0
            save =True
        if save:
            temp = dict(zip(cols,[0]*len(cols)))
            while k<14:
                if k==0:
                    temp[cols[k]]=tags[k+i].get_text().replace('\n','')

                else:
                    temp[cols[k]]=tags[k+i].get_text()

                k+=1
            save=False
            data=data.append(temp,ignore_index=True)
    data.drop(["SKIP"],inplace=True,axis=1)
    return data


#create a Data frame

def Track():
    '''
    Print the current Covid19 cases in Integer Dtype 
    '''
    data = pd.DataFrame(columns=cols)
    #Extracting Tags <td>
    tags=soup('td')
    Nr_tags = 19
    i=0
    j=1
    k=0
    save=True
    while i<len(tags)-Nr_tags*10:
        i+=1
        if i == j:
            j+=19
            k=0
            save =True
        if save:
            temp = dict(zip(cols,[0]*len(cols)))
            while k<14:
                if k==0:
                    temp[cols[k]]=tags[k+i].get_text().replace('\n','')

                else:
                    if k==2 or k==4:
                        temp[cols[k]]=tags[k+i].get_text()
                        
                    else:
                        s=tags[k+i].get_text()
                        if s=='' or s=='N/A':
                            s=0
                        else:
                            s=s.replace(',','')
                        try:
                            temp[cols[k]]=int(float(s))
                        except:
                            temp[cols[k]] = 0

                k+=1
            save=False
            data=data.append(temp,ignore_index=True)
    data.drop(["SKIP"],inplace=True,axis=1)
    return data

def main_function(x):
    '''
    Base of All Functions
    '''
    all_date=soup.find_all(type="text/javascript")[x].string
    i=re.search(r'categories: ',all_date).span()[1]
    j=re.search(r' yAxis',all_date).span()[0]
    Z=all_date[i:j]
    (i,j)=re.match(r"\[(.*?)\]",Z).span()
    final_date = Z[i+1:j-1]
    final_date = final_date.replace("\"","").split(',')
    i=re.search(r'data: ',all_date).span()[1]
    j=re.search(r'responsive',all_date).span()[0]
    Z=all_date[i:j]
    (i,j)=re.match(r"\[(.*?)\]",Z).span()
    final_active_world = Z[i+1:j-1]
    final_active_world = list(map(float,final_active_world.replace("\"","").split(',')))
    

    return final_date,final_active_world

def co_main(x,lable=None):
    t=soup.find_all(type="text/javascript")[x].string
    i=re.search(lable,t).span()[1]
    Z=t[i:]
    (i,j)=re.search(r"\[(.*?)\]",Z).span()
    final_date = Z[i+1:j-1]
    final_date = final_date.replace("null","0")
    final_active_world = list(map(float,final_date.replace("\"","").split(',')))

    return final_active_world
def active():
    '''
    This Method Returns the Day Wise Current Active Cases in World
    
    PS : Remember this is Total Day wise Cases
    '''
    a,b = main_function(7)
    return pd.DataFrame({"Date":a , "Active_cases":b})

def death_recovery_rate():
    '''
    This Method Returns the Day Wise Current Death Rate and Recovery Rate in World
    
    PS : Remember this is Total Death Rate
    '''
    a,b = main_function(8)
    recovery_rate = co_main(8,"Recovery Rate")
    return pd.DataFrame({"Date":a , "Death_rate":b,"Recovey_rate":recovery_rate})

def total_cases():
    '''
    This Method Returns the Day Wise Current Active Cases in World
    
    PS : Remember this is Total Day wise Cases
    '''
    a,b = main_function(9)
    daily_cases = co_main(9,"Daily Cases")
    return pd.DataFrame({"Date":a , "Active_cases":b,"Daily_cases":daily_cases})
def total_deaths():
    '''
    This Method Returns the Day Wise Current Deaths and Daily Deaths in World
    
    return : DataFrame With date,Total Deaths,Daily Deaths
    
    '''
    a,b = main_function(10)
    c=[0]
    for i in range(1,len(b)):
        c.append(b[i]-b[i-1])
    return pd.DataFrame({"Date":a,"Deaths":b,"Daily Deaths":c})
