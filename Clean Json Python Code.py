# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 11:36:13 2020

@author: Yadnesh
"""

import json
import re  

def cleanfile():
    with open('data.json',encoding='utf-8') as f:
        filedata = f.read()
        filedata = filedata.replace("'id'", '"id"')
        filedata = filedata.replace("'threadId'", '"threadId"')
        filedata = filedata.replace("'labelIds'", '"labelIds"')
        filedata = filedata.replace("'payload'", '"payload"')
        filedata = filedata.replace("'partId'", '"partId"')
        filedata = filedata.replace("'headers'", '"headers"')
        filedata = filedata.replace("'name'", '"name"')
        filedata = filedata.replace("'value'", '"value"')
        filedata = filedata.replace("'sizeEstimate'", '"sizeEstimate"')
        filedata = filedata.replace("'historyId'", '"historyId"')
        filedata = filedata.replace("'internalDate'", '"internalDate"')
        filedata = filedata.replace("NONE", "")
        filedata = filedata.replace("none", "")
        print(filedata)
        f=eval(filedata)
        
        return f

def check(email):  
    # Make a regular expression 
    # for validating an Email 
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    # pass the regular expression 
    # and the string in search() method 
    if(re.search(regex,email)):  
        print("Valid Email")  
        return 1
    else:  
        print("Invalid Email") 

def ProcessData(f):
    list1= list(f['messages'])
    list_final=[]
    for elements in list1:
        sep_dict = dict(elements)
    
        dictionary = {  
            "id": '',
            "history_id":'' ,
            "thread_id" : '',
            "labels": [],
            "from": "",
            "from_name": "",
            "subject": "",
            "date": "",
            "to": {}
        }

        dictionary['id']=sep_dict['id']
        dictionary['history_id']=sep_dict['historyId']
        dictionary['thread_id']=sep_dict['threadId']
        dictionary['labels']=sep_dict['labelIds']

        InnerList=list(sep_dict['payload']['headers'])

        print(len(InnerList))

        for i in InnerList:
            fromstring=str(i['name'])
            x=[]
            if(fromstring)==str('From'):
                #print(i['value'])
                try:
                    x = str(i['value']).split("<", 2)
                    x[1].replace('>', '')
                    #print(x[0])
                    #print(x[1])
                    #dictionary['from']=i['value']
                    dictionary['from']=str(x[0])
                    dictionary['from_name']=str(x[1])
                except:
                    print("")
            if(fromstring)==str('Subject'):
                dictionary['subject']=str(i['value'])
                #print(str(i['value']))
            if(fromstring)==str('Date'):
                dictionary['date']=str(i['value'])
                #print(str(i['value']))
            if(fromstring)==str('To'):
                try:
                    y = str(i['value']).split(",")
                except:
                    y = str(i['value'])
                print(y)
                final_inner_list=[]
                for details in y:
                    InnerDict={
                        "name":"",
                        "email":""
                        }
                    #print(details)
                    
                    try:
                        x1= str(details).split("<", 2)
                        str(x1[1]).replace('>', '')
                        
                        InnerDict["name"] = str(x1[0])
                        InnerDict["email"] = str(x1[1])
                        final_inner_list.append(InnerDict)
                    except:
                        c=check(x1[0])
                        if(c==1):
                            InnerDict["name"] = ""
                            InnerDict["email"] = str(x1[0])
                            final_inner_list.append(InnerDict)
                        elif not str(x1[0]):
                            InnerDict["name"] = str(x1[0])
                            InnerDict["email"] = "" 
                            final_inner_list.append(InnerDict)
                        print("single Entry")
                        
                dictionary['to']=final_inner_list

        list_final.append(dictionary)
    return list_final

# Defining main function 
def main(): 
    filedata = cleanfile()
    finallist =ProcessData(filedata)
    #data=dict(finallist)
    
    with open('Processdata.json', 'w', encoding='utf-8') as f:
        json.dump(finallist, f,indent=4)
  
  
# Using the special variable  
# __name__ 
if __name__=="__main__": 
    main() 





